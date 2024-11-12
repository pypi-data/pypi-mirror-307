from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_object import baseTEMSObject


class Trial6Object(baseTEMSObject):
    subtitle = models.CharField(max_length=255, blank=True, null=True, default="")
    editor = models.CharField(max_length=255, blank=True, null=True, default="")
    contributors = models.TextField(blank=True, null=True, default="")
    url = models.CharField(max_length=255, blank=True, null=True, default="")

    class Meta(baseTEMSObject.Meta):
        container_path = "/objects/trial6/"
        verbose_name = _("TEMS Trial 6 Object")
        verbose_name_plural = _("TEMS Trial 6 Objects")

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
            "subtitle",
            "editor",
            "contributors",
            "url",
            "assets",
        ]
        nested_fields = [
            "licences",
            "assets",
            "images",
        ]
        rdf_type = "tems:Object"
