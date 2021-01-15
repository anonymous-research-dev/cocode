#!/usr/bin/env python
import os
import sys

def prc_args():
    if len(sys.argv) == 1 or sys.argv[1] != 'runserver': 
        return sys.argv
    elif '--fromnode' not in sys.argv:
        raise Exception(
            "It seems like you are not running server via node start script. "
            "This will result in no template and webpack bundle support.\n" 
            "Try running \"$ yarn start\""
        )
    else:
        return [arg for arg in sys.argv if arg != '--fromnode']

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cocode.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    args = prc_args()
    execute_from_command_line(args)

if __name__ == '__main__':
    main()
