from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model

from djangoldp_tems.models.__base_model import baseTEMSModel
from djangoldp_tems.models.images import TEMSImages
from djangoldp_tems.models.licence import TEMSLicence


class baseTEMSObject(baseTEMSModel):
    title = models.CharField(max_length=254, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    copyright = models.CharField(max_length=254, blank=True, null=True, default="")
    website = models.CharField(max_length=2000, blank=True, null=True, default="")
    licences = models.ManyToManyField(TEMSLicence, blank=True)
    images = models.ManyToManyField(TEMSImages, blank=True)

    class Meta(Model.Meta):
        abstract = True
        verbose_name = _("Base TEMS Object")
        verbose_name_plural = _("Base TEMS Objects")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "title",
            "description",
            "copyright",
            "website",
            "licences",
            "images",
        ]
        nested_fields = [
            "licences",
            "images",
        ]
