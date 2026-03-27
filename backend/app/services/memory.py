# sessions = {}


# def add_message(session_id, role, content):

#     if session_id not in sessions:
#         sessions[session_id] = []

#     sessions[session_id].append({
#         "role": role,
#         "content": content
#     })


# def get_history(session_id):

#     if session_id not in sessions:
#         return []

#     return sessions[session_id][-6:]

from app.core.logger import logger

sessions = {}

def add_message(session_id: str, role: str, content: str):
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append({
        "role": role,
        "content": content
    })
    logger.debug(f"Added {role} message to session {session_id}")

def get_history(session_id: str):
    if session_id not in sessions:
        return []
    # Return last 6 messages for context
    return sessions[session_id][-6:]