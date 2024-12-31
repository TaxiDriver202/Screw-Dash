import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor


stats = {
    "data_format": 5,
    "humidity": 0,
    "temperature": 0,
    "pressure": 0,
    "acceleration": 0,
    "acceleration_x": 0,
    "acceleration_y": 0,
    "acceleration_z": 0,
    "tx_power": 0,
    "battery": 0,
    "movement_counter": 0,
    "measurement_sequence_number": 0,
    "mac": 0,
    "data_format": 0,
    "rssi": 0,
}

async def main():
    async for found_data in RuuviTagSensor.get_data_async():
       # print(f"MAC: {found_data[0]}")
       # print(f"Data: {found_data[1]}")
        for value in found_data[1]:
            if value == "humidity":
                stats["humidity"] = found_data[1][value]
            elif value == "temperature":
                stats["temperature"] = found_data[1][value]
            elif value == "pressure":
                stats["pressure"] = found_data[1][value]
            elif value == "acceleration":
                stats["acceleration"] = found_data[1][value]
            elif value == "acceleration_x":
                stats["acceleration_x"] = found_data[1][value]
            elif value == "acceleration_y":
                stats["acceleration_y"] = found_data[1][value]
            elif value == "acceleration_z":
                stats["acceleration_z"] = found_data[1][value]
            elif value == "tx_power":
                stats["tx_power"] = found_data[1][value]
            elif value == "battery":
                stats["battery"] = found_data[1][value]
            elif value == "movement_counter":
                stats["movement_counter"] = found_data[1][value]
            elif value == "measurement_sequence_number":
                stats["measurement_sequence_number"] = found_data[1][value]
            elif value == "mac":
                stats["mac"] = found_data[1][value]
            elif value == "data_format":
                stats["data_format"] = found_data[1][value]
            elif value == "rssi":
                stats["rssi"] = found_data[1][value]
        print(stats["temperature"])
        



if __name__ == "__main__":
    asyncio.run(main())