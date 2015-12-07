# -*- coding: utf-8 -*-
from django.conf import settings


BATCH_API_MAX_REQUESTS = getattr(settings, 'BATCH_API_MAX_REQUESTS', 25)