from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv
import openai
from openai import OpenAIError

load_dotenv()


@csrf_exempt
@require_http_methods(["POST"])
def smart_scan(request):
    if 'photo' not in request.POST:
        return JsonResponse({'error': 'No image data provided'}, status=400)

    image_data = request.POST['photo']

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Określ, do jakiego śmietnika powinien trafić przedmiot znajdujący się na zdjęciu. "
                                                 "Weź pod uwagę materiał i jego zabrudzenie. "
                                                 "Odpowiedź tylko jednym słowem: plastik, szkło, papier, elektronika, biodegradowalne, zmieszane."},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpg;base64,{image_data}"
                        }}
                    ]
                }
            ],
            max_tokens=500,
            temperature=0
        )

        return JsonResponse({
            'status': 'success',
            'data': response.choices[0].message.content
        })
    except OpenAIError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'API request failed',
            'details': str(e)
        }, status=500)
