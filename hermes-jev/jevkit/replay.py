"""Offline evaluation: replay real turns through a routing policy and cost the result.

A router that has never been measured against your own traffic is a guess. This
replays turns you have actually served, asks a candidate policy what it would have
done, and prices both the answer and the baseline — so "is this router worth it"
becomes arithmetic instead of an opinion.

Nothing here calls a routed model. It calls Jev to get decisions and then costs
them from the catalogue, so a full replay of a few hundred turns costs cents.
"""
from __future__ import annotations

import json
import statistics
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence

from . import catalog as catalog_mod
from . import route

# A turn's true cost is dominated by the tool loop: the context is re-sent, and grows,
# on every call. Costing only the first call understates a real turn by ~an order of
# magnitude and makes every model look equally cheap.
DEFAULT_LOOP_CALLS = 8
DEFAULT_START_TOKENS = 8_000
DEFAULT_END_TOKENS = 40_000
DEFAULT_OUTPUT_TOKENS = 700


@dataclass
class Turn:
    """One real turn to replay. `prompt` is the user text; the rest is context."""

    prompt: str
    session_id: str = ""
    profile: Optional[str] = None
    current: Optional[str] = None
    context_tokens: int = 0
    has_images: bool = False
    loop_calls: int = DEFAULT_LOOP_CALLS


@dataclass
class Priced:
    """What a turn costs on one model, over the whole tool loop."""

    model: str
    dollars: float
    input_tokens: int
    output_tokens: int


def loop_tokens(calls: int = DEFAULT_LOOP_CALLS, start: int = DEFAULT_START_TOKENS,
                end: int = DEFAULT_END_TOKENS, output: int = DEFAULT_OUTPUT_TOKENS) -> Dict[str, int]:
    """Cumulative tokens for a tool loop whose context grows linearly from start to end."""
    calls = max(int(calls), 1)
    steps = [start + (end - start) * i / max(calls - 1, 1) for i in range(calls)]
    return {"input": int(sum(steps)), "output": calls * output}


def price_table(rows: Optional[Sequence[Mapping[str, Any]]] = None) -> Dict[str, Dict[str, float]]:
    """{'provider:model': {'input': $/M, 'output': $/M}} from the catalogue."""
    rows = rows if rows is not None else catalog_mod.models()
    out: Dict[str, Dict[str, float]] = {}
    for row in rows:
        try:
            out[f"{row['provider']}:{row['model']}"] = {
                "input": float(row["input"]), "output": float(row["output"])}
        except (KeyError, TypeError, ValueError):
            continue
    return out


def cost_turn(model: Optional[str], tokens: Mapping[str, int], prices: Mapping[str, Mapping[str, float]]) -> Optional[Priced]:
    price = prices.get(model or "")
    if price is None:
        return None
    dollars = tokens["input"] * price["input"] / 1e6 + tokens["output"] * price["output"] / 1e6
    return Priced(model=model or "", dollars=dollars, input_tokens=tokens["input"], output_tokens=tokens["output"])


