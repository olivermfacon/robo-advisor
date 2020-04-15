import os
import pytest

from app.robo_advisor import to_usd, get_response, compile_url

def test_to_usd():
    result = to_usd(5)
    assert result == "$5.00"
    result = to_usd(2100.1)
    assert result == "$2,100.10"
    result = to_usd(21.99)
    assert result == "$21.99"

def test_compile_url():
    result = compile_url("MSFT")
    assert result[:72] == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT"

#CI_ENV = os.environ.get("api_key_env") == "true"
#
#@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")
#def test_get_response():
#    symbol = "MSFT"
#
#    parsed_response = get_response(symbol)
#
#    assert isinstance(parsed_response, dict)
#    assert "Meta Data" in parsed_response.keys()
#    assert "Time Series (Daily)" in parsed_response.keys()
#    assert parsed_response["Meta Data"]["2. Symbol"] == symbol

