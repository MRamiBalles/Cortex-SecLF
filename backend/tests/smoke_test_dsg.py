import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engines.scientist.hive.orchestrator import hive_orchestrator

def test_dsg_synapse():
    print("--- CORTEX-SEC DSG SYNAPSE SMOKE TEST ---")
    topic = "Privacy-Preserving EEG Infiltration Defense"
    
    results = hive_orchestrator.execute_complete_cycle(topic)
    
    print(f"Project ID: {results['project_id']}")
    print(f"Global Status: {results['status']}")
    
    # Verify Nodes
    ideation = results['nodes']['ideation']
    realization = results['nodes']['realization']
    audit = results['nodes']['audit']
    
    print(f"[NODE 1] Ideation: {ideation['status']} (|Citations|: {len(ideation['grounding'])})")
    print(f"[NODE 2] Realization: {realization['status']} (Trials: {len(realization['trials'])})")
    print(f"[NODE 3] Audit: {audit['status']} (Verdict: {audit['verdict']}, Score: {audit['score']}/10)")
    
    if results['status'] == "COMPLETED" and audit['verdict'] == "ACCEPT":
        print("DSG SYNAPSE TEST: PASS")
        return True
    else:
        print("DSG SYNAPSE TEST: FAIL")
        return False

if __name__ == "__main__":
    success = test_dsg_synapse()
    sys.exit(0 if success else 1)
