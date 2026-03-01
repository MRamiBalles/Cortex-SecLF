import asyncio
import logging
from app.engines.neuro_sim.mesh_bus import mesh_bus
from app.engines.scientist.hive.orchestrator import ParallelHive

async def test_mart_coordination():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test.mart")
    
    logger.info("INITIALIZING MART CLUSTER...")
    cluster = ParallelHive(cluster_id="TEST_CLUSTER_P2P")
    
    # Spawn two teams
    team_a = cluster.spawn_team("ALPHA_TEAM")
    team_b = cluster.spawn_team("BETA_TEAM")
    
    # Team A finds a mock insight
    logger.info("ALPHA_TEAM: Simulating discovery...")
    await team_a.broadcast_insight({
        "vulnerability": "CVE-2026-XSS-MOCK",
        "detail": "Cross-Team collaboration test signal."
    })
    
    # Wait for propagation across the LibP2P-bridged mesh
    await asyncio.sleep(1)
    
    # Check if Team B received it
    if len(team_b.collaborative_findings) > 0:
        logger.info(f"SUCCESS: Team Beta received Alpha's insight via LibP2P Bridge.")
        logger.info(f"Insight Data: {team_b.collaborative_findings[0]['data']['vulnerability']}")
    else:
        logger.error("FAILURE: Beta Team did not receive the gossip message.")

if __name__ == "__main__":
    asyncio.run(test_mart_coordination())
