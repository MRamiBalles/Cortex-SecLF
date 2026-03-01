import docker
import time
import logging
from typing import Dict, Any, List
from docker.errors import DockerException, NotFound

from ..policy_engine.engine import policy_engine
from .incident_ledger import incident_ledger
from ..shared.telemetry import lattice_monitor

class ActiveWatcher:
    """
    Advanced Blue Team Agent. 
    Intercepts and neutralizes rogue behavior at the OS level (Process/Network).
    """
    def __init__(self, container_name: str = "cslf-rogue-agent"):
        self.container_name = container_name
        self.logger = logging.getLogger("cslf.watcher")
        self.client = docker.from_env()

    def get_container(self):
        try:
            return self.client.containers.get(self.container_name)
        except NotFound:
            return None

    def inspect_network(self, container) -> List[str]:
        """Detects active TCP/UDP connections inside the jail."""
        try:
            res = container.exec_run("ss -tunp")
            output = res.output.decode('utf-8').strip()
            return [line for line in output.split('\n') if "ESTAB" in line]
        except:
            return []

    def inspect_processes(self, container) -> List[str]:
        """Scans the process tree for policy violations."""
        try:
            res = container.exec_run("ps -Ao user,comm")
            output = res.output.decode('utf-8').strip()
            return output.split('\n')[1:] # Skip header
        except:
            return []

    def trigger_kill_switch(self, container, reason: str, evidence: str):
        """Immmediate isolation and memory freeze."""
        policy = policy_engine.current_policy_name
        self.logger.critical(f"🚨 ACTIVE THREAT NEUTRALIZED | Policy: {policy} | {reason}")
        
        action = "KILLED"
        try:
            if policy_engine.get_current_policy()["auto_kill"]:
                container.kill()
                action = "KILLED"
            else:
                container.pause()
                action = "PAUSED"
        except:
            pass

        incident_ledger.log_incident(
            agent_id=self.container_name,
            policy=policy,
            breach_type=reason,
            evidence=evidence,
            action=action
        )
        
        return {
            "timestamp": time.time(),
            "reason": reason,
            "evidence": evidence,
            "status": action,
            "policy": policy
        }

    def monitor_cycle(self) -> Dict[str, Any]:
        """
        Executes a deep inspection cycle based on active policy.
        """
        container = self.get_container()
        if not container:
            return {"status": "error", "msg": "Target container dormant."}

        policy = policy_engine.get_current_policy()

        # 1. Inspect Network Layer
        connections = self.inspect_network(container)
        for conn in connections:
            # Simple check: any connection established is a breach if not permissive
            if policy["forbidden_network"] or policy["isolation_level"] == "MAX":
                 return self.trigger_kill_switch(container, "Unsanctioned Out-of-Bounds Connection", conn)

        # 2. Inspect Process Layer
        processes = self.inspect_processes(container)
        for ps in processes:
            for forbidden in policy["forbidden_processes"]:
                if forbidden in ps.lower():
                    return self.trigger_kill_switch(container, f"Unauthorized Process Activity: {forbidden}", ps)
        
        lattice_monitor.update_heartbeat("lab", status="WATCHING")
        
        return {
            "status": "watching",
            "active_policy": policy_engine.current_policy_name,
            "active_processes": len(processes),
            "threat_level": "ZERO" if not connections else "ELEVEATED"
        }

    def reset_lab(self):
        container = self.get_container()
        if container:
            try: container.unpause()
            except: pass
            try: container.restart()
            except: pass
            return {"status": "ready", "msg": "Sandbox environment recycled."}
        return {"status": "error", "msg": "Hardware link lost."}

watcher = ActiveWatcher()
