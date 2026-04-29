"""Per-run cost / step / time budgets. The pipeline calls `check()` between
stages and aborts if any budget is exhausted. Budgets are advisory — they
don't preempt an in-flight LLM call — but they prevent runaway loops."""

from __future__ import annotations

import time
from dataclasses import dataclass


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    max_seconds: float = 600.0
    max_cost_usd: float = 2.50
    max_llm_calls: int = 80
    started_at: float = 0.0
    spent_usd: float = 0.0
    llm_calls: int = 0

    def __post_init__(self) -> None:
        self.started_at = time.monotonic()

    def add_spend(self, usd: float) -> None:
        self.spent_usd += usd
        self.llm_calls += 1

    def check(self) -> None:
        if self.spent_usd > self.max_cost_usd:
            raise BudgetExceeded(
                f"cost ${self.spent_usd:.3f} exceeded cap ${self.max_cost_usd:.2f}"
            )
        if self.llm_calls > self.max_llm_calls:
            raise BudgetExceeded(f"{self.llm_calls} LLM calls exceeded cap {self.max_llm_calls}")
        if time.monotonic() - self.started_at > self.max_seconds:
            raise BudgetExceeded(f"runtime exceeded {self.max_seconds}s")

    def snapshot(self) -> dict:
        return {
            "elapsed_s": round(time.monotonic() - self.started_at, 2),
            "spent_usd": round(self.spent_usd, 4),
            "llm_calls": self.llm_calls,
        }
