from django.contrib import admin
from djangoldp_tems_trial8.models import *

from djangoldp_tems.admin import TemsModelAdmin

admin.site.register(Trial8Category, TemsModelAdmin)
admin.site.register(Trial8Compatibility, TemsModelAdmin)
admin.site.register(Trial8Format, TemsModelAdmin)
admin.site.register(Trial8Keyword, TemsModelAdmin)
admin.site.register(Trial8Location, TemsModelAdmin)
admin.site.register(Trial8Object, TemsModelAdmin)
