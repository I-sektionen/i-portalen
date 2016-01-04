from django.contrib import admin
from .models import Question, Topic, FAQ


class FAQAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(FAQAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter(organisations__in=request.user.get_organisations())
        return qs


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    def get_queryset(self, request):
        qs = super(TopicAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter(faq__organisations__in=request.user.get_organisations())
        return qs

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.user.is_superuser:
            return super(TopicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "faq":
            kwargs["queryset"] = FAQ.objects.filter(organisations__in=request.user.get_organisations())
        return super(TopicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'sort_order', 'created_by', 'created_on',
                    'updated_by', 'updated_on', 'status']
    list_editable = ['sort_order', 'status']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("created_by", "updated_by", "created_on", "updated_on", "slug" )
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter(topic__faq__organisations__in=request.user.get_organisations())
        return qs

    def save_model(self, request, obj, form, change): 
        '''
        Update created-by / modified-by fields.
        
        The date fields are upadated at the model layer, but that's not got
        access to the user.
        '''
        # If the object's new update the created_by field.
        if not change:
            obj.created_by = request.user
        
        # Either way update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.user.is_superuser:
            return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "topic":
            kwargs["queryset"] = Topic.objects.filter(faq__organisations__in=request.user.get_organisations())
        return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(FAQ, FAQAdmin)
