from .p2p_bridge import p2p_bridge

class SovereignMessageBus:
    """
    Simulates a decentralized P2P gossip network (the Sovereign Mesh).
    Bridges internal telemetry to a real LibP2P GossipSub layer.
    """
    def __init__(self):
        self.logger = logging.getLogger("cslf.mesh_bus")
        self.subscribers: List[Callable] = []
        # Bridge: Subscribe internal bus to LibP2P GossipSub
        p2p_bridge.subscribe(self._on_p2p_message)

    def subscribe(self, callback: Callable):
        """Register a handler for incoming mesh messages (e.g., the Ledger)."""
        self.subscribers.append(callback)

    async def _on_p2p_message(self, envelope: Dict[str, Any]):
        """Callback from LibP2P bridge: deliver to internal lattice components."""
        message = envelope["data"]
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(message)
                else:
                    callback(message)
            except Exception as e:
                self.logger.error(f"Internal delivery error: {e}")

    async def broadcast(self, message: Dict[str, Any], topic: str = "lattice/mesh/v1"):
        """
        Publishes a message to the LibP2P GossipSub mesh.
        """
        node_id = message.get("node_id", "UNKNOWN_NODE")
        self.logger.info(f"MESH_GOSSIP: Node {node_id} publishing to [{topic}]")
        
        # Bridge to LibP2P
        await p2p_bridge.publish(topic, message)

mesh_bus = SovereignMessageBus()
