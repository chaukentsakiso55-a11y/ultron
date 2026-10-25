"""Reviewable learning and improvement proposals for ULTRON."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

class EvolutionEngine:
    def __init__(self, storage: str | Path):
        self.storage = Path(storage)

    def _load(self):
        if not self.storage.exists():
            return {"feedback": [], "proposals": []}
        data = json.loads(self.storage.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("feedback"), list) or not isinstance(data.get("proposals"), list):
            raise ValueError("Invalid evolution data")
        return data

    def _save(self, data):
        self.storage.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.storage.with_suffix(self.storage.suffix + ".tmp")
        temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        temporary.replace(self.storage)

    def record_feedback(self, task: str, lesson: str, rating: int):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be 1 through 5")
        if not task.strip() or not lesson.strip():
            raise ValueError("Task and lesson are required")
        data = self._load()
        item = {"id": str(uuid4()), "task": task[:500], "lesson": lesson[:2000], "rating": rating,
                "created_at": datetime.now(timezone.utc).isoformat()}
        data["feedback"].append(item)
        self._save(data)
        return item

    def propose_improvement(self, title: str, rationale: str, test_plan: str):
        if not all(x.strip() for x in (title, rationale, test_plan)):
            raise ValueError("Title, rationale, and test plan are required")
        data = self._load()
        proposal = {"id": str(uuid4()), "title": title[:200], "rationale": rationale[:2000],
                    "test_plan": test_plan[:2000], "status": "pending_review",
                    "created_at": datetime.now(timezone.utc).isoformat()}
        data["proposals"].append(proposal)
        self._save(data)
        return proposal

    def list_pending(self):
        return [p for p in self._load()["proposals"] if p["status"] == "pending_review"]

    def review(self, proposal_id: str, approved: bool):
        data = self._load()
        for proposal in data["proposals"]:
            if proposal["id"] == proposal_id:
                if proposal["status"] != "pending_review":
                    raise ValueError("Proposal already reviewed")
                proposal["status"] = "approved_for_manual_implementation" if approved else "rejected"
                self._save(data)
                return proposal
        raise KeyError(proposal_id)
