import time

class GridMaster:
    """The central brain managing energy flow and sustainability goals"""
    def __init__(self, battery, solar_model, environment):
        self.battery = battery
        self.solar_model = solar_model
        self.env = environment
        self.infrastructure_list = []
        
        # Performance Tracking (SDG 13 Metrics)
        self.total_carbon_offset = 0.0  # kg of CO2 saved
        self.grid_energy_purchased = 0.0 # Energy bought from fossil fuels
        self.blackout_events = 0
        self.money_saved = 0.0

    def register_building(self, building):
        """Adds a house, hospital, or factory to the grid"""
        self.infrastructure_list.append(building)

    def _calculate_grid_priorities(self):
        """Sorts buildings by priority: 1 (Hospital) > 2 (Factory) > 3 (House)"""
        return sorted(self.infrastructure_list, key=lambda x: x.priority_level)

    def run_dispatch_logic(self, hour):
        """The core algorithm that decides how to distribute energy"""
        
        # 1. Update Environment and Solar Generation
        weather = self.env.update_environment(hour)
        irradiance = self.solar_model.get_effective_irradiation(hour, weather['clouds'])
        
        # Calculate total supply available (Solar + Battery)
        solar_gen = sum([b.area * 0.20 * irradiance for b in self.infrastructure_list if hasattr(b, 'area')])
        battery_reserve = self.battery.current_energy
        
        # 2. Get Sorted Demand
        buildings_by_need = self._calculate_grid_priorities()
        total_demand = sum([b.get_hourly_demand(hour) for b in buildings_by_need])
        
        current_supply = solar_gen
        distributed_power = 0
        status_report = []

        # 3. Energy Distribution Loop (Priority Based)
        for building in buildings_by_need:
            demand = building.get_hourly_demand(hour)
            
            if current_supply >= demand:
                # Fully powered by Solar
                current_supply -= demand
                distributed_power += demand
                building.is_powered = True
                status_report.append(f"[SOLAR] {building.name} fully powered.")
            
            elif (current_supply + self.battery.current_energy) >= demand:
                # Powered by Solar + Battery
                needed_from_battery = demand - current_supply
                drawn = self.battery.discharge_battery(needed_from_battery)
                
                current_supply = 0
                distributed_power += (current_supply + drawn)
                building.is_powered = True
                status_report.append(f"[HYBRID] {building.name} powered by Storage.")
            
            else:
                # Energy Crisis: Load Shedding or Grid Purchase
                if building.priority_level == 1: # Hospitals MUST stay on
                    deficit = demand - (current_supply + self.battery.current_energy)
                    self.grid_energy_purchased += deficit
                    self.money_saved -= (deficit * 0.18) # Cost of grid power
                    building.is_powered = True
                    status_report.append(f"[CRITICAL] {building.name} using Grid Power.")
                else:
                    # Lower priority buildings get turned off (SDG 12: Efficiency)
                    building.is_powered = False
                    self.blackout_events += 1
                    status_report.append(f"[SHED] {building.name} power cut to save energy.")

        # 4. Handle Surplus (SDG 7: Storage Optimization)
        if current_supply > 0:
            waste = self.battery.charge_battery(current_supply)
            status_report.append(f"[STORAGE] {current_supply - waste:.2f}kW saved to battery.")

        # 5. Sustainability Math (SDG 13)
        # Assuming 1kWh of Solar saves 0.5kg of CO2
        self.total_carbon_offset += (distributed_power * 0.5)

        return {
            "hour": hour,
            "weather": weather,
            "gen": solar_gen,
            "load": total_demand,
            "reports": status_report
        }

    def print_final_audit(self):
        """Final presentation output showing SDG achievement"""
        print("\n" + "="*60)
        print("          NEXUS-GRID SUSTAINABILITY AUDIT")
        print("="*60)
        print(f"Total Carbon Offset:    {self.total_carbon_offset:.2f} kg CO2")
        print(f"Grid Dependency:        {self.grid_energy_purchased:.2f} kWh")
        print(f"System Reliability:     {100 - (self.blackout_events):.1f}%")
        print(f"Final Battery Status:   {self.battery.current_energy:.2f} kWh")
        print("="*60)
      
