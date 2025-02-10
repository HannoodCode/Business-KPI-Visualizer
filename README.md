# Business KPI Visualizer

## 📌 Project Overview
The **Business KPI Visualizer** is an interactive dashboard that allows users to track and analyze **Amazon sales data** using AI-driven insights. Built with **Dash and Plotly**, the application connects to a **PostgreSQL database** to provide real-time business performance metrics.

## 🤝 Prerequisites
Before setting up the project, ensure you have:
- **Python 3.8+** installed
- **pip** installed
- **(Optional)** Virtual environment for dependency management
- **(Optional)** PostgreSQL if you want to use the database features

> **Note:** The database connection is optional for testing the UI. If you don't have a PostgreSQL setup, you can still run `python app.py` and interact with the dashboard.

## 🤍 Technologies Used
- **Python** (Backend logic)
- **PostgreSQL** (Database for sales data)
- **SQLAlchemy** (ORM for database interaction)
- **Dash & Plotly** (For interactive visualizations)
- **Pandas** (Data processing & aggregation)
- **Dash Bootstrap Components** (Enhanced UI/UX)
- **AI Integration** (Trend analysis & anomaly detection)

## 🚀 Features
✅ **Interactive Data Filtering**: Users can select multiple order statuses using a checklist for dynamic KPI analysis.  
✅ **Customizable Metrics**: Toggle between **Sales (in rupees)** and **Quantity Sold** as Y-axis values.  
✅ **AI-Driven Insights**: Integrated AI features for predictive analytics and anomaly detection.  
✅ **Optimized Queries**: Handles **large datasets efficiently** without performance issues.  
✅ **Real-Time Updates**: Graphs update instantly when selections change.

## 🛠️ Installation & Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/business-kpi-visualizer.git
   cd business-kpi-visualizer
   ```

2. **(Optional) Create a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **(Optional) Configure Environment Variables**  
   If your app requires a `.env` file for credentials, create it:
   ```sh
   cp .env.example .env  # Manually update credentials
   ```

5. **Run the Application**:
   ```sh
   python app.py
   ```

6. **Open in Browser**:  
   Go to `http://127.0.0.1:8050/` to access the dashboard.

## 📊 Example Visualization
(Include a screenshot of the dashboard output here)  

![Dashboard Screenshot](assets/dashboard_example.png)

## ✨ Future Enhancements
- Improve UI design for better user experience
- Add more AI-driven insights and forecasting
- Deploy the application for public access

## ❓ Troubleshooting
- **ModuleNotFoundError** → Run `pip install -r requirements.txt`
- **Port already in use** → Run `kill -9 $(lsof -t -i:8050)` (Mac/Linux) or `taskkill /F /IM python.exe` (Windows)
- **Database connection issues** → Ensure credentials in `.env` are correct or skip database setup for UI testing

## 📚 License
This project is open-source and available under the **MIT License**.

---
### 💪 Contributing
Feel free to contribute and enhance this project! Fork, submit issues, or create pull requests. 🚀