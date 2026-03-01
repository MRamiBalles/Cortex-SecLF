import docker
import time
import logging
from typing import Dict, Any, List
from docker.errors import DockerException, NotFound

class ActiveWatcher:
    """
    Advanced Blue Team Agent. 
    Intercepts and neutralizes rogue behavior at the OS level (Process/Network).
    """
    def __init__(self, container_name: str = "cslf-rogue-agent"):
        self.container_name = container_name
        self.logger = logging.getLogger("cslf.watcher")
        self.client = docker.from_env()
        
        # Policy: Forbidden Activity Patterns
        self.forbidden_processes = ["nmap", "nc", "netcat", "socat", "scapy", "root"]
        self.forbidden_files = ["/etc/shadow", "/etc/passwd", "/root/.ssh"]

    def get_container(self):
        try:
            return self.client.containers.get(self.container_name)
        except NotFound:
            return None

    def inspect_network(self, container) -> List[str]:
        """Detects active TCP/UDP connections inside the jail."""
        try:
            # -t: tcp, -u: udp, -n: numeric, -p: show process
            res = container.exec_run("ss -tunp")
            output = res.output.decode('utf-8').strip()
            # Filter for established or suspicious connections
            return [line for line in output.split('\n') if "ESTAB" in line or "127.0.0.1" not in line]
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

    def trigger_kill_switch(self, container, reason: str, evidence: Any):
        """Immmediate isolation and memory freeze."""
        self.logger.critical(f"🚨 ACTIVE THREAT NEUTRALIZED | {reason}")
        try:
            container.pause()
            status = "FROZEN"
        except:
            container.kill()
            status = "KILLED"

        report = {
            "timestamp": time.time(),
            "reason": reason,
            "evidence": evidence,
            "status": status,
            "containment_type": "L1_ISOLATION"
        }
        # In production, persist this to a database
        return report

    def monitor_cycle(self) -> Dict[str, Any]:
        """
        Executes a deep inspection cycle. 
        Moving beyond logs into actual system state.
        """
        container = self.get_container()
        if not container:
            return {"status": "error", "msg": "Target container dormant."}

        # 1. Inspect Network Layer
        connections = self.inspect_network(container)
        for conn in connections:
            if "ESTAB" in conn: # Any established connection in a jail is a violation
                return self.trigger_kill_switch(container, "Unsanctioned Out-of-Bounds Connection", conn)

        # 2. Inspect Process Layer
        processes = self.inspect_processes(container)
        for ps in processes:
            for forbidden in self.forbidden_processes:
                if forbidden in ps.lower():
                    return self.trigger_kill_switch(container, f"Unauthorized Process Activity: {forbidden}", ps)

        # 3. Log Stream (Legacy but kept for context)
        # We can't block here in a real loop, so we'd typically use a background thread 
        # or grab recent chunks. For this PoC, we assume success if no violations found.
        
        return {
            "status": "watching",
            "active_processes": len(processes),
            "network_status": "isolated" if not connections else "BREACH_ATTEMPT"
        }

    def reset_lab(self):
        container = self.get_container()
        if container:
            try: container.unpause()
            except: pass
            container.restart()
            return {"status": "ready", "msg": "Sandbox environment recycled."}
        return {"status": "error", "msg": "Hardware link lost."}

watcher = ActiveWatcher()
