"""
Module for getting structured movie recommendations using the Neat framework.
"""

from neat import Neat
from neat.constants import LLMModel
from pydantic import BaseModel, Field


class MovieRecommendation(BaseModel):
    """Represents a movie recommendation with details."""

    title: str = Field(..., description="The title of the recommended movie")
    year: int = Field(..., description="The release year of the movie")
    genre: str = Field(..., description="The primary genre of the movie")
    reason: str = Field(
        ..., description="A brief explanation for why this movie is recommended"
    )


neat = Neat()


@neat.lm(model=LLMModel.MISTRAL_LARGE_LATEST, response_model=MovieRecommendation)
def recommend_movie(preferences: str) -> list:
    """Get a movie recommendation based on user preferences."""
    return [
        neat.system(
            "You are a movie recommendation expert. Provide recommendations based on user preferences."
        ),
        neat.user(f"Recommend a movie based on these preferences: {preferences}"),
    ]


def main() -> None:
    """Run the movie recommendation example."""
    preferences = (
        "I like sci-fi movies with mind-bending plots and strong character development"
    )
    movie = recommend_movie(preferences)

    print(
        f"""
Movie Recommendation:
Title: {movie.title} ({movie.year})
Genre: {movie.genre}
Reason: {movie.reason}
""".strip()
    )


if __name__ == "__main__":
    main()
