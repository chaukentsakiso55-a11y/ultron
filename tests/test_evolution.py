import tempfile
import unittest
from pathlib import Path
from ultron.evolution import EvolutionEngine

class EvolutionTests(unittest.TestCase):
    def test_feedback_and_review(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = EvolutionEngine(Path(directory) / "memory.json")
            feedback = engine.record_feedback("Summarize", "Use shorter answers", 4)
            self.assertEqual(feedback["rating"], 4)
            proposal = engine.propose_improvement("Improve summaries", "Feedback suggests brevity", "Compare sample outputs")
            self.assertEqual(len(engine.list_pending()), 1)
            result = engine.review(proposal["id"], True)
            self.assertEqual(result["status"], "approved_for_manual_implementation")
            self.assertEqual(engine.list_pending(), [])

    def test_reject_invalid_rating(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                EvolutionEngine(Path(directory) / "memory.json").record_feedback("a", "b", 6)

if __name__ == "__main__":
    unittest.main()
