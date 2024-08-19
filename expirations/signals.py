from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.utils import timezone
from django.apps import apps

class ContractEmailSender:
    def __init__(self, subject, template_name):
        self.subject = subject
        self.template_name = template_name

    def send_email(self, instance):
        html_message = render_to_string(self.template_name, {'contract': instance})
        plain_message = strip_tags(html_message)
        sender = 'matheuskins7@gmail.com'
        recipient = 'matheuskins7@gmail.com'
        send_mail(self.subject, plain_message, sender, [recipient], html_message=html_message)



class ContractExpiryNotifier:
    def __init__(self, days_before_expiry, email_sender):
        self.days_before_expiry = days_before_expiry
        self.email_sender = email_sender

    def register_signal(self):
        Contract = apps.get_model('contracts', 'Contract')
        post_save.connect(self.check_contract, sender=Contract)

    def check_contract(self, sender, instance, **kwargs):

        current_date = timezone.now().date()
        expiry_date = current_date + timezone.timedelta(days=self.days_before_expiry)

        if (instance.end_date <= expiry_date and
            instance.end_date > current_date and not instance.email_sent):
            self.email_sender.send_email(instance)
            instance.email_sent = True
            instance.save()



class ExpiryNotifications:

    @staticmethod
    def setup_notifications():
       
        sender_45_days = ContractEmailSender(
            subject='Contract Alert - 45 Days Until Expiry',
            template_name='emails/contracts_due_in_45_days.html'
        )
        notifier_45_days = ContractExpiryNotifier(days_before_expiry=45, email_sender=sender_45_days)
        notifier_45_days.register_signal()


        sender_30_days = ContractEmailSender(
            subject='Contract Alert - 30 Days Until Expiry',
            template_name='emails/contracts_due_in_30_days.html'
        )
        notifier_30_days = ContractExpiryNotifier(days_before_expiry=30, email_sender=sender_30_days)
        notifier_30_days.register_signal()

ExpiryNotifications.setup_notifications()