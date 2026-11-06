"""Config flow for GKD Bayern Wassertemperatur."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .api import GkdConnectionError, GkdParseError, async_fetch_measurement
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_URL,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_URL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)

INTERVAL_VALIDATOR = vol.All(
    vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)
)


class GkdConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> OptionsFlow:
        return GkdOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input[CONF_URL].split("#")[0].strip()
            await self.async_set_unique_id(url)
            self._abort_if_unique_id_configured()

            try:
                await async_fetch_measurement(self.hass, url)
            except GkdConnectionError:
                errors["base"] = "cannot_connect"
            except GkdParseError:
                errors["base"] = "parse_error"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={CONF_URL: url},
                    options={CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL]},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_URL, default=DEFAULT_URL): str,
                vol.Required(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): INTERVAL_VALIDATOR,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(schema, user_input),
            errors=errors,
        )


class GkdOptionsFlow(OptionsFlow):
    """Handle options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Required(CONF_SCAN_INTERVAL, default=current): INTERVAL_VALIDATOR}
            ),
        )
