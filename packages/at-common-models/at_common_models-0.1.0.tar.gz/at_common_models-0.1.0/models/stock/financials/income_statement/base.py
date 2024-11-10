from sqlalchemy import Column, String, DateTime, DOUBLE
from models.base import Base

class BaseIncomeStatementModel(Base):
    """Base model for income statements (both annual and quarter)"""
    __abstract__ = True

    # Identifying information
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Revenue and direct costs
    revenue = Column(DOUBLE, nullable=False, default=0.0)
    cost_of_revenue = Column(DOUBLE, nullable=False, default=0.0)
    gross_profit = Column(DOUBLE, nullable=False, default=0.0)
    gross_profit_ratio = Column(DOUBLE, nullable=False, default=0.0)

    # Operating expenses breakdown
    research_and_development_expenses = Column(DOUBLE, nullable=False, default=0.0)
    general_and_administrative_expenses = Column(DOUBLE, nullable=False, default=0.0)
    selling_and_marketing_expenses = Column(DOUBLE, nullable=False, default=0.0)
    selling_general_and_administrative_expenses = Column(DOUBLE, nullable=False, default=0.0)
    other_expenses = Column(DOUBLE, nullable=False, default=0.0)
    operating_expenses = Column(DOUBLE, nullable=False, default=0.0)
    cost_and_expenses = Column(DOUBLE, nullable=False, default=0.0)

    # Interest and depreciation
    interest_income = Column(DOUBLE, nullable=False, default=0.0)
    interest_expense = Column(DOUBLE, nullable=False, default=0.0)
    depreciation_and_amortization = Column(DOUBLE, nullable=False, default=0.0)

    # Profitability metrics
    ebitda = Column(DOUBLE, nullable=False, default=0.0)
    operating_income = Column(DOUBLE, nullable=False, default=0.0)
    total_other_income_expenses_net = Column(DOUBLE, nullable=False, default=0.0)
    income_before_tax = Column(DOUBLE, nullable=False, default=0.0)
    income_tax_expense = Column(DOUBLE, nullable=False, default=0.0)
    net_income = Column(DOUBLE, nullable=False, default=0.0)

    # Per share metrics
    eps = Column(DOUBLE, nullable=False, default=0.0)
    eps_diluted = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()