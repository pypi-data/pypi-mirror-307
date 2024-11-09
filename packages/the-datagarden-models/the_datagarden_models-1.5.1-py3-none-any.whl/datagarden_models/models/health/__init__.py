from pydantic import Field

from ..base import DataGardenModel, DataGardenModelLegends
from .base_health import HealthBaseKeys
from .death_statistics import DeathStatistics, DeathStatisticsKeys
from .health_care_facilities import HealthCareFacilities, HealthCareFacilitiesKeys


class HealthV1Keys(HealthBaseKeys, DeathStatisticsKeys, HealthCareFacilitiesKeys):
	DEATH_STATISTICS = "death_statistics"
	HEALTH_CARE_FACILITIES = "health_care_facilities"
	DATAGARDEN_MODEL_NAME = "Health"


class HealthV1Legends(DataGardenModelLegends):
	DEATH_RATE_BY_IDC10 = (
		"Death rate by IDC10 categorization, see https://icd.who.int/browse10/2010/en"
		" (for detailed description of IDC10 categories (keys in this dataset))"
		" Death rate in deaths per 100.000 population."
	)
	DEATH_STATISTICS = "Death statistics for the rgion"
	HEALTH_CARE_FACILITIES = "Healthcare facilities available in the region"


L = HealthV1Legends


class HealthV1(DataGardenModel):
	MODEL_LEGEND: str = "Health data for a region. "
	datagarden_model_version: str = Field(
		"v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION
	)

	death_statistics: DeathStatistics = Field(
		default_factory=DeathStatistics, description=L.DEATH_STATISTICS
	)
	health_care_facilities: HealthCareFacilities = Field(
		default_factory=HealthCareFacilities, description=L.HEALTH_CARE_FACILITIES
	)
