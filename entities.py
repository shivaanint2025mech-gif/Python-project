import random

# ============================================================
# BASE CLASS: The Foundation for all Buildings
# ============================================================
class Infrastructure:
    def __init__(self, name, area, base_consumption):
        self.name = name
        self.area = area
        self.base_consumption = base_consumption # kW per hour
        self.priority_level = 3 # 1 is Highest, 3 is Lowest
        self.is_powered = True
        self.energy_history = []

    def log_usage(self, consumed):
        self.energy_history.append(consumed)

# ============================================================
# SUB-CLASSES: Specific logic for different SDGs
# ============================================================

class ResidentialHouse(Infrastructure):
    """Aligns with SDG 11: Sustainable Communities"""
    def __init__(self, house_id):
        super().__init__(f"House_{house_id}", 120, 1.5)
        self.occupants = random.randint(1, 5)

    def get_hourly_demand(self, hour):
        # Morning and Evening peaks for families
        multiplier = 1.0
        if 6 <= hour <= 9: multiplier = 1.8
        if 18 <= hour <= 22: multiplier = 2.5
        
        # Add random noise for realistic behavior
        variation = random.uniform(0.8, 1.2)
        demand = self.base_consumption * multiplier * variation * (self.occupants / 2)
        self.log_usage(demand)
        return demand

class GreenHospital(Infrastructure):
    """Critical Infrastructure - High Priority"""
    def __init__(self):
        super().__init__("City General Hospital", 5000, 50.0)
        self.priority_level = 1 # MUST have power 24/7
        self.backup_generator_active = False

    def get_hourly_demand(self, hour):
        # Hospitals have steady, high demand regardless of time
        variation = random.uniform(0.95, 1.05)
        demand = self.base_consumption * variation
        self.log_usage(demand)
        return demand

class EcoFactory(Infrastructure):
    """Aligns with SDG 12: Responsible Production"""
    def __init__(self):
        super().__init__("Sustainable Textile Mill", 2000, 30.0)
        self.priority_level = 2
        self.shift_active = False

    def get_hourly_demand(self, hour):
        # Factories only work during business hours (9 to 5)
        if 9 <= hour <= 17:
            self.shift_active = True
            demand = self.base_consumption * random.uniform(1.2, 1.5)
        else:
            self.shift_active = False
            demand = self.base_consumption * 0.1 # Standby power
        
        self.log_usage(demand)
        return demand

# ============================================================
# ENERGY STORAGE: Advanced Battery Management
# ============================================================

class BatteryBank:
    """The 'Energy Reservoir' for the community"""
    def __init__(self, total_capacity):
        self.capacity = total_capacity
        self.current_energy = total_capacity * 0.3 # Start at 30%
        self.charge_efficiency = 0.94
        self.discharge_efficiency = 0.96
        self.lifecycle_degradation = 0.0001 # Small wear per use

    def charge_battery(self, energy_input):
        """Logic to add energy to the system"""
        if energy_input <= 0: return 0
        
        space_left = self.capacity - self.current_energy
        if space_left <= 0: return energy_input # All rejected
        
        actual_addition = min(energy_input * self.charge_efficiency, space_left)
        self.current_energy += actual_addition
        
        # Simulate degradation
        self.capacity -= (actual_addition * self.lifecycle_degradation)
        
        wasted = energy_input - (actual_addition / self.charge_efficiency)
        return max(0, wasted)

    def discharge_battery(self, energy_requested):
        """Logic to draw energy from the system"""
        if self.current_energy <= (self.capacity * 0.05): # 5% safety buffer
            return 0
        
        available = self.current_energy * self.discharge_efficiency
        actual_output = min(energy_requested, available)
        
        self.current_energy -= (actual_output / self.discharge_efficiency)
        return actual_output

