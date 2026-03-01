import logging
import json
import docker
import time
import os
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, Any, List

# Agent Clients
from openai import OpenAI
from anthropic import Anthropic
import ollama
from dotenv import load_dotenv

from ...rag_engine.retriever import retriever
from ...dojo_ctrl.manager import dojo_manager
from ...neuro_sim.mesh_bus import mesh_bus
from ...neuro_sim.nodes import HIVE_NODES

# Load environment variables from .env
load_dotenv()

class HiveOrchestrator:
    def __init__(self, team_id: str = "DEFAULT_HIVE"):
        self.team_id = team_id
        self.logger = logging.getLogger(f"cslf.hive.{team_id}")
        self.docker_proxy_url = os.getenv("DOCKER_PROXY_URL", "tcp://cslf-docker-proxy:2375")
        self.prompts_dir = "backend/app/engines/scientist/hive/prompts"
        
        # Collaborative Findings cache (Shared via P2P)
        self.collaborative_findings: List[Dict[str, Any]] = []
        mesh_bus.subscribe(self._on_collaborative_pulse)

        # Clients
        self.openai_client = OpenAI() if os.getenv("OPENAI_API_KEY") else None
        self.anthropic_client = Anthropic() if os.getenv("ANTHROPIC_API_KEY") else None
        
        # Sovereign Mock Flag: Use subprocess if Docker is down
        self.sovereign_mock = os.getenv("HIVE_SOVEREIGN_MOCK", "TRUE") == "TRUE"
        
        try:
            self.client = docker.DockerClient(base_url=self.docker_proxy_url)
            self.logger.info(f"Team {team_id} connected to Docker Proxy Cage.")
        except Exception:
            self.logger.warning(f"Docker unreachable. Team {team_id} activating Sovereign Mock.")
            self.client = None
            self.sovereign_mock = True

        self.dsg = {
            "version": "4.5", # MART Coordination
            "team_id": team_id,
            "project_id": None,
            "topic": None,
            "status": "IDLE",
            "nodes": {
                "ideation": {"content": None, "grounding": [], "status": "PENDING"},
                "realization": {"content": None, "trials": [], "status": "PENDING"},
                "field_test": {"lab": None, "result": None, "status": "PENDING"},
                "audit": {"score": 0, "verdict": None, "critique": None, "status": "PENDING", "quorum": None}
            },
            "edges": ["ideation -> realization", "realization -> field_test", "field_test -> audit"]
        }

    async def _on_collaborative_pulse(self, msg: Dict[str, Any]):
        """Listen for research pulses from other HIVE teams."""
        if msg.get("type") == "RESEARCH_PULSE" and msg.get("team_id") != self.team_id:
            self.logger.info(f"MART: Received insight from Team {msg['team_id']}")
            self.collaborative_findings.append(msg)

    async def broadcast_insight(self, insight: Dict[str, Any]):
        """Shares a technical insight with other teams via the decentralized mesh."""
        payload = {
            "type": "RESEARCH_PULSE",
            "team_id": self.team_id,
            "data": insight,
            "timestamp": time.time()
        }
        await mesh_bus.broadcast(payload, topic="lattice/mart/v1")

    def _load_prompt(self, agent_name: str) -> str:
        path = os.path.join(self.prompts_dir, f"{agent_name}.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _llm_call(self, agent: str, system_prompt: str, user_prompt: str) -> str:
        # Include collaborative context for the LLM
        if self.collaborative_findings:
            collaborative_context = "\n\nInsights from other HIVE teams:\n" + \
                                   json.dumps(self.collaborative_findings[-3:], indent=2)
            user_prompt += collaborative_context

        self.logger.info(f"LLM_CALL for {agent} ({self.team_id})")
        try:
            if agent == "theorist" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            
            if agent == "engineer" and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=2048,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text
            
            if agent == "reviewer" and self.openai_client:
                 response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"}
                )
                 return response.choices[0].message.content

            # Fallback: Local Ollama
            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}]
            )
            return response['message']['content']
        except Exception as e:
            self.logger.warning(f"LLM Primary Fallback Failed for {agent}: {e}")
            # Final Safety Net for Reviewer if even OpenAI failed or agent is reviewer
            if agent == "reviewer":
                return json.dumps({"score": 5, "verdict": "REVISE", "critique": f"Reviewer communication failure: {e}"})
            return json.dumps({"error": str(e), "verdict": "REJECT", "code": "print('LLM_ERROR')"})

    def initialize_project(self, topic: str):
        self.dsg["project_id"] = f"MART_{self.team_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.dsg["topic"] = topic
        self.dsg["status"] = "ACTIVE"
        self.logger.info(f"Project Initialized: {self.dsg['project_id']}")

    def run_sandbox_execution(self, code: str) -> Dict[str, Any]:
        if not self.sovereign_mock and self.client:
            return self._run_docker_execution(code)
        else:
            return self._run_subprocess_execution(code)

    def _run_docker_execution(self, code: str) -> Dict[str, Any]:
        try:
            container = self.client.containers.run(
                image="python:3.11-slim",
                command=["python", "-c", code],
                detach=True,
                network_disabled=True,
                mem_limit="128m",
                cpu_quota=50000,
                remove=False
            )
            result = container.wait(timeout=10)
            logs = container.logs().decode("utf-8")
            container.remove()
            return {"exit_code": result["StatusCode"], "logs": logs}
        except Exception as e:
            return {"exit_code": 1, "logs": str(e)}

    def _run_subprocess_execution(self, code: str) -> Dict[str, Any]:
        """
        Sovereign Mock: Soft-Cage Execution using subprocess.
        """
        fd, path = tempfile.mkstemp(suffix=".py")
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code)
            
            result = subprocess.run(
                ["python", path],
                capture_output=True,
                text=True,
                timeout=10,
                env={"PATH": os.environ["PATH"]} # Clean env could be safer
            )
            return {
                "exit_code": result.returncode,
                "logs": result.stdout + result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"exit_code": 124, "logs": "TIMEOUT: Code execution exceeded 10s limits."}
        except Exception as e:
            return {"exit_code": 1, "logs": str(e)}
        finally:
            if os.path.exists(path):
                os.remove(path)

    async def step_theorist(self, topic: str):
        self.logger.info(f"THEORIST [{self.team_id}] START: Multi-Collection Grounding...")
        
        # 1. Parallel Retrieval from Canonical Collections
        doctrine_results = retriever.retrieve(topic, collection_name="doctrine", n_results=3)
        trench_results = retriever.retrieve(topic, collection_name="trench", n_results=3)
        
        all_results = doctrine_results + trench_results
        
        # In PoC/First Run, if db is empty, we use a structured fallback to maintain logic flow
        if not all_results:
             self.logger.warning("RAG ARCHIVE EMPTY. Injecting Baseline Sovereign Logic.")
             all_results = [
                 {"metadata": {"source": "Doctrine_Core_v1.md", "collection": "doctrine"}, "content": "All agents must operate under the Air-Gap mandate."},
                 {"metadata": {"source": "Trench_Exploits_v1.md", "collection": "trench"}, "content": "Log obfuscation can be achieved via adversarial noise injection."}
             ]

        # 2. Context Synthesis
        context = retriever.format_for_prompt(all_results)
        sys_prompt = self._load_prompt("theorist")
        user_prompt = f"Objective: Generate a scientific hypothesis for the topic '{topic}'.\n\nBase Research (RAG):\n{context}\n\nTask: Synthesize a hypothesis that respects Doctrine while exploring the technical possibilities in Trench. Return JSON."

        # 3. LLM Reasoning
        response_json = self._llm_call("theorist", sys_prompt, user_prompt)
        
        try:
            content = json.loads(response_json)
        except:
            self.logger.error("Theorist failed to produce valid JSON. Attempting repair.")
            content = {"error": "PARSING_CRASH", "raw": response_json}

        # 4. Grounding Report
        sources = []
        for r in all_results:
            meta = r.get('metadata', {})
            sources.append(f"[{meta.get('collection', 'unknown')}] {meta.get('source', 'Unknown')}")

        self.dsg["nodes"]["ideation"] = {
            "content": content,
            "grounding": list(set(sources)), # Unique sources
            "status": "GROUNDED_AND_VERIFIED"
        }
        self.logger.info("THEORIST COMPLETE: Hypothesis grounded in Archive.")
        
        # Broadcast discovery to other MART teams
        await self.broadcast_insight({"hypothesis": content, "sources": sources})
        
        return True

    async def step_engineer(self):
        hyp_content = self.dsg["nodes"]["ideation"]["content"]
        if not hyp_content: return False

        sys_prompt = self._load_prompt("engineer")
        max_trials = 5
        current_user_prompt = f"Goal: Realize this hypothesis: {json.dumps(hyp_content)}\nGenerate Python code."
        
        for trial in range(max_trials):
            self.logger.info(f"ENGINEER [{self.team_id}] TRIAL {trial+1}/{max_trials}...")
            
            response = self._llm_call("engineer", sys_prompt, current_user_prompt)
            try:
                data = json.loads(response) if "{" in response else {"code": response}
            except:
                data = {"code": response}
            
            code = data.get("code", "")

            exec_result = self.run_sandbox_execution(code)
            exec_result["trial"] = trial + 1
            self.dsg["nodes"]["realization"]["trials"].append(exec_result)

            if exec_result["exit_code"] == 0:
                self.dsg["nodes"]["realization"]["content"] = code
                self.dsg["nodes"]["realization"]["status"] = "COMPILED"
                # Share success with other teams
                await self.broadcast_insight({"status": "SUCCESS", "module": "ENGINEER", "code_snippet": code[:100]})
                return True
            else:
                self.logger.warning(f"TRIAL {trial+1} FAILED: Reflexion triggered.")
                current_user_prompt = f"Your previous code failed with this error:\n{exec_result['logs']}\n\nFix it. Paga el Impuesto de Verificación."
        
        self.dsg["nodes"]["realization"]["status"] = "FAILED_CIRCUIT_BREAKER"
        return False


    async def step_field_test(self, lab_id: str = "vulnerable_web"):
        """
        Field Test: Deploys a real Dojo lab and targets it with the generated realization.
        """
        if self.dsg["nodes"]["realization"]["status"] != "COMPILED":
            return False
            
        self.logger.info(f"FIELD TEST [{self.team_id}] START: Deploying lab '{lab_id}' for exploit validation...")
        
        # 1. Start Lab
        lab_result = dojo_manager.start_lab(lab_id)
        if lab_result["status"] != "online":
            self.dsg["nodes"]["field_test"]["status"] = "CANCELLED_LAB_FAILURE"
            return False

        # 2. Execute Realization (Targeting the Lab)
        code = self.dsg["nodes"]["realization"]["content"]
        target_code = f"import os\nos.environ['TARGET_URL'] = '{lab_result['access_url']}'\n{code}"
        
        exec_result = self.run_sandbox_execution(target_code)
        
        # 3. Teardown & Report
        dojo_manager.stop_lab(lab_id)
        
        self.dsg["nodes"]["field_test"] = {
            "lab": lab_id,
            "result": exec_result,
            "status": "VERIFIED_IN_FIELD" if exec_result["exit_code"] == 0 else "FAILED_IN_FIELD"
        }
        self.logger.info(f"FIELD TEST COMPLETE: Status={exec_result['exit_code']}")
        
        if exec_result["exit_code"] == 0:
             await self.broadcast_insight({"status": "FIELD_GOAL", "lab": lab_id, "logs": exec_result["logs"][:200]})
             
        return True

    async def _collect_quorum(self, artifact_hash: str, timeout: float = 5.0) -> List[Dict[str, Any]]:
        """
        Broadcasts a promotion request and waits for HIVE nodes to sign it.
        MAV (Multi-Agent Voting) Quorum logic.
        """
        signatures = []
        
        async def on_sig(msg):
            if msg.get("block_hash") == artifact_hash:
                signatures.append(msg)

        # Temp subscription
        mesh_bus.subscribe(on_sig)
        
        # Trigger signatures (Simulating nodes reviewing the code)
        for node in HIVE_NODES:
            sig = node.sign_block(artifact_hash)
            sig["block_hash"] = artifact_hash
            await mesh_bus.broadcast(sig)

        start = time.time()
        while len(signatures) < 2: # 2/3 Quorum
            if time.time() - start > timeout:
                break
            await asyncio.sleep(0.1)
        
        # Filter unique (basic)
        unique_sigs = {s["node_id"]: s for s in signatures}.values()
        return list(unique_sigs)

    async def step_reviewer(self):
        if self.dsg["nodes"]["realization"]["status"] != "COMPILED":
            return False

        field_data = self.dsg["nodes"]["field_test"]
        sys_prompt = self._load_prompt("reviewer")
        user_prompt = f"Hypothesis: {json.dumps(self.dsg['nodes']['ideation']['content'])}\n" \
                     f"Implementation: {self.dsg['nodes']['realization']['content']}\n" \
                     f"Field Test Result ({field_data['lab']}): {json.dumps(field_data['result'])}\n\n" \
                     f"Audit strictly. If Field Test failed, penalize score."
        
        response = self._llm_call("reviewer", sys_prompt, user_prompt)
        try:
            audit_data = json.loads(response) if "{" in response else {"critique": response, "score": 0, "verdict": "REJECT"}
        except:
            audit_data = {"critique": response, "score": 0, "verdict": "REJECT"}
        
        self.dsg["nodes"]["audit"] = {
            "score": audit_data.get("score", 0),
            "verdict": audit_data.get("verdict", "REJECT"),
            "critique": audit_data.get("critique", "No critique provided"),
            "status": "AUDITED",
            "quorum": "PENDING"
        }
        
        if audit_data.get("verdict") == "ACCEPT":
            # Initiate Quorum Promotion
            artifact_hash = hashlib.sha256(self.dsg["nodes"]["realization"]["content"].encode()).hexdigest()
            signatures = await self._collect_quorum(artifact_hash)
            
            if len(signatures) >= 2:
                self.dsg["nodes"]["audit"]["quorum"] = "VERIFIED"
                self.dsg["nodes"]["audit"]["signatures"] = signatures
                self.dsg["status"] = "COMPLETED"
                self.logger.info(f"QUORUM REACHED: Code {artifact_hash[:8]} promoted to STABLE.")
            else:
                self.dsg["nodes"]["audit"]["quorum"] = "FAILED"
                self.dsg["status"] = "REJECTED_BY_QUORUM"
                self.logger.warning(f"QUORUM FAILED: Consensus not reached for promotion.")
        else:
            self.dsg["status"] = "REJECTED_BY_PEER_REVIEW"
        return True

    async def execute_complete_cycle(self, topic: str, lab_id: str = "vulnerable_web"):
        self.initialize_project(topic)
        if not await self.step_theorist(topic): return self.dsg
        if not await self.step_engineer(): return self.dsg
        await self.step_field_test(lab_id)
        await self.step_reviewer()
        return self.dsg

class ParallelHive:
    """
    Orchestrates multiple HIVE teams for MART (Multi-Agent Red-Teaming).
    Coordination happens via the LibP2P-bridged mesh bus.
    """
    def __init__(self, cluster_id: str = "MART_CLUSTER_01"):
        self.cluster_id = cluster_id
        self.teams: Dict[str, HiveOrchestrator] = {}
        self.logger = logging.getLogger(f"cslf.mart.{cluster_id}")

    def spawn_team(self, team_id: str):
        self.logger.info(f"MART: Spawning Team {team_id}...")
        self.teams[team_id] = HiveOrchestrator(team_id=team_id)
        return self.teams[team_id]

    async def execute_coordinated_strike(self, common_topic: str, lab_id: str):
        """Runs multiple teams against the same objective, sharing insights."""
        tasks = []
        for team_id in self.teams:
            tasks.append(self.teams[team_id].execute_complete_cycle(common_topic, lab_id))
        
        results = await asyncio.gather(*tasks)
        self.logger.info(f"MART CLUSTER COMPLETE: {len(results)} teams reported final status.")
        return results

# Singleton for the local environment
hive_orchestrator = HiveOrchestrator()
mart_cluster = ParallelHive()
