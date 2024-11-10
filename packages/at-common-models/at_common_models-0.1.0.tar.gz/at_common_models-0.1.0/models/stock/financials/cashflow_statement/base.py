from sqlalchemy import Column, String, DateTime, DOUBLE
from models.base import Base

class BaseCashflowStatementModel(Base):
    """Base model for cash flow statements (both annual and quarter)"""
    __abstract__ = True

    # Primary identifiers
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Operating Activities - Core Operations
    net_income = Column(DOUBLE, nullable=False, default=0.0)
    depreciation_and_amortization = Column(DOUBLE, nullable=False, default=0.0)
    deferred_income_tax = Column(DOUBLE, nullable=False, default=0.0)
    stock_based_compensation = Column(DOUBLE, nullable=False, default=0.0)

    # Operating Activities - Working Capital Changes
    change_in_working_capital = Column(DOUBLE, nullable=False, default=0.0)
    accounts_receivables = Column(DOUBLE, nullable=False, default=0.0)
    inventory = Column(DOUBLE, nullable=False, default=0.0)
    accounts_payables = Column(DOUBLE, nullable=False, default=0.0)
    other_working_capital = Column(DOUBLE, nullable=False, default=0.0)
    other_non_cash_items = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_provided_by_operating_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Investing Activities
    investments_in_property_plant_and_equipment = Column(DOUBLE, nullable=False, default=0.0)
    acquisitions_net = Column(DOUBLE, nullable=False, default=0.0)
    purchases_of_investments = Column(DOUBLE, nullable=False, default=0.0)
    sales_maturities_of_investments = Column(DOUBLE, nullable=False, default=0.0)
    other_investing_activities = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_used_for_investing_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Financing Activities
    debt_repayment = Column(DOUBLE, nullable=False, default=0.0)
    common_stock_issued = Column(DOUBLE, nullable=False, default=0.0)
    common_stock_repurchased = Column(DOUBLE, nullable=False, default=0.0)
    dividends_paid = Column(DOUBLE, nullable=False, default=0.0)
    other_financing_activities = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_used_provided_by_financing_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Cash Position and Summary Metrics
    effect_of_forex_changes_on_cash = Column(DOUBLE, nullable=False, default=0.0)
    net_change_in_cash = Column(DOUBLE, nullable=False, default=0.0)
    cash_at_end_of_period = Column(DOUBLE, nullable=False, default=0.0)
    cash_at_beginning_of_period = Column(DOUBLE, nullable=False, default=0.0)
    operating_cash_flow = Column(DOUBLE, nullable=False, default=0.0)
    capital_expenditure = Column(DOUBLE, nullable=False, default=0.0)
    free_cash_flow = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()
