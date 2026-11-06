"""Fetching and parsing of the GKD Bayern measurement table."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import HEADERS


class GkdError(Exception):
    """Base error."""


class GkdConnectionError(GkdError):
    """Request failed or was rejected."""


class GkdParseError(GkdError):
    """Page did not contain a usable table."""


@dataclass
class Measurement:
    """A single measurement."""

    value: float
    timestamp: str | None


def parse_measurement(html: str) -> Measurement:
    """Return the newest valid measurement from the HTML table."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise GkdParseError("Keine Tabelle gefunden (Request evtl. geblockt)")

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        raw = cells[1].get_text(strip=True).replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            continue  # z. B. "-" bei fehlendem Messwert
        return Measurement(value, cells[0].get_text(strip=True) or None)

    raise GkdParseError("Kein gültiger Messwert in der Tabelle")


async def async_fetch_measurement(hass: HomeAssistant, url: str) -> Measurement:
    """Download the page and parse it."""
    session = async_get_clientsession(hass)
    try:
        async with session.get(
            url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            response.raise_for_status()
            html = await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as err:
        raise GkdConnectionError(str(err)) from err

    return await hass.async_add_executor_job(parse_measurement, html)
