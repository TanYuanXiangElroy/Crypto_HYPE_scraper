import pytest
import requests
# The imports now include the top-level package name
from Crypto_HYPE_scraper.scraper import hyperliquid_native
from Crypto_HYPE_scraper.scraper.exceptions import ScrapingError

# Mark all tests in this file as belonging to the "scrapers" group
pytestmark = pytest.mark.scrapers


def test_scrape_hyperliquid_native_success(mocker):
    """
    Tests the happy path for the hyperliquid_native scraper where the API
    call is successful and returns valid data.
    """
    # 1. Arrange
    fake_api_response = {"midPx": "123.45"}
    
    # We also update the path to patch for the mock
    mock_post = mocker.patch('Crypto_HYPE_scraper.scraper.hyperliquid_native.requests.post')
    
    mock_post.return_value.json.return_value = fake_api_response
    mock_post.return_value.raise_for_status.return_value = None

    # 2. Act
    result = hyperliquid_native.scrape()

    # 3. Assert
    assert result is not None
    assert result['spot_price'] == 123.45
    assert result['pool_name'] == "HYPE / USDC (Native)"
    mock_post.assert_called_once()


def test_scrape_hyperliquid_native_api_error(mocker):
    """
    Tests that the hyperliquid_native scraper correctly raises ScrapingError
    when the API call fails (e.g., HTTPError).
    """
    # 1. Arrange
    # Configure the mock to raise an HTTPError when requests.post is called
    mock_post = mocker.patch('Crypto_HYPE_scraper.scraper.hyperliquid_native.requests.post')
    mock_post.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url: http://example.com")

    # 2. Act & Assert
    # We expect a ScrapingError to be raised when the scraper is called
    with pytest.raises(ScrapingError) as excinfo:
        hyperliquid_native.scrape()
    
    # Optionally, you can assert details about the raised exception
    assert "Hyperliquid API request failed" in str(excinfo.value)
    assert "404 Client Error" in str(excinfo.value)