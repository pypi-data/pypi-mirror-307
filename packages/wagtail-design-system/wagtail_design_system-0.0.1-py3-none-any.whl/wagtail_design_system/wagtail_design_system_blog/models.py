from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count
from django.db.models.expressions import F
from django.forms.widgets import Textarea
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, TitleFieldPanel
from wagtail.admin.widgets.slug import SlugInput
from wagtail.contrib.forms.models import AbstractFormField, EmailFormMixin, FormMixin
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable
from wagtail.models.i18n import Locale, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtail_design_system.managers import TagManager
from wagtail_design_system.models import ContentPage, Tag, WagtailDesignSystemBasePage, WagtailDesignSystemConfig
from wagtail_design_system.wagtail_design_system_blog.blocks import COLOPHON_BLOCKS
from wagtail_design_system.wagtail_design_system_blog.managers import CategoryManager
from wagtail_design_system.wagtail_design_system_forms.widgets import WagtailDesignSystemFormsRadioSelect
from wagtail_design_system.widgets import WagtailDesignSystemIconPickerWidget


User = get_user_model()


class BlogIndexPage(ContentPage):
    posts_per_page = models.PositiveSmallIntegerField(
        default=10,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        verbose_name=_("Posts per page"),
    )

    settings_panels = ContentPage.settings_panels + [
        FieldPanel("posts_per_page"),
    ]

    subpage_types = ["wagtail_design_system.BlogEntryPage", "wagtail_design_system.DirectoryEntryPage"]

    class Meta:
        verbose_name = _("Blog index")

    order_by = "-date"

    @property
    def posts(self):
        # Get list of blog pages that are descendants of this page
        posts = BlogEntryPage.objects.descendant_of(self).live()
        posts = (
            posts.order_by(self.order_by)
            .select_related("owner")
            .prefetch_related("tags", "blog_categories", "date__year")
        )
        return posts

    def get_context(self, request, tag=None, category=None, author=None, year=None, *args, **kwargs):  # NOSONAR
        # context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context = super().get_context(request, *args, **kwargs)

        posts = self.posts
        locale = Locale.objects.get(language_code=get_language())

        breadcrumb = None

        if tag is None:
            tag = request.GET.get("tag")
        if tag:
            tag = get_object_or_404(Tag, slug=tag)
            posts = posts.filter(tags__slug=tag.slug)
            breadcrumb = {
                "links": [
                    {"url": self.get_url(), "title": self.title},
                    {
                        "url": reverse("wagtail_design_system_blog:tags_list", kwargs={"blog_slug": self.slug}),
                        "title": _("Tags"),
                    },
                ],
                "current": tag,
            }

        if category is None:  # Not coming from category_view in views.py
            if request.GET.get("category"):
                category = get_object_or_404(
                    Category,
                    slug=request.GET.get("category"),
                    locale=locale,
                )
        if category:
            if not request.GET.get("category"):
                category = get_object_or_404(Category, slug=category, locale=locale)
            posts = posts.filter(blog_categories__slug=category.slug)

            breadcrumb = {
                "links": [
                    {"url": self.get_url(), "title": self.title},
                    {
                        "url": reverse("wagtail_design_system_blog:categories_list", kwargs={"blog_slug": self.slug}),
                        "title": _("Categories"),
                    },
                ],
                "current": category.name,
            }
        if author:
            author = get_object_or_404(User, id=author)

            breadcrumb = {
                "links": [
                    {"url": self.get_url(), "title": self.title},
                ],
                "current": _("Posts written by") + f" {author.first_name} {author.last_name}",
            }
            posts = posts.filter(owner=author)

        if year:
            posts = posts.filter(date__year=year)

        # Pagination
        page = request.GET.get("page")
        page_size = self.posts_per_page

        paginator = Paginator(posts, page_size)  # Show <page_size> posts per page
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        if category is not None:
            context["category"] = category.name
            context["category_description"] = category.description
        context["tag"] = tag
        context["author"] = author
        context["year"] = year
        context["paginator"] = paginator

        if breadcrumb:
            context["breadcrumb"] = breadcrumb

        return context

    def list_categories(self) -> list:
        posts = self.posts.specific()
        return (
            posts.values(
                cat_slug=F("blog_categories__slug"),
                cat_name=F("blog_categories__name"),
            )
            .annotate(cat_count=Count("cat_slug"))
            .filter(cat_count__gte=1)
            .order_by("-cat_count")
        )

    def list_tags(self, min_count: int = 1) -> list:
        posts = self.posts.specific()
        return (
            posts.values(tag_name=F("tags__name"), tag_slug=F("tags__slug"))
            .annotate(tag_count=Count("tag_slug"))
            .filter(tag_count__gte=min_count)
            .order_by("-tag_count")
        )


