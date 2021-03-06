import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .services.services import * 
from core.views import base_view, BaseView


# Открыть логгер можно командой tail -f src/log.log
# tail следит за обновлениями файла
logger = logging.getLogger(__name__)


def add_to_common_list_view(request):
    """
    Веб-сервис, добавляющий email в общий лист рассылки
    """
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    add_email_to_common_mailchimp_list(email=email)

    return JsonResponse({'success': True}) 


def add_to_case_list_view(request):
    """
    Веб-сервис, добавляющий email в лист рассылок по конкретному делу
    """
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = request.GET.get('case_id')

    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    case = Case.objects.get(pk=case_id)

    case_tag = f'Case {case.name}'

    add_email_to_case_mailchimp_list(email=email, case_id=case_id)

    return JsonResponse({'success': True}) 


@base_view
def tmp_view(request):
    logger.warning('Hello!')
    logger.info('Inf')
    logger.error('err')
    return JsonResponse({'success': True})


class MyView(BaseView):
    def get(self, request):
        return {'success': True}

