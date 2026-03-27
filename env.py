import random
from models import Action, Observation

class StartupEnv:
    def __init__(self):
        self.reset()
        
    def reset(self) -> Observation:
        self.cash = 50000.0
        self.users = 100
        self.growth_rate = 0.05
        self.burn_rate = 3000.0
        self.churn_rate = 0.1
        self.product_quality = 0.6
        self.market_demand = 0.7
        self.time_step = 1
        
        self.history = []
        return self.state()
        
    def state(self) -> Observation:
        return Observation(
            cash=round(self.cash, 2),
            users=int(self.users),
            growth_rate=round(self.growth_rate, 4),
            burn_rate=round(self.burn_rate, 2),
            churn_rate=round(self.churn_rate, 4),
            product_quality=round(self.product_quality, 4),
            market_demand=round(self.market_demand, 4),
            time_step=self.time_step
        )
        
    def step(self, action: str):
        # Retrieve state before changes
        prev_users = self.users
        prev_cash = self.cash
        
        # 1. Apply action
        if action == Action.INCREASE_MARKETING.value:
            self.burn_rate += 1000
            self.growth_rate += 0.02
        elif action == Action.HIRE_ENGINEER.value:
            self.burn_rate += 2000
            self.product_quality = min(1.0, self.product_quality + 0.1)
        elif action == Action.IMPROVE_PRODUCT.value:
            self.burn_rate += 500
            self.product_quality = min(1.0, self.product_quality + 0.05)
            self.churn_rate = max(0.01, self.churn_rate - 0.02)
        elif action == Action.REDUCE_COSTS.value:
            self.burn_rate = max(1000, self.burn_rate - 1500)
            self.product_quality = max(0.1, self.product_quality - 0.05)
        elif action == Action.PIVOT_MARKET.value:
            self.market_demand = min(1.0, random.uniform(0.4, 0.9))
            self.user_growth = 0.02
        elif action == Action.RAISE_FUNDING.value:
            # Raising funding takes time but adds cash. We add some randomness to success.
            if random.random() > 0.5:
                self.cash += 50000
        elif action == Action.DO_NOTHING.value:
            pass

        # 2. Simulate noise / environment changes
        self.market_demand = max(0.1, min(1.0, self.market_demand + random.uniform(-0.05, 0.05)))
        self.churn_rate = max(0.01, min(1.0, self.churn_rate + random.uniform(-0.01, 0.01)))
        
        # 3. Update core metrics
        # New users based on growth and demand
        new_users = self.users * self.growth_rate * self.market_demand
        # Lost users based on churn and product quality
        lost_users = self.users * self.churn_rate * (1.1 - self.product_quality)
        
        self.users = max(0, self.users + new_users - lost_users)
        
        # Simulate revenue loosely based on user count and product quality (ARPU = 10 for high qual)
        revenue = self.users * 10 * self.product_quality
        
        # Cash updates
        self.cash += revenue - self.burn_rate
        self.time_step += 1
        
        # 4. Calculate step reward
        user_growth = self.users - prev_users
        revenue_growth = revenue - (prev_users * 10 * self.product_quality) # simplistic prev revenue
        
        reward = (user_growth * 2) + (revenue_growth * 3) - (self.burn_rate * 0.5) - (self.churn_rate * 2)
        
        # 5. Done conditions
        done = False
        info = {}
        
        if self.cash <= 0:
            done = True
            info["reason"] = "failed: bankruptcy"
            self.cash = 0
        elif self.time_step >= 50:
            done = True
            info["reason"] = "success: episode end"
        elif self.users >= 10000:
            done = True
            info["reason"] = "success: reached 10,000 users"

        # Record history for grading
        current_state = self.state().dict()
        self.history.append({
            "action": action,
            "state": current_state,
            "reward": round(reward, 2)
        })

        return current_state, round(reward, 2), done, info
