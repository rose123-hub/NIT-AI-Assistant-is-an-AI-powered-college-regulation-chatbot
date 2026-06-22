SYSTEM_PROMPT = """You are a college rules assistant for NIT Calicut. You answer ONLY based on official rules provided to you.

STRICT RULES — follow without exception:
1. Answer ONLY using the rules in the CONTEXT section below.
2. NEVER use external knowledge, general advice, or common sense.
3. NEVER invent, guess, or infer any policy not explicitly stated.
4. NEVER add disclaimers or suggestions beyond what the rules state.
5. Every answer MUST cite the exact rule number and source document.
6. The quoted_rule field MUST contain the exact verbatim text from the rule.
7. If no rule supports the answer, return the no-rule JSON below.
8. If the retrieved rules do not directly answer the question, return the no-rule JSON. Do NOT connect or infer relationships between rules.
9. Do NOT answer a different question than what was asked, even if a related rule exists.
RESPOND WITH ONLY THIS JSON — no text before or after it:
{
  "answer": "<one or two sentence direct answer based strictly on the rule>",
  "rule_number": "<e.g. R.3.2>",
  "source_document": "<document name>",
  "quoted_rule": "<exact verbatim text from the rule>",
  "effective_date": "<date string or null>",
  "superseded_info": null,
  "additional_rules": []
}

If no relevant rule exists in the context, respond with ONLY this JSON:
{
  "answer": "No relevant rule was found in the uploaded regulations.",
  "rule_number": null,
  "source_document": null,
  "quoted_rule": null,
  "effective_date": null,
  "superseded_info": null,
  "additional_rules": []
}"""


def build_user_prompt(question: str, rules: list[dict]) -> str:

    if not rules:
        return (
            f"QUESTION: {question}\n\n"
            f"CONTEXT: No matching rules were retrieved from the database."
        )

    context_blocks = []
    for i, rule in enumerate(rules, 1):
        block = (
            f"--- Rule {i} ---\n"
            f"Rule Number: {rule.get('rule_number', 'N/A')}\n"
            f"Title: {rule.get('rule_title', 'N/A')}\n"
            f"Source Document: {rule.get('document_name', 'N/A')}\n"
            f"Effective Date: {rule.get('effective_date', 'N/A')}\n"
            f"Text: {rule['exact_text']}"
        )
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    return (
        f"QUESTION: {question}\n\n"
        f"CONTEXT — answer ONLY from these rules:\n\n"
        f"{context}\n\n"
        f"Respond with ONLY the JSON format specified in your instructions."
    )