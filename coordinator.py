"""DataUpdateCoordinator for GKD Bayern Wassertemperatur."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GkdError, Measurement, async_fetch_measurement
from .const import CONF_SCAN_INTERVAL, CONF_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class GkdCoordinator(DataUpdateCoordinator[Measurement]):
    """Fetch data from GKD Bayern."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        minutes = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=timedelta(minutes=minutes),
        )
        self._url = entry.data[CONF_URL]

    async def _async_update_data(self) -> Measurement:
        try:
            return await async_fetch_measurement(self.hass, self._url)
        except GkdError as err:
            raise UpdateFailed(f"Abruf fehlgeschlagen: {err}") from err
