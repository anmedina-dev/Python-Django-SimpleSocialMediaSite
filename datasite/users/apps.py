from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    #creates a profile when user is created
    def ready(self):
        import users.signals