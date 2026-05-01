import time
import os
import csv
from datetime import datetime

# Import your custom modules
from entities import ResidentialHouse, GreenHospital, EcoFactory, BatteryBank
from environment import WeatherSystem, SolarIrradianceModel, SimulationLogger
from controller import GridMaster

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("""
    ##########################################################
    #                                                        #
    #             NEXUS-GRID: SMART CITY SIMULATOR           #
    #          Sustainable Infrastructure AI v1.0            #
    #                                                        #
    ##########################################################
    """)

def run_simulation_suite():
    print_header()
    
    # --------------------------------------------------------
    # STEP 1: USER INPUTS (Perfect for Teammate to present)
    # --------------------------------------------------------
    print("[SYSTEM] Configuring City Parameters...")
    try:
        city_name = input("Enter City Name: ") or "Neo-Tokyo"
        house_count = int(input("Number of Residential Houses: ") or 20)
        battery_size = float(input("Community Battery Capacity (kWh): ") or 500)
        panel_tilt = float(input("Solar Panel Tilt Angle (0-90): ") or 30)
    except ValueError:
        print("[ERROR] Invalid input. Using Engineering Defaults.")
        house_count, battery_size, panel_tilt = 20, 500, 30

    # --------------------------------------------------------
    # STEP 2: OBJECT INITIALIZATION
    # --------------------------------------------------------
    env = WeatherSystem(city_name)
    solar_model = SolarIrradianceModel(panel_tilt)
    battery = BatteryBank(battery_size)
    logger = SimulationLogger()
    master = GridMaster(battery, solar_model, env)

    # Adding Buildings to the Grid
    master.register_building(GreenHospital()) # Priority 1
    master.register_building(EcoFactory())    # Priority 2
    for i in range(house_count):              # Priority 3
        master.register_building(ResidentialHouse(i))

    print(f"\n[SUCCESS] {len(master.infrastructure_list)} Buildings connected to Nexus-Grid.")
    input("\nPress Enter to begin 24-Hour Simulation...")

    # --------------------------------------------------------
    # STEP 3: THE 24-HOUR EXECUTION LOOP
    # --------------------------------------------------------
    print_header()
    print(f"{'HOUR':<6} | {'GEN(kW)':<10} | {'LOAD(kW)':<10} | {'BATT(kWh)':<10} | {'REPORTS'}")
    print("-" * 90)

    daily_results = []

    for h in range(24):
        # Run the controller logic
        result = master.run_dispatch_logic(h)
        
        # Log data for Excel
        logger.record_step(h, result['weather'], result)
        daily_results.append([
            h, result['gen'], result['load'], 
            battery.current_energy, result['weather']['temp']
        ])

        # Live Display
        report_preview = result['reports'][0] if result['reports'] else "Stable"
        print(f"{h:02d}:00  | {result['gen']:<10.2f} | {result['load']:<10.2f} | "
              f"{battery.current_energy:<10.2f} | {report_preview[:40]}...")
        
        # Artificial delay to make it look like "Processing"
        time.sleep(0.1)

    # --------------------------------------------------------
    # STEP 4: DATA EXPORT (SDG 12: Reporting)
    # --------------------------------------------------------
    filename = f"grid_data_{datetime.now().strftime('%H%M')}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Hour', 'Generation_kW', 'Demand_kW', 'Battery_SOC', 'Temp_C'])
        writer.writerows(daily_results)

    # --------------------------------------------------------
    # STEP 5: FINAL AUDIT
    # --------------------------------------------------------
    master.print_final_audit()
    summary = logger.get_summary()
    print(f"Daily Fulfillment: {summary['fulfillment']}%")
    print(f"Data exported to: {filename}")
    print("\n[FINISH] Simulation complete. Press any key to exit.")

if __name__ == "__main__":
    run_simulation_suite()

