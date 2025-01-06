from django.apps import AppConfig


# class AuthappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'authapp'

class PrjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'


class authappConfig(AppConfig):
    name = 'authapp'
    verbose_name = 'A Much Better Name'