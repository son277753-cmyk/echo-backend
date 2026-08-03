"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ECHO AI — NEXUS LAYER                            ║
║         Financial Intelligence · Business Brain · Co-CEO            ║
║                                                                      ║
║  Core Responsibilities (from notes):                                 ║
║    - Market analysis                                                 ║
║    - Worker/payroll management                                       ║
║    - Fintech integration                                             ║
║    - Acts as Co-CEO                                                  ║
║                                                                      ║
║  JARVIS additions (not in notes but essential):                      ║
║    - Proactive financial alerts (JARVIS warned Tony of risks)        ║
║    - Portfolio tracking & auto-rebalancing suggestions               ║
║    - Cash flow forecasting                                           ║
║    - Business meeting prep & briefings                               ║
║    - Contract & deal analysis                                        ║
║    - Spending pattern detection                                       ║
║    - Investment opportunity scoring                                  ║
║    - Risk assessment engine                                          ║
║    - Financial anomaly detection (fraud-like behavior)               ║
║    - Business KPI dashboard                                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import json
import uuid
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Nexus")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class RiskLevel(Enum):
    MINIMAL  = "minimal"
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    OPPORTUNITY   = "opportunity"    # Good thing to act on
    WARNING       = "warning"        # Something to watch
    URGENT        = "urgent"         # Needs immediate attention
    INFO          = "info"           # General update
    ANOMALY       = "anomaly"        # Something unusual detected


class MarketSentiment(Enum):
    BULLISH      = "bullish"
    BEARISH      = "bearish"
    NEUTRAL      = "neutral"
    VOLATILE     = "volatile"
    UNCERTAIN    = "uncertain"


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class FinancialAlert:
    alert_id:   str       = field(default_factory=lambda: str(uuid.uuid4())[:8])
    alert_type: AlertType = AlertType.INFO
    title:      str       = ""
    message:    str       = ""
    amount:     float     = 0.0
    priority:   int       = 1          # 1=low, 5=critical
    timestamp:  str       = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actioned:   bool      = False

    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "alert_type": self.alert_type.value
        }


@dataclass
class MarketAsset:
    symbol:      str   = ""
    name:        str   = ""
    price:       float = 0.0
    change_pct:  float = 0.0          # % change today
    volume:      float = 0.0
    market_cap:  float = 0.0
    sector:      str   = ""
    sentiment:   str   = MarketSentiment.NEUTRAL.value
    last_updated: str  = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PortfolioPosition:
    asset_symbol: str   = ""
    quantity:     float = 0.0
    avg_buy_price: float = 0.0
    current_price: float = 0.0
    allocation_pct: float = 0.0      # % of total portfolio

    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def profit_loss(self) -> float:
        return (self.current_price - self.avg_buy_price) * self.quantity

    @property
    def profit_loss_pct(self) -> float:
        if self.avg_buy_price == 0:
            return 0.0
        return ((self.current_price - self.avg_buy_price) / self.avg_buy_price) * 100

    def to_dict(self) -> Dict:
        return {
            "asset_symbol"   : self.asset_symbol,
            "quantity"       : self.quantity,
            "avg_buy_price"  : self.avg_buy_price,
            "current_price"  : self.current_price,
            "current_value"  : round(self.current_value, 2),
            "profit_loss"    : round(self.profit_loss, 2),
            "profit_loss_pct": round(self.profit_loss_pct, 2),
            "allocation_pct" : self.allocation_pct
        }


@dataclass
class Worker:
    worker_id:   str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name:        str   = ""
    role:        str   = ""
    department:  str   = ""
    salary:      float = 0.0
    pay_cycle:   str   = "monthly"    # monthly, biweekly, weekly
    start_date:  str   = ""
    performance: float = 1.0          # multiplier for bonuses
    status:      str   = "active"

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Transaction:
    tx_id:       str   = field(default_factory=lambda: str(uuid.uuid4())[:10])
    timestamp:   str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    amount:      float = 0.0
    currency:    str   = "USD"
    category:    str   = ""
    description: str   = ""
    direction:   str   = "out"        # in / out
    flagged:     bool  = False
    flag_reason: str   = ""

    def to_dict(self) -> Dict:
        return asdict(self)


# ─────────────────────────────────────────────
#  MARKET INTELLIGENCE ENGINE
#  JARVIS always had real-time market awareness
# ─────────────────────────────────────────────

