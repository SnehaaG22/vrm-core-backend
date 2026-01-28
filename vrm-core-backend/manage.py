#!/usr/bin/env python
import os
import sys

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Add backend to Python path
    sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

    os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.settings.dev"
)


    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
