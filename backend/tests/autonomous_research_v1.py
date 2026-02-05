import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engines.scientist.hive.orchestrator import hive_orchestrator

def run_autonomous_research():
    print("--- CORTEX-SEC AUTONOMOUS RESEARCH: V3.3 SYNAPSE ---")
    
    topic = (
        "Investiga vectores de ataque teóricos contra el protocolo de transmisión de datos del NeuroDashboard. "
        "Específicamente, ¿es posible realizar un ataque de inferencia de atributos (Attribute Inference Attack) "
        "sobre los datos EEG cifrados para deducir el estado emocional sin descifrar el payload? Propón una PoC en Python."
    )
    
    print(f"TARGET TOPIC: {topic}")
    print("STATUS: Initiating Synthetic Hive...")
    
    results = hive_orchestrator.execute_complete_cycle(topic)
    
    print("\n" + "="*50)
    print(f"RESEARCH PROJECT: {results['project_id']}")
    print(f"FINAL STATUS: {results['status']}")
    print("="*50)
    
    # 1. Ideation Results
    ideation = results['nodes']['ideation']
    if ideation['status'] == "VERIFIED_GROUNDING":
        print(f"\n[AGENT THEORIST] SUCCESS")
        print(f"Hypothesis: {ideation['content'].get('title', 'N/A')}")
        print(f"Grounding Sources: {', '.join(ideation['grounding'])}")
    else:
        print(f"\n[AGENT THEORIST] ABORTED: {results['status']}")
        return

    # 2. Engineering Results
    realization = results['nodes']['realization']
    print(f"\n[AGENT ENGINEER] Status: {realization['status']}")
    print(f"Trials: {len(realization['trials'])}")
    if realization['status'] == "COMPILED":
        print(f"Verification: PASS (Exit Code 0)")
        # Show first few lines of code
        code_preview = realization['content'].split('\n')[:5]
        print("Code Preview:")
        for line in code_preview: print(f"  {line}")

    # 3. Audit Results
    audit = results['nodes']['audit']
    print(f"\n[AGENT REVIEWER] Verdict: {audit['verdict']}")
    print(f"Score: {audit['score']}/10")
    print(f"Critique: {audit['critique']}")

    print("\n--- RESEARCH CYCLE COMPLETE ---")

if __name__ == "__main__":
    run_autonomous_research()