class MarketIntelligence:
    """
    Tracks market conditions and assets.
    In production this connects to real market APIs
    (Alpha Vantage, Yahoo Finance, CoinGecko etc.)
    For now runs on a simulation layer that can be
    swapped for live feeds.

    JARVIS addition: Proactive opportunity/risk detection.
    Echo doesn't wait to be asked — it tells you first.
    """

    # Simulated market data — replace with API calls in production
    SIMULATED_ASSETS = {
        "AAPL": MarketAsset("AAPL", "Apple Inc",       182.50,  1.2,  55e6,  2.8e12, "Technology",   "bullish"),
        "TSLA": MarketAsset("TSLA", "Tesla Inc",        195.80, -2.4,  80e6,  620e9,  "Automotive",   "volatile"),
        "BTC":  MarketAsset("BTC",  "Bitcoin",        68500.00,  3.8,  25e9,  1.3e12, "Crypto",       "bullish"),
        "ETH":  MarketAsset("ETH",  "Ethereum",        3800.00,  2.1,   12e9, 456e9,  "Crypto",       "bullish"),
        "NVDA": MarketAsset("NVDA", "NVIDIA Corp",      875.00,  4.5,  42e6,  2.1e12, "Technology",   "bullish"),
        "AMZN": MarketAsset("AMZN", "Amazon.com",       185.00,  0.8,  35e6,  1.9e12, "E-Commerce",   "neutral"),
        "GOLD": MarketAsset("GOLD", "Gold Spot",       2350.00,  0.3,   8e9,  14e12,  "Commodities",  "neutral"),
        "OIL":  MarketAsset("OIL",  "Crude Oil WTI",     82.50, -1.1,  15e9,   0.0,   "Energy",       "bearish"),
    }

    def __init__(self):
        self._watchlist: List[str]         = []
        self._price_alerts: Dict[str, float] = {}   # symbol -> trigger price
        self._market_open = True                     # Simulate market hours

    def get_asset(self, symbol: str) -> Optional[MarketAsset]:
        return self.SIMULATED_ASSETS.get(symbol.upper())

    def get_market_overview(self) -> Dict:
        """Overall market health summary."""
        assets    = list(self.SIMULATED_ASSETS.values())
        gainers   = [a for a in assets if a.change_pct > 0]
        losers    = [a for a in assets if a.change_pct < 0]
        avg_change = sum(a.change_pct for a in assets) / len(assets)

        if avg_change > 1.5:
            sentiment = MarketSentiment.BULLISH
        elif avg_change < -1.5:
            sentiment = MarketSentiment.BEARISH
        elif abs(avg_change) < 0.3:
            sentiment = MarketSentiment.NEUTRAL
        else:
            sentiment = MarketSentiment.VOLATILE

        return {
            "overall_sentiment" : sentiment.value,
            "avg_change_pct"    : round(avg_change, 2),
            "gainers"           : len(gainers),
            "losers"            : len(losers),
            "top_gainer"        : max(assets, key=lambda a: a.change_pct).symbol,
            "top_loser"         : min(assets, key=lambda a: a.change_pct).symbol,
            "market_open"       : self._market_open,
            "timestamp"         : datetime.now(timezone.utc).isoformat()
        }

    def scan_opportunities(self, portfolio: Dict[str, PortfolioPosition]) -> List[Dict]:
        """
        JARVIS addition: Proactively scan for opportunities
        Echo spots these and tells you — you don't have to ask.
        """
        opportunities = []

        for symbol, asset in self.SIMULATED_ASSETS.items():
            # Strong momentum + not overweight in portfolio
            if asset.change_pct > 3.0 and symbol not in portfolio:
                opportunities.append({
                    "type"    : "MOMENTUM_OPPORTUNITY",
                    "symbol"  : symbol,
                    "name"    : asset.name,
                    "change"  : asset.change_pct,
                    "reason"  : f"{asset.name} is up {asset.change_pct}% today with strong volume.",
                    "action"  : "Consider adding a position.",
                    "priority": 3
                })

            # Existing position showing strong profit
            if symbol in portfolio:
                pos = portfolio[symbol]
                if pos.profit_loss_pct > 20:
                    opportunities.append({
                        "type"    : "TAKE_PROFIT_SIGNAL",
                        "symbol"  : symbol,
                        "name"    : asset.name,
                        "gain_pct": pos.profit_loss_pct,
                        "reason"  : f"{asset.name} is up {pos.profit_loss_pct:.1f}% from your buy price.",
                        "action"  : "Consider taking partial profits.",
                        "priority": 2
                    })

        return sorted(opportunities, key=lambda x: x["priority"], reverse=True)

    def scan_risks(self, portfolio: Dict[str, PortfolioPosition]) -> List[Dict]:
        """
        JARVIS addition: Proactive risk detection.
        Flags risks before they become problems.
        """
        risks = []

        for symbol, pos in portfolio.items():
            asset = self.get_asset(symbol)
            if not asset:
                continue

            # Sharp decline
            if asset.change_pct < -3.0:
                risks.append({
                    "type"    : "SHARP_DECLINE",
                    "symbol"  : symbol,
                    "change"  : asset.change_pct,
                    "reason"  : f"{asset.name} is down {abs(asset.change_pct)}% today.",
                    "action"  : "Review position. Consider stop-loss.",
                    "priority": 4
                })

            # Overconcentration
            if pos.allocation_pct > 30:
                risks.append({
                    "type"      : "OVERCONCENTRATION",
                    "symbol"    : symbol,
                    "allocation": pos.allocation_pct,
                    "reason"    : f"{pos.allocation_pct}% of portfolio in {symbol} — above safe threshold.",
                    "action"    : "Consider rebalancing.",
                    "priority"  : 3
                })

            # Unrealized loss threshold
            if pos.profit_loss_pct < -15:
                risks.append({
                    "type"    : "UNREALIZED_LOSS",
                    "symbol"  : symbol,
                    "loss_pct": pos.profit_loss_pct,
                    "reason"  : f"{symbol} is down {abs(pos.profit_loss_pct):.1f}% from your entry.",
                    "action"  : "Evaluate if thesis still holds.",
                    "priority": 3
                })

        return sorted(risks, key=lambda x: x["priority"], reverse=True)

    def add_to_watchlist(self, symbol: str):
        if symbol not in self._watchlist:
            self._watchlist.append(symbol)

    def set_price_alert(self, symbol: str, target_price: float):
        self._price_alerts[symbol] = target_price

    def check_price_alerts(self) -> List[Dict]:
        """Check if any price alerts have been triggered."""
        triggered = []
        for symbol, target in self._price_alerts.items():
            asset = self.get_asset(symbol)
            if asset and asset.price >= target:
                triggered.append({
                    "symbol"      : symbol,
                    "target_price": target,
                    "current_price": asset.price,
                    "message"     : f"{symbol} has reached your target of ${target:,.2f}"
                })
        return triggered


# ─────────────────────────────────────────────
#  PORTFOLIO MANAGER
# ─────────────────────────────────────────────

