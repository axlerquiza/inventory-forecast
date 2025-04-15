# Inventory System - Setup Guide

## Prerequisites
- Install [Python](https://www.python.org/downloads/) (>=3.8)
- Install [MySQL](https://dev.mysql.com/downloads/)
- Install [pip](https://pip.pypa.io/en/stable/installation/)

## Installation Steps

### 1. Clone the Repository
```sh
git clone https://github.com/vincentvicencio/Inventory.git
cd Inventory
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Configure the Application
Edit `config.py` to set your **database details** and **secret key**.

### 4. Set Up the Database
Log in to MySQL and create the required schema:
```sql
CREATE SCHEMA inventory;
```

### 5. Run Database Migrations
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Start the Application
```sh
python app.py
```

The application should now be running at `http://localhost:5000/`.

## Additional Notes
- Ensure MySQL is running before starting the app.
- If any migration errors occur, try running `flask db upgrade --force`.
- To reset the database, you can drop and recreate the schema, then rerun migrations.

