from django.contrib.admin import ModelAdmin


class MultiModelAdmin(ModelAdmin):
    """Admin class for editing multiple models simultaneously.

       Instances of MultiModelAdmin are associated with a primary
       model (and hence inherit from ModelAdmin) but also with
       parent models to which the primary model is related to by a
       foreign key. This is useful when we want to work directly with
       a child model as opposed to working with it in an inline 
       instance associated to its parent.
    """

    parent_models = []


    # methods that may need to be extended

    def get_fields(self, request, obj=None):
        pass

    def get_form(self, request, obj=None, **kwargs):
        pass

    def get_object(self, request, object_id, from_field=None):
        pass

    def log_addition(self, request, object, message):
        pass

    def log_change(self, request, object, message):
        pass

    def log_deletion(self, request, object, message):
        pass

    def save_form(self, request, form, change):
        pass

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_formset(self, request, form, formset, change):
        pass

    def save_related(self, request, form, formsets, change):
        pass