class DirectoryIndexPage(BlogIndexPage):
    order_by = "title"

    subpage_types = ["wagtail_design_system.DirectoryEntryPage"]

    class Meta:
        verbose_name = _("Directory Index")


@register_snippet
class Person(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    role = models.CharField(_("Role"), max_length=255)
    organization = models.CharField(_("Organization"), max_length=255)
    contact_info = models.CharField(_("Contact info"), max_length=500, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("organization"),
        FieldPanel("contact_info"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Person")


class BlogEntryPage(ContentPage):
    #  tags = ClusterTaggableManager(through="TagEntryPage", blank=True)
    blog_categories = ParentalManyToManyField(
        "Category",
        through="CategoryEntryPage",
        blank=True,
        verbose_name=_("Categories"),
    )
    date = models.DateTimeField(verbose_name=_("Post date"), default=timezone.now)
    authors = ParentalManyToManyField(
        "wagtail_design_system.Person", blank=True, help_text=_("Author entries can be created in Snippets > Persons")
    )

    parent_page_types = ["wagtail_design_system.BlogIndexPage", "wagtail_design_system.DirectoryIndexPage"]
    subpage_types = []

    settings_panels = ContentPage.settings_panels + [
        FieldPanel("authors"),
        FieldPanel("date"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("go_live_at"),
                        FieldPanel("expire_at"),
                    ],
                    classname="label-above",
                ),
            ],
            _("Scheduled publishing"),
            classname="publishing",
        ),
        MultiFieldPanel(
            [
                FieldPanel("blog_categories"),
                FieldPanel("tags"),
            ],
            heading=_("Tags and Categories"),
        ),
    ]

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = _("Blog page")


# class ContentOrBlogPage(ContentPage, BlogEntryPage):
#     pass


@register_snippet
class Category(TranslatableMixin, index.Indexed, models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=_("Category name"))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_("Parent category"),
        on_delete=models.SET_NULL,
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Displayed on the top of the category page"),
    )
    colophon = StreamField(
        COLOPHON_BLOCKS,
        blank=True,
        use_json_field=True,
        help_text=_("Text displayed at the end of every page in the category"),
    )
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_("Parent category cannot be self."))
            if parent.parent and parent.parent == self:
                raise ValidationError(_("Cannot have circular Parents."))
            if parent.parent and parent.parent.parent and parent.parent.parent == self:
                raise ValidationError(_("Cannot have circular Grand Parents."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("slug", widget=SlugInput),
        FieldPanel("description"),
        FieldPanel("colophon"),
        FieldPanel("parent"),
    ]

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        unique_together = [
            ("translation_key", "locale"),
            ("name", "locale"),
            ("slug", "locale"),
        ]

    search_fields = [index.SearchField("name")]


class DirectoryEntryPage(BlogEntryPage):
    class Meta:
        verbose_name = _("Directory Entry")
        verbose_name_plural = _("Directory Entries")

    parent_page_types = ["wagtail_design_system.DirectoryIndexPage"]


class CategoryEntryPage(models.Model):
    category = models.ForeignKey(Category, related_name="+", verbose_name=_("Category"), on_delete=models.CASCADE)
    page = ParentalKey("BlogEntryPage", related_name="entry_categories")
    panels = [FieldPanel("category")]

    def __str__(self):
        return self.category


class TagEntryPage(TaggedItemBase):
    content_object = ParentalKey("BlogEntryPage", related_name="entry_tags")
