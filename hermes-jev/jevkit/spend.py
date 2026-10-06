"""What the week actually cost, and what it would have cost on every other model.

Two things make agent spend hard to reason about:

1. **A subscription seat looks free at the margin.** Work run on a flat-fee seat bills
   nothing per token, so it vanishes from a cost report and the seat looks like pure
   overhead. It is not free — it has a market value, which is what the same tokens
   would have cost metered. A seat is worth keeping when that value exceeds its fee.
2. **A per-token price is not a per-task price.** Models differ by an order of magnitude
   in how many tokens they burn reaching the same answer, so the cheapest price can be
   the dearest week. Counterfactuals here are priced on *observed* tokens, and the
   report says plainly that a model which thinks more would not have used the same ones.

So this answers the only question worth asking: given what actually ran this week, was
there a better deal available, and by how much.
"""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from . import catalog as catalog_mod

WEEK = 7 * 86400


@dataclass
class Usage:
    """One model's usage over the window. `cost_usd` is what was actually billed."""

    model: str                     # "provider:model" or a catalogue id
    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    source: str = "metered"        # "metered" | "subscription"
    seat: Optional[str] = None     # which flat-fee seat, when source == "subscription"
    label: Optional[str] = None    # lane / api key, when known

    @property
    def tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class Seat:
    """A flat-fee subscription. Its value is what its tokens would have cost metered."""

    name: str
    monthly_usd: float
    # What the seat's work would otherwise have run on. Without this a seat cannot be
    # valued at all — "free" and "priceless" are not the same number.
    market_equivalent: str
    note: str = ""


def _price(model: str, prices: Mapping[str, Mapping[str, float]]) -> Optional[Dict[str, float]]:
    if model in prices:
        return dict(prices[model])
    bare = model.split(":", 1)[-1]
    for key, value in prices.items():
        if key.split(":", 1)[-1] == bare:
            return dict(value)
    return None


def price_table(rows: Optional[Sequence[Mapping[str, Any]]] = None) -> Dict[str, Dict[str, float]]:
    rows = rows if rows is not None else catalog_mod.models()
    out: Dict[str, Dict[str, float]] = {}
    for row in rows:
        try:
            out[f"{row['provider']}:{row['model']}"] = {"input": float(row["input"]), "output": float(row["output"])}
        except (KeyError, TypeError, ValueError):
            continue
    return out


def cost_of(usage: Usage, model: str, prices: Mapping[str, Mapping[str, float]]) -> Optional[float]:
    """What `usage`'s tokens would have cost on `model`."""
    price = _price(model, prices)
    if price is None:
        return None
    return usage.input_tokens * price["input"] / 1e6 + usage.output_tokens * price["output"] / 1e6


def counterfactuals(
    rows: Sequence[Usage], candidates: Sequence[str], *,
    prices: Optional[Mapping[str, Mapping[str, float]]] = None, include_subscription: bool = True,
) -> List[Dict[str, Any]]:
    """What the whole window would have cost had every row run on each candidate."""
    prices = prices or price_table()
    considered = [r for r in rows if include_subscription or r.source == "metered"]
    total_in = sum(r.input_tokens for r in considered)
    total_out = sum(r.output_tokens for r in considered)
    out: List[Dict[str, Any]] = []
    for model in candidates:
        price = _price(model, prices)
        if price is None:
            out.append({"model": model, "cost_usd": None, "note": "not in the catalogue"})
            continue
        out.append({
            "model": model,
            "cost_usd": round(total_in * price["input"] / 1e6 + total_out * price["output"] / 1e6, 4),
            "input_per_m": price["input"], "output_per_m": price["output"],
        })
    out.sort(key=lambda row: (row["cost_usd"] is None, row["cost_usd"] or 0))
    return out


def seat_value(rows: Sequence[Usage], seats: Sequence[Seat], *,
               prices: Optional[Mapping[str, Mapping[str, float]]] = None, days: float = 7.0) -> List[Dict[str, Any]]:
    """Is each flat-fee seat earning its keep this window?"""
    prices = prices or price_table()
    out: List[Dict[str, Any]] = []
    for seat in seats:
        used = [r for r in rows if r.source == "subscription" and (r.seat or "") == seat.name]
        market = 0.0
        priced = True
        for row in used:
            value = cost_of(row, seat.market_equivalent, prices)
            if value is None:
                priced = False
                continue
            market += value
        share = seat.monthly_usd * days / 30.0
        out.append({
            "seat": seat.name,
            "fee_for_window_usd": round(share, 2),
            "tokens": sum(r.tokens for r in used),
            "requests": sum(r.requests for r in used),
            "market_value_usd": round(market, 2) if priced else None,
            "net_usd": round(market - share, 2) if priced else None,
            "verdict": ("unused — cancel or use it" if not used else
                        "earning its keep" if priced and market >= share else
                        "costing more than it saves" if priced else "market equivalent not priced"),
            "priced_against": seat.market_equivalent,
            "note": seat.note,
        })
    return out


