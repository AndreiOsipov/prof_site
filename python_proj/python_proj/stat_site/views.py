from django.shortcuts import render
from .models import Professions,ProfessionImages, YaersAnalitics, LocationAnaliticsWithProfession, ProfessionalYaersAnalitics, ProfessionalSkillsByYear, LocationAnalitics 
# Create your views here.
def ret_welcome_page(request):
    return render(request,template_name="stat_site/base.html")
def ret_main_page(request):
    profession = Professions.objects.first()
    photos  = ProfessionImages.objects.filter(profession_id=profession.profession_id)
    context = {
        'profession': profession,
        'photos': photos
    }
    return render(request, template_name='stat_site/prof_page.html', context=context)

def ret_demand_page(request):
    profession = Professions.objects.first()
    years_anatics = YaersAnalitics.objects.all()
    location_anatics = LocationAnalitics.objects.all()

    prof_years_anatics = ProfessionalYaersAnalitics.objects.filter(profession_id = profession.profession_id)
    prof_location_anatics = LocationAnaliticsWithProfession.objects.filter(profession_id = profession.profession_id)
    
    context = {
        'years_analitics':years_anatics,
        'prof_years_anatics':prof_years_anatics,
        'location_anatics':location_anatics,
        'prof_location_anatics':prof_location_anatics
        }
    
    return render(request, template_name="stat_site/demadn_page.html",context=context)

def ret_location_page(request):
    profession = Professions.objects.first()
    locations_anaticis = LocationAnalitics.objects.all()
    prof_location_analicis = LocationAnaliticsWithProfession.objects.filter(profession_id = profession.profession_id)
    context = {
        'locations': locations_anaticis,
        'prof_locations': prof_location_analicis,
    }

    return render(request, template_name="stat_site/locations_page.html", context=context)

def ret_skills_page(request):
    profession = Professions.objects.first()
    skills = ProfessionalSkillsByYear.objects.filter(profession_id = profession.profession_id)
    context = {'skills_by_year': skills}
    return render(request,"stat_site/skills_page.html",context=context)

def ret_last_vacancys_page(request):
    return render(request,"stat_site/last_vacncies.html")