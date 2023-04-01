from django.http import HttpResponse
from django.views import View
from django.conf import settings
import subprocess

class RunScriptView(View):
    def get(self, request, *args, **kwargs):
        # Определение пути к файлу, который нужно запустить
        script_path = settings.BASE_DIR / 'scripts' / 'my_script.py'
        # Запуск скрипта
        result = subprocess.run(['python', script_path], capture_output=True)
        # Возвращение содержимого stdout в виде http-ответа
        return HttpResponse(result.stdout.decode('utf-8'))
