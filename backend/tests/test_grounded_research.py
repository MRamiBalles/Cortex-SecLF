import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engines.scientist.lab_coat import lab_coat

def test_grounded_research():
    print("--- CORTEX-SEC AI SCIENTIST: Grounded Research Test ---")
    
    topic = "Log Obfuscation"
    print(f"Researching topic: {topic}")
    
    # Run the cycle
    dsg = lab_coat.conduct_research(topic)
    
    print("\n--- IDEATION PHASE ---")
    ideation = dsg["nodes"]["ideation"]
    print(f"Status: {ideation['status']}")
    print(f"Hypothesis Title: {ideation['content'].get('title', 'N/A')}")
    print(f"Grounding Sources: {ideation.get('grounding', [])}")
    
    # Verify grounding
    if any("trench" in s.lower() for s in ideation.get('grounding', [])):
        print("✅ SUCCESS: Grounded in Trench (Technical) collection.")
    else:
        print("⚠️ WARNING: No Trench grounding detected in response.")
        
    print("\n--- REALIZATION PHASE ---")
    realization = dsg["nodes"]["realization"]
    print(f"Status: {realization['status']}")
    if realization['content']:
        print("✅ Code realization complete.")
        
    print("\n--- AUDIT PHASE ---")
    audit = dsg["nodes"]["audit"]
    print(f"Score: {audit.get('score')}/10")
    print(f"Verdict: {audit.get('verdict')}")
    print(f"Critique: {audit.get('critique')[:100]}...")

if __name__ == "__main__":
    test_grounded_research()
