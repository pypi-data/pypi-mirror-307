from pydantic import Field

from ..base import DataGardenModel, DataGardenModelLegends
from .base_economics import EconomicBaseKeys
from .gdp import GDP, GDPV1Keys
from .inflation import Inflation, InflationV1Keys
from .trade import TradeV1, TradeV1Keys


class EconomicsV1Keys(GDPV1Keys, EconomicBaseKeys, InflationV1Keys, TradeV1Keys):
	GDP = "gdp"
	DATAGARDEN_MODEL_NAME = "Economics"
	INFLATION = "inflation"
	TRADE = "trade"


class EconomicsV1Legends(DataGardenModelLegends):
	GDP = "Gross Domestic Product"
	INFLATION = "Inflation numbers"
	TRADE = "Trade statistics"


L = EconomicsV1Legends


class EconomicsV1(DataGardenModel):
	MODEL_LEGEND: str = "Economic data for a region. "
	datagarden_model_version: str = Field(
		"v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION
	)
	gdp: GDP = Field(default_factory=GDP, description=L.GDP)
	inflation: Inflation = Field(default_factory=Inflation, description=L.INFLATION)
	trade: TradeV1 = Field(default_factory=TradeV1, description=L.TRADE)
