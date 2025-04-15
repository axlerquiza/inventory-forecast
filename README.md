# inventory-forecast

A web-based inventory management system with demand forecasting capabilities. Built with Flask, it enables businesses to monitor stock levels, record sales and restocking activities, and predict future inventory needs using linear regression.

## Features

- **Inventory Management**: Track and manage product stock levels.
- **Sales and Restocking Logs**: Record sales transactions and restocking events.
- **Demand Forecasting**: Utilize linear regression to predict future stock demand.
- **Reporting**: Generate reports on inventory status and forecasted needs.

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Web framework for backend development.
- **MySQL**: Relational database for data storage.
- **SQLAlchemy**: ORM for database interactions.
- **scikit-learn**: Library for implementing linear regression models.
- **Pandas & NumPy**: Data manipulation and numerical operations.
- **Jinja2**: Templating engine for rendering HTML.
- **JavaScript & DataTables**: Enhance frontend interactivity and data presentation.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/axlerquiza/inventory-forecast.git
   cd inventory-forecast
   ```

2. **Set Up a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Application**:
   - **Create a `.env` File** in the project root with your database credentials and secret key:
     ```
     DATABASE_URI=mysql+pymysql://username:password@localhost/inventory_db
     SECRET_KEY=your_secret_key
     ```
   - Make sure `config.py` is set up to read from this `.env` file.

5. **Start the Flask Application**:
   ```bash
   flask run
   ```
   Then open your browser and go to `http://127.0.0.1:5000/`

## Project Structure

```
inventory-forecast/
├── controllers/           # Handles route logic and business processes
├── models/                # Defines database schemas
├── templates/             # HTML templates for rendering views
├── utils/                 # Utility functions for LR prediction
├── app.py                 # Main entry point for the Flask application
├── config.py              # Application configuration settings
├── extensions.py          # Initialization of Flask extensions
├── requirements.txt       # List of dependencies
└── sample_data.sql        # Sample SQL data for populating the database
```