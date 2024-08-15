from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\d{9,15}$",
    message="Número de telefone deve conter entre 9 e 15 dígitos.",
)
