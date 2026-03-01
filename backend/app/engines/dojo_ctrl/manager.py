import docker
import logging
from typing import List, Dict, Any

class DojoManager:
    def __init__(self):
        self.client = docker.from_env()
        self.logger = logging.getLogger("DojoManager")
        
        # Predefined Labs (Can be expanded)
        self.available_labs = {
            "vulnerable_web": {
                "name": "DVWA (Damn Vulnerable Web App)",
                "image": "vulnerables/web-dvwa",
                "port": 80,
                "description": "Clásico lab de vulnerabilidades web (SQLi, XSS, etc.)"
            },
            "juice_shop": {
                "name": "OWASP Juice Shop",
                "image": "bkimminich/juice-shop",
                "port": 3000,
                "description": "Arquitectura moderna de JS/Node con fallos de seguridad."
            },
            "metasploitable": {
                "name": "Metasploitable 3 (Linux)",
                "image": "tleemcjr/metasploitable2", # Using v2 image as common substitute
                "port": 80,
                "description": "Entorno multipropósito con servicios vulnerables."
            }
        }

    def list_labs(self) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in self.available_labs.items()]

    def start_lab(self, lab_id: str) -> Dict[str, Any]:
        if lab_id not in self.available_labs:
            return {"status": "error", "msg": "Lab not found"}

        lab_config = self.available_labs[lab_id]
        container_name = f"cslf-dojo-{lab_id}"

        # Clean existing if any
        try:
            old_container = self.client.containers.get(container_name)
            old_container.remove(force=True)
        except docker.errors.NotFound:
            pass

        try:
            container = self.client.containers.run(
                lab_config["image"],
                name=container_name,
                detach=True,
                network="cslf-net", # Connect to main net or separate jail? 
                                    # For now, cslf-net but isolated logic needed later
                ports={f'{lab_config["port"]}/tcp': None} # Auto-map to host port
            )
            
            # Refresh to get dynamic port
            container.reload()
            host_port = container.ports[f'{lab_config["port"]}/tcp'][0]['HostPort']
            
            return {
                "status": "online",
                "lab": lab_config["name"],
                "container_id": container.id[:12],
                "access_url": f"http://localhost:{host_port}"
            }
        except Exception as e:
            self.logger.error(f"Failed to start lab {lab_id}: {e}")
            return {"status": "error", "msg": str(e)}

    def stop_lab(self, lab_id: str) -> Dict[str, Any]:
        container_name = f"cslf-dojo-{lab_id}"
        try:
            container = self.client.containers.get(container_name)
            container.remove(force=True)
            return {"status": "offline", "msg": f"Lab {lab_id} stopped."}
        except docker.errors.NotFound:
            return {"status": "error", "msg": "Lab not running."}

    def get_status(self, lab_id: str) -> Dict[str, Any]:
        container_name = f"cslf-dojo-{lab_id}"
        try:
            container = self.client.containers.get(container_name)
            return {
                "id": lab_id,
                "status": container.status,
                "ports": container.ports
            }
        except docker.errors.NotFound:
            return {"id": lab_id, "status": "down"}

dojo_manager = DojoManager()
