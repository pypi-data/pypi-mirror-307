from datetime import datetime
from models.news.news_article import NewsArticleModel
from models.news.news_stock import NewsStockModel

def test_news_article_model(session):
    # Create test data
    article = NewsArticleModel(
        id="test123",
        source="Reuters",
        headline="Test Headline",
        summary="This is a test summary",
        url="https://example.com/news",
        published_at=datetime.now()
    )
    
    session.add(article)
    session.commit()
    
    result = session.query(NewsArticleModel).filter_by(id="test123").first()
    assert result.id == "test123"
    assert result.source == "Reuters"
    assert result.headline == "Test Headline"

def test_news_stock_model(session):
    # Create test data
    news_stock = NewsStockModel(
        news_id="test123",
        symbol="AAPL",
        published_at=datetime.now()
    )
    
    session.add(news_stock)
    session.commit()
    
    result = session.query(NewsStockModel).filter_by(news_id="test123").first()
    assert result.news_id == "test123"
    assert result.symbol == "AAPL"

def test_news_relationship(session):
    # Test the relationship between news articles and stocks
    article = NewsArticleModel(
        id="test123",
        source="Reuters",
        headline="Test Headline",
        summary="This is a test summary",
        url="https://example.com/news",
        published_at=datetime.now()
    )
    
    news_stock = NewsStockModel(
        news_id="test123",
        symbol="AAPL",
        published_at=datetime.now()
    )
    
    session.add(article)
    session.add(news_stock)
    session.commit()
    
    result = session.query(NewsStockModel).filter_by(news_id="test123").first()
    assert result.news_id == article.id
    assert result.symbol == "AAPL" 