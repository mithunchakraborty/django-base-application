from mailchimp3 import MailChimp
from typing import Optional
from django.conf import settings


def add_mailchimp_email_with_tag(audience_id:str, email:str, tag: str) -> None:
    """
    Добавляет в Mailchimp email в аудиторию с идентификатором audience_id
    """
    _add_email_to_mailchimp_audience(
        audience_id=audience_id,
        email=email
    )

    _add_mailchimp_tag(
        audience_id=audience_id,
        subscriber_hash=_get_mailchimp_subscriber_hash(email=email),
        tag=tag
    )


def _get_mailchimp_client() -> MailChimp:   
    """
    Возвращает клиент API для работы с Mailchimp
    """
    return MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY, 
        mc_user=settings.MAILCHIMP_USERNAME
    )


def _add_email_to_mailchimp_audience(audience_id:str, email:str) -> None:
    """
    Добавляет email в MailChimp аудиторию с идентификатором audience_id
    """
    _get_mailchimp_client().lists.members.create(
        audience_id, 
        {
            'email_address': 'john.doe@example.com',
            'status': 'subscribed',
        }
    )


def _get_mailchimp_subscriber_hash(email:str) -> Optional[str]:
    """
    Возвращает идентификатор email в mailchimp.
    None, если email не найден
    """
    members = _get_mailchimp_client() \
        .search_members \
        .get(
            query=email,
            fields='exact_matches.members.id'
        ) \
        .get('exact_matches').get('members')
         
    if not members:
        return None
    else:
        return members.[0].get('id')


def _add_mailchimp_tag(audience_id:str, subscriber_hash:str, tag:str) -> None:
    """
    Добавляет тег для email с идентификатором subscriber_hash 
    в аудитории audience_id
    """
    _get_mailchimp_client().lists.members.tags.update(
        list_id=audience_id,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': tag, 'status': 'active'}]}
    )
     
