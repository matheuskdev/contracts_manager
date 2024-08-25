from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from departments.models import Department
from folders.models import Folder
from parts.models import Part
from utils import mixins


class Contract(
    mixins.TimestampModelMixin,
    mixins.OwnerModelMixin,
    mixins.SoftDeleteModelMixin,
):
    """ "
    Model representing a Contract
    """

    CONTRACT_STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('approved', 'Aprovado'),
        ('completed', 'Finalizado'),
        ('canceled', 'Cancelado'),
        ('renewed', 'Renovado'),
    ]

    CONTRACT_TYPE_CHOICES = [
        ('service', 'Prestação de Serviços'),
        ('sales', 'Venda'),
        ('rental', 'Locação'),
        ('partnership', 'Parceria'),
    ]

    pdf = models.FileField(
        upload_to="contracts_pdfs",
        validators=[FileExtensionValidator(["pdf", "DOCX", "DOC"])],
        help_text="Faça o upload do arquivo PDF do contrato.",
    )
    description = models.TextField(help_text="Descrição detalhada do contrato.")
    amount = models.DecimalField(
        max_digits=40, decimal_places=2, help_text="Valor total do contrato."
    )
    number = models.CharField(
        max_length=20, help_text="Número identificador do contrato."
    )
    subject = models.CharField(
        unique=True, max_length=100, help_text="Assunto ou objeto principal do contrato."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Anotações gerais sobre o contrato."
    )
    start_date = models.DateField(help_text="Data de início do contrato.")
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Data de término do contrato. Se não definido, o contrato será renovado automaticamente.",
    )
    """     active = models.BooleanField(
        default=True, help_text="Indica se o contrato está ativo."
    ) """
    status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default='draft',
        help_text="Status atual do contrato."
    )
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        help_text="Tipo de contrato."
    )
    lgpd = models.BooleanField(
        default=True,
        help_text="Indica se o contrato está em conformidade com a LGPD (Lei Geral de Proteção de Dados).",
    )
    automatic_renewal = models.BooleanField(
        default=False, help_text="Indica se o contrato será renovado automaticamente."
    )
    contains_addendum = models.BooleanField(
        default=False, help_text="Indica se o contrato contém um aditivo."
    )
    parts = models.ManyToManyField(
        Part, blank=True, help_text="Partes envolvidas no contrato."
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.DO_NOTHING,
        help_text="Pasta onde o contrato está armazenado.",
    )
    email_sent = models.BooleanField(
        default=False,
        blank=True,
        help_text="Indica se o e-mail de notificação foi enviado.",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        help_text="Identificador único para a URL do contrato.",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        help_text="Setor ao qual o contrato pertence.",
    )

    class Meta:
        ordering = ["subject"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        indexes = [
            models.Index(fields=["subject"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["subject"], name="unique_contract_subject"),
        ]

    def __str__(self):
        return f"{self.department} - {self.subject}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        if not self.end_date:
            self.automatic_renewal = True
            self.end_date = timezone.now().date() + timezone.timedelta(days=365)
        super().save(*args, **kwargs)
