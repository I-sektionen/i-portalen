from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.files.base import ContentFile
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from PIL import Image
import io
import os
from tags.models import Tag
from utils.validators import less_than_160_characters_validator
from utils import time
from organisations.models import Organisation
from .managers import ArticleManager


class Article(models.Model):
    DRAFT = 'd'
    BEING_REVIEWED = 'b'
    REJECTED = 'r'
    APPROVED = 'a'
    STATUSES = (
        (DRAFT, _("Utkast")),
        (BEING_REVIEWED, _("väntar på godkännande")),
        (REJECTED, _("Avslaget")),
        (APPROVED, _("Godkännt"))
    )
    headline = models.CharField(
        verbose_name=_("rubrik"),
        max_length=255,
        help_text=_("Rubriken till artikeln"))
    lead = models.TextField(
        verbose_name=_("ingress"),
        help_text=_("Ingressen är den text som syns i nyhetsflödet. Max 160 tecken."),
        validators=[less_than_160_characters_validator])
    body = models.TextField(
        verbose_name=_("brödtext"),
        help_text=_("Brödtext syns när en artikel visas enskilt."))
    visible_from = models.DateTimeField(
        verbose_name=_("publicering"),
        help_text=_("Publiceringsdatum"),
        default=time.now)
    visible_to = models.DateTimeField(
        verbose_name=_("avpublicering"),
        help_text=_("Avpubliceringsdatum"),
        default=time.now_plus_one_month)
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=DRAFT,
        blank=False,
        null=False)
    rejection_message = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som skrivit texten"),
        null=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tag"),
        blank=True,
        help_text=_("Håll ner Ctrl för att markera flera."))

    attachment = models.FileField(
        verbose_name=_("Bifogad fil"),  # This field should be removed. It is saved by legacy reasons.
        help_text=_("Bifogad fil för artikel"),  # TODO: When no articles uses this field, remove it.(Tricky to migrate)
        upload_to=_("article_attachments"),
        null=True,
        blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        verbose_name=_("organisationer"),
        help_text=_("Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln."
                    " Håll ner Ctrl för att markera flera."))
    sponsored = models.BooleanField(
        verbose_name=_("sponsrat"),
        default=False,
        help_text=_("Kryssa i om innehållet är sponsrat"))
    objects = ArticleManager()  # Manager

    ###########################################################################
    # Meta data for model
    ###########################################################################
    class Meta:
        verbose_name = _("Artikel")
        verbose_name_plural = _("Artiklar")
        permissions = (('can_approve_article', 'Can approve article'),)

    ###########################################################################
    # Overridden and standard functions
    ###########################################################################

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return self.headline

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('articles:article', kwargs={'pk': self.pk})

    ###########################################################################
    # Properties reachable in template
    ###########################################################################

    def _type(self):
        """Return model name"""
        return "article"

    type = property(_type)

    ###########################################################################
    # Member function
    ###########################################################################

    def filename(self):
        return os.path.basename(self.attachment.name)

    def can_administer(self, user):
        if not user.is_authenticated():
            return False
        article_orgs = self.organisations.all()
        user_orgs = user.get_organisations()
        intersection = set(article_orgs).intersection(user_orgs)
        # Like a venn diagram where the intersections is the organisations that both the user and the event have.
        if intersection:
            return True
        if self.user == user:
            return True
        if user.has_perm("articles.can_approve_article"):
            return True
        return False

    def get_new_status(self, draft):  # TODO: Reduce complexity
        try:
            s_db = Article.objects.get(pk=self.pk)
            if s_db.status == self.DRAFT:
                if draft:
                    return {"new": False, "status": self.DRAFT}
                else:
                    return {"new": False, "status": self.BEING_REVIEWED}
            elif s_db.status == self.BEING_REVIEWED:
                if draft:
                    return {"new": False, "status": self.DRAFT}
                else:
                    return {"new": False, "status": self.BEING_REVIEWED}
            elif s_db.status == self.APPROVED:
                if draft:
                    return {"new": True, "status": self.DRAFT}
                else:
                    return {"new": True, "status": self.BEING_REVIEWED}
            elif s_db.status == self.REJECTED:
                if draft:
                    return {"new": False, "status": self.DRAFT}
                else:
                    return {"new": False, "status": self.BEING_REVIEWED}
        except:
            if draft:
                return {"new": False, "status": self.DRAFT}
            else:
                return {"new": False, "status": self.BEING_REVIEWED}

    # Rejects an event from being published, attaches message if present.
    def reject(self, user, msg=None):
        if not user.has_perm('articles.can_approve_article'):
            return False
        if self.status == self.BEING_REVIEWED:
            if msg:
                send_mail(
                    ugettext("Din artikel har blivit avslagen."),
                    "",
                    settings.EMAIL_HOST_USER,
                    [self.user.email, ],
                    fail_silently=False,
                    html_message="".join(["<p>",
                                          ugettext("Din artikel"),
                                          " {head} ",
                                          ugettext("har blivit avslagen med motiveringen:"),
                                          "</p><p>{msg}</p>"]).format(head=self.headline, msg=msg))
            self.rejection_message = msg
            self.status = self.REJECTED
            self.save()
            return True
        return False

    # Approves the event.
    @transaction.atomic
    def approve(self, user):
        if self.status == self.BEING_REVIEWED and user.has_perm('articles.can_approve_article'):
            self.status = self.APPROVED
            self.save()
            if self.replacing:

                exclude = ["article",
                           "id",
                           "created",
                           "modified",
                           "replacing",
                           "imageattachment",
                           "otherattachment"]
                multi = ["tags", "organisations"]
                for field in self.replacing._meta.get_fields():
                    if field.name not in exclude:
                        if field.name not in multi:
                            setattr(self.replacing, field.name, getattr(self, field.name))
                        else:
                            getattr(self.replacing, field.name).clear()
                            setattr(self.replacing, field.name, getattr(self, field.name).all())
                self.delete()
                self.replacing.save()
            return True
        return False

