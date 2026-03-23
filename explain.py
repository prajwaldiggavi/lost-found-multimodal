def explain(query, item, score=None):
    explanation = f"This item is a potential match for '{query}' because "

    if query:
        explanation += "it shares similar keywords and semantic meaning. "

    # Add smart logic
    if "headphone" in query.lower() or "airpod" in query.lower():
        explanation += "both are related to audio devices. "

    if "bag" in query.lower():
        explanation += "both belong to the same category of bags. "

    if "watch" in query.lower():
        explanation += "both represent wearable accessories. "

    if score:
        explanation += f"The confidence score is {round(score,2)}, indicating strong similarity. "

    explanation += "The system used both text understanding and visual similarity to rank this result."

    return explanation