"""Support for Internode"""
from datetime import timedelta
import logging

import internode
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    CONF_SCAN_INTERVAL,
    DATA_GIGABYTES
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SENSOR_USAGE = 'Usage'
SENSOR_HISTORY = 'History'
SENSOR_SERVICE = 'Service'

#POSSIBLE_MONITORED = [ SENSOR_USAGE, SENSOR_HISTORY, SENSOR_SERVICE]
POSSIBLE_MONITORED = [ SENSOR_USAGE, SENSOR_HISTORY]

DEFAULT_MONITORED = POSSIBLE_MONITORED

DEFAULT_NAME = 'Internode'

DEFAULT_SCAN_INTERVAL = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_MONITORED_CONDITIONS, default=DEFAULT_MONITORED):
            vol.All(cv.ensure_list, [vol.In(POSSIBLE_MONITORED)])
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Internode platform for sensors."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    name = config.get(CONF_NAME)

    try:
        internode.api(username, password)
    except OSError as err:
        _LOGGER.error("Connection to Internode failed: %s", err)
    
    for sensor in config.get(CONF_MONITORED_CONDITIONS):
        add_entities([InternodeAccountSensor(username, password, sensor, name)], True)


class InternodeAccountSensor(SensorEntity):
    """Representation of a Internode sensor."""

    def __init__(self, username, password, sensor, name):
        """Initialize the Internode sensor."""
        self._username = username
        self._password = password
        self._name = name + ' ' + sensor
        self._sensor = sensor
        self._state = None
        self._unit_of_measurement = None
        self._attributes = {}
        self._data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:connection"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return DATA_GIGABYTES

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if self._sensor == SENSOR_USAGE:   
            attributes = {}
            attributes['Quota'] = self._data.quota
            attributes['Plan Interval'] = self._data.planinterval
            attributes['Rollover'] = self._data.rollover
            return attributes

    def update(self): 
        try:
            Internode = internode.api(self._username , self._password)

            if self._sensor == SENSOR_USAGE:
                Internode.getusage()
            elif self._sensor == SENSOR_HISTORY:
                Internode.gethistory()
            #elif self._sensor == SENSOR_SERVICE:
            #    Internode.getservice()
            self._data = Internode
        except OSError as err:
            _LOGGER.error("Updating Internode failed: %s", err)

        """Collect updated data from Internode API."""
        if self._sensor == SENSOR_USAGE:
            self._state = self._data.usage
        elif self._sensor == SENSOR_HISTORY:
            self._state = self._data.history
        #elif self._sensor == SENSOR_SERVICE:
        #    self._state = self._data.service
        else:
            _LOGGER.error("Unknown sensor type found")