def replay(
    turns: Sequence[Turn], *, config: Optional[Dict[str, Any]] = None,
    rows: Optional[Sequence[Mapping[str, Any]]] = None, only_provider: Optional[str] = None,
    workers: int = 8, timeout: float = 8.0, decide: Optional[Callable[..., Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Run every turn through the policy and return decisions plus a cost comparison.

    `decide` defaults to ``route.decide``; pass your own to A/B a policy variant.
    """
    config = config or route.load_config()
    catalog_rows = list(rows if rows is not None else catalog_mod.models())
    prices = price_table(catalog_rows)
    decider = decide or route.decide

    def one(turn: Turn) -> Dict[str, Any]:
        decision = decider(
            turn.prompt, current=turn.current, profile=turn.profile, session_id=turn.session_id,
            context_tokens=turn.context_tokens, has_images=turn.has_images,
            config=config, rows=catalog_rows, only_provider=only_provider, timeout=timeout)
        tokens = loop_tokens(turn.loop_calls)
        chosen = cost_turn(decision.get("model"), tokens, prices)
        baseline = cost_turn(turn.current, tokens, prices)
        return {"decision": decision, "chosen": chosen, "baseline": baseline, "loop_calls": turn.loop_calls}

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        results = list(pool.map(one, turns))
    return {"results": results, "summary": summarize(results)}


def summarize(results: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """The numbers that decide whether to ship a policy."""
    total = len(results)
    decisions = [r["decision"] for r in results]
    judged = [d for d in decisions if d.get("tier")]
    skipped = [d for d in decisions if "automated" in str(d.get("reason", ""))]
    unsure = [d for d in decisions if not d.get("tier") and d not in skipped]
    switched = [d for d in decisions if d.get("routed")]

    def dollars(key: str) -> float:
        return sum((r[key].dollars if r.get(key) else 0.0) for r in results)

    chosen_cost, baseline_cost = dollars("chosen"), dollars("baseline")
    tiers: Dict[str, int] = {}
    models: Dict[str, int] = {}
    for d in judged:
        tiers[d["tier"]] = tiers.get(d["tier"], 0) + 1
    for d in decisions:
        key = str(d.get("model") or "-")
        models[key] = models.get(key, 0) + 1
    latencies = [d["latency_ms"] for d in decisions if d.get("latency_ms")]
    confidences = [d["confidence"] for d in judged if d.get("confidence") is not None]

    return {
        "turns": total,
        "not_routed_template": len(skipped),
        "not_routed_unsure_or_failed": len(unsure),
        "judged": len(judged),
        "switched_model": len(switched),
        "tier_mix": {k: {"n": v, "pct_of_judged": round(100 * v / max(len(judged), 1), 1)} for k, v in sorted(tiers.items())},
        "models_chosen": dict(sorted(models.items(), key=lambda kv: -kv[1])[:12]),
        "cost": {
            "policy_dollars": round(chosen_cost, 4),
            "baseline_dollars": round(baseline_cost, 4),
            "delta_dollars": round(chosen_cost - baseline_cost, 4),
            "delta_pct": round(100 * (chosen_cost - baseline_cost) / baseline_cost, 1) if baseline_cost else None,
            "per_turn_policy": round(chosen_cost / max(total, 1), 5),
            "per_turn_baseline": round(baseline_cost / max(total, 1), 5),
        },
        "jev_latency_ms": {
            "p50": round(statistics.median(latencies)) if latencies else None,
            "p90": round(sorted(latencies)[int(len(latencies) * 0.9)]) if latencies else None,
            "calls": len(latencies),
        },
        "confidence": {
            "p10": round(sorted(confidences)[int(len(confidences) * 0.1)], 3) if confidences else None,
            "p50": round(statistics.median(confidences), 3) if confidences else None,
            "p90": round(sorted(confidences)[int(len(confidences) * 0.9)], 3) if confidences else None,
        },
    }


def compare(turns: Sequence[Turn], variants: Mapping[str, Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
    """Replay the same turns under several configs. The only honest way to pick thresholds."""
    return {name: replay(turns, config=config, **kwargs)["summary"] for name, config in variants.items()}


def turns_from_jsonl(path: str, *, current: Optional[str] = None, limit: int = 0) -> List[Turn]:
    """Read turns from a JSONL file of {prompt, session_id, profile, context_tokens, ...}."""
    turns: List[Turn] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            prompt = row.get("prompt") or row.get("content") or ""
            if not str(prompt).strip():
                continue
            turns.append(Turn(
                prompt=str(prompt), session_id=str(row.get("session_id") or ""),
                profile=row.get("profile"), current=row.get("current") or current,
                context_tokens=int(row.get("context_tokens") or 0),
                has_images=bool(row.get("has_images")),
                loop_calls=int(row.get("loop_calls") or DEFAULT_LOOP_CALLS)))
            if limit and len(turns) >= limit:
                break
    return turns
