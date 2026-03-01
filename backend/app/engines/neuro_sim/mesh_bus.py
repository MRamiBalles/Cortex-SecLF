import asyncio
import logging
import random
from typing import Dict, Any, List, Callable

class SovereignMessageBus:
    """
    Simulates a decentralized P2P gossip network (the Sovereign Mesh).
    Handles asynchronous message propagation between nodes with simulated latency.
    """
    def __init__(self):
        self.logger = logging.getLogger("cslf.mesh_bus")
        self.subscribers: List[Callable] = []

    def subscribe(self, callback: Callable):
        """Register a handler for incoming mesh messages (e.g., the Ledger)."""
        self.subscribers.append(callback)

    async def broadcast(self, message: Dict[str, Any]):
        """
        Simulates broadcasting a message to all peers in the mesh.
        Introduces random latency to reflect air-gapped/distributed network conditions.
        """
        node_id = message.get("node_id", "UNKNOWN_NODE")
        self.logger.info(f"MESH_BROADCAST: Node {node_id} publishing signature...")
        
        # Simulate network propagation latency (50ms to 500ms)
        latency = random.uniform(0.05, 0.5)
        await asyncio.sleep(latency)
        
        # Deliver to subscribers
        for callback in self.subscribers:
            if asyncio.iscoroutinefunction(callback):
                await callback(message)
            else:
                callback(message)

mesh_bus = SovereignMessageBus()
