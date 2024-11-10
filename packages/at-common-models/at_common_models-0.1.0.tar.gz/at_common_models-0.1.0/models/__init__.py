# Import all models to register them with SQLAlchemy
from models.stock.overview import OverviewModel
from models.stock.daily_candlestick import DailyCandlestickModel
from models.stock.daily_indicator import DailyIndicatorModel
from models.stock.quotation import QuotationModel
from models.stock.financials.balance_sheet_statement.annual import AnnualBalanceSheetStatementModel
from models.stock.financials.balance_sheet_statement.quarter import QuarterBalanceSheetStatementModel
from models.stock.financials.income_statement.annual import AnnualIncomeStatementModel
from models.stock.financials.income_statement.quarter import QuarterlyIncomeStatementModel
from models.stock.financials.cashflow_statement.annual import AnnualCashFlowStatementModel
from models.stock.financials.cashflow_statement.quarter import QuarterCashflowStatementModel
from models.news.news_article import NewsArticleModel
from models.news.news_stock import NewsStockModel

# These imports will register all models with the Base.metadata
__all__ = [
    'OverviewModel',
    'DailyCandlestickModel',
    'DailyIndicatorModel',
    'QuotationModel',
    'AnnualBalanceSheetStatementModel',
    'QuarterBalanceSheetStatementModel',
    'AnnualIncomeStatementModel',
    'QuarterlyIncomeStatementModel',
    'AnnualCashFlowStatementModel',
    'QuarterCashflowStatementModel',
    'NewsArticleModel',
    'NewsStockModel'
]
