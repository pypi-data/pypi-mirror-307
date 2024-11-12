from flask import current_app, abort

from ..presenters.pagination import generate_govuk_frontend_pagination_params

from .frameworks import get_framework_or_404
from .pagination import default_pagination_config


def get_framework_and_check_allowed_or_404(client, framework_slug):
    if framework_slug in current_app.config.get('FRAMEWORKS_ALLOWING_COMMUNICATIONS'):
        return get_framework_or_404(
            client,
            framework_slug,
            current_app.config.get('VIEW_COMMUNICATIONS_STATUSES')
        )
    else:
        abort(404)


def get_compliance_communications_content(
    request,
    table_params_method,
    data,
    page_param,
    preserved_kwargs,
    url_params,
    with_supplier=False
):
    return {
        "table_params": table_params_method(
            data['communications'],
            with_supplier
        ),
        "pagination_params": generate_govuk_frontend_pagination_params(
            default_pagination_config(data['meta'], request, page_param),
            url_params,
            {
                "request_args": request.args,
                "preserved_kwargs": preserved_kwargs,
                "page_param": page_param
            }
        )
    }
