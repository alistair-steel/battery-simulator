from abc import ABC, abstractmethod
from decimal import Decimal
from random import randint
from typing import List

from battery import Battery, BatteryState


class SiteChargingStrategy(ABC):
    """
    Abstract class defining functionality of a site charging strategy.

    The purpose is to select which batteries to charge or discharge
    based on a given logic
    """

    @abstractmethod
    def determine_charge_battery(self, charge_rate: Decimal, batteries: List[Battery]):
        """
        Defines which battery or batteries to charge
        """

    @abstractmethod
    def determine_discharge_battery(self, discharge_rate: Decimal, batteries: List[Battery]):
        """
        Defines which battery or batteries to charge
        """


class LowestToHighestChargingStrategy(SiteChargingStrategy):
    """
    Charging strategy that charges the least full battery(s) first and
    discharges and most full battery(s)
    """

    def __init__(self):
        pass

    def determine_charge_battery(self, charge_rate: Decimal, batteries: List[Battery]):
        """
        Finds the battery with the lowest charge level and tells it to charge
        """
        lowest_charge = min(
            [
                battery.current_capacity
                for battery in batteries
                if battery.state != BatteryState.CHARGING
            ]
        )

        eligible_batteries = [
            battery
            for battery in batteries
            if battery.current_capacity == lowest_charge
        ]

        return eligible_batteries[0]

    def determine_discharge_battery(self, discharge_rate: Decimal, batteries: List[Battery]):
        """
        Finds the battery with the highest charge level.

        If the required discharge rate is greater than the power capacity
        of a battery, ie the rate required is larger than a single battery can
        provide, recursively finds the next eligible battery.

        If there are multiple batteries eligible but only one needed, returns only one.
        """

        highest_charge = max(
            [
                battery.current_capacity
                for battery in batteries
                if battery.state != BatteryState.DISCHARGING
            ]
        )

        eligible_batteries = [
            battery
            for battery in batteries
            if battery.current_capacity == highest_charge
        ]

        return eligible_batteries[0]


class RandomChargingStrategy(SiteChargingStrategy):
    """
    Selects a random battery to charge, regardless of charging state
    """

    def __init__(self):
        pass

    def determine_charge_battery(self, batteries: List[Battery]):
        """
        Finds a random battery to charge that isn't currently charging
        """
        eligible_batteries = [
            battery
            for battery in batteries
            if battery.state != BatteryState.CHARGING
        ]

        return eligible_batteries[randint(0, len(eligible_batteries))]

    def determine_discharge_battery(self, batteries: List[Battery]):
        """
        Finds a random battery to discharge that isn't currently discharging
        """
        eligible_batteries = [
            battery
            for battery in batteries
            if battery.state != BatteryState.DISCHARGING
        ]

        return eligible_batteries[randint(0, len(eligible_batteries))]
