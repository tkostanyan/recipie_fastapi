from typing import Dict

from recipie.schemas import RecipeGenerationRequest
from recipie.utils import get_llm_class


class BaseBLL:
    """
        Base class for the Business Logic Layer (BLL) that interacts with an LLM (Large Language Model).

        Attributes:
            _llm_client: An instance of the LLM client used to interact with the language model.
    """

    def __init__(self, llm: str = 'openai'):
        self._llm_client = get_llm_class(llm)()


class RecipieGenerationBLL(BaseBLL):
    """
        The class responsible for generating recipes and calculating nutritional values using an LLM.

        Inherits from BaseBLL and contains methods to generate recipe prompts, nutrition prompts,
        and methods for synchronous and asynchronous recipe generation and nutrition calculations.
    """

    def _generate_recipie_prompt(self, data: RecipeGenerationRequest):
        """
            Generates a prompt for the LLM to create a recipe based on user input.

            Args:
                data (RecipeGenerationRequest): The user's input containing details like number of persons,
                                                dish type, cooking time, dietary restrictions, and preferred cuisine.

            Returns:
                str: A string prompt to be sent to the LLM to generate a recipe.
        """

        return f"""
            Hey, ChatGPT, generate me a meal recipe for {data.amountOfPersons} persons and {data.dishType}
            with cooking time under {data.maxCooking} minutes,
            good for people with allergies to {', '.join(data.allergieList)},
            following {', '.join(data.dietRequirements)} diet requirements,
            preferring the {', '.join(data.cuisineList)} cuisine.
            
            Your output should look like {data.outputDataFormat}, You are not asking questions,
            just responding with recipe. 
            
            where: {data.outputDataFormat}
            1. Each of your answers is a JSON, consisting of few main parameters "Name",
            "CookingTime", "RequiredTools", "Ingredients", "Step-by-step directions"
            2. Each ingredient should contain main parameters "Name",
            3. For each ingredient you should display measurements in few units "grams" , "ml",
            "cups", "teaspoons", "tablespoons", "piece" 
            """

    def _generate_nutrition_prompt(self, recipie: str):
        """
            Generates a prompt for the LLM to calculate nutritional information for a given recipe.

            Args:
                recipie (str): The generated recipe in string format to calculate nutritional values.

            Returns:
                str: A string prompt to be sent to the LLM to calculate the nutrition of the recipe.
        """

        return f"""
        You are food technologist.
        The recipe is defined between <recipe> and </recipe>.
        Calculate the weight of this dish, the number of servings,
        and the nutritional values (calories, protein, fat, carbohydrates)
        Your output should be in format defined between <format> and </format>.
        You are not asking questions, just responding with JSON that contains nutritional value
        <format>
        1. Each of your answers is a JSON, consisting of few main parameters "calories",
        "protein", "fat", "carbohydrates", "totalWeight"
        </format>
        <recipe>
            {recipie}
        </recipe>
        """

    def generate_recipe(self, data: RecipeGenerationRequest) -> Dict:
        """
            Generates a recipe synchronously using the LLM client.

            Args:
                data (RecipeGenerationRequest): The user's input data for generating the recipe prompt.

            Returns:
                Dict: The generated recipe in JSON format.
        """
        prompt = self._generate_recipie_prompt(data)

        # Send the request to OpenAI's API
        output = self._llm_client.generate(prompt)
        return output

    async def generate_recipe_async(self, data: RecipeGenerationRequest) -> Dict:
        """
            Asynchronously generates a recipe using the LLM client.

            Args:
                data (RecipeGenerationRequest): The user's input data for generating the recipe prompt.

            Returns:
                Dict: The generated recipe in JSON format.
        """
        prompt = self._generate_recipie_prompt(data)

        # Send the request to OpenAI's API
        output = await self._llm_client.generate_async(prompt)
        return output

    def calculate_nutrition(self, recipie: Dict) -> Dict:
        """
            Calculates the nutritional values of a given recipe synchronously.

            Args:
                recipie (Dict): The recipe data for which nutritional values are to be calculated.

            Returns:
                Dict: The calculated nutritional values s.t. calories, protein, fat, carbohydrates, and total weight.
        """
        prompt = self._generate_nutrition_prompt(str(recipie))

        # Send the request to OpenAI's API
        output = self._llm_client.generate(prompt)
        return output

    async def calculate_nutrition_async(self, recipie: Dict) -> Dict:
        """
            Asynchronously calculates the nutritional values of a given recipe.

            Args:
                recipie (Dict): The recipe data for which nutritional values are to be calculated.

            Returns:
                Dict: The calculated nutritional values, s.t. calories, protein, fat, carbohydrates, and total weight.
        """
        prompt = self._generate_nutrition_prompt(str(recipie))

        # Send the request to OpenAI's API
        output = await self._llm_client.generate_async(prompt)
        return output
