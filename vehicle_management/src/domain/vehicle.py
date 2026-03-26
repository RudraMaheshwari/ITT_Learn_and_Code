from __future__ import annotations
from abc import ABC, abstractmethod
from ..config.constants import (
    EMPTY_ENERGY_THRESHOLD_PERCENT,
    REGISTRATION_NOTICE_DEFAULT,
    TEMPLATE_VEHICLE_STOPPED,
)
from ..utils.validation import validated_price

class Vehicle(ABC):
    def __init__(self, make: str, model: str, year: int, price: float) -> None:
        self._make = make
        self._model = model
        self._year = year
        self._price = validated_price(price)
        self._is_running = False

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model

    @property
    def year(self) -> int:
        return self._year

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = validated_price(value)

    @property
    def is_running(self) -> bool:
        return self._is_running

    def registration_notice(self) -> str:
        return REGISTRATION_NOTICE_DEFAULT

    def stop(self) -> tuple[str, ...]:
        self._is_running = False
        line = TEMPLATE_VEHICLE_STOPPED.format(make=self.make, model=self.model)
        return (line,)

    def _start_when_energy_available(
        self,
        energy_percent: float,
        blocked_notice: str,
        started_notice: str,
    ) -> tuple[str, ...]:
        if energy_percent <= EMPTY_ENERGY_THRESHOLD_PERCENT:
            return (blocked_notice,)
        self._is_running = True
        return (started_notice,)

    @abstractmethod
    def start(self) -> tuple[str, ...]:
        raise NotImplementedError

    @abstractmethod
    def summary_line(self) -> str:
        raise NotImplementedError

