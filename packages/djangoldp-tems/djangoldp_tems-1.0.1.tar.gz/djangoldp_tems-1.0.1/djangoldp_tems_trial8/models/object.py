from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_object import baseTEMSObject
from djangoldp_tems_trial8.models.category import Trial8Category
from djangoldp_tems_trial8.models.compatibility import Trial8Compatibility
from djangoldp_tems_trial8.models.format import Trial8Format
from djangoldp_tems_trial8.models.keyword import Trial8Keyword
from djangoldp_tems_trial8.models.location import Trial8Location


class Trial8Object(baseTEMSObject):
    identifier = models.CharField(max_length=255, blank=True, null=True, default="")
    historical_period = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    polygons = models.IntegerField(blank=True, null=True, default=0)
    summits = models.IntegerField(blank=True, null=True, default=0)
    geometry = models.TextField(blank=True, null=True, default="")
    uv_layers = models.BooleanField(default=False)
    vertex_colors = models.BooleanField(default=False)
    rigged_geometry = models.BooleanField(default=False)
    file_size = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    vertives = models.IntegerField(blank=True, null=True, default=0)
    textures = models.IntegerField(blank=True, null=True, default=0)
    materials = models.IntegerField(blank=True, null=True, default=0)
    animations = models.IntegerField(blank=True, null=True, default=0)
    original_material = models.TextField(blank=True, null=True, default="")
    format = models.ForeignKey(
        Trial8Format, blank=True, null=True, on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        Trial8Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    location = models.ForeignKey(
        Trial8Location, blank=True, null=True, on_delete=models.SET_NULL
    )
    keywords = models.ManyToManyField(Trial8Keyword, blank=True)
    compatibilities = models.ManyToManyField(Trial8Compatibility, blank=True)

    def __str__(self):
        return self.title or self.urlid

    class Meta(baseTEMSObject.Meta):
        container_path = "/objects/trial8/"
        verbose_name = _("TEMS Trial 8 Object")
        verbose_name_plural = _("TEMS Trial 8 Objects")

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
            "identifier",
            "historical_period",
            "polygons",
            "summits",
            "geometry",
            "uv_layers",
            "vertex_colors",
            "rigged_geometry",
            "file_size",
            "vertives",
            "textures",
            "materials",
            "animations",
            "original_material",
            "format",
            "category",
            "location",
            "keywords",
            "compatibilities",
        ]
        nested_fields = [
            "licences",
            "images",
            "format",
            "category",
            "location",
            "keywords",
            "compatibilities",
        ]
        rdf_type = "tems:Object"
