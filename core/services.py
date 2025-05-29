import openai
from django.conf import settings
import json
from .models import Module, Chapter, Quiz, Assignment

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_course(course):
    prompt = f"""
Loo AI kursus teemal "{course.topic}".
Struktuur: JSON kujul.
Formaat:
{{
  "modules": [
    {{
      "title": "...",
      "chapters": [
        {{
          "title": "...",
          "content": "...",
          "quiz": [
            {{
              "question": "...",
              "answer": "..."
            }}
          ],
          "assignments": [
            {{
              "instruction": "..."
            }}
          ]
        }}
      ]
    }}
  ]
}}
Vasta ainult puhtas JSON-formaadis ilma selgitusteta.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        data = json.loads(response['choices'][0]['message']['content'])
    except json.JSONDecodeError:
        return  # optionally log error

    for module_data in data.get("modules", []):
        module = Module.objects.create(course=course, title=module_data["title"])
        for chapter_data in module_data.get("chapters", []):
            chapter = Chapter.objects.create(
                module=module,
                title=chapter_data["title"],
                content=chapter_data["content"]
            )
            for quiz_data in chapter_data.get("quiz", []):
                Quiz.objects.create(
                    chapter=chapter,
                    question=quiz_data["question"],
                    answer=quiz_data["answer"]
                )
            for task_data in chapter_data.get("assignments", []):
                Assignment.objects.create(
                    chapter=chapter,
                    instruction=task_data["instruction"]
                )

def get_ai_course_recommendation(topics):
    prompt = (
        "Siin on kasutaja senised kursuste teemad:\n"
        + "\n".join(f"- {topic}" for topic in topics) +
        "\n\nSoovita järgmine AI-kursus, mis põhineks nende teadmiste laiendamisel. "
        "Vasta ainult kursuse pealkirjaga. Ei mingit selgitust."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content'].strip()
