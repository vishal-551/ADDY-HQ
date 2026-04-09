from __future__ import annotations

import httpx

from shared.config import get_settings


class AIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def summarize(self, text: str, max_words: int = 120) -> str:
        tokens = text.split()
        if len(tokens) <= max_words:
            return text
        return " ".join(tokens[:max_words]) + "..."

    async def moderate(self, text: str) -> dict[str, bool]:
        flagged_words = {"scam", "phishing", "malware"}
        lowered = text.lower()
        return {"flagged": any(w in lowered for w in flagged_words)}

    async def health(self) -> dict[str, str]:
        if not self.settings.openai_api_key:
            return {"provider": "offline", "status": "disabled_no_key"}
        async with httpx.AsyncClient(timeout=self.settings.ai_request_timeout) as client:
            response = await client.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {self.settings.openai_api_key}"})
            return {"provider": "openai", "status": "ok" if response.status_code < 400 else "degraded"}
