import asyncio
from bydhvs import BYDHVS  # Assuming the BYDHVS class is in a file named bydhvs.py


async def main():
    # Replace '192.168.1.100' with the IP address of your BYD HVS battery system
    battery_ip = '192.168.16.254'
    battery = BYDHVS(ip_address=battery_ip)

    try:
        # Perform the polling to retrieve data
        await battery.poll()

        # Get the collected data
        data = battery.get_data()

        # Print the retrieved data
        print("Battery Data:")
        print(f"Serial Number: {data['serial_number']}")
        print(f"BMU Firmware: {data['bmu_firmware']}")
        print(f"BMS Firmware: {data['bms_firmware']}")
        print(f"Modules: {data['modules']}")
        print(f"Towers: {data['towers']}")
        print(f"Grid Type: {data['grid_type']}")
        print(f"SOC: {data['soc']}%")
        print(f"Max Voltage: {data['max_voltage']} V")
        print(f"Min Voltage: {data['min_voltage']} V")
        print(f"SOH: {data['soh']}%")
        print(f"Current: {data['current']} A")
        print(f"Battery Voltage: {data['battery_voltage']} V")
        print(f"Max Temperature: {data['max_temperature']} °C")
        print(f"Min Temperature: {data['min_temperature']} °C")
        print(f"Battery Temperature: {data['battery_temperature']} °C")
        print(f"Voltage Difference: {data['voltage_difference']} V")
        print(f"Power: {data['power']} W")
        print(f"Error Number: {data['error_number']}")
        print(f"Error String: {data['error_string']}")
        print(f"Charge Total: {data['charge_total']} Ah")
        print(f"Discharge Total: {data['discharge_total']} Ah")
        print(f"ETA: {data['eta']}")
        print(f"Battery Type: {data['battery_type']}")
        print(f"Inverter Type: {data['inverter_type']}")
        for idx, tower in enumerate(data['tower_attributes']):
            print(f"\nTower {idx + 1}:")
            print(f"  Max Cell Voltage (mV): {tower.get('maxCellVoltage_mV')}")
            print(f"  Min Cell Voltage (mV): {tower.get('minCellVoltage_mV')}")
            print(f"  Max Cell Voltage Cell: No. {tower.get('maxCellVoltageCell')}")
            print(f"  Min Cell Voltage Cell: No. {tower.get('minCellVoltageCell')}")
            print(f"  Max Cell Temp: {tower.get('maxCellTemp')}°C")
            print(f"  Min Cell Temp: {tower.get('minCellTemp')}°C")
            print(f"  Max Cell Temp Cell: No. {tower.get('maxCellTempCell')}")
            print(f"  Min Cell Temp Cell: No. {tower.get('minCellTempCell')}")
            print(f"  Balancing Status: {tower.get('balancingStatus')}")
            print(f"  Balancing Count: {tower.get('balancingCount')}")
            print(f"  Total Charge: {tower['chargeTotal']}")
            print(f"  Discharge Total:  {tower.get('dischargeTotal')}")
            print(f"  ETA: {tower.get('eta')}")
            print(f"  Battery Volt: {tower.get('batteryVolt')}")
            print(f"  Output Volt: {tower.get('outVolt')}")
            print(f"  SOCDiagnosis: {tower.get('hvsSOCDiagnosis')}%")
            print(f"  State of Health: {tower.get('soh')}%")
            print(f"  State: {tower.get('state')}")
            print(f"  Cell Voltages: {tower.get('cellVoltages')}")
            print(f"  Cell Temperatures: {tower.get('cellTemperatures')}")


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed properly
        await battery.close()


if __name__ == '__main__':
    asyncio.run(main())
    
