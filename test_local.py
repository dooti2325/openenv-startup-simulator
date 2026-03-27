from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

def run_tests():
    print("Testing /reset...")
    r = client.get("/reset")
    print(r.json())
    
    print("\nTesting /state...")
    r = client.get("/state")
    print(r.json())
    
    print("\nTesting /step...")
    r = client.post("/step", json={"action": "increase_marketing"})
    print(r.json())

    print("\nTesting /tasks...")
    r = client.get("/tasks")
    print(r.json())
    
    print("\nTesting /grader...")
    r = client.get("/grader?task=survival")
    print(r.json())

    print("\nTesting /baseline...")
    r = client.get("/baseline")
    print(r.json())
    
if __name__ == "__main__":
    run_tests()
