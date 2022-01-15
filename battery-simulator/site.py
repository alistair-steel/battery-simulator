"""
Code relating to batery sites.

A site is a collection of batteries
"""

from decimal import Decimal
from typing import List

from battery import Battery, BatteryState


def generate_site_id():
    """
    Generate a unique site identifier.

    Needs implementing
    """
    return "Site A"


class Site:
    """
    A site is a collection of batteries in the same location
    and subjected to the same charging strategy.
    """

    def __init__(self, batteries: List[Battery], location: str):
        self.site_id = generate_site_id()
        self.location = location
        self.batteries = batteries

    def __post_init__(self):
        """
        Initialise the batteries within the site after the site is created
        """
        raise NotImplementedError

    @property
    def energy_capacity(self) -> Decimal:
        """
        The total maximum energy capacity of the site.

        Defined as the sum of the energy capacities for the constituent batteries
        """
        return Decimal(sum([battery.energy_capacity for battery in self.batteries]))

    @property
    def current_capacity(self) -> Decimal:
        """
        Calculates the current energy contained within the site batteries
        """
        return Decimal(sum([battery.current_capacity for battery in self.batteries]))

    @property
    def power_capacity(self) -> Decimal:
        """
        The total possble instantaneous charge/discharge capability of the site.

        The sum of the power capacity of the site batteries
        """
        return Decimal(sum([battery.power_capacity for battery in self.batteries]))

    @property
    def state(self) -> BatteryState:
        """
        The current state of the site.

        If any single battery is charging or discharging, the site is defined
        as discharging.
        """

        for battery in self.batteries:
            if battery.state == BatteryState.CHARGING:
                return BatteryState.CHARGING
            elif battery.state == BatteryState.DISCHARGING:
                return BatteryState.DISCHARGING

        return BatteryState.IDLE

    @property
    def power_input(self) -> List[Decimal]:
        """
        Power input is the sum of each power input step for each battery
        """

        # create list of lists
        battery_input_lists = [battery.battery_inputs for battery in self.batteries]

        return [Decimal(sum(x)) for x in zip(*battery_input_lists)]

    def charge(self, rate):
        """
        Method to tell the site to begin charging at a specific rate.

        Initially, the rate will be rounded to the nearest value divisable
        by the power capacity of the site batteries.
        """
