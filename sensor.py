"""Sensor platform for GKD Bayern Wassertemperatur."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GkdConfigEntry
from .const import DOMAIN
from .coordinator import GkdCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GkdConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor from a config entry."""
    async_add_entities([WatertempSensor(entry.runtime_data, entry)])


class WatertempSensor(CoordinatorEntity[GkdCoordinator], SensorEntity):
    """Water temperature sensor."""

    _attr_has_entity_name = True
    _attr_name = None  # Entity übernimmt den Gerätenamen
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: GkdCoordinator, entry: GkdConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="GKD Bayern",
            entry_type=None,
        )

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.value if self.coordinator.data else None

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        data = self.coordinator.data
        return {"gemessen_am": data.timestamp if data else None}
