from django.contrib import admin
from .models import Route, Workflow, Note, RouteWorkflow

admin.site.register(Route)
admin.site.register(Workflow)
admin.site.register(Note)
admin.site.register(RouteWorkflow)
# admin.site.register(Role)

