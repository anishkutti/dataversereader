import json


def extract_reaction_feedback(content_json, reactions_to_extract=None):
    """
    Extracts feedback for specified reactions from conversation activities.

    Args:
        content_json (str, bytes, bytearray, or dict): The JSON content of the conversation.
            Can be a JSON string or an already parsed dictionary.
        reactions_to_extract (list, optional): List of reaction types to extract (e.g., ['dislike', 'like']).
            If None, defaults to ['dislike', 'like'].

    Returns:
        list: A list of dictionaries containing reaction details, each with keys:
            - 'reaction': The type of reaction (e.g., 'dislike' or 'like').
            - 'feedbackText': The feedback text provided by the user.
            - 'user_aadObjectId': The Azure AD Object ID of the user.
            - 'timestamp': The timestamp of the activity.

    Raises:
        TypeError: If content_json is not a valid type.
        json.JSONDecodeError: If content_json is a string but not valid JSON.
    """
    if reactions_to_extract is None:
        reactions_to_extract = ['dislike', 'like']

    # Parse JSON if necessary
    if isinstance(content_json, (str, bytes, bytearray)):
        data = json.loads(content_json)
    elif isinstance(content_json, dict):
        data = content_json
    else:
        raise TypeError("content_json must be a JSON string or a dict")

    results = []

    # Iterate through each activity in the conversation
    for activity in data.get("activities", []):
        # Check if the activity is an invoke action for message submission
        if activity.get("type") == "invoke" and activity.get("name") == "message/submitAction":

            # Extract the action value
            value = activity.get("value", {})
            action = value.get("actionValue", {})

            reaction = action.get("reaction")

            # If the reaction matches one we're interested in
            if reaction in reactions_to_extract:
                # Extract feedback text
                feedback_text = (
                    action.get("feedback", {})
                    .get("feedbackText")
                )

                # Collect the reaction details
                results.append({
                    "reaction": reaction,
                    "feedbackText": feedback_text,
                    "user_aadObjectId": activity.get("from", {}).get("aadObjectId"),
                    "timestamp": activity.get("timestamp")
                })

    return results