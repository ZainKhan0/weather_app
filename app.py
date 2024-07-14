from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from fetch_data import data_fetch
import os

app = Flask(__name__)

DELETE_PASS = "123456"

#checking if db file exist or not.....
def init_db():
    if not os.path.exists('weather.db'):
        conn = sqlite3.connect('weather.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
                     id INTEGER PRIMARY KEY, 
                     city TEXT, 
                     temp REAL, 
                     pressure INTEGER, 
                     humidity INTEGER, 
                     description TEXT)''')
        conn.commit()
        conn.close()

@app.before_request
def initialize():
    init_db()

#updating the data.......
def update_weather(city):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute("SELECT * FROM weather WHERE city = ?", (city,))
    data = c.fetchone()

    if data:
        data_fetch(city)
        msg = f"Weather data updated successfully for : {city}"
    else:
        data_fetch(city)
        msg = f"Weather data fetched and stored successfully for : {city}"
    
    conn.close()
    return msg

def delete_weather(city):
        
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    
    # Delete all records for the specified city
    c.execute("DELETE FROM weather WHERE city = ?", (city,))
    
    if c.rowcount > 0:
        conn.commit()
        msg = "Weather data deleted successfully"
    else:
        msg = "City not found in database"
    
    conn.close()
    return msg


@app.route('/weather/<city>', methods=['POST'])
def update_or_delete_weather(city):
    method = request.form.get('_method', '').lower()
    if method == 'put':
        msg = update_weather(city)
        return redirect(url_for('index', message=msg))
    elif method == 'delete':
        msg = delete_weather(city)
        return redirect(url_for('index', message=msg))
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    message = request.args.get('message')
    detailed_data = None
    if request.method == 'POST':
        city = request.form['city']
        data_fetch(city)
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute("SELECT * FROM weather")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data, message=message, detailed_data=detailed_data)

if __name__ == '__main__':
    app.run(debug = True)