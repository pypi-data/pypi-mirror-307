from models.stock.financials.cashflow_statement.base import BaseCashflowStatementModel

class AnnualCashFlowStatementModel(BaseCashflowStatementModel):
    __tablename__ = "stock_financials_annual_cashflow_statements"