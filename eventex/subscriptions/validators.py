from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('Cpf deve conter apenas números', 'digits_error')

    if len(value) != 11:
        raise ValidationError('Cpf deve ter 11 números', 'length_error')
