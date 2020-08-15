from django.db import models


class CommonMailingList(models.Model):
    """
    Рассылка на общие материалы сайта
    """
    email = models.EmailField('Email подписчика')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'common_mailing_list'


class CaseMailingList(models.Model):
    """
    Рассылка на материалы конкретного дело
    """
    email = models.EmailField('Email подписчика')
    case = models.ForeignKey(
        to='cases.Case', 
        verbose_name='Дело',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'case_mailing_list'

