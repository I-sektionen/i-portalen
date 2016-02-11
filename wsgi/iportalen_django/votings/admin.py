from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from . import models
from utils.admin import iportalen_admin_site
from django.db.models import Q, ManyToManyField
from django.contrib.admin.widgets import FilteredSelectMultiple


class OptionsInline(admin.StackedInline):
    model = models.Option
    extra = 1
    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.status != models.Question.DRAFT:  # This is retarded but the obj is the question not the option.
                return self.readonly_fields + ('name',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.status != models.Question.DRAFT:  # This is retarded but the obj is the question not the option.
                return False
        return True

    def has_add_permission(self, request, obj=None):  # This is retarded but you can't add since the name field is hidden.
        return True


class QuestionAdmin(admin.ModelAdmin):
    model = models.Question
    extra = 1
    readonly_fields = ('modified_by',)
    list_display = ['name', 'status']
    list_editable = ['status']
    formfield_overrides = {ManyToManyField: {'widget': FilteredSelectMultiple(
        "Användare som kan se resultatet", is_stacked=False)}, }

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter((
            Q(question_group__visible_from__lte=timezone.now()) &
            Q(question_group__visible_to__gte=timezone.now())) &
            (Q(question_group__organisations__in=request.user.get_organisations()) |
            Q(question_group__creator=request.user)))
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.status != models.Question.DRAFT:  # editing an existing object
                return self.readonly_fields + (
                    'result_readers',
                    'anonymous',
                    'nr_of_picks',
                    'publish_results',
                    'result',
                    'body',
                    'name',
                    'question_group')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Update modified-by fields.

        The date fields are updated at the model layer, but that's not got
        access to the user.
        """

        obj.modified_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        elif obj:
            if obj.status != models.Question.DRAFT:  # This is retarded but the obj is the question not the option.
                return False
        return True

    inlines = [OptionsInline, ]


################################################################


class QuestionInlineHidden(admin.TabularInline):

    def change_url(self):
        if self.id:
            changeform_url = reverse('admin:votings_question_change', args=(self.id,))
            return '<a href="{url}" target="_blank">Ändra</a>'.format(url=changeform_url)
        return ''
    change_url.allow_tags = True
    change_url.short_description = mark_safe('<a href="{url}" target="_blank">Ny fråga</a>'.format(url="/admin/votings/question/add/"))   # omit column header
    model = models.Question
    extra = 0
    fields = ('name', 'status', 'verification', change_url)
    readonly_fields = (
        change_url,
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
        return False

    def has_add_permission(self, request, obj=None):
        return False


class QuestionGroupAdmin(admin.ModelAdmin):
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

    inlines = [QuestionInlineHidden]


iportalen_admin_site.register(models.QuestionGroup, QuestionGroupAdmin)
iportalen_admin_site.register(models.Question, QuestionAdmin)