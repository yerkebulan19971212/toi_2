#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewToi.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

# dd = {
#     "fields": [
#         {"name": "bride_name", "type": "text", "label": "Бойжеткен есімі", "required": true,
#          "placeholder": "Мысалы: Айгерім"},
#         {"name": "groom_name", "type": "text", "label": "Жігіт есімі", "required": true,
#          "placeholder": "Мысалы: Асан"},
#         {"name": "date", "type": "date", "label": "Той күні", "required": true},
#         {"name": "time", "type": "time", "label": "Уақыты", "required": true},
#         {"name": "location", "type": "text", "label": "Мекеме / Зал атауы", "required": true,
#          "placeholder": "Мысалы: Рахат сарайы"},
#         {"name": "address", "type": "textarea", "label": "Мекен-жай", "placeholder": "Толық мекен-жай..."},
#         {"name": "map_url", "type": "url", "label": "Карта сілтемесі (Google Maps)",
#          "placeholder": "https://maps.google.com/..."}
#     ]
# }
