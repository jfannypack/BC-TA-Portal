from django.shortcuts import render
from django.core.exceptions import ValidationError

# Create your views here.

def validate_eagleid(value):
    if not isinstance(value, str) or len(value) != 8:
        raise ValidationError('Eagleid must be an 8 digit value')
