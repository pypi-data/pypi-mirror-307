import os
from enum import Enum
from typing import List, Type, Dict, Any
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import instructor
import logging

# Load environment variables
load_dotenv()

# Ensure that the environment variable name matches what is in your .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_structured_output(text_input: str, system_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
    """Generate a response from a user query."""
    try:
        return client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user",
                 "content": f"Use the given format to extract information from the following input: {text_input}."},
                {"role": "system", "content": system_prompt},
            ],
            response_model=response_model,
        )
    except Exception as e:
        logging.error(f"Error creating structured output: {e}")
        return response_model()

# Define Pydantic models
class Range(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class UserModel(BaseModel):
    """UserModel for a simple user"""
    pets: bool
    budget: List[Range]
    smoker: bool
    vegan: bool
    dining_budget: List[Range]


class LocationRange(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class LocationModel(BaseModel):
    """LocationModel for a location"""
    pets: bool
    budget: List[LocationRange]
    smoker: bool
    vegan: bool
    dining_budget: List[LocationRange]


def save_to_versioned_csv(data: pd.DataFrame, base_filename: str):
    """Save DataFrame to a versioned CSV file."""
    version = 1
    filename = f"{base_filename}_v{version}.csv"
    while os.path.exists(filename):
        version += 1
        filename = f"{base_filename}_v{version}.csv"
    data.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")


def generate_data(prompt: str, system_prompt: str, setup: List[List[Any]]) -> List[Dict[str, Any]]:
    """Generate data and return as a list of dictionaries."""
    results = []
    for item in setup:
        result = create_structured_output(text_input=item[0], system_prompt=item[1], response_model=item[2])
        results.append(result.dict())
    return results


def main():
    prompt = "GIVEN all these information, make a test user who is a working student and has a lot of free time, but a small budget"

    user_generation_setup = [["bla", "system_bla", UserModel], ["bla", "system_bla", UserModel],
                             ["bla", "system_bla", UserModel]]
    location_generation_setup = [["bla", "system_bla", LocationModel], ["bla", "system_bla", LocationModel],
                                 ["bla", "system_bla", LocationModel]]

    logging.info("Generating user data...")
    user_results = generate_data(prompt, "system_bla", user_generation_setup)
    logging.info("User data generation complete.")

    logging.info("Generating location data...")
    location_results = generate_data(prompt, "system_bla", location_generation_setup)
    logging.info("Location data generation complete.")

    # Convert results to DataFrames
    user_df = pd.DataFrame(user_results)
    location_df = pd.DataFrame(location_results)

    # Save to versioned CSV
    save_to_versioned_csv(user_df, "user_data")
    save_to_versioned_csv(location_df, "location_data")


if __name__ == "__main__":
    main()
