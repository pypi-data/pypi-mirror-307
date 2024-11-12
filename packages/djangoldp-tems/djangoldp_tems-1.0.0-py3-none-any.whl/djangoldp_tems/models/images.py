from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel


class TEMSImages(baseTEMSModel):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    url = models.CharField(max_length=2000, blank=True, null=True, default="")

    class Meta(baseTEMSModel.Meta):
        container_path = "/objects/images/"
        verbose_name = _("TEMS Image")
        verbose_name_plural = _("TEMS Images")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "url",
        ]
        nested_fields = []
        rdf_type = "tems:Image"
