from typing import Optional

from pydantic import Field

from ..base import DataGardenSubModel
from .base_demographics import AgeGender


class PopulationV1Legends:
	BY_AGE_GENDER = "Age gender distribution for males and females. "
	TOTAL = "Total population. " "In number of individuals."

	TOTAL_MALE = "Total number of males in the population. " "In number of individuals."
	TOTAL_FEMALE = (
		"Total number of females in the population. " "In number of individuals."
	)
	POPULATION_TOTAL = (
		"Total number of persons in the population. " "In number of individuals."
	)
	MALE_FEMALE_RATIO = "Males to femal ratio. " "In number of males per 100 females."
	DENSITY = "Persons per square KM."
	CHANGE = (
		"Population change in number of persons. "
		"In number of individuals per 1000 people."
	)
	NATURAL_CHANGE = "Births minus Deaths. In number of individuals."
	NATURAL_CHANGE_RATE = "Rate of Natural change per 1.000 persons."


L = PopulationV1Legends


class Population(DataGardenSubModel):
	by_age_gender: AgeGender = Field(
		default_factory=AgeGender, description=L.BY_AGE_GENDER
	)
	total: Optional[float] = Field(default=None, description=L.TOTAL)

	total_male: Optional[float] = Field(default=None, description=L.TOTAL_MALE)
	total_female: Optional[float] = Field(default=None, description=L.TOTAL_FEMALE)
	male_to_female_ratio: Optional[float] = Field(
		default=None, description=L.MALE_FEMALE_RATIO
	)
	density: Optional[float] = Field(default=None, description=L.DENSITY)
	change: Optional[float] = Field(default=None, description=L.CHANGE)
	natural_change: Optional[float] = Field(default=None, description=L.NATURAL_CHANGE)
	natural_change_rate: Optional[float] = Field(
		default=None, description=L.NATURAL_CHANGE_RATE
	)


class PopulationV1Keys:
	POPULATION = "population"
	BY_AGE_GENDER = "by_age_gender"
	TOTAL = "total"
	TOTAL_MALE = "total_male"
	TOTAL_FEMALE = "total_female"
	MALE_TO_FEMALE_RATIO = "male_to_female_ratio"
	DENSITY = "density"
	CHANGE = "change"
	NATURAL_CHANGE = "natural_change"
	NATURAL_CHANGE_RATE = "natural_change_rate"
