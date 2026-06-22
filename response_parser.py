import json
import re
import logging
from app.schemas.chat import ChatResponse

logger = logging.getLogger(__name__)

NO_RULE_RESPONSE = ChatResponse(
    answer="No relevant rule was found in the uploaded regulations.",
    rule_number=None,
    source_document=None,
    quoted_rule=None,
    effective_date=None,
    superseded_info=None,
    additional_rules=[],
)


def parse_llm_response(raw: str) -> ChatResponse:

    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()

    # Extract first JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        logger.warning(f"No JSON found in LLM response: {raw[:300]}")
        return NO_RULE_RESPONSE

    try:
        data = json.loads(match.group())
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse failed: {e} | raw: {raw[:300]}")
        return NO_RULE_RESPONSE

    # If LLM explicitly said no rule found
    answer = data.get("answer", "")
    if "no relevant rule" in answer.lower():
        return NO_RULE_RESPONSE

    # If rule_number missing, treat as no rule found
    if not data.get("rule_number"):
        return NO_RULE_RESPONSE

    try:
        return ChatResponse(**data)
    except Exception as e:
        logger.warning(f"ChatResponse build failed: {e} | data: {data}")
        return NO_RULE_RESPONSE