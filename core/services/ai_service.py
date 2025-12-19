import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_project_description(title):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write a short description for {title}"}]
    )
    return response.choices[0].message.content
