from django.contrib import admin
from .models import Professions, ProfessionalYaersAnalitics, \
    ProfessionalSkillsByYear, LocationAnaliticsWithProfession, ProfessionImages, LocationAnalitics, YaersAnalitics

admin.site.register(Professions)
admin.site.register(ProfessionalYaersAnalitics)
admin.site.register(ProfessionalSkillsByYear)
admin.site.register(LocationAnaliticsWithProfession)
admin.site.register(ProfessionImages)
admin.site.register(LocationAnalitics)
admin.site.register(YaersAnalitics)
# Register your models here.
