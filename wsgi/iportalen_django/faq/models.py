import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
from .managers import QuestionManager
from organisations.models import Organisation


class FAQ(models.Model):
    name = models.CharField(_('namn'), max_length=150)
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        default=None,
        verbose_name='Ägare',
        help_text="Organisation(er) som äger FAQ:n. Håll ner Ctrl för att markera flera.")

    def __str__(self):
        return self.name


class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    name = models.CharField(_('namn'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150, unique=True)
    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the topic to be displayed.'))
    faq = models.ForeignKey(FAQ, verbose_name=_('FAQ'), max_length=150, related_name="topics", null=True, blank=False)

    def get_absolute_url(self):
        return reverse('faq:faq_topic_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Create a unique slug, if needed.
        if not self.slug:
            suffix = 0
            potential = base = slugify(self.name[:90])
            while not self.slug:
                if suffix:
                    potential = "%s-%s" % (base, suffix)
                if not Topic.objects.filter(slug=potential).exists():
                    self.slug = potential
                # We hit a conflicting slug; increment the suffix and try again.
                suffix += 1

        super(Topic, self).save(*args, **kwargs)


class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,    _('Active')),
        (INACTIVE,  _('Inactive')),
        (HEADER,    _('Group Header')),
    )
    
    text = models.TextField(_('fråga'))
    answer = models.TextField(_('svar'), null=True, blank=False)
    topic = models.ForeignKey(Topic, verbose_name=_('ämne'), related_name='questions')
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    status = models.IntegerField(_('status'),
        choices=STATUS_CHOICES, default=ACTIVE,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed. Questions marked as 'Group Header' are treated "
                    "as such by views and templates that are set up to use them."))
    
    protected = models.BooleanField(_('is protected'), default=False,
        help_text=_("Set true if this question is only visible by authenticated users."))

    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    created_on = models.DateTimeField(_('created on'), default=datetime.datetime.now)
    updated_on = models.DateTimeField(_('updated on'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
        null=True, related_name="+")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('updated by'),
        null=True, related_name="+")  
    
    objects = QuestionManager()
    
    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'created_on']

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        # Set the date updated.
        self.updated_on = datetime.datetime.now()
        
        # Create a unique slug, if needed.
        if not self.slug:
            suffix = 0
            potential = base = slugify(self.text[:90])
            while not self.slug:
                if suffix:
                    potential = "%s-%s" % (base, suffix)
                if not Question.objects.filter(slug=potential).exists():
                    self.slug = potential
                # We hit a conflicting slug; increment the suffix and try again.
                suffix += 1
        
        super(Question, self).save(*args, **kwargs)

    def is_header(self):
        return self.status == Question.HEADER

    def is_active(self):
        return self.status == Question.ACTIVE

    def get_absolute_url(self):
        return reverse('faq:faq_question_detail', args=[str(self.topic.slug), str(self.slug)])