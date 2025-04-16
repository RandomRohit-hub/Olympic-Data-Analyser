





# 🏅 Olympics Data Analysis

This project dives into historical Olympic Games data, focusing exclusively on the **Summer Olympics**. The primary goal is to clean, analyze, and draw meaningful insights from the dataset that includes information about athletes, their participation over the years, events, and the countries they represent

By combining the athlete data with regional metadata, the analysis aims to uncover patterns and trends in Olympic history — such as which countries have dominated specific sports, how athlete participation has evolved over time, and the geographic distribution of medals.




I discovered a method to read the dataset from a ZIP file and successfully deploy the app on Streamlit.(line 10-18 in app.py)


https://olympic-data-analyser-vpklbhhpfnaaghioztddgw.streamlit.app/



---

## 📘 Project Overview

The project is structured as an **exploratory data analysis (EDA)** using Python and Jupyter Notebook. It sets the foundation for more advanced analytics or interactive dashboards.

### Objectives:

- 🧹 **Data Cleaning**: Filter only Summer Olympic data and join with country-region mapping.
- 🔍 **Data Exploration**: Identify patterns in athlete participation, medals, and country performance.
- 🌍 **Geographic Analysis**: Map medals and participation trends by country/region.
- 📈 **Trend Detection**: Analyze changes in Olympic sports, gender representation, and athlete demographics.

---

## 📁 Dataset Files

- **`athlete_events.csv`**: Contains records of Olympic athletes, including year, event, medal, and physical stats.
- **`noc_regions.csv`**: Maps National Olympic Committee (NOC) codes to country and region names.

---

## 🛠️ Technologies Used

- **Python 3**
- **Jupyter Notebook**
- **Pandas** – for data manipulation
- **NumPy** – for numerical operations
- *(Optional tools for visualization, if added later: Matplotlib, Seaborn, Plotly)*

---

## 🚀 How to Run

1. Clone this repository or download the notebook and datasets.
2. Install dependencies:
   ```bash
   pip install pandas numpy jupyter
