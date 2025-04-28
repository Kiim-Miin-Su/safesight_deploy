# tasks/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import base64
import json
from io import BytesIO

@login_required
def task_select_view(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        image_data = request.POST.get('image_data')

        if image_data:
            header, encoded = image_data.split(',', 1)
            binary_data = base64.b64decode(encoded)
            image = BytesIO(binary_data)

            files = {'image': ('captured.jpg', image, 'image/jpeg')}
            response = requests.post('http://127.0.0.1:8002/detect', files=files)

            if response.status_code == 200:
                result = response.json()
                detected = result.get('labels', [])

                task_to_equipment = {
                    "실험작업": ["Not Wearing"]
                }

                required = task_to_equipment.get(task, [])
                missing = [item for item in required if item in detected]

                return render(request, 'tasks/result.html', {
                    'task': task,
                    'required': required,
                    'detected': detected,
                    'missing': missing
                })

    return render(request, 'tasks/select_task.html')

@csrf_exempt
def task_result_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        labels = data.get('labels', [])
        task = data.get('task', '')

        print(f"🚨 위반 감지: {labels} (작업 종류: {task})")

        return JsonResponse({"message": "결과 저장 완료", "labels": labels})

    return JsonResponse({"error": "잘못된 요청"}, status=400)