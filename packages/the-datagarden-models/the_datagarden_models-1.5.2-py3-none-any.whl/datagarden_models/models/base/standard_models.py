from typing import Optional

from pydantic import Field

from .models import DataGardenSubModel


class EconomicBaseKeys:
	VALUE = "value"
	UNIT = "unit"
	CURRENCY = "currency"


class EconomicBaseLegends:
	VALUE = "value in units of given currency,"
	UNIT = "units of measure."
	CURRENCY = "currency of measure."


L = EconomicBaseLegends


class EconomicsValue(DataGardenSubModel):
	value: Optional[float] = Field(default=None, description=L.VALUE)
	unit: int = Field(default=1, description=L.UNIT)
	currency: str = Field(default="EUR", description=L.CURRENCY)
