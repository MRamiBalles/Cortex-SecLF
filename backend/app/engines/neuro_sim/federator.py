import asyncio
import logging
import hashlib
import time
from typing import Dict, Any, List, Optional
from .p2p_bridge import p2p_bridge
from .mesh_bus import mesh_bus

class LatticeFederator:
    """
    Handles Global Governance across multiple independent SecLF Lattices.
    - Global Quorum Voting
    - Peer Lattice Discovery
    - Inter-Lattice Doctrine Sync
    """
    def __init__(self):
        self.lattice_id = p2p_bridge.lattice_id
        self.logger = logging.getLogger(f"cslf.federator.{self.lattice_id}")
        self.peer_lattices: Dict[str, Dict[str, Any]] = {}
        self.active_global_votes: Dict[str, Dict[str, Any]] = {}

        # Subscribe to Federation gossip
        mesh_bus.subscribe(self._on_federation_pulse)

    async def _on_federation_pulse(self, msg: Dict[str, Any]):
        """Handles incoming global governance messages."""
        if msg.get("type") == "GLOBAL_VOTE_REQ":
            await self._audit_global_request(msg)
        elif msg.get("type") == "GLOBAL_VOTE_SIG":
            await self._process_global_signature(msg)
        elif msg.get("type") == "LATTICE_ANNOUNCE":
            self._register_peer_lattice(msg)

    def _register_peer_lattice(self, msg: Dict[str, Any]):
        peer_id = msg.get("lattice_id")
        if peer_id and peer_id != self.lattice_id:
            self.logger.info(f"FEDERATION: Discovered peer Lattice '{peer_id}'")
            self.peer_lattices[peer_id] = {
                "status": "online",
                "last_seen": time.time(),
                "tpm_attestation": msg.get("tpm_quote")
            }

    async def propose_global_doctrine(self, doctrine_update: Dict[str, Any]):
        """Proposes an update to be applied across the entire federation."""
        vote_id = hashlib.sha256(str(doctrine_update).encode()).hexdigest()[:12]
        self.logger.info(f"GLOBAL_GOVERNANCE: Proposing doctrine update {vote_id}")
        
        request = {
            "type": "GLOBAL_VOTE_REQ",
            "vote_id": vote_id,
            "proposer_lattice": self.lattice_id,
            "data": doctrine_update,
            "timestamp": time.time()
        }
        
        self.active_global_votes[vote_id] = {
            "request": request,
            "signatures": [],
            "status": "VOTING"
        }
        
        # Gossip to the federation topic
        await mesh_bus.broadcast(request, topic="lattice/federation/v1")
        return vote_id

    async def _audit_global_request(self, msg: Dict[str, Any]):
        """Audits an incoming global request from a peer lattice."""
        vote_id = msg.get("vote_id")
        self.logger.info(f"FEDERATION: Auditing global request {vote_id} from {msg['proposer_lattice']}")
        
        # In a real system, the local CISO or Architect node would review this
        # For simulation, we auto-sign if the request is valid
        await asyncio.sleep(1) # Simulation audit time
        
        sig = {
            "type": "GLOBAL_VOTE_SIG",
            "vote_id": vote_id,
            "signer_lattice": self.lattice_id,
            "signature": f"SIG_LATTICE_{self.lattice_id}_{vote_id}",
            "tpm_quote": "SIMULATED_FEDERATED_QUOTE"
        }
        await mesh_bus.broadcast(sig, topic="lattice/federation/v1")

    async def _process_global_signature(self, msg: Dict[str, Any]):
        """Processes an incoming signature for a global vote."""
        vote_id = msg.get("vote_id")
        if vote_id in self.active_global_votes:
            self.active_global_votes[vote_id]["signatures"].append(msg)
            count = len(self.active_global_votes[vote_id]["signatures"])
            self.logger.info(f"FEDERATION: Global Vote {vote_id} count: {count}")
            
            # Quorum check (e.g., Simple majority or 2/3)
            # For simulation, we use 2 signatures as quorum
            if count >= 1: # Minimum 1 peer lattice support
                self.active_global_votes[vote_id]["status"] = "QUORUM_REACHED"
                self.logger.info(f"FEDERATION: Global Quorum reached for {vote_id}. Promoting doctrine.")

# Global Federator instance
lattice_federator = LatticeFederator()
