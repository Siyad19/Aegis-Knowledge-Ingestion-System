import json

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

KB_PATH = "processed/knowledge/knowledge_base.json"


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

with open(KB_PATH, "r", encoding="utf-8") as f:
    kb = json.load(f)


# ============================================================
# IMPORTANT TERMS
# ============================================================

IMPORTANT_TERMS = [

    # Component identifiers
    "ps-04",
    "ps-04a",
    "ps-40",
    "iv-21",
    "plc-03",
    "a17",

    # Document / engineering identifiers
    "ecn-1042",
    "ecn-1058",
    "aeg-cr-700",
    "aeg-dwg-h01",
    "aeg-dwg-e02",
    "aeg-dwg-w03",

    # Software revision
    "3.2",
    "revision history",
    "effective",
    "effective date",
    "took effect",
    "software revision",

    # Pressure
    "150 bar",
    "180 bar",
    "200 bar",

    # Electrical
    "400v",
    "400 v",
    "3-phase",
    "3 phase",
    "3phase",
    "480:120v",

    # Configuration
    "sensor_ps04a_threshold_bar",

    # Technical terms
    "hpu",
    "hcs controller",
    "hydraulic power unit",
    "pressure sensor",
    "voltage sensor",
    "isolation valve",
    "calibration",
    "mean time between failures",
    "mtbf",

    # General technical terms
    "change",
    "changed",
    "date",
]


# ============================================================
# QUERY INTENT
# ============================================================

def detect_query_intent(query):

    query_lower = query.lower()

    warning_terms = [
        "warning",
        "danger",
        "caution",
        "prohibited",
        "must not",
        "do not",
        "cannot"
    ]

    requirement_terms = [
        "must",
        "must be",
        "required",
        "requirement",
        "before",
        "after",
        "prior to",
        "when",
        "if",
        "condition",
        "conditions",
        "start",
        "starting",
        "startup",
        "reset"
    ]

    if any(
        term in query_lower
        for term in warning_terms
    ):
        return "warning"

    if any(
        term in query_lower
        for term in requirement_terms
    ):
        return "requirement"

    return "general"


# ============================================================
# KEYWORD SEARCH
# ============================================================

def keyword_search(query, top_k=10):

    query_words = query.lower().split()

    results = []

    for item_type in [
        "claims",
        "requirements",
        "warnings",
        "entities",
        "relationships"
    ]:

        for item in kb[item_type]:

            text = json.dumps(
                item,
                ensure_ascii=False
            ).lower()

            score = 0

            for word in query_words:

                if len(word) >= 2 and word in text:
                    score += 1

            if score > 0:

                results.append(
                    (
                        score,
                        item_type,
                        item
                    )
                )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# GET IMPORTANT TERMS FROM QUERY
# ============================================================

def get_query_terms(query):

    query_lower = query.lower()

    found_terms = []

    for term in IMPORTANT_TERMS:

        if term in query_lower:

            found_terms.append(term)

    return found_terms


# ============================================================
# EXACT SEARCH
# ============================================================

def exact_search(query, top_k=10):

    query_lower = query.lower()

    query_terms = get_query_terms(query)

    results = []

    for item_type in [
        "claims",
        "requirements",
        "warnings",
        "entities",
        "relationships"
    ]:

        for item in kb[item_type]:

            text = json.dumps(
                item,
                ensure_ascii=False
            ).lower()

            score = 0

            matched_terms = []

            for term in query_terms:

                if term in text:

                    score += 10

                    matched_terms.append(term)

            if score > 0:

                results.append({

                    "score": score,

                    "type": item_type,

                    "item": item,

                    "method": "exact",

                    "matched_terms": matched_terms

                })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# GET ALL KNOWLEDGE ITEMS
# ============================================================

def get_all_items():

    items = []

    # Claims
    for claim in kb["claims"]:

        items.append(
            (
                "claims",
                claim
            )
        )

    # Requirements
    for requirement in kb["requirements"]:

        items.append(
            (
                "requirements",
                requirement
            )
        )

    # Warnings
    for warning in kb["warnings"]:

        items.append(
            (
                "warnings",
                warning
            )
        )

    # Entities
    for entity in kb["entities"]:

        items.append(
            (
                "entities",
                entity
            )
        )

    # Relationships
    for relationship in kb["relationships"]:

        items.append(
            (
                "relationships",
                relationship
            )
        )

    return items


# ============================================================
# BUILD VECTOR INDEX
# ============================================================

items = get_all_items()

texts = [

    json.dumps(
        item,
        ensure_ascii=False
    )

    for _, item in items
]


print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


print(
    f"Creating embeddings for {len(texts)} knowledge items..."
)

embeddings = model.encode(
    texts,
    normalize_embeddings=True
)

embeddings = np.array(
    embeddings,
    dtype="float32"
)


index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

index.add(embeddings)


print("Vector index ready.")


# ============================================================
# VECTOR SEARCH
# ============================================================

def vector_search(query, top_k=10):

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    scores, indexes = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, i in zip(
        scores[0],
        indexes[0]
    ):

        item_type, item = items[i]

        results.append(
            (
                float(score),
                item_type,
                item
            )
        )

    return results


