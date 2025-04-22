import json
from typing import TYPE_CHECKING, cast

from griptape.drivers.prompt.ollama import OllamaPromptDriver
from griptape.structures import Agent
from griptape.tools import CalculatorTool
from griptape.memory.structure import ConversationMemory
from griptape.rules import Rule, Ruleset, JsonSchemaRule
from griptape.tasks import PromptTask
from griptape.utils import Chat
from griptape.memory.structure import ConversationMemory 
from griptape.structures import Workflow
from griptape.tasks import PromptTask

if TYPE_CHECKING:
    from griptape.artifacts.text_artifact import TextArtifact

from griptape.structures import Agent
from griptape.drivers.prompt.ollama import OllamaPromptDriver
from griptape.rules import Rule
from tools.assessments import HollandTool, WorkValuesTool



driver = OllamaPromptDriver(model="llama3.1")


class Agents:
    def intake_agent() -> Agent():
        return Agent(
            prompt_driver=driver,
            rules=[
                Rule("Collect background, education, and career worries empathically."),
                # Rule("Return JSON keys: education, experience, concerns."),
            ],
        )
    
    def interviewer_agent() -> Agent():
        return Agent(
            prompt_driver=driver,
            rules=[
                Rule("Ask questions about client's background, education, interests, motivations, and aspirations")

            ]
        )

    def interest_agent() -> Agent():
        return Agent(
            prompt_driver=driver,
            tools=[HollandTool()],
            rules=[Rule("If HollandTool is not yet scored, ask concise 60‑item quiz.")]
        )

    def values_agent() -> Agent():
        return Agent(
            prompt_driver=driver,
            tools=[WorkValuesTool()],
            rules=[Rule("If WorkValuesTool is not yet scored, ask 30 paired choices quiz.")]
        )

    def planner_agent() -> Agent():
        return Agent(
            prompt_driver=driver,
            rules=[
                Rule("Combine intake, RIASEC code, and values profile."),
                Rule("Draft 3 career paths, each with ‑ why it fits  ‑ next skills  ‑ first action.")
            ],
        )

