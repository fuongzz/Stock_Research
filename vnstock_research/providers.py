from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ResearchNarrator(Protocol):
    def narrate(self, prompt: str) -> str: ...


@dataclass
class DisabledProvider:
    """Default provider: guarantees the quantitative pipeline has no API dependency."""
    def narrate(self, prompt: str) -> str:
        return "LLM provider disabled; use the machine-readable experiment report."


class OpenAIProvider:
    def __init__(self, client):
        self.client = client

    def narrate(self, prompt: str) -> str:
        response = self.client.responses.create(model="gpt-5", input=prompt)
        return response.output_text


class ClaudeProvider:
    def __init__(self, client, model: str):
        self.client, self.model = client, model

    def narrate(self, prompt: str) -> str:
        message = self.client.messages.create(model=self.model, max_tokens=1200, messages=[{"role": "user", "content": prompt}])
        return message.content[0].text

