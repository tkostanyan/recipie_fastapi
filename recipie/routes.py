from typing import Dict

from fastapi import APIRouter, HTTPException, Depends

from recipie.blls import RecipieGenerationBLL
from recipie.schemas import RecipeGenerationRequest
import logging

router = APIRouter()


@router.post("/generate/", response_model=Dict)
async def generate_recipe(request: RecipeGenerationRequest, bll: RecipieGenerationBLL = Depends()) -> Dict:
    """
        Generate a recipe based on the user's input and calculate its nutritional information.

        This endpoint uses the `RecipieGenerationBLL` to generate a recipe and
        calculates the nutritional value of the generated recipe.

        Args:
            request (RecipeGenerationRequest): The input request containing recipe parameters like the number of
                                                persons,
                                                dish type, cooking time, allergy information, diet requirements, and
                                                preferred cuisine.
            bll (RecipieGenerationBLL, optional): The business logic layer that handles interaction with the
                                                  LLM (Language Model) for generating the recipe and calculating
                                                  nutrition. It's injected by FastAPI's dependency injection system.
        Returns:
            Dict: A dictionary containing both the generated recipe and its nutritional information.
                  The final response consists of two combined dictionaries:
                  - The generated recipe (e.g., ingredients, cooking steps).
                  - The calculated nutritional information (e.g., calories, protein, fat, carbohydrates).
        Raises:
            HTTPException: If there is an error while generating the recipe or calculating the nutrition,
                           it logs the error and raises an HTTP 500 Internal Server Error.
    """

    try:
        recipie = await bll.generate_recipe_async(request)
        recipie_with_nutrition = await bll.calculate_nutrition_async(recipie)
        combined_recipe = {**recipie, **recipie_with_nutrition}
        return combined_recipe

    except Exception as e:
        logging.error(
            f"Error generating recipe or calculating nutrition for request: {request.model_dump()}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the recipe.")
