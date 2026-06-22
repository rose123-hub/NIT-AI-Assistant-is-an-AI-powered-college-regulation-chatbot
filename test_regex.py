from app.ingestion.pdf_extractor import extract_text_with_layout
from app.ingestion.rule_parser import parse_rules

pages = extract_text_with_layout(
    "data/uploads/ordinances-and-regulations-2023.pdf"
)

rules = parse_rules(pages)

print("Total rules:", len(rules))

for rule in rules[:5]:
    print("\n" + "=" * 60)
    print(rule["rule_number"])
    print(rule["rule_title"])
    print(rule["exact_text"][:300])