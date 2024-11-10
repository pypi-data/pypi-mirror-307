from sqlalchemy import Column, String, DateTime, DOUBLE
from models.base import Base

class BaseBalanceSheetStatementModel(Base):
    """Base model for balance sheet statements (both annual and quarter)"""
    __abstract__ = True

    # Primary identifiers
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Current Assets
    cash_and_cash_equivalents = Column(DOUBLE, nullable=False, default=0.0)
    short_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    cash_and_short_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    net_receivables = Column(DOUBLE, nullable=False, default=0.0)
    inventory = Column(DOUBLE, nullable=False, default=0.0)
    other_current_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_current_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Non-Current Assets
    property_plant_equipment_net = Column(DOUBLE, nullable=False, default=0.0)
    goodwill = Column(DOUBLE, nullable=False, default=0.0)
    intangible_assets = Column(DOUBLE, nullable=False, default=0.0)
    goodwill_and_intangible_assets = Column(DOUBLE, nullable=False, default=0.0)
    long_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    tax_assets = Column(DOUBLE, nullable=False, default=0.0)
    other_non_current_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_non_current_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Asset Totals
    other_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Current Liabilities
    account_payables = Column(DOUBLE, nullable=False, default=0.0)
    short_term_debt = Column(DOUBLE, nullable=False, default=0.0)
    tax_payables = Column(DOUBLE, nullable=False, default=0.0)
    deferred_revenue = Column(DOUBLE, nullable=False, default=0.0)
    other_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    total_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Non-Current Liabilities
    long_term_debt = Column(DOUBLE, nullable=False, default=0.0)
    deferred_revenue_non_current = Column(DOUBLE, nullable=False, default=0.0)
    deferred_tax_liabilities_non_current = Column(DOUBLE, nullable=False, default=0.0)
    other_non_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    total_non_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Liability Totals
    other_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    capital_lease_obligations = Column(DOUBLE, nullable=False, default=0.0)
    total_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Stockholders' Equity
    preferred_stock = Column(DOUBLE, nullable=False, default=0.0)
    common_stock = Column(DOUBLE, nullable=False, default=0.0)
    retained_earnings = Column(DOUBLE, nullable=False, default=0.0)
    accumulated_other_comprehensive_income_loss = Column(DOUBLE, nullable=False, default=0.0)
    other_total_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    total_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    total_equity = Column(DOUBLE, nullable=False, default=0.0)

    # Balance Sheet Totals
    total_liabilities_and_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    minority_interest = Column(DOUBLE, nullable=False, default=0.0)
    total_liabilities_and_total_equity = Column(DOUBLE, nullable=False, default=0.0)

    # Additional Financial Metrics
    total_investments = Column(DOUBLE, nullable=False, default=0.0)
    total_debt = Column(DOUBLE, nullable=False, default=0.0)
    net_debt = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()
