import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from flask import Flask, render_template, request, redirect, url_for
import os
#import matplotlib.pyplot as plt
#import pandas as pd
import threading

app = Flask(__name__)

kitchen= {
    "temp": 0,
    "humidity": 0,
    "pressure": 0
}

outside = {
    "temp": 0,
    "humidity": 0,
    "pressure": 0
}

#todo: labels corrected

async def collect_data():
    async for found_data in RuuviTagSensor.get_data_async():
       # print(f"MAC: {found_data[0]}")
        if(found_data[0]=="DD:60:98:83:37:20"):
            kitchen.update({'temp': found_data[1]["temperature"], 'humidity': found_data[1]["humidity"], 'pressure': found_data[1]["pressure"]})
        elif(found_data[0]=="D6:34:9B:BF:40:B2"):
            outside.update({'temp': found_data[1]["temperature"], 'humidity': found_data[1]["humidity"], 'pressure': found_data[1]["pressure"]})

       # print(f"Data: {found_data[1]['temperature']}")
       # print(f"Kitchen: {kitchendata['temp']}")
       # print(f"Outside: {outside['temp1']}")
        
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
    data_thread.start()
    app.run(debug=True)
