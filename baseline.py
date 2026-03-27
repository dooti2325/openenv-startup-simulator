import os
import json
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from models import Action

def get_action_from_llm(state: dict, client) -> str:
    prompt = f"""You are an AI managing a startup. Here is the current state of your company:
{json.dumps(state, indent=2)}

Your goal is to survive 30 steps, reach as many users as possible, and maximize profit efficiency.
Choose ONE action from the following list to take this month:
{', '.join([a.value for a in Action])}

Respond ONLY with the action name, nothing else. Make sure it is exactly one of the options."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strategic AI startup CEO."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        action = response.choices[0].message.content.strip().lower()
        
        # Validation fallback
        valid_actions = [a.value for a in Action]
        if action not in valid_actions:
            for va in valid_actions:
                if va in action:
                    return va
            return Action.IMPROVE_PRODUCT.value
            
        return action
    except Exception as e:
        print(f"LLM Error: {e}")
        return Action.IMPROVE_PRODUCT.value

def run_baseline(env_class):
    # Runs the baseline against a fresh environment and returns history
    env = env_class()
    env.reset()
    done = False
    
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if (api_key and OpenAI) else None
    
    if not client:
        print("Warning: OPENAI_API_KEY not found or openai not installed. Using deterministic fallback baseline.")

    while not done:
        state = env.state().dict()
        
        if client:
            action = get_action_from_llm(state, client)
        else:
            cash = state.get("cash", 0)
            users = state.get("users", 0)
            
            if cash < 10000:
                action = Action.REDUCE_COSTS.value
            elif users < 500:
                action = Action.INCREASE_MARKETING.value
            else:
                action = Action.IMPROVE_PRODUCT.value
                
        _, _, done, _ = env.step(action)
        
    return env.history
