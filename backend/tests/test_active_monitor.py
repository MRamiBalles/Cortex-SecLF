import requests
import time
import json

BASE_URL = "http://localhost:8000/lab"

def test_active_monitor():
    print("--- CORTEX-SEC AGENT LAB: Active Monitor Test ---")
    
    scenarios = ["scream_test", "exfiltration"]
    
    for scenario in scenarios:
        print(f"\nTriggering scenario: {scenario}")
        try:
            response = requests.post(f"{BASE_URL}/start", json={"scenario": scenario}, timeout=10)
            data = response.json()
            
            print(f"Status: {data.get('status')}")
            containment = data.get('active_containment', {})
            
            if containment.get('status') in ['FROZEN', 'KILLED']:
                print(f"✅ SUCCESS: Kill-Switch triggered for {scenario}")
                print(f"Reason: {containment.get('reason')}")
                print(f"Evidence: {containment.get('evidence')}")
            else:
                print(f"❌ FAILURE: Kill-Switch not triggered. Report: {json.dumps(containment, indent=2)}")
                
        except Exception as e:
            print(f"Error during test: {e}")
        
        # Reset for next test
        requests.post(f"{BASE_URL}/reset")
        time.sleep(2)

if __name__ == "__main__":
    # Note: Requires the backend to be running
    print("Pre-requisite: Local API must be running at http://localhost:8000")
    test_active_monitor()