class PortfolioManager:
    """
    Tracks and analyzes the user's investment portfolio.
    JARVIS addition: Auto-rebalancing suggestions,
    diversification scoring, tax-loss harvesting hints.
    """

    def __init__(self):
        self._positions: Dict[str, PortfolioPosition] = {}
        self._cash_balance: float = 0.0
        self._target_allocations: Dict[str, float]   = {}   # symbol -> target %

    def add_position(self, symbol: str, quantity: float,
                     avg_price: float, current_price: float):
        self._positions[symbol] = PortfolioPosition(
            asset_symbol  = symbol,
            quantity      = quantity,
            avg_buy_price = avg_price,
            current_price = current_price
        )
        self._recalculate_allocations()

    def set_cash(self, amount: float):
        self._cash_balance = amount

    def set_target_allocation(self, symbol: str, pct: float):
        self._target_allocations[symbol] = pct

    def _recalculate_allocations(self):
        total = sum(p.current_value for p in self._positions.values())
        if total == 0:
            return
        for symbol, pos in self._positions.items():
            pos.allocation_pct = round((pos.current_value / total) * 100, 2)

    def get_summary(self) -> Dict:
        """Full portfolio summary."""
        total_value  = sum(p.current_value for p in self._positions.values())
        total_cost   = sum(p.avg_buy_price * p.quantity for p in self._positions.values())
        total_pl     = total_value - total_cost
        total_pl_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0

        return {
            "total_value"       : round(total_value, 2),
            "total_invested"    : round(total_cost, 2),
            "total_profit_loss" : round(total_pl, 2),
            "total_pl_pct"      : round(total_pl_pct, 2),
            "cash_balance"      : self._cash_balance,
            "num_positions"     : len(self._positions),
            "positions"         : {s: p.to_dict() for s, p in self._positions.items()},
            "timestamp"         : datetime.now(timezone.utc).isoformat()
        }

    def get_rebalancing_plan(self) -> List[Dict]:
        """
        JARVIS addition: Auto-generate a rebalancing plan
        to bring portfolio back to target allocations.
        """
        if not self._target_allocations:
            return []

        total_value = sum(p.current_value for p in self._positions.values())
        plan = []

        for symbol, target_pct in self._target_allocations.items():
            current_pct = self._positions[symbol].allocation_pct if symbol in self._positions else 0
            diff = target_pct - current_pct

            if abs(diff) > 2:  # Only suggest if drift > 2%
                action = "BUY" if diff > 0 else "SELL"
                amount = abs(diff / 100 * total_value)
                plan.append({
                    "symbol"     : symbol,
                    "action"     : action,
                    "current_pct": current_pct,
                    "target_pct" : target_pct,
                    "drift_pct"  : round(diff, 2),
                    "amount_usd" : round(amount, 2),
                    "reason"     : f"Drift of {diff:.1f}% from target allocation."
                })

        return sorted(plan, key=lambda x: abs(x["drift_pct"]), reverse=True)

    def get_diversification_score(self) -> Dict:
        """
        JARVIS addition: Score how well-diversified the portfolio is.
        A JARVIS-level insight Echo gives proactively.
        """
        if not self._positions:
            return {"score": 0, "assessment": "No positions"}

        sectors: Dict[str, float] = defaultdict(float)
        # In production, fetch sector from market API
        # For now use simulated mapping
        sector_map = {
            "AAPL": "Technology", "NVDA": "Technology",
            "TSLA": "Automotive", "AMZN": "E-Commerce",
            "BTC": "Crypto", "ETH": "Crypto",
            "GOLD": "Commodities", "OIL": "Energy"
        }

        total = sum(p.current_value for p in self._positions.values())
        for symbol, pos in self._positions.items():
            sector = sector_map.get(symbol, "Other")
            sectors[sector] += pos.current_value / total * 100

        max_sector_concentration = max(sectors.values()) if sectors else 100
        num_sectors = len(sectors)

        # Score: more sectors + lower concentration = better
        score = min(100, (num_sectors * 15) + (100 - max_sector_concentration))

        if score >= 80:
            assessment = "Excellent diversification"
        elif score >= 60:
            assessment = "Good diversification"
        elif score >= 40:
            assessment = "Moderate — consider diversifying"
        else:
            assessment = "Poor — highly concentrated portfolio"

        return {
            "score"        : round(score, 1),
            "assessment"   : assessment,
            "sectors"      : dict(sectors),
            "num_sectors"  : num_sectors,
            "max_concentration": round(max_sector_concentration, 2)
        }

    @property
    def positions(self) -> Dict[str, PortfolioPosition]:
        return self._positions


# ─────────────────────────────────────────────
#  PAYROLL MANAGER
# ─────────────────────────────────────────────

