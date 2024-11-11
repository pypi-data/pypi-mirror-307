import json
from os.path import isfile

from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.models import Site

from wagtail_design_system.models import WagtailDesignSystemConfig


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """Sets the site hostname, and imports contents from the config.json file if present"""
        site = Site.objects.filter(is_default_site=True).first()
        site.hostname = settings.HOST_URL
        site.save()

        if isfile("config.json"):
            with open("config.json") as config_file:
                config_data = json.load(config_file)

                config_data["site_id"] = site.id

                _config, created = WagtailDesignSystemConfig.objects.get_or_create(id=1, defaults=config_data)
                # if _config.operator_logo_file_wagtail:
                #     _config.operator_logo_file = _config.operator_logo_file_wagtail
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Config imported for {config_data.get('site_title', '')}"))
                else:
                    self.stdout.write(self.style.SUCCESS("Config already existing, data not imported."))
