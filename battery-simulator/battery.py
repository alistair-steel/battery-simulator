"""
Code covering battery classes and core functions
"""
from abc import ABC
from decimal import Decimal
from enum import Enum, auto


def generate_battery_id():
    return "abcdfgt"


class BatteryState(Enum):
    """
    Class responsible for enumerating the possible
    states a battery can be in.
    """

    CHARGING = auto()
    DISCHARGING = auto()
    IDLE = auto()


# TODO:
# add logging to Error classes


class BatteryError(Exception):
    """
    Generic Battery Error class. Likely won't be called on it's own.
    """

    def __init__(self, battery_id):
        self.battery_id = battery_id

        super().__init__()


class BatteryFullError(BatteryError):
    """
    Raise when the battery has been instructed to charge but is unable to
    due to the battery capacity being reached
    """


class BatteryEmptyError(BatteryError):
    """
    Raise when the battery has been instructed to discharge but is unable to
    due to no charge in the battery
    """


class Battery(ABC):
    """
    Base class representing a batery object.

    Responsible for handling basic charging and discharging
    behaviour and reporting battery state.
    """

    def __init__(self, battery_inputs=None, battery_outputs=None) -> None:
        self.battery_id = generate_battery_id()

        if battery_inputs is None:
            self.battery_inputs = []
        else:
            self.battery_inputs = battery_inputs

        if battery_outputs is None:
            self.battery_outputs = []
        else:
            self.battery_outputs = battery_outputs

    # energy capacity
    @property
    def energy_capacity(self) -> Decimal:
        """
        The maximum amount of stored energy in kilowatt-hours [kWh]
        """
        return self._energy_capacity

    @energy_capacity.setter
    def energy_capacity(self, value):
        if value < 0:
            raise ValueError("Energy capacity cannot be negative")
        self._energy_capacity = value

    # current capacity
    @property
    def current_capacity(self):
        """
        The total current charge level in kWh.
        """
        return sum(self.battery_inputs) - sum(self.battery_outputs)

    # state of charge
    @property
    def state_of_charge(self):
        """
        The total current charge as a fraction of total battery
        capacity.
        """
        return self.current_capacity / self.energy_capacity

    # power capacity
    @property
    def power_capacity(self) -> Decimal:
        """
        The total possible instantaneous charge/discharge capability,
        in kilowatts, of the Battery. In other words, the maximum rate
        of charge or discharge that the Battery can achieve.

        Initially, this will be the only rate the battery can charge at.
        """
        return self._power_capacity

    @power_capacity.setter
    def power_capacity(self, value):
        if value < 0:
            raise ValueError("Power capacity cannot be zero")

        self._power_capacity = value

    # storage duration
    @property
    def storage_duration(self) -> Decimal:
        """
        The amount of time the battery can discharge at its
        power capacity before depleting its energy capacity.

        Expressed in hours
        """

        return self.energy_capacity / self.power_capacity

    # state
    @property
    def state(self) -> BatteryState:
        """
        The current state of the battery (charging, discharging, idle etc.)
        """

        return self._state

    @state.setter
    def state(self, state_value: BatteryState):
        self._state = state_value

    # battery inputs

    # battery outputs

    # charge and discharge methods
    def charge(self):
        """
        Orders the battery to begin charging.

        Will set the battery parameters to enable charging. Currently,
        the battery will simply charge at the power capacity rate of
        the battery (all or nothing).

        If the battery is full, raises an exception.

        Will update battery state to show it's charging and important
        charging parameters such as charge rate.

        Will not update the battery capacity. This is done at the beginning
        of the next time increment.
        """

        # This should just update the battery parameters to show it's charging

        if self.current_capacity == self.energy_capacity:
            raise BatteryFullError(
                f"{self.battery_id} - Battery is full and cannot charge"
            )
        else:
            self.state = BatteryState.CHARGING

    def idle(self):
        """
        Orders the battery to stop charging or discharging. Will override the current
        charging instructions.

        If the battery is already idle, nothing chnages.
        """

        self.state = BatteryState.IDLE

    def discharge(self):
        """
        Orders the battery to begin discharging.

        Will set the battery state to discharge.

        If the current battery capacity is zero (the battery is empty), raise
        a BatteryEmptyError
        """

        if self.current_capacity == 0:
            raise BatteryEmptyError(
                f"{self.battery_id} Battery is empty and cannot discharge"
            )
        else:
            self.state = BatteryState.DISCHARGING

    def increment(self):
        """
        Updates the battery charge state for each time increment.

        This is always called at the beginning of each time increment.

        """

        if self.state == BatteryState.CHARGING:
            self.battery_inputs.append(Decimal(self.power_capacity) / 60)
        elif self.state == BatteryState.DISCHARGING:
            self.battery_outputs.append(Decimal(self.power_capacity) / 60)
        else:
            pass

    def __str__(self) -> str:
        return f"""
            State: {self.state} \n
            Current capacity: {self.current_capacity} \n
            Current state of charge: {self.state_of_charge}"""


# Create different battery variants


class GridBattery(Battery):
    """
    Standard single grid storage battery
    """

    def __init__(self):
        self.energy_capacity = Decimal(5000)
        self.power_capacity = Decimal(2500)
        self.state = BatteryState.IDLE
        self.cycle_rate = 0
        super().__init__([5000], [0])


if __name__ == "__main__":
    print("creating grid battery")
    gb = GridBattery()

    print(gb)

    gb.discharge()
    gb.increment()
    print(gb)
