"""Market data MCP server (stdio).

Small, fast surface for an investing assistant: quotes, performance summary,
fund details and recent news. Backed by yfinance with an in-memory TTL cache.

Run standalone:  uv run python -m market_mcp.server
Inspect:         uv run mcp dev market_mcp/server.py   (or MCP Inspector)
"""

from __future__ import annotations

import logging
import math
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from functools import wraps
from typing import Any

import pandas as pd
import yfinance as yf
from mcp.server.mcpserver import MCPServer

log = logging.getLogger("market_mcp")

mcp = MCPServer(
    "market-data",
    instructions=(
        "Live market data for an investing assistant. Use get_quotes for current "
        "prices/valuation, get_performance for historical returns and risk, "
        "get_fund_info for ETF/mutual fund costs and holdings, get_news for recent "
        "headlines. Prefer batching symbols into one get_quotes call."
    ),
)

MAX_SYMBOLS = 10
PROVIDER = "Yahoo Finance via yfinance (delayed, not real-time)"
_pool = ThreadPoolExecutor(max_workers=8)
_cache: dict[tuple, tuple[float, Any]] = {}


def ttl_cache(seconds: int):
    """Memoize a function's result per-arguments for `seconds`. Errors aren't cached."""

    def deco(fn):
        @wraps(fn)
        def wrapper(*args):
            key = (fn.__name__, *args)
            hit = _cache.get(key)
            if hit and time.monotonic() - hit[0] < seconds:
                return hit[1]
            value = fn(*args)
            if not (isinstance(value, dict) and "error" in value):
                _cache[key] = (time.monotonic(), value)
            return value

        return wrapper

    return deco


