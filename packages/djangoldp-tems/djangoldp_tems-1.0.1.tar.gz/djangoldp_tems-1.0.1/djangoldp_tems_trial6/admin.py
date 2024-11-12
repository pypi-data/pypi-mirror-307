from django.contrib import admin
from djangoldp_tems_trial6.models import *

from djangoldp_tems.admin import TemsModelAdmin

admin.site.register(Trial6Asset, TemsModelAdmin)
admin.site.register(Trial6Category, TemsModelAdmin)
admin.site.register(Trial6Format, TemsModelAdmin)
admin.site.register(Trial6Object, TemsModelAdmin)
