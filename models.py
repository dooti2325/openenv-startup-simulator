from enum import Enum
from pydantic import BaseModel, Field

class Action(str, Enum):
    INCREASE_MARKETING = "increase_marketing"
    HIRE_ENGINEER = "hire_engineer"
    IMPROVE_PRODUCT = "improve_product"
    REDUCE_COSTS = "reduce_costs"
    PIVOT_MARKET = "pivot_market"
    RAISE_FUNDING = "raise_funding"
    DO_NOTHING = "do_nothing"

class Observation(BaseModel):
    cash: float = Field(..., description="Current cash available")
    users: int = Field(..., description="Number of active users")
    growth_rate: float = Field(..., description="Current user growth rate")
    burn_rate: float = Field(..., description="Monthly cash burn rate")
    churn_rate: float = Field(..., description="Monthly user churn rate")
    product_quality: float = Field(..., description="Product quality score (0.0 to 1.0)")
    market_demand: float = Field(..., description="Current market demand score (0.0 to 1.0)")
    time_step: int = Field(..., description="Current time step of the simulation")
