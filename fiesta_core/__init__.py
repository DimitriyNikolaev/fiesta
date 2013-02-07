# -*- coding: utf-8 -*-
import os

FIESTA_CORE_APPS = [
    'fiesta_core',
    'fiesta_core.apps.blog',
    'fiesta_core.apps.dashboard',
    'fiesta_core.apps.dashboard.blog',
    'fiesta_core.models'
]

def get_core_apps():
    return FIESTA_CORE_APPS

FIESTA_MAIN_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates/fiesta')