# ============================================================
# HYBRID SEARCH
#
# Combines:
#   1. Exact search
#   2. Keyword search
#   3. Vector search
#
# Also considers:
#   - Query intent
#   - Requirements
#   - Warnings
# ============================================================

def hybrid_search(query, top_k=10):

    # ----------------------------------------
    # Detect query intent
    # ----------------------------------------

    query_intent = detect_query_intent(query)

    print(
        f"\nQuery intent: {query_intent}"
    )

    # ----------------------------------------
    # Run all retrieval methods
    # ----------------------------------------

    exact_results = exact_search(
        query,
        top_k=20
    )

    keyword_results = keyword_search(
        query,
        top_k=20
    )

    vector_results = vector_search(
        query,
        top_k=20
    )

    combined = {}

    # ----------------------------------------
    # Exact results
    # ----------------------------------------

    for result in exact_results:

        key = json.dumps(
            result["item"],
            sort_keys=True,
            ensure_ascii=False
        )

        combined[key] = {

            "score": 10.0,

            "type": result["type"],

            "item": result["item"],

            "method": "exact"

        }

    # ----------------------------------------
    # Keyword results
    # ----------------------------------------

    for score, item_type, item in keyword_results:

        key = json.dumps(
            item,
            sort_keys=True,
            ensure_ascii=False
        )

        if key in combined:

            combined[key]["score"] += 3

            combined[key]["method"] = (
                "exact + keyword"
            )

        else:

            combined[key] = {

                "score": float(score),

                "type": item_type,

                "item": item,

                "method": "keyword"

            }

    # ----------------------------------------
    # Vector results
    # ----------------------------------------

    for score, item_type, item in vector_results:

        key = json.dumps(
            item,
            sort_keys=True,
            ensure_ascii=False
        )

        vector_score = float(score)

        if key in combined:

            combined[key]["score"] += vector_score

            if "keyword" in combined[key]["method"]:

                combined[key]["method"] = (
                    "exact + keyword + vector"
                )

            else:

                combined[key]["method"] = (
                    "exact + vector"
                )

        else:

            combined[key] = {

                "score": vector_score,

                "type": item_type,

                "item": item,

                "method": "vector"

            }

    # ----------------------------------------
    # Convert to list
    # ----------------------------------------

    results = list(
        combined.values()
    )

    # ----------------------------------------
    # Type priority
    #
    # Used only as a tie-breaker.
    # ----------------------------------------

    type_priority = {

        "requirements": 4,

        "warnings": 3,

        "claims": 3,

        "relationships": 2,

        "entities": 1

    }

    # ----------------------------------------
    # Intent-based boosting
    # ----------------------------------------

    for result in results:

        if query_intent == "requirement":

            if result["type"] == "requirements":

                result["score"] += 5

                result["method"] += (
                    " + requirement boost"
                )

            elif result["type"] == "warnings":

                result["score"] += 3

                result["method"] += (
                    " + warning boost"
                )

            elif result["type"] == "claims":

                result["score"] += 1

                result["method"] += (
                    " + claim boost"
                )

        elif query_intent == "warning":

            if result["type"] == "warnings":

                result["score"] += 5

                result["method"] += (
                    " + warning boost"
                )

            elif result["type"] == "requirements":

                result["score"] += 3

                result["method"] += (
                    " + requirement boost"
                )

    # ----------------------------------------
    # Boost direct relationship claims
    # ----------------------------------------

    query_lower = query.lower()

    for result in results:

        item = result["item"]

        if result["type"] == "claims":

            predicate = str(
                item.get(
                    "predicate",
                    ""
                )
            ).lower()

            subject = str(
                item.get(
                    "subject",
                    ""
                )
            ).lower()

            value = str(
                item.get(
                    "value",
                    ""
                )
            ).lower()

            # Direct replacement / supersession
            if (
                "ps-04" in query_lower
                and "ps-04a" in query_lower
                and "ps-04" in subject
                and "ps-04a" in value
                and (
                    "superseded" in predicate
                    or "replaced" in predicate
                    or "replacement" in predicate
                )
            ):

                result["score"] += 10

                result["method"] += (
                    " + direct relationship"
                )

    # ----------------------------------------
    # Sort AFTER all boosts
    # ----------------------------------------

    results.sort(

        key=lambda x: (

            x["score"],

            type_priority.get(
                x["type"],
                0
            )

        ),

        reverse=True

    )

    return results[:top_k]


# ============================================================
# TEST / DEBUG
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nEnter your question: "
    )

    results = hybrid_search(
        question,
        top_k=10
    )

    print(
        "\nRetrieved Evidence:"
    )

    if not results:

        print(
            "\nNo relevant evidence found."
        )

    else:

        for number, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n--- Result {number} ---"
            )

            print(
                f"Score: {result['score']:.3f}"
            )

            print(
                f"Type: {result['type']}"
            )

            print(
                f"Method: {result['method']}"
            )

            print(
                json.dumps(
                    result["item"],
                    indent=2,
                    ensure_ascii=False
                )
            )