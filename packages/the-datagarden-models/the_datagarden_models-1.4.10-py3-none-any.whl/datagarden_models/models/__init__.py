from datagarden_models.models.weather import WeatherObservationV1, WeatherV1Keys

from .demographics import DemographicsV1, DemographicsV1Keys
from .economics import EconomicsV1, EconomicsV1Keys
from .health import HealthV1, HealthV1Keys


class DatagardenModels:
	DEMOGRAPHICS = DemographicsV1
	ECONOMICS = EconomicsV1
	HEALTH = HealthV1
	WEATHER = WeatherObservationV1


class DatagardenModelKeys:
	DEMOGRAPHICS = DemographicsV1Keys
	ECONOMICS = EconomicsV1Keys
	HEALTH = HealthV1Keys
	WEATHER = WeatherV1Keys


__all__ = ["DatagardenModels", "DatagardenModelKeys"]
