from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager

from core.models import TimeStampedModel


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class BlogManager(models.Manager):

    def publicly_viewable(self):
        """
        Return blog posts that have a status of 'published' and date_published
        that is less than or equal to the current date and time.
        """
        return self.select_related().filter(
            date_published__lte=datetime.now(),
            status__iexact='published'
        )

    def recent_posts(self, count=5):
        """
        Return the most recent posts, defaults to the last 5 by date published.
        """
        return self.publicly_viewable().order_by('-date_published')[:count]


class Blog(TimeStampedModel):
    author = models.ForeignKey(User)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )
    title = models.CharField(max_length=250)
    slug = AutoSlugField(
        max_length=255,
        null=False,
        blank=False,
        populate_from='title',
        editable=True,
        unique=True,
        db_index=True
    )
    content = models.TextField()
    date_published = models.DateTimeField(null=True, blank=True)
    tags = TaggableManager(blank=True, help_text=None)

    @property
    def is_published(self):
        return self.status == 'published'

    def preview_link(self):
        if self.slug:
            return '<a href="%s" target="_blank">%s</a> (will open in a new' \
                   ' window, make sure to save your changes first)' % \
                   (reverse('blog_detail_view', args=[self.slug]), self.title)
        else:
            return 'Not available (you must save this article first)'
    preview_link.allow_tags = True

    objects = BlogManager()

    def __unicode__(self):
        return self.title
