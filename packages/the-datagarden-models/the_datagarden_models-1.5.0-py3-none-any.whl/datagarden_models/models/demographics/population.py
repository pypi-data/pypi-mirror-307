from typing import Optional

from pydantic import Field

from ..base import DataGardenSubModel
from .base_demographics import AgeGender


###########################################
########## Start Model defenition #########
###########################################
class MigrationBackgroundKeys:
	PERCENTAGE_OF_POPULATION = "percentage_of_population"
	POPULATION_COUNT = "population_count"


class MigrationBackgroundLegends:
	PERCENTAGE_OF_POPULATION = (
		"Percentage of the population by type of migration background."
	)
	POPULATION_COUNT = "Number of individuals with a given migration background."


MB = MigrationBackgroundLegends


class MigrationBackground(DataGardenSubModel):
	percentage_of_population: Optional[float] = Field(
		default=None, description=MB.PERCENTAGE_OF_POPULATION
	)
	population_count: Optional[float] = Field(
		default=None, description=MB.POPULATION_COUNT
	)


###########################################
########## Start Model defenition #########
###########################################
class NativityKeys:
	PERCENTAGE_BY_TYPE = "percentage_by_type"
	PERCENTAGE_BORN_IN_COUNTRY = "percentage_born_in_country"
	PERCENTAGE_BORN_OUTSIDE_COUNTRY = "percentage_born_outside_country"


class NativityLegends:
	PERCENTAGE_BY_TYPE = "Percentage of the population by type of birth location."
	PERCENTAGE_BORN_IN_COUNTRY = "Percentage of the population born in the country."
	PERCENTAGE_BORN_OUTSIDE_COUNTRY = (
		"Percentage of the population born outside the country."
	)


NK = NativityLegends


class Nativity(DataGardenSubModel):
	percentage_born_in_country: Optional[float] = Field(
		default=None, description=NK.PERCENTAGE_BORN_IN_COUNTRY
	)
	percentage_born_outside_country: Optional[float] = Field(
		default=None, description=NK.PERCENTAGE_BORN_OUTSIDE_COUNTRY
	)
	percentage_by_type: Optional[dict[str, float]] = Field(
		default_factory=dict, description=NK.PERCENTAGE_BY_TYPE
	)


###########################################
########## Start Model defenition #########
###########################################
class EthnicityKeys:
	NATIVITY = "nativity"
	MIGRATION_BACKGROUND = "migration_background"


class EthnicityLegends:
	NATIVITY = "Data on birth location of the population."
	MIGRATION_BACKGROUND = "Data on migration background of the population."


EK = EthnicityLegends


class Ethnicity(DataGardenSubModel):
	nativity: Nativity = Field(default_factory=Nativity, description=EK.NATIVITY)
	migration_background: MigrationBackground = Field(
		default_factory=MigrationBackground, description=EK.MIGRATION_BACKGROUND
	)


###########################################
########## Start Model defenition #########
###########################################
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
	ETHNICITY = "Ethnicity distribution for the population."


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
	ethnicity: Ethnicity = Field(default_factory=Ethnicity, description=L.ETHNICITY)


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
	ETHNICITY = "ethnicity"
