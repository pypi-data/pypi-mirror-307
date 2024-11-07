from typing import Annotated, Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


########## Start Model defenition #########
class CurrentAccountBalanceLegends:
	VALUE = "Current account balance value."
	CURRENCY = "Currency of the trade balance value."
	PERCENTAGE_OF_GDP = "Current accounts as a percentage of GDP."


CA = CurrentAccountBalanceLegends


class CurrentAccountBalance(DataGardenSubModel):
	value: Optional[float] = Field(default=None, description=CA.VALUE)
	currency: Optional[str] = Field(default=None, description=CA.CURRENCY)
	percentage_of_gdp: Optional[float] = Field(
		default=None, description=CA.PERCENTAGE_OF_GDP
	)


########## Start Model defenition #########
class TradeBalanceTypeKeys:
	VALUE = "value"
	CURRENCY = "currency"
	PERCENTAGE_OF_IMPORTS = "percentage_of_imports"
	PERCENTAGE_OF_GDP = "percentage_of_gdp"
	NORMALIZED_TRADE_BALANCE = "normalized_trade_balance"


class TradeBalanceTypeLegends:
	VALUE = "Trade balance value."
	CURRENCY = "Currency of the trade balance value."
	PERCENTAGE_OF_IMPORTS = "Trade balance as a percentage of imports."
	PERCENTAGE_OF_GDP = "Trade balance as a percentage of GDP."
	NORMALIZED_TRADE_BALANCE = (
		"Normalized trade balance (-1 to 1, 0 means a fully balanced trade)."
	)


PI = TradeBalanceTypeLegends


class TradeBalanceType(DataGardenSubModel):
	value: Optional[float] = Field(default=None, description=PI.VALUE)
	currency: Optional[str] = Field(default=None, description=PI.CURRENCY)
	percentage_of_imports: Optional[float] = Field(
		default=None, description=PI.PERCENTAGE_OF_IMPORTS
	)
	percentage_of_gdp: Optional[float] = Field(
		default=None, description=PI.PERCENTAGE_OF_GDP
	)
	normalized_trade_balance: Optional[Annotated[float, Field(ge=-1, le=1)]] = Field(
		default=None, description=PI.NORMALIZED_TRADE_BALANCE
	)


########## Start Model defenition #########
class TradeBalanceKeys:
	SERVICES = "services"
	GOODS = "goods"
	SERVICES_AND_GOODS = "services_and_goods"
	CURRENT_ACCOUNT_BALANCE = "current_account_balance"


class TradeBalanceLegends:
	SERVICES = "Trade balance information for services."
	GOODS = "Trade balance information for goods."
	SERVICES_AND_GOODS = "Trade balance information for services and goods."
	CURRENT_ACCOUNT_BALANCE = "Current account balance information."


L_TB = TradeBalanceLegends


class TradeBalance(DataGardenSubModel):
	services: TradeBalanceType = Field(
		default_factory=TradeBalanceType, description=L_TB.SERVICES
	)
	goods: TradeBalanceType = Field(
		default_factory=TradeBalanceType, description=L_TB.GOODS
	)
	services_and_goods: TradeBalanceType = Field(
		default_factory=TradeBalanceType, description=L_TB.SERVICES_AND_GOODS
	)
	current_account_balance: CurrentAccountBalance = Field(
		default_factory=CurrentAccountBalance, description=L_TB.CURRENT_ACCOUNT_BALANCE
	)


########## Start Model defenition #########
class ImportExportKeys:
	SERVICES = "services"
	GOODS = "goods"
	SERVICES_AND_GOODS = "goods_and_services"


class ImportExportLegends:
	SERVICES = "Value for services trade."
	GOODS = "Value for goods trade."
	SERVICES_AND_GOODS = "Value for services and goods trade."


L_IMP_EXP = ImportExportLegends


class Import(DataGardenSubModel):
	goods: Optional[float] = Field(default=None, description=L_IMP_EXP.GOODS)
	services: Optional[float] = Field(default=None, description=L_IMP_EXP.SERVICES)
	goods_and_services: Optional[float] = Field(
		default=None, description=L_IMP_EXP.SERVICES_AND_GOODS
	)


class Export(Import): ...


########## Start Model defenition #########
class TradeV1Legends:
	IMPORTS = "Imports information."
	EXPORTS = "Exports information."
	TRADE_BALANCE = "Trade balance information."


L_TRADE_V1 = TradeV1Legends


class TradeV1(DataGardenSubModel):
	trade_balance: TradeBalance = Field(
		default_factory=TradeBalance, description=L_TRADE_V1.TRADE_BALANCE
	)
	imports: Import = Field(default_factory=Import, description=L_TRADE_V1.IMPORTS)
	exports: Export = Field(default_factory=Export, description=L_TRADE_V1.EXPORTS)


class TradeV1Keys(TradeBalanceTypeKeys, TradeBalanceKeys, ImportExportKeys):
	IMPORTS = "imports"
	EXPORTS = "exports"
	TRADE_BALANCE = "trade_balance"
