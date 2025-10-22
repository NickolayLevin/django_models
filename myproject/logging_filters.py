from django.conf import settings
import logging

class DebugTrueFilter(logging.Filter):
    def filter(self, record):
        return settings.DEBUG

class DebugFalseFilter(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG