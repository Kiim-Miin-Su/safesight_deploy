from django.apps import AppConfig  # ✅ 꼭 필요!

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