class PayrollManager:
    """
    Worker and payroll management system.
    JARVIS addition: Performance tracking,
    automated payroll scheduling, budget forecasting.
    """

    def __init__(self):
        self._workers: Dict[str, Worker]   = {}
        self._payroll_log: List[Dict]      = []
        self._budget_monthly: float        = 0.0

    def add_worker(self, name: str, role: str, department: str,
                   salary: float, pay_cycle: str = "monthly") -> Worker:
        worker = Worker(
            name       = name,
            role       = role,
            department = department,
            salary     = salary,
            pay_cycle  = pay_cycle,
            start_date = datetime.now(timezone.utc).isoformat()[:10]
        )
        self._workers[worker.worker_id] = worker
        log.info(f"[NEXUS/PAYROLL] Worker added: {name} | {role} | ${salary:,.0f}/yr")
        return worker

    def remove_worker(self, worker_id: str) -> bool:
        if worker_id in self._workers:
            worker = self._workers.pop(worker_id)
            worker.status = "inactive"
            log.info(f"[NEXUS/PAYROLL] Worker removed: {worker.name}")
            return True
        return False

    def set_budget(self, monthly_budget: float):
        self._budget_monthly = monthly_budget

    def get_payroll_summary(self) -> Dict:
        """Full payroll overview."""
        active     = [w for w in self._workers.values() if w.status == "active"]
        total_annual = sum(w.salary for w in active)
        total_monthly = total_annual / 12

        by_dept: Dict[str, float] = defaultdict(float)
        for w in active:
            by_dept[w.department] += w.salary / 12

        budget_health = "OK"
        if self._budget_monthly > 0:
            usage_pct = (total_monthly / self._budget_monthly) * 100
            if usage_pct > 100:
                budget_health = "OVER_BUDGET"
            elif usage_pct > 85:
                budget_health = "WARNING"

        return {
            "active_workers"   : len(active),
            "total_annual_cost": round(total_annual, 2),
            "total_monthly_cost": round(total_monthly, 2),
            "budget_monthly"   : self._budget_monthly,
            "budget_health"    : budget_health,
            "by_department"    : dict(by_dept),
            "workers"          : [w.to_dict() for w in active]
        }

    def process_payroll(self) -> Dict:
        """
        Run payroll for all active workers.
        In production: integrates with banking APIs.
        """
        active = [w for w in self._workers.values() if w.status == "active"]
        total  = 0.0
        payments = []

        for worker in active:
            if worker.pay_cycle == "monthly":
                amount = worker.salary / 12
            elif worker.pay_cycle == "biweekly":
                amount = worker.salary / 26
            else:
                amount = worker.salary / 52

            amount *= worker.performance
            total  += amount

            payment = {
                "worker_id" : worker.worker_id,
                "name"      : worker.name,
                "amount"    : round(amount, 2),
                "cycle"     : worker.pay_cycle,
                "processed" : datetime.now(timezone.utc).isoformat()
            }
            payments.append(payment)
            self._payroll_log.append(payment)

        result = {
            "status"        : "PROCESSED",
            "total_paid"    : round(total, 2),
            "num_workers"   : len(active),
            "payments"      : payments,
            "timestamp"     : datetime.now(timezone.utc).isoformat()
        }

        log.info(f"[NEXUS/PAYROLL] Payroll processed: ${total:,.2f} for {len(active)} workers")
        return result

    def forecast_payroll(self, months: int = 12) -> Dict:
        """
        JARVIS addition: Project payroll costs forward.
        Helps plan hiring budget intelligently.
        """
        active = [w for w in self._workers.values() if w.status == "active"]
        monthly = sum(w.salary / 12 for w in active)
        annual  = monthly * 12

        projections = []
        for i in range(1, months + 1):
            month_date = datetime.now(timezone.utc) + timedelta(days=30 * i)
            projections.append({
                "month"          : month_date.strftime("%Y-%m"),
                "projected_cost" : round(monthly, 2),
                "budget_status"  : "OK" if monthly <= self._budget_monthly else "OVER"
            })

        return {
            "monthly_cost"  : round(monthly, 2),
            "annual_cost"   : round(annual, 2),
            "projections"   : projections,
            "hiring_budget" : max(0, self._budget_monthly - monthly)
        }


# ─────────────────────────────────────────────
#  CASH FLOW ENGINE
#  JARVIS addition — Tony always knew his runway
# ─────────────────────────────────────────────

