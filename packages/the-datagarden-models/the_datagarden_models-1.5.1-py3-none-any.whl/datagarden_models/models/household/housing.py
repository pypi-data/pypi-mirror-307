from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel, EconomicsValue
from datagarden_models.models.economics.inflation import PriceIndexFixedKeys


class HousingCharacteristicsKeys:
	NUMBER_OF_ROOMS = "number_of_rooms"
	CONSTRUCTION_PERIOD = "construction_period"


class HousingCharacteristicsLegends:
	NUMBER_OF_ROOMS = "Number of rooms."
	CONSTRUCTION_PERIOD = "Construction period."


HC = HousingCharacteristicsLegends


class HousingCharacteristics(DataGardenSubModel):
	number_of_rooms: Optional[int] = Field(default=None, description=HC.NUMBER_OF_ROOMS)
	construction_period: Optional[str] = Field(
		default=None, description=HC.CONSTRUCTION_PERIOD
	)


class HousingV1Legends:
	DWELLING_TYPE = "Housing type."
	CHARACTERISTICS = "Housing characteristics."
	TENURE = "Ownership status of the house."
	AVG_REAL_ESTATE_VALUE = "Average value of real estate in the regpion."


L = HousingV1Legends


class Housing(DataGardenSubModel):
	dwelling_type: Optional[str] = Field(default=None, description=L.DWELLING_TYPE)
	characteristics: HousingCharacteristics = Field(
		default=HousingCharacteristics, description=L.CHARACTERISTICS
	)
	tenure: Optional[str] = Field(default=None, description=L.TENURE)
	avg_real_estate_value: Optional[EconomicsValue] = Field(
		default=None, description=L.AVG_REAL_ESTATE_VALUE
	)


class HousingV1Keys(PriceIndexFixedKeys):
	INFLATION_YOY = "inflation_yoy"
	PRICE_INDEX = "price_index"
