from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel
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
	DWELLING_TYPE = "Type of dwelling."
	CHARACTERISTICS = "Housing characteristics."
	TENURE = "Tenure of the dwelling."
	OWNERSHIP = "Ownership status of the house."


L = HousingV1Legends


class Housing(DataGardenSubModel):
	dwelling_type: Optional[str] = Field(default=None, description=L.DWELLING_TYPE)
	characteristics: HousingCharacteristics = Field(
		default=HousingCharacteristics, description=L.CHARACTERISTICS
	)
	tenure: Optional[str] = Field(default=None, description=L.TENURE)


class HousingV1Keys(PriceIndexFixedKeys):
	INFLATION_YOY = "inflation_yoy"
	PRICE_INDEX = "price_index"
