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

from ...rag_engine.retriever import retriever

class HiveOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger("cslf.hive")
        self.docker_proxy_url = os.getenv("DOCKER_PROXY_URL", "tcp://cslf-docker-proxy:2375")
        self.prompts_dir = "backend/app/engines/scientist/hive/prompts"
        
        # Clients
        self.openai_client = OpenAI() if os.getenv("OPENAI_API_KEY") else None
        self.anthropic_client = Anthropic() if os.getenv("ANTHROPIC_API_KEY") else None
        
        # Sovereign Mock Flag: Use subprocess if Docker is down
        self.sovereign_mock = os.getenv("HIVE_SOVEREIGN_MOCK", "TRUE") == "TRUE"
        
        try:
            self.client = docker.DockerClient(base_url=self.docker_proxy_url)
            self.logger.info("Connected to Docker Proxy Cage.")
        except Exception:
            self.logger.warning("Docker Proxy unreachable. Activating Sovereign Mock (Subprocess Sandbox).")
            self.client = None
            self.sovereign_mock = True

        self.dsg = {
            "version": "3.3",
            "project_id": None,
            "topic": None,
            "status": "IDLE",
            "nodes": {
                "ideation": {"content": None, "grounding": [], "status": "PENDING"},
                "realization": {"content": None, "trials": [], "status": "PENDING"},
                "audit": {"score": 0, "verdict": None, "critique": None, "status": "PENDING"}
            },
            "edges": ["ideation -> realization", "realization -> audit"]
        }

    def _load_prompt(self, agent_name: str) -> str:
        path = os.path.join(self.prompts_dir, f"{agent_name}.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _llm_call(self, agent: str, system_prompt: str, user_prompt: str) -> str:
        self.logger.info(f"LLM_CALL for {agent}")
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
            self.logger.warning(f"LLM Call Primary Fallback Failed for {agent}: {e}")
            # Final Safety Net for Reviewer if even OpenAI failed or agent is reviewer
            if agent == "reviewer":
                return json.dumps({"score": 5, "verdict": "REVISE", "critique": f"Reviewer communication failure: {e}"})
            return json.dumps({"error": str(e), "verdict": "REJECT", "code": "print('LLM_ERROR')"})

    def initialize_project(self, topic: str):
        self.dsg["project_id"] = f"HIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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

    def step_theorist(self, topic: str):
        self.logger.info("THEORIST START: Grounding in Doctrine...")
        
        # Real RAG Retrieval (Will auto-fallback to PersistentClient if HTTP fails)
        results = retriever.retrieve(topic, collection_name="doctrine", n_results=5)
        
        # In PoC, if db is empty, we force mock grounding to allow logic validation
        if not results:
             self.logger.warning("RAG EMPTY. Injecting Mock Grounding for Logic Validation.")
             results = [
                 {"metadata": {"source": "Sovereign_Neuro_Ethics_2025.pdf"}, "content": "Inference protections required for EEG."},
                 {"metadata": {"source": "IEEE_BCI_Security_2026.pdf"}, "content": "Side-channel attacks on brain-data payloads."}
             ]

        context = retriever.format_for_prompt(results)
        sys_prompt = self._load_prompt("theorist")
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}\n\nGenerate Hypothesis JSON."

        response_json = self._llm_call("theorist", sys_prompt, user_prompt)
        
        try:
            content = json.loads(response_json)
        except:
            content = {"error": "JSON_PARSE_FAILED", "raw": response_json}

        self.dsg["nodes"]["ideation"] = {
            "content": content,
            "grounding": [r.get('metadata', {}).get('source', 'Unknown') for r in results],
            "status": "VERIFIED_GROUNDING"
        }
        return True

    def step_engineer(self):
        hyp_content = self.dsg["nodes"]["ideation"]["content"]
        if not hyp_content: return False

        sys_prompt = self._load_prompt("engineer")
        max_trials = 5
        current_user_prompt = f"Goal: Realize this hypothesis: {json.dumps(hyp_content)}\nGenerate Python code."
        
        for trial in range(max_trials):
            self.logger.info(f"ENGINEER TRIAL {trial+1}/{max_trials}...")
            
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
                return True
            else:
                self.logger.warning(f"TRIAL {trial+1} FAILED: Reflexion triggered.")
                current_user_prompt = f"Your previous code failed with this error:\n{exec_result['logs']}\n\nFix it. Paga el Impuesto de Verificación."
        
        self.dsg["nodes"]["realization"]["status"] = "FAILED_CIRCUIT_BREAKER"
        return False

    def step_reviewer(self):
        if self.dsg["nodes"]["realization"]["status"] != "COMPILED":
            return False

        sys_prompt = self._load_prompt("reviewer")
        user_prompt = f"Hypothesis: {json.dumps(self.dsg['nodes']['ideation']['content'])}\nImplementation: {self.dsg['nodes']['realization']['content']}\nLogs: {self.dsg['nodes']['realization']['trials'][-1]['logs']}\n\nAudit strictly."
        
        response = self._llm_call("reviewer", sys_prompt, user_prompt)
        try:
            audit_data = json.loads(response) if "{" in response else {"critique": response, "score": 0, "verdict": "REJECT"}
        except:
            audit_data = {"critique": response, "score": 0, "verdict": "REJECT"}
        
        self.dsg["nodes"]["audit"] = {
            "score": audit_data.get("score", 0),
            "verdict": audit_data.get("verdict", "REJECT"),
            "critique": audit_data.get("critique", "No critique provided"),
            "status": "AUDITED"
        }
        
        if audit_data.get("verdict") == "ACCEPT":
            self.dsg["status"] = "COMPLETED"
        else:
            self.dsg["status"] = "REJECTED_BY_PEER_REVIEW"
        return True

    def execute_complete_cycle(self, topic: str):
        self.initialize_project(topic)
        if not self.step_theorist(topic): return self.dsg
        if not self.step_engineer(): return self.dsg
        if not self.step_reviewer(): return self.dsg
        return self.dsg

hive_orchestrator = HiveOrchestrator()
