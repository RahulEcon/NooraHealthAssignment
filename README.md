# 🚀 Noora Health Assignment for Lead Data Engineer

## 📌 Overview
This project **extracts, loads, and transforms** data from stored CSV files, performs **data validation**, and dynamically manages **schema evolution** using `dlthub`.  
The final output is visualized in **Power BI**.

🔗 **Final Dashboard:** [View in Power BI](https://app.powerbi.com/reportEmbed?reportId=80730d73-ee38-4fdc-b481-e97311a78dba&autoAuth=true&ctid=42783e7f-e805-41c6-ba39-5ce93898e685)

## ⚙️ Tech Stack
- 🐍 **Python** – Core ETL processing  
- 🔹 **dlthub** – Handles schema evolution and data ingestion  
- 🐘 **PostgreSQL** – Data storage and validation 

## 🏃 Installation Guide: Running `run.sh` 
### 📌 Overview
This script **sets up and runs** the project by installing dependencies, setting up a virtual environment, and executing necessary scripts.
### 🚀 How to Run
First, ensure that you have a working instance of postgres set up a ready to go. Once ready, add a .env file with the following keys:
POSTGRES_USER = 'POSTGRES USERNAME HERE'
POSTGRES_PASS = 'POSTGRES PASSWORD HERE'
POSTGRES_HOST = 'POSTGRES HOST NAME HERE'
POSTGRES_DATABASE = 'POSTGRES DATABASE HERE'

#### 🔹 For WSL, Linux & macOS
Open a terminal and navigate to the project directory:
```sh
cd path/to/project
chmod +x run.sh  # Ensure script is executable
./run.sh
```

## 📂 Project Structure
- **`extract/`** → Extracts data from CSV files.  
- **`load/`** → Loads extracted data into **PostgreSQL** with schema stored in `schemas/`.  
- **`transform/`** → Applies transformations using SQL files stored in `sql/`.  
- **`logger/`** → Custom logging module for tracking ETL processes.  
- **`data/`** → Stores input CSV files.  
- **`.dlt/`** → Configuration directory for `dlthub`.  
- **`run.sh`** → Shell script to automate execution. 

## ✨ Key Features

✅ **Dynamically Creates New Tables**  
   - Automatically detects and loads **new CSV files**.  
   - No manual intervention needed—just drop in a new file and watch it get processed!  

✅ **Handles Schema Evolution**  
   - Thanks to **dlthub**, the pipeline **adapts** when CSV structures change.  
   - No worries about column additions, removals, or type changes—everything is handled smoothly.  

✅ **Robust Data Validation**  
   - Implements **table-level** and **database-level** validation to ensure data integrity.  
   - Prevents bad data from being loaded, keeping your PostgreSQL database clean and reliable.  

🚀 **This system ensures a seamless, automated, and reliable data pipeline!**  

