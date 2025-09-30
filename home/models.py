from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, HelpPanel, TitleFieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model

from modelcluster.fields import ParentalKey

# Model for gallery images linked to HomePage
class HomePageGalleryImage(Orderable):
    page = ParentalKey(
        'home.HomePage',
        related_name='gallery_images',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        get_image_model(),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='+',
    )

class HomePage(Page):

    template = "home/home_page.html"
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    custom_document = models.ForeignKey(
        get_document_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    cta_url = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    # Renamed field from cta_external_url to youtube_url, with default set to https://www.youtube.com
    youtube_url = models.URLField(blank=True, null=True, default='https://www.youtube.com')

    content_panels = Page.content_panels + [
        TitleFieldPanel(
            'subtitle',
            help_text='The subtitle will appear below the title',
            placeholder='Enter your subtitle',
        ),
        InlinePanel(
            'gallery_images',
            label="Gallery images",
            min_num=2,
            max_num=4,
        ),
        MultiFieldPanel(
            [
                HelpPanel(
                    content="<strong>Help Panel</strong><p>Help text goes here</p>",
                    heading="Note:",
                ),
                FieldRowPanel(
                    [
                        PageChooserPanel(
                            'cta_url',
                            'blogpages.BlogDetail',
                            help_text='Select the approriate blog page',
                            heading='Blog Page Selection',
                            classname="col6"
                        ),
                        FieldPanel(
                            'youtube_url',
                            help_text='Enter the external Youtube URL',
                            heading='Youtube URL',
                            classname="col6"
                        ),
                    ],
                    help_text="Select a page or enter a URL",
                    heading="Call to action URLs"
                ),
            ],
            heading="MultiFieldPanel Demo",
            help_text='Random help text',
        )
    ]

    @property
    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.youtube_url:
            return self.youtube_url
        else:
            return None

    def clean(self):
        super().clean()

        if self.cta_url and self.youtube_url:
            raise ValidationError({
                'cta_url': 'You can only have one CTA URL',
                'youtube_url': 'You can only have one CTA URL',
            })
