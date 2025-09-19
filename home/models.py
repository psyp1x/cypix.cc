from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils import timezone

class HomePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class AboutPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class ContactPage(Page):
    body = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('email'),
        FieldPanel('address'),
    ]

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['posts'] = BlogPostPage.objects.child_of(self).live().order_by('-date')
        return context

class BlogPostPage(Page):
    date = models.DateField(default=timezone.now)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('author'),
        FieldPanel('category'),
    ]

    parent_page_types = ['home.BlogIndexPage']  # Can only be created under Blog section
