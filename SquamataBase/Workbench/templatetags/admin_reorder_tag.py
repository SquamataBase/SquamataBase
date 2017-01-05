# module modified from https://djangosnippets.org/snippets/1939/
from django import template
from django.conf import settings
from collections import OrderedDict


register = template.Library()


# from http://www.djangosnippets.org/snippets/1937/
def register_render_tag(renderer):
    """
    Decorator that creates a template tag using the given renderer as the 
    render function for the template tag node - the render function takes two 
    arguments - the template context and the tag token
    """
    def tag(parser, token):
        class TagNode(template.Node):
            def render(self, context):
                return renderer(context, token)
        return TagNode()
    for copy_attr in ("__dict__", "__doc__", "__name__"):
        setattr(tag, copy_attr, getattr(renderer, copy_attr))
    return register.tag(tag)


@register_render_tag
def admin_reorder(context, token):
    """
    Called in admin/base_site.html template override and applies custom ordering 
    of apps/models defined by settings.ADMIN_REORDER
    """
    # sort key function - use index of item in order if exists, otherwise item
    sort = lambda order, item: (order.index(item), "") if item in order else (
        len(order), item)
    if "app_list" in context:
        # sort the app list
        context["app_list"].sort(key=lambda app: sort(settings.ADMIN_REORDER['app_layout'], 
            app["app_label"]))
        for i, app in enumerate(context["app_list"]):
            # sort the model list for each app
            app_name = app["app_label"]
            model_order = [m for m in settings.ADMIN_REORDER['model_layout'].get(app_name, [])]
            context["app_list"][i]["models"].sort(key=lambda model: 
                sort(model_order, model["object_name"]))
    return ""


@register_render_tag
def admin_exclude(context, token):
    if "app_list" in context:
        exclude = settings.ADMIN_REORDER["exclude"]
        for i, app in enumerate(context["app_list"]):
            app_name = app["app_label"]
            app_models = exclude["app_models"].get(app_name, [])
            context["app_list"][i]["models"][:] = [model for model in context["app_list"][i]["models"] if model["object_name"] not in app_models]
        context["app_list"][:] = [app for app in context["app_list"] if app["app_label"] not in exclude["apps"]]

    return ""
