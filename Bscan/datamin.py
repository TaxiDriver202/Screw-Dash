import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor

#retrieves ruuvitag sensor data and displays in tuple format on console
async def main():
    async for found_data in RuuviTagSensor.get_data_async():
        print(f"MAC: {found_data[0]}")
        print(f"Data: {found_data[1]['temperature']}")
        
            

if __name__ == "__main__":
    asyncio.run(main())