from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Article

class AuthorCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Обработка запроса перед передачей его в представление
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Проверяем, если это запрос на редактирование или удаление статьи
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            article_id = view_kwargs.get('pk')  # Получаем ID статьи из URL

            # Проверяем, аутентифицирован ли пользователь
            if request.user.is_authenticated:
                article = get_object_or_404(Article, pk=article_id)

                # Проверяем, является ли текущий пользователь автором статьи
                if article.author != request.user:
                    return JsonResponse({'error': 'У вас нет прав для выполнения этого действия.'}, status=403)
            else:
                return JsonResponse({'error': 'Необходима аутентификация.'}, status=401)

        return None
