import logging
import json
import docker
import time
from datetime import datetime
from typing import Dict, Any

class HiveOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger("cslf.hive")
        # Ensure we talk to the Cage, not the Host
        self.docker_proxy_url = "tcp://cslf-docker-proxy:2375"
        try:
            self.client = docker.DockerClient(base_url=self.docker_proxy_url)
        except Exception as e:
            self.logger.error(f"Failed to connect to Docker Proxy: {e}")
            self.client = None

        self.dsg = {
            "version": "3.1",
            "project_id": None,
            "state": "IDLE",
            "artifacts": {
                "hypothesis": None,
                "implementation": None,
                "review": None
            },
            "trials": []
        }

    def initialize_project(self, topic: str):
        self.dsg["project_id"] = f"HIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.dsg["topic"] = topic
        self.dsg["state"] = "IDEATION"
        self.logger.info(f"Project {self.dsg['project_id']} Initialized: {topic}")

    def run_sandbox_execution(self, code: str) -> Dict[str, Any]:
        """
        Executes code within the 'Cage' using ephemeral containers.
        """
        if not self.client:
            return {"exit_code": -1, "logs": "Docker Proxy not available."}

        try:
            # Launching isolated container
            container = self.client.containers.run(
                image="python:3.11-slim",
                command=["python", "-c", code],
                detach=True,
                network_disabled=True, # Physically enforced by Proxy even if requested
                mem_limit="128m",
                cpu_quota=50000,
                remove=False # We need to capture logs first
            )
            
            # Wait for completion
            result = container.wait(timeout=10)
            logs = container.logs().decode("utf-8")
            container.remove()

            return {
                "exit_code": result["StatusCode"],
                "logs": logs
            }
        except Exception as e:
            return {"exit_code": 1, "logs": str(e)}

    def run_loop(self):
        """
        Orchestrates the MAS flow: Theorist -> Engineer (with Reflection) -> Reviewer
        """
        # Step 1: Theorist (Ideation)
        self.dsg["state"] = "THEORIZING"
        self.logger.info("Theorist generating hypothesis...")
        self.dsg["artifacts"]["hypothesis"] = {
            "title": "Recursive vs Iterative Efficiency Audit",
            "status": "GENERATED"
        }

        # Step 2: Engineer (Execution in Cage with Reflection)
        self.dsg["state"] = "ENGINEERING"
        max_retries = 3
        current_code = "print('Simulated Code Artifact')" # Mock starting code
        
        for attempt in range(max_retries):
            self.logger.info(f"Engineer Attempt {attempt+1}/{max_retries}")
            
            # Execute in Sandbox
            exec_result = self.run_sandbox_execution(current_code)
            self.dsg["trials"].append(exec_result)

            if exec_result["exit_code"] == 0:
                self.logger.info("Engineering SUCCESS: Code verified in sandbox.")
                self.dsg["artifacts"]["implementation"] = {
                    "code": current_code,
                    "logs": exec_result["logs"],
                    "status": "VERIFIED"
                }
                break
            else:
                self.logger.warning(f"Engineering FAILED (Attempt {attempt+1}): {exec_result['logs']}")
                # Simulation: Agent 'fixes' it in next iteration (Reflexion)
                current_code = "# Fixed code simulation\nprint('Success after correction')"
        
        # Step 3: Reviewer (Audit)
        if self.dsg["artifacts"]["implementation"]:
            self.dsg["state"] = "REVIEWING"
            self.dsg["artifacts"]["review"] = {
                "verdict": "ACCEPT",
                "score": "9/10",
                "critique": "Code is secure and follows standard library constraints."
            }
            self.dsg["state"] = "COMPLETED"
        else:
            self.dsg["state"] = "FAILED"

        return self.dsg

hive_orchestrator = HiveOrchestrator()
