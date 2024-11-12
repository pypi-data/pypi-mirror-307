from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel


class TEMSLicence(baseTEMSModel):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    short_desc = models.CharField(max_length=255, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    url = models.CharField(max_length=2000, blank=True, null=True, default="")

    def __str__(self):
        return self.name or self.url or self.urlid

    class Meta(baseTEMSModel.Meta):
        container_path = "/objects/licences/"
        verbose_name = _("TEMS Licence")
        verbose_name_plural = _("TEMS Licences")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "short_desc",
            "description",
            "url",
        ]
        nested_fields = []
        rdf_type = "tems:Licence"
