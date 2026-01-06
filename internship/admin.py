from django.contrib import admin
from .models import Internship,StipendType,SubjectType,ProjectType,ToolsType

admin.site.register(Internship)
admin.site.register(StipendType)
admin.site.register(SubjectType)
admin.site.register(ProjectType)
admin.site.register(ToolsType)