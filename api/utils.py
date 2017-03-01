from api.models import APIKey


def is_valid_api_key(key):
    return APIKey.objects.filter(key=key).exists()
