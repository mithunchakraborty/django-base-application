from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import *
from cases.models import Case
from .services.mailchimp import add_mailchimp_email_with_tag


def add_to_common_list_view(request):
    """
    Веб-сервис, добавляющий email в общий лист рассылки
    """
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    add_mailchimp_email_with_tag(
        audience_id=settings.MAILCHIMP_COMMON_LIST_ID,
        email=email,
        tag='COMMON TAG'
    )

    CommonMailingList.objects.get_or_create(email=email)

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

    add_mailchimp_email_with_tag(
        audience_id=settings.MAILCHIMP_CASE_LIST_ID,
        email=email,
        tag=case_id
    )

    CaseMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success': True}) 


