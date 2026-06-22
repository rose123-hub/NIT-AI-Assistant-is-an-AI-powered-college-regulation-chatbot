import httpx
import logging
from fastapi import HTTPException
from app.config import OLLAMA_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)


async def ollama_chat(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_p": 1.0,
            "num_predict": 2048,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
    except httpx.ReadTimeout:
        logger.error("Ollama timed out")
        raise HTTPException(503, "The LLM is taking too long. Please try again.")
    except httpx.ConnectError:
        logger.error("Ollama not reachable")
        raise HTTPException(503, "LLM service is not running. Start Ollama.")