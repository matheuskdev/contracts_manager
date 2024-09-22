from typing import Callable, Dict, Any, Type
from django.apps import apps
from django.core.mail import send_mail
from django.db.models import Model
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from contracts.models import Contract


class ContractExpirationNotificationBase:
    """
    Base class for sending email notifications when a contract is about to expire.
    Subclasses should define the number of days before expiration and the corresponding
    email template and subject.
    """

    days_until_expiration: int = 0
    email_subject: str = ""
    email_template: str = ""
    renewal_check: Callable[[Contract], bool] = lambda instance: False

    @classmethod
    def register_signal(cls) -> None:
        """
        Registers a signal to listen for the post_save event on the Contract model.
        When a contract is saved, the expiration check is triggered.
        """
        ContractModel: Type[Model] = apps.get_model("contracts", "Contract")
        post_save.connect(cls.check_contract, sender=ContractModel)

    @classmethod
    def check_contract(cls, sender: Type[Model], instance: Contract, **kwargs: Any) -> None:
        """
        Checks if a contract is nearing expiration based on the defined number of days.
        If the contract is set to expire within the specified days and no email has been sent,
        it triggers the email notification.

        :param sender: The Contract model class.
        :param instance: The instance of the contract being checked.
        :param kwargs: Additional arguments passed by the signal.
        """
        if not cls.renewal_check(instance):
            return

        current_date = timezone.now().date()
        expiration_warning_date = current_date + timezone.timedelta(
            days=cls.days_until_expiration
        )

        if (
            instance.end_date <= expiration_warning_date
            and instance.end_date > current_date
            and not instance.email_sent
        ):
            cls.send_expiration_email(instance)
            instance.email_sent = True
            instance.save()

    @classmethod
    def send_expiration_email(cls, instance: Contract) -> None:
        """
        Sends an expiration warning email to the contract owner.
        The email is rendered using the specified template and subject.

        :param instance: The contract instance for which the email is being sent.
        """
        context: Dict[str, Any] = {
            "contract": instance,
        }
        html_message: str = render_to_string(cls.email_template, context)
        plain_message: str = strip_tags(html_message)
        send_mail(
            cls.email_subject,
            plain_message,
            "matheuskdev@gmail.com",
            [instance.owner.email],
            html_message=html_message,
        )


def automatic_renewal_check(instance: Contract) -> bool:
    """
    Check if the contract has automatic renewal enabled.

    :param instance: The contract instance.
    :return: True if automatic renewal is enabled, False otherwise.
    """
    return instance.automatic_renewal


def no_renewal_check(instance: Contract) -> bool:
    """
    Check if the contract does not have automatic renewal enabled.

    :param instance: The contract instance.
    :return: True if automatic renewal is not enabled, False otherwise.
    """
    return not instance.automatic_renewal


class ContractExpirationNotification45(ContractExpirationNotificationBase):
    """
    Notification class for contracts expiring in 45 days without automatic renewal.
    """
    days_until_expiration: int = 45
    email_subject: str = "Contract Alert - 45 Days to Expiration"
    email_template: str = "emails/contracts_due_in_45_days.html"
    renewal_check: Callable[[Contract], bool] = no_renewal_check


class ContractExpirationNotification30(ContractExpirationNotificationBase):
    """
    Notification class for contracts expiring in 30 days with automatic renewal.
    """
    days_until_expiration: int = 30
    email_subject: str = "Contract Alert - 30 Days to Expiration"
    email_template: str = "emails/contracts_due_in_30_days.html"
    renewal_check: Callable[[Contract], bool] = automatic_renewal_check
