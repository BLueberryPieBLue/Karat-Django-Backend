from django.apps import AppConfig
from django.db.models.signals import post_migrate


def do_init_data(sender, **kwargs):
    from RootAPP.init_data import init_datas
    init_datas()


class RootappConfig(AppConfig):
    name = 'RootAPP'

    def ready(self):
        post_migrate.connect(do_init_data, sender=self)

