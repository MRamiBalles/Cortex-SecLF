import asyncio
import logging
from app.engines.neuro_sim.federator import LatticeFederator
from app.engines.neuro_sim.p2p_bridge import LibP2PBridge

async def test_global_federation():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test.federation")
    
    logger.info("INITIALIZING FEDERATION TEST...")
    
    # We use the singleton lattice_federator
    from app.engines.neuro_sim.federator import lattice_federator
    
    # 1. Propose a Global Doctrine Update
    doctrine = {
        "id": "DOCTRINE_FED_001",
        "policy": "ENFORCE_HARDWARE_ROOT_ONLY",
        "scope": "GLOBAL"
    }
    
    logger.info("PROPOSING GLOBAL DOCTRINE...")
    vote_id = await lattice_federator.propose_global_doctrine(doctrine)
    
    # 2. Simulate discovery of a peer lattice
    logger.info("DISCOVERING PEER LATTICE...")
    peer_announcement = {
        "type": "LATTICE_ANNOUNCE",
        "lattice_id": "LATTICE_OSLO_01",
        "tpm_quote": "PEER_HARDWARE_QUOTE_VALID"
    }
    await lattice_federator._on_federation_pulse(peer_announcement)
    
    # 3. Simulate peer lattice signing the vote
    logger.info("SIMULATING PEER SIGNATURE...")
    peer_sig = {
        "type": "GLOBAL_VOTE_SIG",
        "vote_id": vote_id,
        "signer_lattice": "LATTICE_OSLO_01",
        "signature": "SIG_PEER_VALID_001",
        "tpm_quote": "PEER_SIG_QUOTE"
    }
    await lattice_federator._on_federation_pulse(peer_sig)
    
    # 4. Verify Status
    vote_status = lattice_federator.active_global_votes.get(vote_id, {}).get("status")
    if vote_status == "QUORUM_REACHED":
        logger.info(f"SUCCESS: Global Quorum reached for {vote_id}")
    else:
        logger.error(f"FAILURE: Quorum not reached. Status: {vote_status}")

if __name__ == "__main__":
    asyncio.run(test_global_federation())
