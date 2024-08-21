from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.apps import apps


class ContractExpirationNotificationBase:

    days_until_expiration = None
    email_subject = ''
    email_template = ''

    @classmethod
    def register_signal(cls):
        Contract = apps.get_model('contracts', 'Contract')
        post_save.connect(cls.check_contract, sender=Contract)

    @classmethod
    def check_contract(cls, sender, instance, **kwargs):
        if not instance.automatic_renewal:
            return

        current_date = timezone.now().date()
        expiration_warning_date = current_date + timezone.timedelta(days=cls.days_until_expiration)

        if (instance.end_date <= expiration_warning_date and
            instance.end_date > current_date and not instance.email_sent):
            cls.send_expiration_email(instance)
            instance.email_sent = True
            instance.save()

    @classmethod
    def send_expiration_email(cls, instance):
        html_message = render_to_string(cls.email_template, {'contract': instance})
        plain_message = strip_tags(html_message)
        send_mail(
            cls.email_subject,
            plain_message,
            'matheuskdev@gmailcom',
            [instance.owner.email],
            html_message=html_message
        )


class ContractExpirationNotification45(ContractExpirationNotificationBase):
    days_until_expiration = 45
    email_subject = 'Alerta Contrato - 45 Dias para Expirar'
    email_template = 'emails/contracts_due_in_45_days.html'


class ContractExpirationNotification30(ContractExpirationNotificationBase):
    days_until_expiration = 30
    email_subject = 'Alerta Contrato - 30 Dias para Expirar'
    email_template = 'emails/contracts_due_in_30_days.html'