class CashFlowEngine:
    """
    Tracks income, expenses, and forecasts cash position.
    JARVIS always kept Tony aware of his financial runway.
    Echo does the same — proactively, not reactively.
    """

    def __init__(self):
        self._transactions: List[Transaction] = []
        self._recurring_income: List[Dict]    = []
        self._recurring_expenses: List[Dict]  = []

    def add_transaction(self, amount: float, category: str,
                        description: str, direction: str = "out",
                        currency: str = "USD") -> Transaction:
        tx = Transaction(
            amount      = amount,
            currency    = currency,
            category    = category,
            description = description,
            direction   = direction
        )

        # Anomaly detection — JARVIS addition
        tx.flagged, tx.flag_reason = self._detect_anomaly(tx)

        self._transactions.append(tx)

        if tx.flagged:
            log.warning(
                f"[NEXUS/CASHFLOW] Anomaly flagged: {tx.flag_reason} | "
                f"Amount: ${amount:,.2f}"
            )

        return tx

    def add_recurring_income(self, source: str, amount: float, frequency: str):
        self._recurring_income.append({
            "source"   : source,
            "amount"   : amount,
            "frequency": frequency
        })

    def add_recurring_expense(self, name: str, amount: float, frequency: str):
        self._recurring_expenses.append({
            "name"     : name,
            "amount"   : amount,
            "frequency": frequency
        })

    def get_summary(self, days: int = 30) -> Dict:
        """Cash flow summary for the last N days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        recent = [
            t for t in self._transactions
            if datetime.fromisoformat(t.timestamp) > cutoff
        ]

        inflow  = sum(t.amount for t in recent if t.direction == "in")
        outflow = sum(t.amount for t in recent if t.direction == "out")
        net     = inflow - outflow
        flagged = [t for t in recent if t.flagged]

        # Spending by category
        by_category: Dict[str, float] = defaultdict(float)
        for t in recent:
            if t.direction == "out":
                by_category[t.category] += t.amount

        return {
            "period_days"     : days,
            "total_inflow"    : round(inflow, 2),
            "total_outflow"   : round(outflow, 2),
            "net_flow"        : round(net, 2),
            "health"          : "POSITIVE" if net > 0 else "NEGATIVE",
            "transactions"    : len(recent),
            "flagged"         : len(flagged),
            "top_categories"  : dict(sorted(by_category.items(),
                                            key=lambda x: x[1], reverse=True)[:5]),
            "timestamp"       : datetime.now(timezone.utc).isoformat()
        }

    def forecast(self, months: int = 3) -> List[Dict]:
        """
        JARVIS addition: Cash flow forecast.
        Projects income vs expenses forward.
        """
        monthly_income = sum(
            r["amount"] if r["frequency"] == "monthly" else r["amount"] / 12
            for r in self._recurring_income
        )
        monthly_expenses = sum(
            r["amount"] if r["frequency"] == "monthly" else r["amount"] / 12
            for r in self._recurring_expenses
        )
        monthly_net = monthly_income - monthly_expenses

        projections = []
        running_balance = 0.0
        for i in range(1, months + 1):
            running_balance += monthly_net
            month = (datetime.now(timezone.utc) + timedelta(days=30 * i)).strftime("%Y-%m")
            projections.append({
                "month"          : month,
                "projected_income"  : round(monthly_income, 2),
                "projected_expenses": round(monthly_expenses, 2),
                "projected_net"     : round(monthly_net, 2),
                "running_balance"   : round(running_balance, 2),
                "health"         : "POSITIVE" if monthly_net > 0 else "NEGATIVE"
            })

        return projections

    def _detect_anomaly(self, tx: Transaction) -> Tuple[bool, str]:
        """
        JARVIS addition: Detect unusual transactions.
        Echo flags these automatically — like a built-in fraud detector.
        """
        # Unusually large transaction
        if tx.amount > 10000 and tx.direction == "out":
            return True, f"Large outflow: ${tx.amount:,.2f}"

        # Duplicate detection
        recent = self._transactions[-20:]
        for prev in recent:
            if (prev.amount == tx.amount and
                prev.category == tx.category and
                prev.direction == tx.direction):
                return True, f"Possible duplicate transaction: ${tx.amount:.2f} in {tx.category}"

        return False, ""

    def get_spending_patterns(self) -> Dict:
        """
        JARVIS addition: Detect spending patterns.
        Echo learns your financial behavior over time.
        """
        if not self._transactions:
            return {"patterns": [], "message": "Not enough data yet"}

        by_category: Dict[str, List[float]] = defaultdict(list)
        for t in self._transactions:
            if t.direction == "out":
                by_category[t.category].append(t.amount)

        patterns = []
        for category, amounts in by_category.items():
            avg = sum(amounts) / len(amounts)
            patterns.append({
                "category"  : category,
                "avg_spend" : round(avg, 2),
                "count"     : len(amounts),
                "total"     : round(sum(amounts), 2),
                "trend"     : "increasing" if amounts[-1] > avg else "stable"
            })

        return {
            "patterns": sorted(patterns, key=lambda x: x["total"], reverse=True)
        }


# ─────────────────────────────────────────────
#  ALERT ENGINE
#  JARVIS addition — proactive financial awareness
# ─────────────────────────────────────────────

class AlertEngine:
    """
    Generates and manages financial alerts.
    JARVIS never waited to be asked — he told Tony
    what he needed to know before Tony thought to ask.
    Echo does the same.
    """

    def __init__(self):
        self._alerts: List[FinancialAlert] = []
        self._lock = threading.Lock()

    def add(self, alert_type: AlertType, title: str,
            message: str, amount: float = 0.0,
            priority: int = 1) -> FinancialAlert:
        alert = FinancialAlert(
            alert_type = alert_type,
            title      = title,
            message    = message,
            amount     = amount,
            priority   = priority
        )
        with self._lock:
            self._alerts.append(alert)

        log.info(f"[NEXUS/ALERT] [{alert_type.value.upper()}] {title}")
        return alert

    def get_pending(self, min_priority: int = 1) -> List[Dict]:
        return [
            a.to_dict() for a in self._alerts
            if not a.actioned and a.priority >= min_priority
        ]

    def get_urgent(self) -> List[Dict]:
        return self.get_pending(min_priority=4)

    def mark_actioned(self, alert_id: str):
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.actioned = True
                break

    def clear_all(self):
        with self._lock:
            self._alerts = []

    def count(self) -> Dict:
        pending = self.get_pending()
        return {
            "total"    : len(self._alerts),
            "pending"  : len(pending),
            "urgent"   : len(self.get_urgent())
        }


# ─────────────────────────────────────────────
#  BUSINESS INTELLIGENCE
#  The "co-CEO" brain
# ─────────────────────────────────────────────

class BusinessIntelligence:
    """
    High-level business analysis and decision support.
    This is what makes Nexus a co-CEO and not just
    a calculator — it reasons about the business.

    JARVIS additions:
    - Meeting briefings
    - KPI tracking
    - Deal/contract analysis
    - Strategic recommendations
    """

    def __init__(self):
        self._kpis: Dict[str, Dict]         = {}
        self._meetings: List[Dict]          = []
        self._decisions_log: List[Dict]     = []

    def set_kpi(self, name: str, current: float,
                target: float, unit: str = ""):
        self._kpis[name] = {
            "current"    : current,
            "target"     : target,
            "unit"       : unit,
            "achievement": round((current / target * 100) if target > 0 else 0, 1),
            "updated_at" : datetime.now(timezone.utc).isoformat()
        }

    def get_kpi_dashboard(self) -> Dict:
        """Business KPI overview."""
        if not self._kpis:
            return {"message": "No KPIs set yet. Use set_kpi() to add them."}

        on_track   = [k for k, v in self._kpis.items() if v["achievement"] >= 80]
        at_risk    = [k for k, v in self._kpis.items() if 50 <= v["achievement"] < 80]
        critical   = [k for k, v in self._kpis.items() if v["achievement"] < 50]

        return {
            "kpis"       : self._kpis,
            "on_track"   : on_track,
            "at_risk"    : at_risk,
            "critical"   : critical,
            "overall_health": "GREEN" if not critical else ("YELLOW" if not at_risk else "RED")
        }

    def add_meeting(self, title: str, attendees: List[str],
                    date: str, agenda: List[str]) -> Dict:
        """
        JARVIS addition: Meeting management.
        Echo prepares briefings for every meeting.
        """
        meeting = {
            "meeting_id" : str(uuid.uuid4())[:8],
            "title"      : title,
            "attendees"  : attendees,
            "date"       : date,
            "agenda"     : agenda,
            "briefing"   : self._generate_briefing(title, attendees, agenda),
            "created_at" : datetime.now(timezone.utc).isoformat()
        }
        self._meetings.append(meeting)
        return meeting

    def _generate_briefing(self, title: str, attendees: List[str],
                           agenda: List[str]) -> Dict:
        """Auto-generate a pre-meeting briefing — JARVIS would do this."""
        return {
            "summary"    : f"Meeting: {title} with {len(attendees)} attendee(s).",
            "key_points" : [f"Discuss: {item}" for item in agenda],
            "attendee_count": len(attendees),
            "preparation": [
                "Review relevant financial reports",
                "Prepare KPI dashboard",
                "Check for pending alerts",
                "Review last meeting notes"
            ],
            "echo_note"  : "I'll have all relevant data ready before the meeting starts."
        }

    def analyze_deal(self, deal_name: str, value: float,
                     terms: Dict, risks: List[str]) -> Dict:
        """
        JARVIS addition: Deal/contract analysis.
        Echo evaluates deals and gives a recommendation.
        """
        # Risk scoring
        risk_score = len(risks) * 15
        if value > 1_000_000:
            risk_score += 20

        risk_level = (
            RiskLevel.CRITICAL if risk_score >= 80 else
            RiskLevel.HIGH     if risk_score >= 60 else
            RiskLevel.MODERATE if risk_score >= 40 else
            RiskLevel.LOW      if risk_score >= 20 else
            RiskLevel.MINIMAL
        )

        recommendation = (
            "DECLINE"  if risk_level == RiskLevel.CRITICAL else
            "NEGOTIATE" if risk_level == RiskLevel.HIGH else
            "REVIEW"   if risk_level == RiskLevel.MODERATE else
            "PROCEED"
        )

        analysis = {
            "deal_name"     : deal_name,
            "value"         : value,
            "risk_level"    : risk_level.value,
            "risk_score"    : risk_score,
            "recommendation": recommendation,
            "identified_risks": risks,
            "terms_summary" : terms,
            "echo_note"     : (
                f"Based on my analysis, I recommend you {recommendation} this deal. "
                f"Risk level is {risk_level.value}."
            ),
            "analyzed_at"   : datetime.now(timezone.utc).isoformat()
        }

        self._decisions_log.append(analysis)
        log.info(
            f"[NEXUS/BUSINESS] Deal analyzed: {deal_name} | "
            f"Risk: {risk_level.value} | Recommendation: {recommendation}"
        )

        return analysis

    def generate_executive_summary(self, portfolio_summary: Dict,
                                   cashflow_summary: Dict,
                                   payroll_summary: Dict) -> str:
        """
        JARVIS addition: Daily executive briefing.
        Echo compiles everything into one clear summary —
        exactly what a co-CEO would give you each morning.
        """
        lines = [
            "═══ ECHO — EXECUTIVE BRIEFING ═══",
            f"  {datetime.now(timezone.utc).strftime('%A, %B %d %Y — %H:%M UTC')}",
            "",
            "  PORTFOLIO",
            f"  Total Value    : ${portfolio_summary.get('total_value', 0):>12,.2f}",
            f"  P&L Today      : ${portfolio_summary.get('total_profit_loss', 0):>+12,.2f}  "
            f"({portfolio_summary.get('total_pl_pct', 0):+.2f}%)",
            "",
            "  CASH FLOW (30 days)",
            f"  Inflow         : ${cashflow_summary.get('total_inflow', 0):>12,.2f}",
            f"  Outflow        : ${cashflow_summary.get('total_outflow', 0):>12,.2f}",
            f"  Net            : ${cashflow_summary.get('net_flow', 0):>+12,.2f}",
            f"  Status         : {cashflow_summary.get('health', 'N/A')}",
            "",
            "  PAYROLL",
            f"  Active Workers : {payroll_summary.get('active_workers', 0)}",
            f"  Monthly Cost   : ${payroll_summary.get('total_monthly_cost', 0):>12,.2f}",
            f"  Budget Status  : {payroll_summary.get('budget_health', 'N/A')}",
            "",
            "  Ready for your instructions.",
            "═════════════════════════════════"
        ]
        return "\n".join(lines)


# ─────────────────────────────────────────────
#  NEXUS LAYER — MAIN CLASS
# ─────────────────────────────────────────────

class NexusLayer:
    """
    Nexus Layer — Echo's Financial Intelligence & Co-CEO Brain.

    Integrated into EchoCore. Called by LayerRouter
    when intent targets Layer.NEXUS.

    Also exposes a rich direct API for other layers
    (e.g. Habitat can check budget before buying a smart device,
     Scholar can check if online courses fit the budget).
    """

    def __init__(self):
        self.market      = MarketIntelligence()
        self.portfolio   = PortfolioManager()
        self.payroll     = PayrollManager()
        self.cashflow    = CashFlowEngine()
        self.alerts      = AlertEngine()
        self.business    = BusinessIntelligence()
        self._lock       = threading.Lock()

        # Demo data — gives Echo something to work with from day 1
        self._load_demo_data()

        log.info("[NEXUS] Layer online. Financial intelligence active.")

    def _load_demo_data(self):
        """Load demo portfolio and data so Echo has context from the start."""
        # Demo portfolio
        self.portfolio.add_position("AAPL", 50,  150.00, 182.50)
        self.portfolio.add_position("NVDA", 10, 600.00,  875.00)
        self.portfolio.add_position("BTC",  0.5, 42000, 68500)
        self.portfolio.set_cash(25000)
        self.portfolio.set_target_allocation("AAPL", 30)
        self.portfolio.set_target_allocation("NVDA", 25)
        self.portfolio.set_target_allocation("BTC",  20)

        # Demo KPIs
        self.business.set_kpi("Revenue",       850000,  1000000, "USD")
        self.business.set_kpi("User Growth",   7800,    10000,   "users")
        self.business.set_kpi("Profit Margin", 22,      30,      "%")
        self.business.set_kpi("Team Size",     12,      20,      "people")

        # Demo payroll
        self.payroll.set_budget(50000)
        self.payroll.add_worker("Alex Chen",     "Lead Engineer",   "Engineering", 95000)
        self.payroll.add_worker("Maria Santos",  "Product Manager", "Product",     88000)
        self.payroll.add_worker("James Okafor",  "Designer",        "Design",      75000)

        # Demo cash flow
        self.cashflow.add_recurring_income("Product Sales", 85000, "monthly")
        self.cashflow.add_recurring_income("Consulting",    15000, "monthly")
        self.cashflow.add_recurring_expense("Payroll",      30000, "monthly")
        self.cashflow.add_recurring_expense("Infrastructure", 5000,"monthly")
        self.cashflow.add_recurring_expense("Marketing",    10000, "monthly")

        # Sample transactions
        self.cashflow.add_transaction(85000, "Revenue", "Monthly product sales", "in")
        self.cashflow.add_transaction(30000, "Payroll", "Monthly payroll run",   "out")
        self.cashflow.add_transaction(5000,  "Infra",   "Cloud infrastructure",  "out")
        self.cashflow.add_transaction(2500,  "Marketing","Ad campaign spend",    "out")

        # Initial alerts
        self.alerts.add(AlertType.OPPORTUNITY, "NVDA Strong Momentum",
            "NVIDIA is up 4.5% today — your position is performing well.", 0, 2)
        self.alerts.add(AlertType.INFO, "Payroll Due",
            "Monthly payroll processing due in 3 days.", 30000, 3)

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """
        Main entry point from EchoCore LayerRouter.
        Parses the intent and delegates to the right sub-system.
        """
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[NEXUS] Processing: '{intent_text[:60]}'")

        # Route to appropriate sub-system
        if any(kw in intent_low for kw in ["portfolio", "investment", "stock", "crypto", "position"]):
            return self._handle_portfolio(intent_text)

        elif any(kw in intent_low for kw in ["market", "trend", "price", "asset", "ticker"]):
            return self._handle_market(intent_text)

        elif any(kw in intent_low for kw in ["payroll", "worker", "salary", "employee", "hire", "pay"]):
            return self._handle_payroll(intent_text)

        elif any(kw in intent_low for kw in ["cash", "flow", "spend", "expense", "income", "transaction"]):
            return self._handle_cashflow(intent_text)

        elif any(kw in intent_low for kw in ["kpi", "business", "performance", "meeting", "deal", "briefing"]):
            return self._handle_business(intent_text)

        elif any(kw in intent_low for kw in ["alert", "notification", "urgent", "warning"]):
            return self._handle_alerts()

        elif any(kw in intent_low for kw in ["summary", "overview", "status", "report", "morning"]):
            return self._handle_executive_summary()

        else:
            # General Nexus response
            return self._handle_general(intent_text)

    # ── Sub-handlers ───────────────────────────

    def _handle_portfolio(self, intent: str) -> Dict:
        summary    = self.portfolio.get_summary()
        rebalance  = self.portfolio.get_rebalancing_plan()
        diversity  = self.portfolio.get_diversification_score()
        opps       = self.market.scan_opportunities(self.portfolio.positions)
        risks      = self.market.scan_risks(self.portfolio.positions)

        # Auto-generate alerts for risks
        for risk in risks:
            self.alerts.add(
                AlertType.WARNING,
                f"Risk: {risk['type']} — {risk['symbol']}",
                risk["reason"], 0, risk["priority"]
            )

        return {
            "layer"             : "nexus",
            "status"            : "OK",
            "sub_system"        : "portfolio",
            "summary"           : summary,
            "rebalancing_plan"  : rebalance,
            "diversification"   : diversity,
            "opportunities"     : opps,
            "risks"             : risks,
            "message"           : (
                f"Your portfolio is worth ${summary['total_value']:,.2f} "
                f"with a P&L of ${summary['total_profit_loss']:+,.2f} "
                f"({summary['total_pl_pct']:+.2f}%). "
                f"Diversification score: {diversity['score']}/100."
            ),
            "timestamp"         : datetime.now(timezone.utc).isoformat()
        }

    def _handle_market(self, intent: str) -> Dict:
        overview = self.market.get_market_overview()
        alerts   = self.market.check_price_alerts()

        # Pull out specific asset if mentioned
        mentioned = None
        for symbol in self.market.SIMULATED_ASSETS:
            if symbol.lower() in intent.lower():
                mentioned = self.market.get_asset(symbol)

        response = {
            "layer"         : "nexus",
            "status"        : "OK",
            "sub_system"    : "market",
            "market_overview": overview,
            "price_alerts"  : alerts,
            "message"       : (
                f"Market is currently {overview['overall_sentiment']}. "
                f"Average change: {overview['avg_change_pct']:+.2f}%. "
                f"Top gainer: {overview['top_gainer']}."
            ),
            "timestamp"     : datetime.now(timezone.utc).isoformat()
        }

        if mentioned:
            response["asset_detail"] = mentioned.to_dict()
            response["message"] += (
                f" {mentioned.symbol} is at ${mentioned.price:,.2f} "
                f"({mentioned.change_pct:+.2f}% today)."
            )

        return response

    def _handle_payroll(self, intent: str) -> Dict:
        summary  = self.payroll.get_payroll_summary()
        forecast = self.payroll.forecast_payroll(months=3)

        process_now = any(kw in intent.lower()
                          for kw in ["run payroll", "process payroll", "pay workers"])
        payroll_result = None
        if process_now:
            payroll_result = self.payroll.process_payroll()

        return {
            "layer"          : "nexus",
            "status"         : "OK",
            "sub_system"     : "payroll",
            "summary"        : summary,
            "forecast"       : forecast,
            "payroll_run"    : payroll_result,
            "message"        : (
                f"You have {summary['active_workers']} active workers. "
                f"Monthly payroll: ${summary['total_monthly_cost']:,.2f}. "
                f"Budget status: {summary['budget_health']}."
            ),
            "timestamp"      : datetime.now(timezone.utc).isoformat()
        }

    def _handle_cashflow(self, intent: str) -> Dict:
        summary  = self.cashflow.get_summary()
        forecast = self.cashflow.forecast(months=3)
        patterns = self.cashflow.get_spending_patterns()

        return {
            "layer"      : "nexus",
            "status"     : "OK",
            "sub_system" : "cashflow",
            "summary"    : summary,
            "forecast"   : forecast,
            "patterns"   : patterns,
            "message"    : (
                f"Cash flow over 30 days: "
                f"In ${summary['total_inflow']:,.2f} / "
                f"Out ${summary['total_outflow']:,.2f} / "
                f"Net ${summary['net_flow']:+,.2f}. "
                f"Status: {summary['health']}. "
                f"Flagged transactions: {summary['flagged']}."
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_business(self, intent: str) -> Dict:
        dashboard = self.business.get_kpi_dashboard()

        return {
            "layer"     : "nexus",
            "status"    : "OK",
            "sub_system": "business",
            "kpi_dashboard": dashboard,
            "message"   : (
                f"Business health: {dashboard.get('overall_health', 'N/A')}. "
                f"KPIs on track: {len(dashboard.get('on_track', []))}. "
                f"At risk: {len(dashboard.get('at_risk', []))}. "
                f"Critical: {len(dashboard.get('critical', []))}."
            ),
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_alerts(self) -> Dict:
        pending = self.alerts.get_pending()
        urgent  = self.alerts.get_urgent()
        counts  = self.alerts.count()

        return {
            "layer"    : "nexus",
            "status"   : "OK",
            "sub_system": "alerts",
            "alerts"   : pending,
            "urgent"   : urgent,
            "counts"   : counts,
            "message"  : (
                f"You have {counts['pending']} pending financial alerts, "
                f"{counts['urgent']} urgent."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_executive_summary(self) -> Dict:
        portfolio_s = self.portfolio.get_summary()
        cashflow_s  = self.cashflow.get_summary()
        payroll_s   = self.payroll.get_payroll_summary()
        briefing    = self.business.generate_executive_summary(
            portfolio_s, cashflow_s, payroll_s
        )
        market_s    = self.market.get_market_overview()
        alert_counts = self.alerts.count()

        return {
            "layer"          : "nexus",
            "status"         : "OK",
            "sub_system"     : "executive_summary",
            "briefing"       : briefing,
            "portfolio"      : portfolio_s,
            "market"         : market_s,
            "alerts"         : alert_counts,
            "message"        : briefing,
            "timestamp"      : datetime.now(timezone.utc).isoformat()
        }

    def _handle_general(self, intent: str) -> Dict:
        """Fallback — general Nexus awareness response."""
        alert_counts = self.alerts.count()
        portfolio_s  = self.portfolio.get_summary()
        market_s     = self.market.get_market_overview()

        return {
            "layer"     : "nexus",
            "status"    : "OK",
            "sub_system": "general",
            "message"   : (
                f"Nexus online. Portfolio: ${portfolio_s['total_value']:,.2f} "
                f"({portfolio_s['total_pl_pct']:+.2f}%). "
                f"Market: {market_s['overall_sentiment']}. "
                f"Pending alerts: {alert_counts['pending']}. "
                f"How can I assist with your finances?"
            ),
            "snapshot" : {
                "portfolio_value": portfolio_s["total_value"],
                "market_sentiment": market_s["overall_sentiment"],
                "pending_alerts" : alert_counts["pending"]
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_status(self) -> Dict:
        return {
            "layer"          : "nexus",
            "status"         : "ONLINE",
            "portfolio_value": self.portfolio.get_summary()["total_value"],
            "pending_alerts" : self.alerts.count()["pending"],
            "active_workers" : self.payroll.get_payroll_summary()["active_workers"],
            "market_sentiment": self.market.get_market_overview()["overall_sentiment"]
        }


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║         ECHO NEXUS LAYER — TEST             ║
╚══════════════════════════════════════════════╝
    """)

    nexus   = NexusLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        "Give me an executive summary for this morning",
        "What's my portfolio looking like?",
        "What's the market trend for tech stocks?",
        "Show me payroll summary",
        "What are my cash flow numbers?",
        "How are my business KPIs?",
        "Any financial alerts I should know about?",
    ]

    for i, query in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query}'")
        print("─" * 55)
        result = nexus.process(query, session)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        print(f"  MESSAGE    : {result.get('message', '')[:120]}")

    print("\n" + "═" * 55)
    print("  NEXUS STATUS")
    print("═" * 55)
    status = nexus.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<22}: {v}")