def report(
    rows: Sequence[Usage], *, candidates: Sequence[str] = (), seats: Sequence[Seat] = (),
    days: float = 7.0, prices: Optional[Mapping[str, Mapping[str, float]]] = None,
) -> Dict[str, Any]:
    """The weekly picture: what ran, what it cost, and whether anything was a better deal."""
    prices = prices or price_table()
    metered = [r for r in rows if r.source == "metered"]
    subscription = [r for r in rows if r.source == "subscription"]
    spent = sum(r.cost_usd for r in metered)

    by_model: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        entry = by_model.setdefault(row.model, {"model": row.model, "source": row.source, "requests": 0,
                                                "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0})
        entry["requests"] += row.requests
        entry["input_tokens"] += row.input_tokens
        entry["output_tokens"] += row.output_tokens
        entry["cost_usd"] = round(entry["cost_usd"] + row.cost_usd, 4)
    for entry in by_model.values():
        tokens = entry["input_tokens"] + entry["output_tokens"]
        entry["per_m_effective"] = round(entry["cost_usd"] / (tokens / 1e6), 4) if tokens else None
        entry["tokens_per_request"] = round(tokens / entry["requests"]) if entry["requests"] else None

    by_lane: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if not row.label:
            continue
        entry = by_lane.setdefault(row.label, {"lane": row.label, "cost_usd": 0.0, "tokens": 0, "requests": 0})
        entry["cost_usd"] = round(entry["cost_usd"] + row.cost_usd, 4)
        entry["tokens"] += row.tokens
        entry["requests"] += row.requests

    alternatives = counterfactuals(rows, candidates, prices=prices) if candidates else []
    priced = [a for a in alternatives if a["cost_usd"] is not None]
    best = priced[0] if priced else None
    seat_rows = seat_value(rows, seats, prices=prices, days=days) if seats else []
    seat_fees = sum(s["fee_for_window_usd"] for s in seat_rows)

    return {
        "window_days": days,
        "spend": {
            "metered_usd": round(spent, 2),
            "subscription_fees_usd": round(seat_fees, 2),
            "total_usd": round(spent + seat_fees, 2),
            "requests": sum(r.requests for r in rows),
            "tokens": sum(r.tokens for r in rows),
            "subscription_tokens": sum(r.tokens for r in subscription),
        },
        "by_model": sorted(by_model.values(), key=lambda e: -e["cost_usd"]),
        "by_lane": sorted(by_lane.values(), key=lambda e: -e["cost_usd"]),
        "seats": seat_rows,
        "alternatives": alternatives,
        "best_alternative": best,
        "verdict": _verdict(spent, best, seat_rows),
        "caveat": ("Counterfactuals price the tokens that were actually produced. A model that reasons more "
                   "or less would not have produced the same tokens, so treat them as a floor, not a promise."),
    }


def _verdict(spent: float, best: Optional[Mapping[str, Any]], seats: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    if best and best.get("cost_usd") is not None:
        delta = spent - float(best["cost_usd"])
        if delta > 0.01:
            lines.append(f"Running everything metered on {best['model']} would have cost "
                         f"${best['cost_usd']:.2f} against ${spent:.2f} actually billed — ${delta:.2f} less.")
        else:
            lines.append(f"Nothing in the candidate list beat what was actually used "
                         f"(${spent:.2f}; best alternative ${best['cost_usd']:.2f}).")
    idle = [s["seat"] for s in seats if s["verdict"].startswith("unused")]
    if idle:
        lines.append("Paid for and unused this window: " + ", ".join(idle) + ".")
    paying = [s for s in seats if s.get("net_usd") is not None and s["net_usd"] > 0]
    for seat in paying:
        lines.append(f"{seat['seat']} returned ${seat['market_value_usd']:.2f} of work against a "
                     f"${seat['fee_for_window_usd']:.2f} share of its fee.")
    losing = [s for s in seats if s.get("net_usd") is not None and s["net_usd"] < 0 and s["tokens"]]
    for seat in losing:
        lines.append(f"{seat['seat']} returned only ${seat['market_value_usd']:.2f} against "
                     f"${seat['fee_for_window_usd']:.2f} — that work is cheaper metered.")
    return " ".join(lines) or "No comparison was possible from this window's data."


# ── collectors ───────────────────────────────────────────────────────────────

def from_json(path: str) -> List[Usage]:
    """Usage rows from a JSON list, e.g. an OpenRouter export you saved."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data.get("rows") if isinstance(data, dict) else data
    out: List[Usage] = []
    for row in rows or []:
        out.append(Usage(
            model=str(row.get("model") or row.get("model_permaslug") or "unknown"),
            requests=int(row.get("requests") or row.get("request_count") or 0),
            input_tokens=int(row.get("input_tokens") or row.get("tokens_prompt") or row.get("prompt_tokens") or 0),
            output_tokens=int(row.get("output_tokens") or row.get("tokens_completion") or row.get("completion_tokens") or 0),
            cost_usd=float(row.get("cost_usd") or row.get("usage") or row.get("total_usage") or 0.0),
            source=str(row.get("source") or "metered"),
            seat=row.get("seat"), label=row.get("label") or row.get("api_key") or row.get("lane")))
    return out


def from_hermes_sessions(state_db: str, *, since: Optional[float] = None, label: Optional[str] = None) -> List[Usage]:
    """Usage from a Hermes `state.db`, for work whose cost never reaches an invoice.

    Subscription turns bill nothing per token, so they are invisible to a provider's
    billing page — this is the only way to value them.
    """
    since = since if since is not None else time.time() - WEEK
    try:
        conn = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error:
        return []
    columns = {r[1] for r in conn.execute("pragma table_info(messages)")}
    if not {"role", "timestamp"} <= columns:
        return []
    model_col = "model" if "model" in columns else None
    token_col = "token_count" if "token_count" in columns else None
    if not (model_col and token_col):
        return []
    query = (f"select {model_col} as model, count(*) as n, sum(case when role='assistant' then {token_col} else 0 end) as out_t, "
             f"sum(case when role!='assistant' then {token_col} else 0 end) as in_t "
             f"from messages where timestamp > ? and {model_col} is not null and {token_col} is not null group by {model_col}")
    out: List[Usage] = []
    try:
        for row in conn.execute(query, (since,)):
            out.append(Usage(model=str(row["model"]), requests=int(row["n"] or 0),
                             input_tokens=int(row["in_t"] or 0), output_tokens=int(row["out_t"] or 0),
                             cost_usd=0.0, source="subscription", label=label))
    except sqlite3.Error:
        return []
    return out


def render(data: Mapping[str, Any]) -> str:
    """A report a person reads in a terminal, not a wall of JSON."""
    s = data["spend"]
    lines = [f"Spend over {data['window_days']:.0f} days",
             f"  metered        ${s['metered_usd']:>10,.2f}",
             f"  seat fees      ${s['subscription_fees_usd']:>10,.2f}",
             f"  total          ${s['total_usd']:>10,.2f}   ({s['requests']:,} requests, {s['tokens']:,} tokens)"]
    if data["by_model"]:
        lines += ["", f"  {'model':40}{'$':>10}{'tokens':>14}{'tok/req':>9}{'$/M':>9}"]
        for e in data["by_model"][:12]:
            tokens = e["input_tokens"] + e["output_tokens"]
            lines.append(f"  {e['model'][:38]:40}{e['cost_usd']:>10.2f}{tokens:>14,}"
                         f"{(e['tokens_per_request'] or 0):>9,}{(e['per_m_effective'] or 0):>9.3f}")
    if data["by_lane"]:
        lines += ["", "  by lane:"] + [
            f"    {e['lane'][:28]:30}${e['cost_usd']:>9,.2f}  {e['tokens']:>14,} tokens" for e in data["by_lane"][:8]]
    if data["seats"]:
        lines += ["", "  subscription seats:"]
        for seat in data["seats"]:
            value = f"${seat['market_value_usd']:,.2f}" if seat["market_value_usd"] is not None else "not priced"
            lines.append(f"    {seat['seat'][:20]:22} fee ${seat['fee_for_window_usd']:>8,.2f}   "
                         f"work worth {value:>12}   {seat['verdict']}")
    if data["alternatives"]:
        lines += ["", "  if the same tokens had run entirely on:"]
        for alt in data["alternatives"][:10]:
            if alt["cost_usd"] is None:
                lines.append(f"    {alt['model'][:40]:42} — {alt.get('note','')}")
            else:
                delta = alt["cost_usd"] - s["metered_usd"]
                sign = "+" if delta >= 0 else "-"
                lines.append(f"    {alt['model'][:40]:42}${alt['cost_usd']:>9,.2f}   {sign}${abs(delta):,.2f} vs actual")
    lines += ["", "  " + data["verdict"], "  " + data["caveat"]]
    return "\n".join(lines)
