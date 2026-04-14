from openai import OpenAI
from app.core.config import OPENAI_API_KEY

class GenerationService:
    def __init__(self, model: str = "gpt-4.1-mini"):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def generate_answer(self, prompt: str) -> str:
        # 1. Validate prompt
        if not prompt or not prompt.strip():
            raise ValueError("prompt must not be empty")

        try:
            # 2. Call OpenAI
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )

            # 3. Extract output text
            output_text = response.output_text

            if not output_text:
                raise RuntimeError("Empty response from model")

            return output_text.strip()

        except Exception as e:
            # 4. Wrap error for easier debugging
            raise RuntimeError(f"Generation failed: {str(e)}") from e