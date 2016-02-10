from django.contrib import admin
from django.utils import timezone

from . import models
from utils.admin import iportalen_admin_site
from django.db.models import Q, ManyToManyField
from django.contrib.admin.widgets import FilteredSelectMultiple
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class OptionsInline(NestedStackedInline):
    model = models.Option
    fk_name = 'question'
    extra = 1
    editable_fields = []

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class QuestionInline(NestedStackedInline):
    model = models.Question
    fk_name = 'question_group'
    extra = 1
    readonly_fields = ('modified_by',)
    list_display = ['name', 'status']
    list_editable = ['status']
    formfield_overrides = {ManyToManyField: {'widget': FilteredSelectMultiple(
        "Användare som kan se resultatet", is_stacked=False)}, }

    def get_queryset(self, request):
        qs = super(QuestionInline, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter((
            Q(question_group__visible_from__lte=timezone.now()) &
            Q(question_group__visible_to__gte=timezone.now())) &
            (Q(question_group__organisations__in=request.user.get_organisations()) |
            Q(question_group__creator=request.user)))
        return qs

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        """
        Update modified-by fields.

        The date fields are updated at the model layer, but that's not got
        access to the user.
        """

        obj.modified_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionInline, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    inlines = [OptionsInline, ]


class OptionsInlineHidden(NestedStackedInline):
    model = models.Option
    fk_name = 'question'
    extra = 0
    readonly_fields = ('name',)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        return False


class QuestionInlineHidden(NestedStackedInline):
    model = models.Question
    fk_name = 'question_group'
    extra = 0
    readonly_fields = (
        'modified_by',
        'result_readers',
        'anonymous',
        'nr_of_picks',
        'publish_results',
        'result',
        'body',
        'name',
        'question_group')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        return False
    inlines = [OptionsInlineHidden, ]


class QuestionGroupAdmin(NestedModelAdmin):
    readonly_fields = ('creator',)

    def get_queryset(self, request):
        qs = super(QuestionGroupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter((
            Q(visible_from__lte=timezone.now()) &
            Q(visible_to__gte=timezone.now())) &
            (Q(organisations__in=request.user.get_organisations()) | Q(creator=request.user)))
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('event', 'question_status')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    inlines = [QuestionInlineHidden, QuestionInline]


iportalen_admin_site.register(models.QuestionGroup, QuestionGroupAdmin)
