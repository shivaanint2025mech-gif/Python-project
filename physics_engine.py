import math

class ThermalExchanger:
    """Models heat transfer for sustainable building cooling."""
    def __init__(self, u_value, area):
        self.u_value = u_value # Heat transfer coefficient
        self.area = area

    def calculate_heat_gain(self, temp_outside, temp_inside):
        # Q = U * A * deltaT
        delta_t = temp_outside - temp_inside
        return self.u_value * self.area * delta_t

class SolarPhysics:
    """Advanced Solar Irradiation Math."""
    @staticmethod
    def get_effective_irradiance(base_irradiance, tilt_angle, time_of_day):
        # Using Lambert's Cosine Law for solar panels
        # Converting degrees to radians for math.cos
        rad_tilt = math.radians(tilt_angle)
        # Factor based on sun position (simplified sine curve)
        sun_angle_factor = math.sin(math.pi * (time_of_day - 6) / 12)
        if sun_angle_factor < 0: return 0
        return base_irradiance * sun_angle_factor * math.cos(rad_tilt)

class BatteryChemistry:
    """Simulates Lithium-Ion degradation and efficiency."""
    def __init__(self, capacity, efficiency=0.92):
        self.max_cap = capacity
        self.soc = 0.2 * capacity # 20% initial charge
        self.eff = efficiency
        self.cycles = 0

    def update(self, energy_flow):
        # Positive energy_flow = charging, negative = discharging
        if energy_flow > 0:
            loss = energy_flow * (1 - self.eff)
            actual_add = min(energy_flow - loss, self.max_cap - self.soc)
            self.soc += actual_add
            return energy_flow - actual_add
        else:
            can_draw = self.soc - (0.1 * self.max_cap) # Keep 10% reserve
            actual_draw = min(abs(energy_flow), can_draw)
            self.soc -= actual_draw
            return actual_draw
          
