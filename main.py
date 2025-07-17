import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Config
API_KEY = ''
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/today?unitGroup=metric&key={key}&include=hours'
DB_CONNECTION_STRING = 'mssql+pyodbc://localhost/project?driver=SQL+Server+Native+Client+11.0&trusted_connection=yes'

# Connect to SQL Server
engine = create_engine(DB_CONNECTION_STRING)

def create_main_table():
    with engine.connect() as conn:
        conn.execute(text("""
            IF OBJECT_ID('dbo.HourlyWeather', 'U') IS NULL
            CREATE TABLE dbo.HourlyWeather (
                City NVARCHAR(100),
                ObservationTime DATETIME,
                Temperature FLOAT,
                FeelsLike FLOAT,
                Humidity FLOAT,
                Dew FLOAT,
                Precip FLOAT,
                WindSpeed FLOAT,
                WindDir FLOAT,
                Pressure FLOAT,
                Visibility FLOAT,
                CloudCover FLOAT,
                Conditions NVARCHAR(200),
                Icon NVARCHAR(100),
                CONSTRAINT PK_HourlyWeather PRIMARY KEY (City, ObservationTime)
            );
        """))
        conn.commit()

def create_staging_table():
    with engine.connect() as conn:
        conn.execute(text("""
            IF OBJECT_ID('dbo.HourlyWeather_Staging', 'U') IS NOT NULL
                DROP TABLE dbo.HourlyWeather_Staging;

            CREATE TABLE dbo.HourlyWeather_Staging (
                City NVARCHAR(100),
                ObservationTime DATETIME,
                Temperature FLOAT,
                FeelsLike FLOAT,
                Humidity FLOAT,
                Dew FLOAT,
                Precip FLOAT,
                WindSpeed FLOAT,
                WindDir FLOAT,
                Pressure FLOAT,
                Visibility FLOAT,
                CloudCover FLOAT,
                Conditions NVARCHAR(200),
                Icon NVARCHAR(100)
            );
        """))
        conn.commit()

def fetch_weather_data():
    all_data = []
    for city in CITIES:
        try:
            logging.info(f"📡 Fetching data for {city}")
            url = BASE_URL.format(city=city, key=API_KEY)
            response = requests.get(url)
            data = response.json()

            if 'days' not in data or not data['days'] or 'hours' not in data['days'][0]:
                logging.warning(f"⚠️ No hourly data for {city}.")
                continue

            hours = data['days'][0]['hours']
            df = pd.DataFrame(hours)

            df['City'] = city
            df['ObservationTime'] = pd.to_datetime(df['datetimeEpoch'], unit='s')

            df = df[[
                'City', 'ObservationTime', 'temp', 'feelslike', 'humidity', 'dew', 'precip',
                'windspeed', 'winddir', 'pressure', 'visibility', 'cloudcover',
                'conditions', 'icon'
            ]]

            df.columns = [
                'City', 'ObservationTime', 'Temperature', 'FeelsLike', 'Humidity', 'Dew',
                'Precip', 'WindSpeed', 'WindDir', 'Pressure', 'Visibility',
                'CloudCover', 'Conditions', 'Icon'
            ]

            all_data.append(df)

        except Exception as e:
            logging.error(f"❌ Error for {city}: {e}")
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def load_staging(df):
    df.to_sql('HourlyWeather_Staging', con=engine, if_exists='replace', index=False)

def merge_data():
    with engine.begin() as conn:
        conn.execute(text("""
            MERGE dbo.HourlyWeather AS Target
            USING dbo.HourlyWeather_Staging AS Source
            ON Target.City = Source.City AND Target.ObservationTime = Source.ObservationTime
            WHEN MATCHED AND (
                ISNULL(Target.Temperature, -999) <> ISNULL(Source.Temperature, -999) OR
                ISNULL(Target.FeelsLike, -999) <> ISNULL(Source.FeelsLike, -999) OR
                ISNULL(Target.Humidity, -999) <> ISNULL(Source.Humidity, -999) OR
                ISNULL(Target.Dew, -999) <> ISNULL(Source.Dew, -999) OR
                ISNULL(Target.Precip, -999) <> ISNULL(Source.Precip, -999) OR
                ISNULL(Target.WindSpeed, -999) <> ISNULL(Source.WindSpeed, -999) OR
                ISNULL(Target.WindDir, -999) <> ISNULL(Source.WindDir, -999) OR
                ISNULL(Target.Pressure, -999) <> ISNULL(Source.Pressure, -999) OR
                ISNULL(Target.Visibility, -999) <> ISNULL(Source.Visibility, -999) OR
                ISNULL(Target.CloudCover, -999) <> ISNULL(Source.CloudCover, -999) OR
                ISNULL(Target.Conditions, '') <> ISNULL(Source.Conditions, '') OR
                ISNULL(Target.Icon, '') <> ISNULL(Source.Icon, '')
            )
                THEN UPDATE SET
                    Temperature = Source.Temperature,
                    FeelsLike = Source.FeelsLike,
                    Humidity = Source.Humidity,
                    Dew = Source.Dew,
                    Precip = Source.Precip,
                    WindSpeed = Source.WindSpeed,
                    WindDir = Source.WindDir,
                    Pressure = Source.Pressure,
                    Visibility = Source.Visibility,
                    CloudCover = Source.CloudCover,
                    Conditions = Source.Conditions,
                    Icon = Source.Icon
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (City, ObservationTime, Temperature, FeelsLike, Humidity, Dew,
                        Precip, WindSpeed, WindDir, Pressure, Visibility, CloudCover, Conditions, Icon)
                VALUES (City, ObservationTime, Temperature, FeelsLike, Humidity, Dew,
                        Precip, WindSpeed, WindDir, Pressure, Visibility, CloudCover, Conditions, Icon)
            WHEN NOT MATCHED BY SOURCE THEN
                DELETE;
        """))

def run_sync():
    logging.info("🚀 Starting weather sync job...")
    create_main_table()
    create_staging_table()
    df = fetch_weather_data()
    if not df.empty:
        load_staging(df)
        merge_data()
        logging.info("✅ Weather data synced successfully.")
    else:
        logging.info("⏩ No new data to sync.")

# 🔁 Optional loop to repeat every 5 minutes
if __name__ == '__main__':
    while True:
        run_sync()
        logging.info("⏳ Waiting for 5 minutes...\n")
        time.sleep(300)  # 5 minutes
