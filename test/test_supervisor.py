from app.agents.supervisor_agent import supervisor_agent

thread_config = {"configurable": {"thread_id": "1"}}

query = "what is multi-agent employee system?"

stream = supervisor_agent.stream_events(
    {"messages": [{"role": "user", "content": query}]},
    config=thread_config,
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        print(f"Tool result: {item.output}")
        
# from langchain.messages import AIMessage, HumanMessage

# # streaming the events and printing the latest message content
# for snapshot in stream.values:
#     # Each snapshot contains the full state at that point
#     latest_message = snapshot["messages"][-1]
#     if latest_message.content:
#         if isinstance(latest_message, HumanMessage):
#             print(f"User: {latest_message.content}")
#         elif isinstance(latest_message, AIMessage):
#             print(f"Agent: {latest_message.content}")
#     elif latest_message.tool_calls:
#         print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")