###########################################################################
# Attachment Models
###########################################################################


def _image_file_path(instance, filename):
    """Returns the subfolder in which to upload images for articles. This results in media/article/img/<filename>"""
    return os.path.join(
        'article', str(instance.article.pk), 'images', filename
    )


THUMB_SIZE = (129, 129)  # Size of saved thumbnails.


class ImageAttachment(models.Model):
    """Used to handle image attachments to be shown in the article"""
    img = models.ImageField(
        upload_to=_image_file_path,
        null=False,
        blank=False,
        verbose_name='artikelbild'
    )
    thumbnail = models.ImageField(
        upload_to=_image_file_path,
        null=True,
        blank=True,
        verbose_name='förhandsvisning'
    )
    caption = models.CharField(max_length=100)
    article = models.ForeignKey(Article,
                                null=False,
                                blank=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='användare',
        help_text="Uppladdat av.",
        null=True,
        on_delete=models.SET_NULL)

    def _set_thumbnail(self):
        if self.thumbnail:
            return  # This means no updates! (Otherwise it double saves.)
        path = self.img.path
        try:
            image = Image.open(path)
        except IOError:
            print("Could not open!")
            raise
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumb_name_path, thumb_extension = os.path.splitext(self.img.name)
        thumb_extension = thumb_extension.lower()
        a, thumb_name = os.path.split(thumb_name_path)
        thumb_file_name = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            print('Wrong file extension!')
            return False    # Unrecognized file type

        temp_thumb = io.BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_file_name, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
        return True

    def save(self, *args, **kwargs):
        super(ImageAttachment, self).save(*args, **kwargs)  # It saves first to set the main img.
        self._set_thumbnail()  # Then it generates the thumbnail, and saves again.
        #  It seems the model must be saved once in order to open the img and generate the thumbnail.
        #  This means that a thumbnail only cna be generated once. Since if it is set the _set_thumbnail method
        #  Wont run.

    def __str__(self):
        return os.path.basename(self.img.name) + " (Artikel: " + str(self.article.pk) + ")"

# Clean up when model is removed
@receiver(pre_delete, sender=ImageAttachment)
def other_attachment_delete(sender, instance, **kwargs):
    instance.img.delete(False)  # False avoids saving the model.
    instance.thumb.delete(False)


def _file_path(instance, filename):
    return os.path.join(
        'article', str(instance.article.pk), 'attachments', filename
    )


class OtherAttachment(models.Model):
    """"Regular attachments such as pdf:s and it's like."""

    file = models.FileField(
        upload_to=_file_path,
        null=False,
        blank=False,
        verbose_name='artikelbilaga',
    )
    display_name = models.CharField(max_length=160, null=False, blank=False)
    file_name = models.CharField(max_length=300, null=False, blank=True)
    article = models.ForeignKey(Article,
                                null=False,
                                blank=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='användare',
        help_text="Uppladdat av.",
        null=True,
        on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.file_name = os.path.basename(self.file.name)
        super(OtherAttachment, self).save(*args, **kwargs)

    def __str__(self):
        return self.display_name + " (" + self.file_name + ")" + "för artikel: " + str(self.article)


#  This receiver part here makes sure to remove files if the model instance is deleted.
@receiver(pre_delete, sender=OtherAttachment)
def other_attachment_delete(sender, instance, **kwargs):
    instance.file.delete(False)  # False avoids saving the model.
