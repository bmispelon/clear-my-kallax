import logging
import os

import sentry_sdk
from django.apps import AppConfig
from sentry_sdk.integrations.django import DjangoIntegration


class AutoInitConfig(AppConfig):
    name = 'sentry_auto_init'
    verbose_name = "Sentry Auto Init"

    def ready(self):
        logging.info("Initializing Sentry SDK")
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN_URL'),
            integrations=[DjangoIntegration()],
            traces_sample_rate=float(os.getenv('SENTRY_SAMPLE_RATE', '0')),
            send_default_pii=(os.getenv('SENTRY_SEND_PII', 'FALSE').upper() in {'YES', 'TRUE', 'Y'})
        )
