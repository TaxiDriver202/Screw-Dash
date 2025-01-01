import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import os
import matplotlib.pyplot as plt
import pandas as pd
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

kitchen = {
    "temp": 0,
    "humidity": 0,
    "pressure": 0,
    "acceleration_x": 0,
    "acceleration_y": 0,
    "acceleration_z": 0
}

outside = {
    "temp": 0,
    "humidity": 0,
    "pressure": 0,
    "acceleration_x": 0,
    "acceleration_y": 0,
    "acceleration_z": 0
}

async def collect_data():
    async for found_data in RuuviTagSensor.get_data_async():
        data_updated = False
        if(found_data[0]=="DD:60:98:83:37:20"):
            kitchen.update({
                'temp': found_data[1]["temperature"], 
                'humidity': found_data[1]["humidity"], 
                'pressure': found_data[1]["pressure"],
                'acceleration_x': found_data[1]["acceleration_x"],
                'acceleration_y': found_data[1]["acceleration_y"],
                'acceleration_z': found_data[1]["acceleration_z"]
            })
            data_updated = True
        elif(found_data[0]=="D6:34:9B:BF:40:B2"):
            outside.update({
                'temp': found_data[1]["temperature"], 
                'humidity': found_data[1]["humidity"], 
                'pressure': found_data[1]["pressure"],
                'acceleration_x': found_data[1]["acceleration_x"],
                'acceleration_y': found_data[1]["acceleration_y"],
                'acceleration_z': found_data[1]["acceleration_z"]
            })
            data_updated = True
        
        # Emit updates only when data changes
        if data_updated:
            socketio.emit('data_update', {
                "kitchen": kitchen,
                "outside": outside
            })
        
@app.route('/')
def dashboard(): 
    data = {
        "kitchen": kitchen,
        "outside": outside
    }
    return render_template('dashboard.html', data=data)

def start_data_collection():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(collect_data())

if __name__ == "__main__":
    data_thread = threading.Thread(target=start_data_collection)
    data_thread.daemon = True  # This ensures the thread will exit when the main program exits
    data_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
