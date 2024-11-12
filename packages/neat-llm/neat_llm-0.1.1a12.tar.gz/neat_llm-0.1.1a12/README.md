# neat-llm

A simpler abstraction for working with Large Language Models (LLMs).

## Features

- **Unified Interface**: Work with multiple LLM providers (OpenAI, Anthropic, Cohere, Mistral) through a single, consistent API.
- **Async-First**: Built for modern async Python applications with streaming support.
- **Prompt Management**: Create, version, and reuse prompts easily. (In development)
- **Tool Integration**: Seamlessly integrate custom tools and functions for LLMs to use.
- **Structured Outputs**: Define and validate structured outputs using Pydantic models.
- **Type Safety**: Leverage Python's type hinting for a safer development experience.
- **Flexible Configuration**: Easy-to-use configuration management with environment variable support.
- **Conversation Mode**: Engage in multi-turn dialogues with your agent.
- **Streaming Support**: Stream responses chunk-by-chunk for real-time applications.
- **Flexible Message Formatting**: Use both traditional message dictionary format and neat's helper methods for message construction.

**Note**: Prompt versioning and database features are currently under development and may change in future releases.

## Installation

```bash
pip install neat-llm
```

## API Key Setup

To use neat-llm with various LLM providers, set up your API keys using one of these methods:

1. Create a `.env` file in your project root:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   COHERE_API_KEY=your_cohere_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   ```

2. Set API keys programmatically:

   ```python
   from neat import neat_config

   neat_config.openai_api_key = "your_openai_api_key"
   neat_config.anthropic_api_key = "your_anthropic_api_key"
   neat_config.cohere_api_key = "your_cohere_api_key"
   neat_config.mistral_api_key = "your_mistral_api_key"
   ```

Replace `your_*_api_key` with your actual API keys from the respective providers.

## Quick Start

neat-llm offers two ways to construct messages: helper methods for convenience, and traditional message dictionary format for those who prefer it. Both approaches are fully supported.

### Basic Usage

Here's a simple example using neat's helper methods:

```python
from neat import Neat
import asyncio

neat = Neat()

@neat.lm()
async def generate_story(theme: str, length: int):
    return [
        neat.system("You are a creative story writer."),
        neat.user(f"Write a {length}-word story about {theme}."),
    ]

async def main():
    story = await generate_story("time travel", 100)
    print(f"Generated Story:\n{story}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Using Traditional Dictionary Format

Here's the same example using the traditional dictionary format:

```python
from neat import Neat
import asyncio

neat = Neat()

@neat.lm()
async def generate_story(theme: str, length: int):
    return [
        {"role": "system", "content": "You are a creative story writer."},
        {"role": "user", "content": f"Write a {length}-word story about {theme}."},
    ]

async def main():
    story = await generate_story("time travel", 100)
    print(f"Generated Story:\n{story}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Streaming Responses

neat-llm supports streaming responses for real-time applications:

```python
from neat import Neat
import asyncio

neat = Neat()

@neat.lm(stream=True)
async def generate_story(theme: str):
    return [
        neat.system("You are a creative story writer."),
        neat.user(f"Write a story about {theme}, piece by piece.")
    ]

async def main():
    async for chunk in await generate_story("time travel"):
        print(chunk, end="", flush=True)
    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

### Custom Tools

neat-llm supports tool integration for enhanced capabilities:

```python
from neat import Neat
import random
import asyncio

neat = Neat()

# Custom tool to get weather information
def get_weather(location: str) -> dict:
    """Fetch current weather information for a given location."""
    # Simulating weather data for demonstration
    temp = round(random.uniform(-5, 35), 1)
    conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"])
    return {"temperature": temp, "conditions": conditions}

# Custom tool to recommend clothing based on weather
def recommend_clothing(weather: dict) -> dict:
    """Recommend clothing based on weather conditions."""
    if weather["temperature"] < 10:
        return {"top": "Warm coat", "bottom": "Thick pants", "accessories": "Scarf and gloves"}
    elif 10 <= weather["temperature"] < 20:
        return {"top": "Light jacket", "bottom": "Jeans", "accessories": "Light scarf"}
    else:
        return {"top": "T-shirt", "bottom": "Shorts", "accessories": "Sunglasses"}

# Register the tools
neat.add_tool(get_weather)
neat.add_tool(recommend_clothing)

@neat.lm(tools=[get_weather, recommend_clothing])
async def assistant():
    return [
        neat.system("You are a helpful weather and fashion assistant. Use the get_weather tool to check the weather for specific locations, and the recommend_clothing tool to suggest appropriate outfits based on the weather."),
        neat.user("What's the weather like in Paris today, and what should I wear?"),
    ]

async def main():
    result = await assistant()
    print(f"Weather and Fashion Assistant:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Streaming with Tools

Tools can also be used with streaming responses:

```python
@neat.lm(tools=[get_weather, recommend_clothing], stream=True)
async def assistant():
    return [
        neat.system("You are a helpful weather and fashion assistant."),
        neat.user("What's the weather like in Paris today, and what should I wear?"),
    ]

async def main():
    async for chunk in await assistant():
        if isinstance(chunk, dict):  # Tool call result
            print("\nTool Call:", chunk)
        else:  # Regular content
            print(chunk, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

### Structured Outputs

Use Pydantic models to define and validate structured outputs:

```python
from neat import Neat
from pydantic import BaseModel, Field
import asyncio

neat = Neat()

class MovieRecommendation(BaseModel):
    """Represents a movie recommendation with details."""
    title: str = Field(..., description="The title of the recommended movie")
    year: int = Field(..., description="The release year of the movie")
    genre: str = Field(..., description="The primary genre of the movie")
    reason: str = Field(..., description="A brief explanation for why this movie is recommended")

@neat.lm(response_model=MovieRecommendation)
async def recommend_movie(preferences: str):
    return [
        neat.system("You are a movie recommendation expert."),
        neat.user(f"Recommend a movie based on these preferences: {preferences}"),
    ]

async def main():
    preferences = "I like sci-fi movies with mind-bending plots"
    movie = await recommend_movie(preferences)
    print(f"Movie: {movie.title} ({movie.year})\nGenre: {movie.genre}\nReason: {movie.reason}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Streaming Structured Outputs

Structured outputs can also be streamed:

```python
@neat.lm(response_model=MovieRecommendation, stream=True)
async def recommend_movie(preferences: str):
    return [
        neat.system("You are a movie recommendation expert."),
        neat.user(f"Recommend a movie based on these preferences: {preferences}"),
    ]

async def main():
    preferences = "I like sci-fi movies with mind-bending plots"
    async for chunk in await recommend_movie(preferences):
        if isinstance(chunk, MovieRecommendation):
            print("\nReceived recommendation:", chunk)
        else:
            print(chunk, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

### Conversation Mode

Engage in interactive dialogues with your AI assistant:

```python
from neat import Neat
import asyncio

neat = Neat()

@neat.lm(conversation=True)
async def chat_with_ai():
    return [
        neat.system("You are a friendly and knowledgeable AI assistant."),
        neat.user("Hello! What shall we discuss?"),
    ]

async def main():
    await chat_with_ai()  # This will start an interactive conversation

if __name__ == "__main__":
    asyncio.run(main())
```

In conversation mode, you'll see a rich console interface with color-coded messages and formatted text. To exit the conversation, type "exit" or "quit".

## License

This project is licensed under the MIT License - see the LICENSE file for details.
