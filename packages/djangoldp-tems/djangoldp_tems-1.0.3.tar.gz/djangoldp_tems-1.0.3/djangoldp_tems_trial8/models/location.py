from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel


class Trial8Location(baseTEMSModel):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    address = models.CharField(max_length=254, blank=True, null=True, default="")
    city = models.CharField(max_length=100, blank=True, null=True, default="")
    state = models.CharField(max_length=100, blank=True, null=True, default="")
    country = models.CharField(max_length=100, blank=True, null=True, default="")
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=7, default=0)
    elevation = models.IntegerField(blank=True, null=True, default=0, help_text=_("Elevation in meters"))

    def __str__(self):
        return self.name or self.urlid

    class Meta(baseTEMSModel.Meta):
        container_path = "/objects/locations/trial8/"
        verbose_name = _("TEMS Location")
        verbose_name_plural = _("TEMS Locations")
        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "address",
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "elevation",
        ]
        nested_fields = []
        rdf_type = "tems:Location"