def _num(value: Any, digits: int = 2) -> float | None:
    """Round numeric values, dropping NaN/inf/non-numbers (yfinance returns all of these)."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return round(f, digits) if math.isfinite(f) else None


def _pct(value: Any) -> float | None:
    """Fraction (0.0123) -> percent (1.23)."""
    f = _num(value, 6)
    return None if f is None else round(f * 100, 2)


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _clean_symbol(symbol: str) -> str:
    return symbol.strip().upper()


# --------------------------------------------------------------------------- quotes


@ttl_cache(60)
def _quote(symbol: str) -> dict[str, Any]:
    try:
        info = yf.Ticker(symbol).info or {}
    except Exception as exc:  # yfinance raises a zoo of exception types
        return {"symbol": symbol, "error": f"lookup failed: {exc}"}
    price = info.get("regularMarketPrice") or info.get("currentPrice") or info.get("navPrice")
    if price is None:
        return {"symbol": symbol, "error": "unknown symbol or no price data"}

    # dividendYield is already a percent in current yfinance; yield (funds) is a fraction.
    div_yield = _num(info.get("dividendYield"))
    if div_yield is None and info.get("yield") is not None:
        div_yield = _pct(info.get("yield"))

    quote_time = info.get("regularMarketTime")
    out = {
        "symbol": symbol,
        "name": info.get("longName") or info.get("shortName"),
        "type": info.get("quoteType"),
        "exchange": info.get("fullExchangeName") or info.get("exchange"),
        "currency": info.get("currency"),
        "price": _num(price),
        "previous_close": _num(info.get("regularMarketPreviousClose") or info.get("previousClose")),
        "change_pct_today": _num(info.get("regularMarketChangePercent")),
        "market_state": info.get("marketState"),
        "quote_time": datetime.fromtimestamp(quote_time, UTC).isoformat(timespec="seconds")
        if isinstance(quote_time, int | float)
        else None,
        "data_delay_min": info.get("exchangeDataDelayedBy"),
        "week52_low": _num(info.get("fiftyTwoWeekLow")),
        "week52_high": _num(info.get("fiftyTwoWeekHigh")),
        "market_cap": info.get("marketCap"),
        "trailing_pe": _num(info.get("trailingPE")),
        "forward_pe": _num(info.get("forwardPE")),
        "dividend_yield_pct": div_yield,
        "beta": _num(info.get("beta") or info.get("beta3Year")),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "fund_total_assets": info.get("totalAssets"),
        "provider": PROVIDER,
        "retrieved_at": _now(),
    }
    return {k: v for k, v in out.items() if v is not None}


@mcp.tool()
def get_quotes(symbols: list[str]) -> dict[str, Any]:
    """Current price, today's % change, 52-week range, valuation (P/E), dividend yield
    and beta for up to 10 stock/ETF/fund tickers in one call, e.g. ["VOO", "AAPL"]."""
    clean = list(dict.fromkeys(_clean_symbol(s) for s in symbols if s.strip()))[:MAX_SYMBOLS]
    if not clean:
        return {"error": "no symbols given"}
    return {"quotes": list(_pool.map(_quote, clean))}


# --------------------------------------------------------------------- performance


@ttl_cache(3600)
def _performance(symbol: str) -> dict[str, Any]:
    try:
        hist = yf.Ticker(symbol).history(period="10y", interval="1d", auto_adjust=True)
    except Exception as exc:
        return {"symbol": symbol, "error": f"history failed: {exc}"}
    closes = hist["Close"].dropna() if not hist.empty else None
    if closes is None or len(closes) < 30:
        return {"symbol": symbol, "error": "not enough price history"}

    last = closes.iloc[-1]
    last_date = closes.index[-1]

    def total_return(days: int) -> float | None:
        window = closes[closes.index >= last_date - _days(days)]
        if window.empty or window.index[0] > last_date - _days(days - 7):
            return None  # history doesn't reach back far enough
        return _pct(last / window.iloc[0] - 1)

    def cagr(years: int) -> float | None:
        window = closes[closes.index >= last_date - _days(365 * years)]
        if window.empty or window.index[0] > last_date - _days(365 * years - 7):
            return None
        return _pct((last / window.iloc[0]) ** (1 / years) - 1)

    daily = closes[closes.index >= last_date - _days(365)].pct_change().dropna()
    drawdown = (closes / closes.cummax() - 1).min()

    return {
        "symbol": symbol,
        "last_close": _num(last),
        "return_pct": {
            "1m": total_return(30),
            "3m": total_return(91),
            "ytd": _pct(last / closes[closes.index.year == last_date.year].iloc[0] - 1),
            "1y": total_return(365),
        },
        "annualized_return_pct": {"3y": cagr(3), "5y": cagr(5), "10y": cagr(10)},
        "volatility_1y_annualized_pct": _pct(daily.std() * math.sqrt(252)),
        "max_drawdown_pct": _pct(drawdown),
        "history_start": closes.index[0].date().isoformat(),
        "as_of": last_date.date().isoformat(),
        "note": "Returns are price + dividends (adjusted). Past performance is not predictive.",
    }


def _days(n: int) -> pd.Timedelta:
    return pd.Timedelta(days=n)


@mcp.tool()
def get_performance(symbol: str) -> dict[str, Any]:
    """Historical performance summary for one ticker: 1m/3m/YTD/1y total return,
    3y/5y/10y annualized return, 1y volatility and max drawdown (up to 10y)."""
    return _performance(_clean_symbol(symbol))


# -------------------------------------------------------------------------- funds


@ttl_cache(86400)
def _fund(symbol: str) -> dict[str, Any]:
    try:
        fd = yf.Ticker(symbol).funds_data
        overview = fd.fund_overview or {}
        ops = fd.fund_operations
        holdings = fd.top_holdings
        sectors = fd.sector_weightings or {}
        classes = fd.asset_classes or {}
    except Exception as exc:
        return {"symbol": symbol, "error": f"not a fund or no fund data: {exc}"}

    def op(attr: str) -> Any:
        try:
            return ops.loc[attr, symbol]
        except Exception:
            return None

    top = (
        [
            {"symbol": sym, "name": row.get("Name"), "weight_pct": _pct(row.get("Holding Percent"))}
            for sym, row in holdings.head(10).iterrows()
        ]
        if holdings is not None and not holdings.empty
        else []
    )

    return {
        "symbol": symbol,
        "category": overview.get("categoryName"),
        "family": overview.get("family"),
        "legal_type": overview.get("legalType"),
        "expense_ratio_pct": _pct(op("Annual Report Expense Ratio")),
        "turnover_pct": _pct(op("Annual Holdings Turnover")),
        "asset_classes_pct": {k: _pct(v) for k, v in classes.items() if _pct(v)},
        "top_sectors_pct": dict(
            sorted(((k, _pct(v)) for k, v in sectors.items() if _pct(v)), key=lambda kv: -kv[1])[:6]
        ),
        "top_holdings": top,
        "top10_weight_pct": round(sum(h["weight_pct"] or 0 for h in top), 2) if top else None,
        "provider": PROVIDER,
        "retrieved_at": _now(),
    }


@mcp.tool()
def get_fund_info(symbol: str) -> dict[str, Any]:
    """ETF / mutual fund details: category, expense ratio, turnover, asset-class mix,
    top sectors and top 10 holdings. Use to compare index funds or check fees."""
    return _fund(_clean_symbol(symbol))


# --------------------------------------------------------------------------- news


@ttl_cache(900)
def _news(query: str, limit: int) -> dict[str, Any]:
    try:
        items = yf.Search(query, news_count=limit, max_results=0).news or []
    except Exception as exc:
        return {"query": query, "error": f"news search failed: {exc}"}
    return {
        "query": query,
        "articles": [
            {
                "title": a.get("title"),
                "publisher": a.get("publisher"),
                "published": datetime.fromtimestamp(a["providerPublishTime"], UTC).date().isoformat()
                if a.get("providerPublishTime")
                else None,
                "tickers": a.get("relatedTickers"),
                "link": a.get("link"),
            }
            for a in items[:limit]
        ],
        "provider": PROVIDER,
        "retrieved_at": _now(),
    }


@mcp.tool()
def get_news(query: str = "stock market", limit: int = 5) -> dict[str, Any]:
    """Recent news headlines. `query` can be a ticker ("NVDA"), company name, or
    topic ("interest rates", "stock market"). Returns title, publisher, date, link."""
    return _news(query.strip() or "stock market", max(1, min(int(limit), 10)))


# --------------------------------------------------------------------------------


def main() -> None:
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # unknown tickers are reported in-band
    mcp.run("stdio")


if __name__ == "__main__":
    main()
