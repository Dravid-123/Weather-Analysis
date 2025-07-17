---

# 🌦️ Weather Analysis Project

A complete data pipeline to analyze weather data using Python, SQL Server, and Power BI.  
The project involves fetching real-time weather data via an API, storing it in a SQL Server database, and visualizing it with Power BI.

---

## 📌 Technologies Used

- Python (Data Fetching & ETL)
- SQL Server (Data Storage & Querying)
- Power BI (Visualization)
- OpenWeatherMap API (or any weather API)

---

## 🔄 Project Workflow

1. **Data Fetching:**  
   - Weather data is fetched from a weather API using Python.

2. **Data Storage:**  
   - The fetched data is cleaned and inserted into SQL Server using `pyodbc`.

3. **Data Analysis:**  
   - SQL queries are used to aggregate and analyze the weather data.

4. **Data Visualization:**  
   - Power BI connects to SQL Server to build dashboards and visuals.

---

## 📂 Project Structure



weather-analysis/
│
├── weather\_fetcher.py         # Python script to fetch and store data
├── config.py                  # Stores API keys and DB config
├── requirements.txt           # Python dependencies
├── weather\_data.sql           # SQL schema and sample queries
├── PowerBI\_Dashboard.pbix     # Power BI file
└── README.md

---

## 🐍 Python Setup

### 1. Clone the Repository

git clone https://github.com/your-username/weather-analysis.git
cd weather-analysis

### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt


---

## 🔑 API Configuration

Edit `config.py` and add your credentials:

API_KEY = 'your_api_key_here'
DB_CONFIG = {
    'server': 'your_server_name',
    'database': 'your_db_name',
    'username': 'your_username',
    'password': 'your_password',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

---

## ☁️ Fetching Weather Data

Run the Python script to fetch data:

python weather_fetcher.py

This will:

* Call the weather API
* Extract required fields
* Insert the data into the SQL Server table

---

## 🗃️ SQL Server Setup

1. Create a database in SQL Server (e.g., `WeatherDB`)
2. Run `weather_data.sql` to create required tables
3. Verify inserted data using:

SELECT * FROM WeatherData;

---

## 📊 Power BI Dashboard

1. Open `PowerBI_Dashboard.pbix`
2. Click `Transform Data` and set your SQL Server credentials
3. Refresh to view updated visuals

---

## 📈 Sample Visuals

* Temperature trends by city
* Humidity comparison
* Daily weather summary
* Custom alerts (e.g., extreme weather)

---

## 🚀 Future Improvements

* Automate data fetching via scheduler (e.g., cron or Task Scheduler)
* Add more cities or parameters
* Deploy dashboard online with Power BI Service

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the MIT License.

---

## 📧 Contact

For queries, contact [dravidsanjay06@gmail.com](mailto:[dravidsanjay06@gmail.com)

<img width="1739" height="733" alt="image" src="https://github.com/user-attachments/assets/e7ead15d-0411-4753-81a5-9e0da8969a1e" />
