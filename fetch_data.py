import requests
import sqlite3

def data_fetch(city):
    # Fetch data from the API
    api_key = "418e27d960a6cb8b3a6aff0ad293d358"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract relevant data
        city_name = data['name']
        temp = round((data['main']['temp']) - 273.15, 1)
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        # Connect to SQLite database
        conn = sqlite3.connect('weather.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
                     id INTEGER PRIMARY KEY, 
                     city TEXT, 
                     temp REAL, 
                     pressure INTEGER, 
                     humidity INTEGER, 
                     description TEXT)''')

        # Check if the city already exists in the database
        c.execute("SELECT * FROM weather WHERE city = ?", (city_name,))
        if c.fetchone():
            # Update the existing record
            c.execute("""UPDATE weather SET 
                         temp = ?, 
                         pressure = ?, 
                         humidity = ?, 
                         description = ? 
                         WHERE city = ?""",
                      (temp, pressure, humidity, description, city_name))
        else:
            # Insert new data into the database
            c.execute("INSERT INTO weather (city, temp, pressure, humidity, description) VALUES (?, ?, ?, ?, ?)",
                      (city_name, temp, pressure, humidity, description))
        
        conn.commit()
        conn.close()
        print("Weather data saved to database")
    else:
        print("Failed to retrieve data from API:", data.get("message"))
