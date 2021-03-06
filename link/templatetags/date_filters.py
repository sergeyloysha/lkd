# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re
from datetime import date, datetime
from decimal import Decimal

from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.encoding import force_text
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.timezone import is_aware, utc
 
register = template.Library()

@register.filter
def difference(value):

    if not isinstance(value, date):  # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value < now:
        delta = now - value
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s ago'
            ) % {'delta':defaultfilters.timesince(value, now)}
        elif delta.seconds == 0:
            return _('now')
        elif delta.seconds < 60:
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a second ago', '%(count)s seconds ago', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a minute ago', '%(count)s minutes ago', count
            ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'an hour ago', '%(count)s hours ago', count
            ) % {'count': count}
    else:
        delta = value - now
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s from now'
            ) % {'delta': defaultfilters.timeuntil(value, now)}
        elif delta.seconds == 0:
            return _('now')
        elif delta.seconds < 60:
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a second from now', '%(count)s seconds from now', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'a minute from now', '%(count)s minutes from now', count
            ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                # Translators: please keep a non-breaking space (U+00A0)
                # between count and time unit.
                'an hour from now', '%(count)s hours from now', count
            ) % {'count': count}