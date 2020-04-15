import os
import pytest

from app.robo_advisor import to_usd, get_response, compile_url, divider

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

def test_divider():
    result = divider()
    assert result == "-------------------------"
