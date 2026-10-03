from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.knowledge.extraction.knowledge_extraction import (
    extract_knowledge
)


def extract_knowledge_from_document(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    print(
        f"\nDocument split into {len(chunks)} chunks."
    )

    all_entities = []
    all_claims = []
    all_requirements = []
    all_relationships = []
    all_warnings = []

    for index, chunk in enumerate(chunks):

        print(
            f"\nProcessing chunk "
            f"{index + 1}/{len(chunks)} "
            f"({len(chunk)} characters)"
        )

        result = extract_knowledge(chunk)

        all_entities.extend(
            result.get("entities", [])
        )

        all_claims.extend(
            result.get("claims", [])
        )

        all_requirements.extend(
            result.get("requirements", [])
        )

        all_relationships.extend(
            result.get("relationships", [])
        )

        all_warnings.extend(
            result.get("warnings", [])
        )

    return {
        "entities": all_entities,
        "claims": all_claims,
        "requirements": all_requirements,
        "relationships": all_relationships,
        "warnings": all_warnings
    }