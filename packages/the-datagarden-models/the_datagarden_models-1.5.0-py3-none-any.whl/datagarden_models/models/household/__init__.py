from pydantic import Field

from datagarden_models.models.base import DataGardenModel
from datagarden_models.models.base.legend import DataGardenModelLegends

from .composition import Composition, CompositionV1Keys
from .housing import Housing, HousingV1Keys


###########################################
########## Start Model defenition #########
###########################################
class HouseholdV1Keys(CompositionV1Keys, HousingV1Keys):
	DATAGARDEN_MODEL_NAME = "Household"
	COMPOSITION = "composition"
	HOUSING = "housing"


class HouseholdV1Legends(DataGardenModelLegends):
	COMPOSITION = "Data on composition of households for a region. "
	HOUSING = "Data on housing for a region. "


L = HouseholdV1Legends


class HouseholdV1(DataGardenModel):
	MODEL_LEGEND: str = "Data on household type and composition for a region. "
	composition: Composition = Field(
		default_factory=Composition, description=L.COMPOSITION
	)
	housing: Housing = Field(default_factory=Housing, description=L.HOUSING)
