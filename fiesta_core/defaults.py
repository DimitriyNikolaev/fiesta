# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.utils.translation import ugettext_lazy as _


FIESTA_NEWSLINE_ENTITY_TYPES = (
    ( 1, _("News")),
    ( 2, _("Advertisement")),
    ( 3, _("Event")),
    ( 4, _("Live")),
    ( 5, _("Place")),
    ( 6, _("Sight"))
)
news_types = dict(FIESTA_NEWSLINE_ENTITY_TYPES)

FIESTA_BLOG_LANGS = (
    ('ru',_("Russian")),
    ('fi',_("Finnish"))
)

FIESTA_NEWS_CITY = (
    (1, _('Saint Petersburg')),
    (2, _('Moscow'))
)