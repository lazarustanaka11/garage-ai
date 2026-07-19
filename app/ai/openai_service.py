import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.client = OpenAI(api_key=api_key)

    def test_connection(self) -> str:
        response = self.client.responses.create(
            model="gpt-5",
            input="Reply with exactly these two words: Garage AI",
        )

        return response.output_text

    def diagnose(
        self,
        make: str,
        model: str,
        year: int,
        mileage: int,
        title: str,
        description: str,
    ) -> str:

        prompt = f"""
You are an ASE-certified master automotive technician.

Analyze this repair request.

Vehicle:
- Year: {year}
- Make: {make}
- Model: {model}
- Mileage: {mileage}

Complaint:
{title}

Customer Description:
{description}

Return:

1. Possible causes
2. Recommended inspections
3. Recommended repair
4. Estimated urgency (Low, Medium or High)

Keep the answer professional and concise.
"""

        response = self.client.responses.create(
            model="gpt-5",
            input=prompt,
        )

        return response.output_text
