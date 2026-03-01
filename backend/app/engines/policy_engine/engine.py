from typing import Dict, Any, List
import logging

class PolicyEngine:
    """
    Dynamic Security Policy Engine for Cortex-SecLF.
    Defines allowed and forbidden behaviors for autonomous agents.
    """
    
    POLICIES = {
        "STRICT": {
            "forbidden_processes": ["nmap", "nc", "netcat", "socat", "scapy", "root", "sh", "bash"],
            "forbidden_network": ["0.0.0.0/0"], # No outbound traffic allowed
            "auto_kill": True,
            "isolation_level": "MAX"
        },
        "BALANCED": {
            "forbidden_processes": ["nmap", "nc", "netcat", "socat", "scapy", "root"],
            "forbidden_network": ["192.168.0.0/16", "10.0.0.0/8"], # Block private subnet scan
            "auto_kill": True,
            "isolation_level": "MED"
        },
        "PERMISSIVE": {
            "forbidden_processes": ["nmap", "socat"],
            "forbidden_network": [],
            "auto_kill": False,
            "isolation_level": "LOW"
        }
    }

    def __init__(self, default_policy: str = "BALANCED"):
        self.current_policy_name = default_policy
        self.logger = logging.getLogger("cslf.policy")

    def get_current_policy(self) -> Dict[str, Any]:
        return self.POLICIES.get(self.current_policy_name, self.POLICIES["BALANCED"])

    def set_policy(self, policy_name: str):
        if policy_name in self.POLICIES:
            self.current_policy_name = policy_name
            self.logger.info(f"POLICY_CHANGE: System now operating under {policy_name} constraints.")
            return True
        return False

policy_engine = PolicyEngine()
