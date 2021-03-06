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
FIESTA_NEWSLINE_ENTITY_SLUGTYPES = {
    'news': 1,
    'ad': 2,
    'events': 3,
    'live': 4,
    'places': 5,
    'sights': 6
}
news_types = dict(FIESTA_NEWSLINE_ENTITY_TYPES)

FIESTA_BLOG_LANGS = (
    ('ru',_("Russian")),
    ('fi',_("Finnish"))
)

FIESTA_NEWS_CITY = (
    (1, _('Saint Petersburg')),
    (2, _('Moscow'))
)
FIESTA_NEWS_CITY_SLUG = {
    'spb':1,
    'msk':2
}
