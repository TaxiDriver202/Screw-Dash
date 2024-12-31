import asyncio
from bleak import discover
from ruuvitag_sensor.decoder import get_decoder
import math
import csv
import os   
import signal
import sys

def write_to_csv(device_name, device_address, data):
    file_exists = os.path.isfile('accel.txt')
    with open('accel.txt', mode='a', newline='') as file:
        fieldnames = ['device_name', 'device_address', 'temperature', 'humidity', 'pressure','acceleration_x', 'acceleration_y', 'acceleration_z']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header

        writer.writerow({
            'device_name': device_name,
            'device_address': device_address,
            'temperature': data['temperature'],
            'humidity': data['humidity'],
            'pressure': data['pressure'],
            'acceleration_x': data['acceleration_x'],
            'acceleration_y': data['acceleration_y'],
            'acceleration_z': data['acceleration_z'],
        })

async def run():
    while True:  # This loop keeps the program running until it's manually stopped.
        devices = await discover()
        ruuvi_devices = [device for device in devices if "Ruuvi" in device.name]

        if not ruuvi_devices:
            print("Ei loytynyt Ruuvi-laitteita")
            await asyncio.sleep(10)  # sleep for a short duration before trying again
            continue

        for device in ruuvi_devices:
            try:
                print(f"Löydetty Ruuvi-laite: {device.name} osoitteessa {device.address}")
                manufacturer_data = device.metadata['manufacturer_data']
                if 1177 not in manufacturer_data:
                    print("Ei löydetty Ruuvi-avainta valmistajan datasta.")
                    continue

                raw_data_bytes = manufacturer_data[1177]
                raw_data_hex = raw_data_bytes.hex()
                decoder = get_decoder("RAWv2")
                data = decoder.decode_data(raw_data_hex)

                if data is None:
                    print("Datan dekoodaus epäonnistui.")
                    continue

                print(f"Sensoridata: {data}")

                if all(key in data for key in ('acceleration_x', 'acceleration_y', 'acceleration_z')):
                    write_to_csv(device.name, device.address, data)
                else:
                    print("Kiihtyvyyden dataa ei saatavilla.")

            except Exception as e:
                print(f"Virhe käsiteltäessä laitetta {device.address}: {e}")

        await asyncio.sleep(10)  # Sleep before starting the next discovery cycle

def exit_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

if __name__ == '__main__':
    # Register a handler for the interrupt signal
    signal.signal(signal.SIGINT, exit_handler)
    print('Running. Press CTRL-C to exit.')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
