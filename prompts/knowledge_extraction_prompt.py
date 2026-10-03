def get_knowledge_extraction_prompt(text):

    return f"""
You are a high-recall technical knowledge extraction system for Aegis HCS documentation.

Your goal is to extract ALL explicitly stated technical information from the provided text.
Do not summarize the document. Do not extract only the most important facts.
Preserve every relevant fact that could be useful for answering technical questions later.

Extract the following:

1. Technical entities
2. Factual claims
3. Explicit relationships
4. Operational requirements and procedures
5. Warnings, restrictions, prohibitions, and exceptions

IMPORTANT:
A fact must not be lost merely because it appears inside:
- a procedure
- a warning
- a note
- a table
- a list
- a diagram description
- a configuration entry
- a revision note
- a condition
- an exception
- a sentence containing "must", "must not", "only", "before", "after",
  "if", "when", "unless", "except", "required", or "prohibited"

Rules:

- Extract only information explicitly present in the text.
- Do not invent or infer information.
- Do not use outside knowledge.
- Preserve exact identifiers, names, values, units, dates, revisions,
  component names, alarm IDs, sensor IDs, and configuration keys.
- Do not merge similar identifiers.
  For example, PS-04, PS-04A, and PS-40 must remain separate entities.
- Do not perform entity resolution.
- Do not resolve contradictions between sources.
- Preserve conditions, scope, applicability, exceptions, and limitations.
- Preserve whether a statement is a requirement, prohibition, warning,
  recommendation, measurement, limit, or ordinary fact.
- Preserve version/revision information whenever present.
- Preserve temporal information such as "before revision 3.2",
  "after revision 3.2", or "effective from [date]".
- Preserve configuration-specific or model-specific applicability.
- If the entity type is unclear, use "unknown".
- Do not convert absence of information into a negative statement.
- Extract information even if it appears only once.
- Do not discard apparently minor technical facts.
- If the same fact appears multiple times in the supplied text, it may be
  represented multiple times if the surrounding conditions or context differ.
- Keep the original meaning of the source text.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations.

ENTITY FORMAT:

{{
    "name": "PS-04A",
    "type": "pressure_sensor"
}}

CLAIM FORMAT:

{{
    "subject": "HPU",
    "predicate": "normal_operating_pressure",
    "value": "200 bar",
    "conditions": [
        "software revision 3.2"
    ],
    "scope": "Aegis Series-7 HCS",
    "source_text": "The normal operating pressure is 200 bar for software revision 3.2."
}}

REQUIREMENT FORMAT:

{{
    "subject": "Hydraulic Power Unit",
    "action": "start",
    "requirement": "Isolation valve IV-21 must be OPEN",
    "conditions": [
        "before starting the Hydraulic Power Unit"
    ],
    "source_text": "Before starting the Hydraulic Power Unit, ensure isolation valve IV-21 is OPEN."
}}

RELATIONSHIP FORMAT:

{{
    "source": "PS-04A",
    "relationship": "replaces",
    "target": "PS-04",
    "conditions": [
        "software revision 3.2"
    ],
    "source_text": "PS-04A replaces PS-04 for software revision 3.2."
}}

WARNING / RESTRICTION FORMAT:

{{
    "subject": "controller",
    "type": "prohibition",
    "statement": "Controller must not be reset above the specified pressure limit",
    "conditions": [],
    "source_text": "The controller must not be reset when pressure exceeds the specified limit."
}}

EXTRACTION GUIDANCE:

For every sentence or table/list item, ask:

- Does it identify an entity?
- Does it state a measurable value or technical property?
- Does it state a requirement?
- Does it state something that must or must not happen?
- Does it describe a condition?
- Does it describe an action to take?
- Does it describe an alarm, cause, response, or threshold?
- Does it describe a limit?
- Does it describe compatibility?
- Does it describe a revision or change?
- Does it describe when something became effective?
- Does it describe a relationship between components?
- Does it describe location, calibration interval, temperature limit,
  pressure limit, voltage, current, or other technical specification?
- Does it identify an exception or scope?
- Does it contain information needed to distinguish similar identifiers?

If yes, extract it.

Return exactly this structure:

{{
    "entities": [],
    "claims": [],
    "requirements": [],
    "relationships": [],
    "warnings": []
}}

DOCUMENT TEXT:
{text}
"""


def get_knowledge_extraction_retry_prompt(text):

    return f"""
You are performing a second-pass technical knowledge extraction.

The previous extraction may have missed important information.

Extract ALL explicitly stated technical information from the text below.

Focus especially on:

- operational requirements
- procedures
- conditions
- warnings
- prohibitions
- exceptions
- alarm meanings
- alarm causes
- alarm responses
- thresholds and limits
- pressure values
- temperature values
- voltage/current values
- calibration intervals
- component locations
- component identifiers
- sensor identifiers
- configuration parameters
- software revisions
- revision dates
- changes between revisions
- compatibility statements
- "must" / "must not" statements
- "before" / "after" conditions
- "if" / "when" / "unless" conditions
- applicability to specific models, configurations, or revisions

Rules:

- Use ONLY information explicitly stated in the text.
- Do not invent information.
- Do not use outside knowledge.
- Preserve exact identifiers.
- Preserve exact values and units.
- Preserve dates and revisions.
- Do not merge similar identifiers.
- Do not resolve contradictions.
- Preserve conditions and scope.
- Preserve the original meaning.
- Include source_text for every extracted claim, requirement,
  relationship, or warning.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not explain your reasoning.

Return exactly:

{{
    "entities": [],
    "claims": [],
    "requirements": [],
    "relationships": [],
    "warnings": []
}}

TEXT:
{text}
"""