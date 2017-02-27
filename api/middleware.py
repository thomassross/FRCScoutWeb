from django.core.exceptions import ObjectDoesNotExist

from api.models import APIKey


def api_middleware(get_response):

    def middleware(request):

        if "api_key" in request.POST:
            api_key_param = request.POST["api_key"]
            try:
                api_key = APIKey.objects.get(pk=api_key_param)
            except ObjectDoesNotExist:
                return
            else:
                request.api_key = api_key

        response = get_response(request)

        return response

    return middleware
