from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


###########################################
########## Start Model defenition #########
###########################################
class CompositionLegends:
	TYPE = "Composition of households descibing nr and type of household members."


CL = CompositionLegends


class Composition(DataGardenSubModel):
	type: Optional[str] = Field(default=None, description=CL.TYPE)


class CompositionKeys:
	TYPE = "type"
