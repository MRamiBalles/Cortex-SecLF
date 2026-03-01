import docker
import logging
from typing import List, Dict, Any, Optional
from docker.errors import DockerException, NotFound, APIError

class DojoManager:
    """
    Orchestrates the lifecycle of vulnerable laboratory environments using Docker.
    Provides isolation and controlled exposure of security testing targets.
    """
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.logger = logging.getLogger("cslf.dojo")
        except DockerException as e:
            # Critical dependency handled at initialization
            print(f"CRITICAL: Docker daemon not accessible: {e}")
            raise
        
        # Predefined Labs Registry
        self.available_labs = {
            "vulnerable_web": {
                "name": "DVWA (Damn Vulnerable Web App)",
                "image": "vulnerables/web-dvwa",
                "internal_port": 80,
                "description": "Legacy web application security lab (SQLi, XSS, Brute Force)."
            },
            "juice_shop": {
                "name": "OWASP Juice Shop",
                "image": "bkimminich/juice-shop",
                "internal_port": 3000,
                "description": "Modern Javascript/Node app with intentional security flaws."
            },
            "metasploitable": {
                "name": "Metasploitable 2 (Substitute)",
                "image": "tleemcjr/metasploitable2",
                "internal_port": 80,
                "description": "Multi-service vulnerable environment for network penetration testing."
            }
        }

    def list_labs(self) -> List[Dict[str, Any]]:
        """Returns the registry of available labs."""
        return [{"id": k, **v} for k, v in self.available_labs.items()]

    def start_lab(self, lab_id: str) -> Dict[str, Any]:
        """
        Deploys a lab container with automatic port mapping.
        Ensures idempotent state by cleaning existing instances.
        """
        if lab_id not in self.available_labs:
            self.logger.error(f"Execution rejected: Unknown lab_id '{lab_id}'")
            return {"status": "error", "msg": "Target laboratory definition not found."}

        lab_config = self.available_labs[lab_id]
        container_name = f"cslf-dojo-{lab_id}"

        # Step 1: Idempotency Check & Cleanup
        try:
            existing = self.client.containers.get(container_name)
            self.logger.info(f"Purging existing instance of {container_name}")
            existing.remove(force=True)
        except NotFound:
            pass
        except APIError as e:
            self.logger.error(f"Infrastucture error during cleanup: {e}")
            return {"status": "error", "msg": "Hardware/API level failure during cleanup."}

        # Step 2: Deployment
        try:
            self.logger.info(f"Deploying {lab_config['name']} ({lab_config['image']})")
            container = self.client.containers.run(
                lab_config["image"],
                name=container_name,
                detach=True,
                network="cslf-net", 
                ports={f'{lab_config["internal_port"]}/tcp': None} 
            )
            
            # Step 3: Health Verification & Port Resolution
            container.reload()
            if container.status != "running" and container.status != "restarting":
                # Some labs take time to spin up, 'running' is preferred
                time.sleep(1) 
                container.reload()

            ports = container.ports.get(f'{lab_config["internal_port"]}/tcp')
            if not ports:
                raise RuntimeError("Failed to resolve dynamic port mapping.")

            host_port = ports[0]['HostPort']
            
            self.logger.info(f"Lab {lab_id} online on port {host_port}")
            return {
                "status": "online",
                "lab": lab_config["name"],
                "container_id": container.id[:12],
                "access_url": f"http://localhost:{host_port}",
                "metrics": {"uptime": "initializing"}
            }
        except Exception as e:
            self.logger.critical(f"Deployment crash for {lab_id}: {e}")
            return {"status": "error", "msg": f"Deployment failed: {str(e)}"}

    def stop_lab(self, lab_id: str) -> Dict[str, Any]:
        """Gracefully terminates and removes a lab instance."""
        container_name = f"cslf-dojo-{lab_id}"
        try:
            container = self.client.containers.get(container_name)
            container.remove(force=True)
            self.logger.info(f"Lab {lab_id} decommissioned successfully.")
            return {"status": "offline", "msg": f"Laboratory '{lab_id}' has been decommissioned."}
        except NotFound:
            return {"status": "error", "msg": "No active instance found for this ID."}
        except Exception as e:
            self.logger.error(f"Teardown failure for {lab_id}: {e}")
            return {"status": "error", "msg": "Resource lock prevent decommissioning."}

    def get_status(self, lab_id: str) -> Dict[str, Any]:
        """Queries the current operational status of a lab."""
        container_name = f"cslf-dojo-{lab_id}"
        try:
            container = self.client.containers.get(container_name)
            return {
                "id": lab_id,
                "status": container.status,
                "uptime": container.attrs.get('State', {}).get('StartedAt'),
                "health": "operational" if container.status == "running" else "degraded"
            }
        except NotFound:
            return {"id": lab_id, "status": "dormant"}

dojo_manager = DojoManager()
