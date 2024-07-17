import logging
from functools import wraps
from typing import Callable

from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.db.models import Model, QuerySet
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html


def build_admin_model_link(obj: Model, view_name: str, target: str = 'self'):
    """
    Build human readable link to a view within admin app.

    For a model instance with pk=1, and view='change' the output is:
        Model / <a href="/admin/app_name/model_name/1/change">model_str</a>
    """
    if not obj:
        return None
    opts = obj._meta  # noqa
    try:
        return format_html(
            '{type} / <a href="{url}" target="{target}">{obj}</a>',
            type=opts.model.__name__,
            url=reverse(f'admin:{opts.app_label}_{opts.model_name}_{view_name}', args=[obj.pk]),
            obj=obj,
            target=target,
        )
    except NoReverseMatch:
        return format_html(
            '{type} / {obj}',
            type=opts.model.__name__,
            obj=obj,
        )


def build_admin_model_change_view_link(obj: Model, target: str = None):
    """
    Build human readable link to a change view within admin app.

    For a model instance with pk=1 the output is:
        Model / <a href="/admin/app_name/model_name/1/change">model_str</a>
    """
    return build_admin_model_link(obj, view_name='change', target=target)


def action_on_entity(  # noqa: MC0001
    *,
    success_message: str = None,
    error_message: str = None,
    only_one: bool = False,
    extra_filter: Callable[[QuerySet], QuerySet] = None,
    no_records_message: str = None,
):
    def _inner_decorator(fn):
        @wraps(fn)
        def _executor(self: ModelAdmin, request, queryset):

            if extra_filter:
                queryset = extra_filter(queryset)

            # We use len(), since we will iterate over results later
            if not len(queryset):  # pylint: disable=len-as-condition
                if no_records_message:
                    self.message_user(request, message=no_records_message, level=messages.WARNING)
                return None

            if only_one and len(queryset) != 1:
                self.message_user(
                    request,
                    message='Only single entry may be selected to execute this action',
                    level=messages.ERROR,
                )
                return None

            for entity in queryset:
                try:
                    msg = fn(self, request, entity)
                    if msg is None and success_message:
                        entity_link = build_admin_model_change_view_link(entity)
                        msg = format_html(success_message, entity=entity, entity_link=entity_link)
                    if msg:
                        self.message_user(request, message=msg)
                except Exception as e:  # pylint: disable=broad-except
                    logging.exception(e)
                    if error_message:
                        entity_link = build_admin_model_change_view_link(entity)
                        msg = format_html(error_message, entity=entity, entity_link=entity_link, error=e)
                        self.message_user(request, message=msg, level=messages.ERROR)

            return HttpResponseRedirect(request.get_full_path())

        return _executor
    return _inner_decorator
