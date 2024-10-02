from pydantic import BaseModel
from typing import List


class RecipeGenerationRequest(BaseModel):
    """
        Request model for generating a recipe based on user input.

        Attributes:
            amountOfPersons (int): The number of people the recipe should serve.
            dishType (str): The type of dish requested (e.g., pasta, salad, soup).
            maxCooking (int): The maximum cooking time allowed in minutes.
            allergieList (List[str]): A list of allergies that the recipe should avoid (e.g., gluten, nuts).
            dietRequirements (List[str]): A list of dietary requirements (e.g., vegetarian, keto).
            cuisineList (List[str]): A list of preferred cuisines (e.g., Italian, Mediterranean, Asian).
            outputDataFormat (str): The expected format of the recipe output, which includes details like ingredients,
                                    tools required, and step-by-step instructions in JSON format.
    """
    amountOfPersons: int
    dishType: str
    maxCooking: int
    allergieList: List[str]
    dietRequirements: List[str]
    cuisineList: List[str]
    outputDataFormat: str
