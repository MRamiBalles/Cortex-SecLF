from app.engines.dojo_ctrl.manager import dojo_manager
import time

def test_dojo_lifecycle():
    print("--- CORTEX-SEC DOJO TEST: Docker Orchestration ---")
    
    # 1. List Labs
    labs = dojo_manager.list_labs()
    print(f"Available Labs: {[l['id'] for l in labs]}")
    
    target_lab = "juice_shop" # Using a lighter one for test
    
    # 2. Start Lab
    print(f"Starting lab: {target_lab}...")
    start_result = dojo_manager.start_lab(target_lab)
    print(f"Start Result: {start_result}")
    
    if start_result["status"] == "online":
        print(f"Lab is UP at {start_result['access_url']}")
        
        # 3. Check Status
        status = dojo_manager.get_status(target_lab)
        print(f"Current Status: {status['status']}")
        
        # 4. Stop Lab
        print("Stopping lab...")
        stop_result = dojo_manager.stop_lab(target_lab)
        print(f"Stop Result: {stop_result}")
    else:
        print("Skipping stop test due to start failure.")

if __name__ == "__main__":
    test_dojo_lifecycle()
