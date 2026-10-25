# ULTRON Evolution Engine

This is an initial local, reviewable learning foundation, not autonomous model training.

## Features
- Store explicit task feedback and lessons in a local JSON file
- Draft improvement proposals with a test plan
- Review and approve or reject proposals
- No code execution, automatic deployment, unrestricted browsing, or silent permission changes

## Example

```python
from ultron.evolution import EvolutionEngine
engine = EvolutionEngine('local/evolution.json')
engine.record_feedback('Summarize a document', 'Use concise headings', 5)
proposal = engine.propose_improvement('Shorter summaries', 'Positive feedback', 'Evaluate 10 example summaries')
print(engine.list_pending())
engine.review(proposal['id'], approved=True)
```

Approval marks a proposal for **manual implementation** only. It never executes or modifies code.

## Test
`python -m unittest discover -s tests`

Store private memory outside the public repository. Do not save secrets in feedback.
