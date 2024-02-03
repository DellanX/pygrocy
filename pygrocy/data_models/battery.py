from datetime import datetime

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import (
    BatteryDetailsResponse,
    BatteryData,
    CurrentBatteryResponse,
    GrocyApiClient,
)

from typing import Dict


class Battery(DataModel):
    def __init__(self, response: CurrentBatteryResponse | BatteryDetailsResponse | None):
        self._init_empty()

        self._next_estimated_charge_time = response.next_estimated_charge_time

        if isinstance(response, CurrentBatteryResponse):
            self._init_from_CurrentBatteryResponse(response)
        elif isinstance(response, BatteryDetailsResponse):
            self._init_from_BatteryDetailsResponse(response)

    def _init_from_CurrentBatteryResponse(self, response: CurrentBatteryResponse):
        self._id = response.id
        self._last_tracked_time = response.last_tracked_time

    def _init_from_BatteryDetailsResponse(self, response: BatteryDetailsResponse):
        self._charge_cycles_count = response.charge_cycles_count
        self._last_charged = response.last_charged
        self._last_tracked_time = response.last_charged  # For compatibility
        _battery: BatteryData | None = response.battery
        if isinstance(_battery, BatteryData):
            self._id = _battery.id
            self._name = _battery.name
            self._description = _battery.description
            self._used_in = _battery.used_in
            self._charge_interval_days = _battery.charge_interval_days
            self._created_timestamp = _battery.created_timestamp
            self._userfields = _battery.userfields

    def _init_empty(self):
        self._last_tracked_time: datetime | None = None
        self._charge_cycles_count: int | None = None
        self._last_charged: datetime | None = None
        self._name: str | None = None
        self._description: str | None = None
        self._used_in: str | None = None
        self._charge_interval_days: int | None = None
        self._created_timestamp: datetime | None = None
        self._userfields: Dict | None = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_battery(self._id)
        self._init_from_BatteryDetailsResponse(details)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def used_in(self) -> str | None:
        return self._used_in

    @property
    def charge_interval_days(self) -> int | None:
        return self._charge_interval_days

    @property
    def created_timestamp(self) -> datetime | None:
        return self._created_timestamp

    @property
    def charge_cycles_count(self) -> int | None:
        return self._charge_cycles_count

    @property
    def userfields(self) -> Dict | None:
        return self._userfields

    @property
    def last_charged(self) -> datetime | None:
        return self._last_charged

    @property
    def last_tracked_time(self) -> datetime | None:
        return self._last_tracked_time

    @property
    def next_estimated_charge_time(self) -> datetime | None:
        return self._next_estimated_charge_time
