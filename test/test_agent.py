import sys
print(sys.path)

from app.agents.coordinator import agent

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                """
Employee:
Employee A

Project:
Project Alpha

Question:

What is the deadline?
"""
            }
        ]
    }
)

print(response)