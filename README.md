---
title: OpenEnv Startup Simulator
emoji: 📈
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Startup Survival Simulator

A complete OpenEnv simulator that accurately models the resource management, marketing economics, and strategic decision-making challenges human entrepreneurs actually perform.

## 🎯 Real-World Motivation & Utility
This is **NOT** a game or toy. Evaluating models strictly on logic puzzles or terminal hacking ignores the high-value category of **strategic enterprise decision making.** 
Entrepreneurs regularly manage capital metrics, runway, burn rates, customer churn, and dynamic market noise using deterministic frameworks. This OpenEnv application empowers agents to train and evaluate AI capabilities in these highly consequential operational management conditions. 

It is designed to test an LLM's capability to probabilistically reason about cash flow, dynamically adjust strategies under changing market conditions, and plan forward without causing immediate bankruptcy.

## 📥 Observation Space (State)
Strictly typed `Observation` schema updated every turn:
| Metric | Description |
|---|---|
| `cash` | Current operating capital (USD) - Agent bankrupts if hits 0 |
| `users` | Total active users (drives organic revenue) |
| `growth_rate` | Monthly user acquisition growth multiplier |
| `burn_rate` | Monthly fixed operational bleed (USD) |
| `churn_rate` | Monthly loss of active users |
| `product_quality` | Scalar value [0.0 - 1.0] impacting retention & ARPU |
| `market_demand` | Market's desire for the product [0.0 - 1.0] |
| `time_step` | Simulation month counting up to standard 50 limit |

## 🎮 Action Space
A discrete, strictly typed `Action` schema of choices. LLM must intelligently pick ONE per turn based on the `Observation`:
- `increase_marketing`: Lowers runway, boosts user growth.
- `hire_engineer`: High cost, heavily boosts product quality.
- `improve_product`: Low cost, improves quality, lowers churn.
- `reduce_costs`: Saves cash, drops product quality aggressively.
- `pivot_market`: Changes market demand probabilistically completely.
- `raise_funding`: Probabilistic check to massively increase cash reserve.
- `do_nothing`: Wait a turn, burning cash predictably.

## 🛠 Tasks & Graders (0.0 - 1.0)
Three progressive tasks evaluate the agent deterministically based on raw mathematical endpoints:
- **Task 1: Survival (EASY)** - Goal: Maintain a positive cash flow for 30 steps. 
  *Grader: Returns strictly fractional `(survived_steps / 30.0)`*
- **Task 2: Growth (MEDIUM)** - Goal: Intelligently spike user base above 1,000 without imploding cash reserves.
  *Grader: Returns strictly fractional `(peak_users / 1000.0)`*
- **Task 3: Scaling (HARD)** - Goal: Extract $50,000 pure profit efficiency from initial seed without collapsing product quality. Requires massive reasoning jumps for LLM.
  *Grader: Returns strictly fractional `(net_profit / 50000.0)`*

## 🤖 Baseline Performance 
The standard `baseline.py` connects to OpenAI GPT-4o-mini using environment variables and achieves reliable (but imperfect) scores dynamically validating its behavior:
- **Survival**: `~0.93 - 1.0`
- **Growth**: `~0.41 - 0.72`
- **Scaling**: `~0.0` (GPT-4o-mini struggles massively on this hard task)

## 🚀 Setup & Execution 

This project perfectly complies with the `uv` backed OpenEnv template structure.

### 1. Build & Test compliance
```bash
uv lock
openenv validate # Will return Exit Code: 0 (multi-mode ready) 
```

### 2. Local Fast Execution
```bash
uv pip install -e .
OPENAI_API_KEY="sk-..." python baseline.py
```

### 3. Docker execution (Hugging Face Validated)
```bash
docker build -t openenv-startup .
docker run -p 7860:7860 openenv-startup
```

Then test via standard endpoints:
```bash
curl http://localhost:7860/reset
curl -X POST http://localhost:7860/step -H "Content-Type: application/json" -d '{"action": "increase_marketing"}'
```
