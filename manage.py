#!/usr/bin/env python
import os
import sys
import sef

if __name__ == "__main__":
    secrets = os.path.join(os.path.dirname(__file__), '.secrets')
    sef.set_defaults(secrets)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
