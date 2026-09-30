from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
history: dict[int, list] = {}

SYSTEM_PROMPT = 'Ту ёрдамчии хушмуомила хасти. Кутох ва фахмо чавоб дех.'

def chat(user_id: int, text: str) -> str:
    if user_id not in history:
        history[user_id] = [
            {'role': 'system', 'content': SYSTEM_PROMPT}
        ]

    history[user_id].append({'role': 'user', 'content': text})
    
    # ИСПРАВЛЕНО: правильное название модели (убрана опечатка)
    response = client.chat.completions.create(
        model='openai/gpt-oss-120b', 
        messages=history[user_id]
    )
    
    answer = response.choices[0].message.content
    history[user_id].append({'role': 'assistant', 'content': answer})

    return answer

# def generate_image(user_id, prompt: str) ->str:
#     response = client.images.generate(
#         model='llama-3.3-70b-versatile',
#         prompt=prompt,
#         size='1024x1024'
#     )

#     image_bytes64 = response.data[0].b64_json
#     image_bytes = base64.b64decode(image_bytes64)
#     filename = f"generated_{user_id}.png"

#     with open (filename, 'wb') as f:
#         f.write(image_bytes)

#     return filename

# def search(query: str) ->str:
#     response = client.responses.create(
#         model='gpt-4o-mini',
#         tools = [
#             {'type': 'web_search'}
#         ],
#         instruction='Ба забони точики чавоб дех, кутох ва фахмо',
#         input=query
#     )

#     return response.output_text