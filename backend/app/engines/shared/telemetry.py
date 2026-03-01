import time
import logging
from typing import Dict, Any, List
from threading import Lock

class LatticeMonitor:
    """
    Centralized telemetry and health monitoring for the Cortex-SecLF lattice.
    Tracks module heartbeats, error rates, and performance metrics.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LatticeMonitor, cls).__new__(cls)
                cls._instance.logger = logging.getLogger("cslf.telemetry")
                cls._instance.metrics = {
                    "modules": {
                        "rag": {"status": "IDLE", "last_heartbeat": 0, "errors": 0},
                        "scientist": {"status": "IDLE", "last_heartbeat": 0, "errors": 0},
                        "dojo": {"status": "IDLE", "last_heartbeat": 0, "errors": 0},
                        "lab": {"status": "IDLE", "last_heartbeat": 0, "errors": 0},
                        "neuro": {"status": "IDLE", "last_heartbeat": 0, "errors": 0}
                    },
                    "system_health": 100
                }
        return cls._instance

    def update_heartbeat(self, module_name: str, status: str = "ALIVE"):
        if module_name in self.metrics["modules"]:
            module = self.metrics["modules"][module_name]
            module["status"] = status
            module["last_heartbeat"] = time.time()
            self.logger.debug(f"HEARTBEAT: {module_name} is {status}")

    def log_error(self, module_name: str):
        if module_name in self.metrics["modules"]:
            self.metrics["modules"][module_name]["errors"] += 1
            self._recalculate_health()
            self.logger.error(f"TELEMETRY_ALERT: Error detected in {module_name}")

    def _recalculate_health(self):
        # Weighted health calculation
        total_errors = sum(m["errors"] for m in self.metrics["modules"].values())
        base_health = 100 - (total_errors * 5)
        
        # Check for stale modules (> 60s since heartbeat)
        now = time.time()
        for mod in self.metrics["modules"].values():
            if mod["last_heartbeat"] > 0 and (now - mod["last_heartbeat"]) > 60:
                base_health -= 10
        
        self.metrics["system_health"] = max(0, base_health)

    def get_summary(self) -> Dict[str, Any]:
        self._recalculate_health()
        return self.metrics

lattice_monitor = LatticeMonitor()
