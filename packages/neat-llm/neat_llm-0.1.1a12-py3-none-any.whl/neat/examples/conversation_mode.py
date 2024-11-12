"""
Example of a conversational AI interface.
"""

import asyncio

from neat import Neat

neat = Neat()

@neat.lm(conversation=True)
async def chat():
    """Start an interactive chat session with the AI."""
    neat.system(
            "You are a friendly and knowledgeable AI assistant. Engage in a conversation with the user, answering their questions and providing helpful information."
    )
    neat.user(
        "Hello! I'd like to chat about various topics. What shall we discuss?"
    )

if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(chat())
