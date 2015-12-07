#!/usr/bin/env python
import os
import sys
from importlib import import_module


if __name__ == "__main__":
    settings_module = "example.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
