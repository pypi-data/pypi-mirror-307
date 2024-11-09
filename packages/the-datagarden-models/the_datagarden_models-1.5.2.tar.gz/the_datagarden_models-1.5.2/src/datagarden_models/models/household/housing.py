from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel, EconomicsValue
from datagarden_models.models.economics.inflation import PriceIndexFixedKeys


###########################################
########## Start Model defenition #########
###########################################
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


###########################################
########## Start Model defenition #########
###########################################
class HousingLegends:
	DWELLING_TYPE = "Housing type."
	CHARACTERISTICS = "Housing characteristics."
	TENURE = "Ownership status of the house."
	AVG_REAL_ESTATE_VALUE = "Average value of real estate in the regpion."
	HOUSEHOLDS_PER_KM2 = "Number of households per square kilometer."
	NR_OF_HOUSEHOLDS = "Number of households."


L = HousingLegends


class Housing(DataGardenSubModel):
	dwelling_type: Optional[str] = Field(default=None, description=L.DWELLING_TYPE)
	characteristics: HousingCharacteristics = Field(
		default=HousingCharacteristics, description=L.CHARACTERISTICS
	)
	tenure: Optional[str] = Field(default=None, description=L.TENURE)
	avg_real_estate_value: Optional[EconomicsValue] = Field(
		default=None, description=L.AVG_REAL_ESTATE_VALUE
	)
	nr_of_households: Optional[int] = Field(
		default=None, description=L.NR_OF_HOUSEHOLDS
	)
	households_per_km2: Optional[float] = Field(
		default=None, description=L.HOUSEHOLDS_PER_KM2
	)


class HousingKeys(PriceIndexFixedKeys):
	DWELLING_TYPE = "dwelling_type"
	CHARACTERISTICS = "characteristics"
	TENURE = "tenure"
	AVG_REAL_ESTATE_VALUE = "avg_real_estate_value"
	NR_OF_HOUSEHOLDS = "nr_of_households"
	HOUSEHOLDS_PER_KM2 = "households_per_km2"
