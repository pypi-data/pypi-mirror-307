from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel
from djangoldp_tems_trial6.models.category import Trial6Category
from djangoldp_tems_trial6.models.format import Trial6Format
from djangoldp_tems_trial6.models.object import Trial6Object


class Trial6Asset(baseTEMSModel):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    size = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    format = models.ForeignKey(Trial6Format, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Trial6Category, blank=True, null=True, on_delete=models.SET_NULL)
    object = models.ForeignKey(
        Trial6Object,
        on_delete=models.CASCADE,
        related_name="assets",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name or self.urlid

    class Meta(baseTEMSModel.Meta):
        container_path = "/objects/assets/trial6/"
        verbose_name = _("TEMS Asset")
        verbose_name_plural = _("TEMS Assets")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "size",
            "format",
            "category",
        ]
        nested_fields = [
            "format",
            "category",
        ]
        rdf_type = "tems:Asset"
