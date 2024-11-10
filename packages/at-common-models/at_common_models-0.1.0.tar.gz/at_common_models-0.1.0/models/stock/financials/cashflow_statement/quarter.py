from models.stock.financials.cashflow_statement.base import BaseCashflowStatementModel

class QuarterCashflowStatementModel(BaseCashflowStatementModel):
    __tablename__ = "stock_financials_quarter_cashflow_statements"