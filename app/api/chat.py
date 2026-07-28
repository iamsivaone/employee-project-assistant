import uuid
from fastapi import APIRouter

from pydantic import BaseModel

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

from app.agents.supervisor_agent import supervisor_agent

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user: int
    project_name: str
    message: str
    thread_id: str = "1"  # Default thread ID if not provided


@router.post("/stream")
async def chat_stream(payload: ChatRequest):
    """Stream AI agent responses and tool execution updates for user messages.

    Handles real-time chat interactions by executing the supervisor agent and streaming tokens,
    tool call details, and completion signals as newline-delimited JSON (NDJSON).

    Args:
        payload (ChatRequest): Request body containing user details, project name, and user message.

    Returns:
        StreamingResponse: An NDJSON stream (`application/x-ndjson`) emitting events:
            - `token`: Generated response text chunks.
            - `tool_call`: Executed tool calls and their outputs.
            - `done`: Signal indicating stream completion.
    """
    print(f"[chat_stream] Received payload: {payload}")
    query = payload.message
    thread_id = str(uuid.uuid4())

    async def event_generator():
        """Async generator that streams supervisor agent events as JSON lines.

        Yields:
            str: Newline-terminated JSON strings representing text tokens, tool call executions, or stream completion.
        """
        thread_config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        stream = supervisor_agent.stream_events(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            f"Current authenticated user_id={payload.user}. "
                            f"Current project={payload.project_name}. "
                            "Always use these values when calling the `check_project_access` tool."
                        ),
                    },
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
            config=thread_config,
            version="v3",
        )
        print(
            f"[chat_stream] Streaming events for query: {query} with thread_id: {thread_id}"
        )

        for kind, item in stream.interleave("messages", "tool_calls"):

            if kind == "messages":
                for token in item.text:
                    yield json.dumps(
                        {
                            "type": "token",
                            "content": token,
                        }
                    ) + "\n"

            elif kind == "tool_calls":
                yield json.dumps(
                    {
                        "type": "tool_call",
                        "tool": item.tool_name,
                        "input": item.input,
                        "output": item.output,
                    }
                ) + "\n"

        yield json.dumps({"type": "done"}) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
    )
