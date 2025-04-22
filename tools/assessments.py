from griptape.tools import BaseTool
from pydantic import Field
from typing import List
from griptape.utils.decorators import activity

from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from griptape.artifacts import TextArtifact
from schema import Schema      # lightweight runtime‑validation lib

class HollandTool(BaseTool):
    @activity(
        config={
            "description": "Return a 3‑letter Holland (RIASEC) code from 60 ratings (1‑5).",
            # list of exactly 60 integers
            "schema": Schema({"answers": [int]}),
        }
    )
    def score(self, answers: list[int]) -> TextArtifact:
        if len(answers) != 60:
            raise ValueError("Need 60 ratings, one for each RIASEC item.")

        dims = "RIASEC"
        bucket = {d: 0 for d in dims}
        for i, rating in enumerate(answers):
            bucket[dims[i % 6]] += rating

        code = "".join(sorted(dims, key=lambda d: -bucket[d])[:3])
        return TextArtifact(code)

class WorkValuesTool(BaseTool):
    @activity(
        config={
            "description": "Ranks the 6 Schein work‑value clusters.",
            "schema": Schema({"answers": [str]}),   # 30 letters A‑F
        }
    )
    def score(self, answers: list[str]) -> TextArtifact:
        from collections import Counter
        clusters = ["A", "I", "R", "L", "S", "W"]   # whatever mapping you use
        tally = Counter(answers)
        top3 = sorted(clusters, key=lambda c: -tally[c])[:3]
        return TextArtifact(",".join(top3))


# class HollandTool(BaseTool):
#     """Scores 6 RIASEC dimensions from user‑rated activities."""
    
#     class ScoreArgs(BaseTool.Args):
#         answers: list[int] = Field(..., description="List of 60 Likert ratings 1‑5")

#     @activity(outputs=["holland_code"])
#     def score(self, args: ScoreArgs):
#         # Very trimmed pseudo‑scoring
#         dims = ["R","I","A","S","E","C"]
#         buckets = {k: 0 for k in dims}
#         for i, a in enumerate(args.answers):
#             buckets[dims[i % 6]] += a
#         code = "".join(sorted(dims, key=lambda d: buckets[d], reverse=True)[:3])
#         return {"holland_code": code}

# # Wrap external APIs for job matches
# from griptape.tools import RestApiTool

# onet_tool = RestApiTool(
#     base_url="https://services.onetcenter.org", 
#     authorization="Basic <API_KEY>"
# )
