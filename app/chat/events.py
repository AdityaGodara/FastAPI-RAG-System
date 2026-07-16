import json


def sse_event(event: str, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"