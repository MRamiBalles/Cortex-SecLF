from typing import Dict, Any

class PeerReviewer:
    def __init__(self):
        pass

    def review_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Acts as the 'Critic' agent in the Multi-Agent System.
        """
        hypothesis = research_data.get("hypothesis", {})
        result = research_data.get("result", {})

        # Simulated Logic of a Reviewer LLM
        score = 0
        comments = []

        # 1. Check Novelty
        if "latency" in hypothesis.get("statement", "").lower():
            score += 3
            comments.append("Topic is relevant to current performance metrics.")
        
        # 2. Check Correctness
        if result.get("success"):
            score += 4
            comments.append("Experiment executed successfully.")
        else:
            comments.append("Experiment failed to execute.")

        # 3. Decision
        decision = "REJECT"
        if score >= 6:
            decision = "ACCEPT"
        elif score >= 4:
            decision = "REVISE"

        return {
            "decision": decision,
            "score": f"{score}/10",
            "comments": comments,
            "publication_ready": decision == "ACCEPT"
        }

peer_reviewer = PeerReviewer()
