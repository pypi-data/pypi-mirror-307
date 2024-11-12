from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel


class Trial8Category(baseTEMSModel):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        return self.name or self.urlid

    class Meta(baseTEMSModel.Meta):
        container_path = "/objects/categories/trial8/"
        verbose_name = _("TEMS Category")
        verbose_name_plural = _("TEMS Categories")
        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
        ]
        nested_fields = []
        rdf_type = "tems:Category"
