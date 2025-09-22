from urllib.parse import urlparse

from rest_framework.serializers import ValidationError

correct_link = ["youtube.com", "rutube.ru", "www.youtube.com", "www.rutube.ru"]


def validation_domain(url):
    parsed_url = urlparse(url)
    if parsed_url.path not in correct_link:
        raise ValidationError(
            f"Ссылку {parsed_url.path} нельзя прикреплять в этом приложении"
        )
