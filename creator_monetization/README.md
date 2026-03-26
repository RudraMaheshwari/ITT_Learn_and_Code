# Creator Monetization Platform (Python refactor)

Layered `src/` package: **Strategy** + **composition**; `Creator` holds many `EarningStrategy` instances; **`MonetizationContext`** supplies views, subscribers, engagement, region, season, live gifts.

## Layout

- `src/config/constants.py` — rates, regional/season multipliers, demo copy  
- `src/utils/` — validation, multiplier lookup (`factors.py`)  
- `src/domain/creator.py` — entity + composed strategies  
- `src/domain/monetization_context.py` — immutable context  
- `src/domain/strategies/` — `EarningStrategy` + ad, subscription, brand, live gift  

## Run

```bash
python main.py
```

## Assignment mapping

| Requirement | Implementation |
|-------------|----------------|
| Multiple sources per creator | `attach_earning_source` + list of strategies |
| New type without editing `Creator` | New class under `strategies/` |
| No earning-type if-chain | Polymorphic `calculate(context)` |
| Encapsulation | Private fields; validated context |
| Engagement, region, season | `MonetizationContext` + `REGION_MULTIPLIERS` / `SEASON_MULTIPLIERS` |

Base rates match the original C# when multipliers are neutral: **$0.05/view**, **$2/subscriber**, brand = contracted amount.

