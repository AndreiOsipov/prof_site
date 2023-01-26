import requests
import re
from django.shortcuts import render
from .models import Professions,ProfessionImages, YaersAnalitics, LocationAnaliticsWithProfession, ProfessionalYaersAnalitics, ProfessionalSkillsByYear, LocationAnalitics 
from .hh_parser import search

class Salary:
    currency_to_rub = {  
        "AZN": 35.68,  
        "BYR": 23.91,  
        "EUR": 59.90,  
        "GEL": 21.74,  
        "KGS": 0.76,  
        "KZT": 0.13,  
        "RUR": 1,  
        "UAH": 1.64,  
        "USD": 60.66,  
        "UZS": 0.0055,  
    }
    def __init__(self, salary_from, salary_to, salary_currency) -> None:
        self.middle_salary =  int(((float(salary_from)+float(salary_to)) * self.currency_to_rub[salary_currency]) / 2)

class Vacancy:
    def __init__(self, name, description, key_skills, salary, employer, pub_date) -> None:
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.salary = salary
        self.employer_name = employer
        self.pub_date = pub_date
        


def get_skill_list(str_skills: str):
    clean_str_skills = str_skills.split()

# Create your views here.
def ret_welcome_page(request):
    return render(request,template_name="stat_site/base.html")

def ret_main_page(request):
    profession = Professions.objects.first()
    db_image  = ProfessionImages.objects.get(image_name='db_admin')
    context = {
        'profession': profession,
        'photo': db_image
    }
    return render(request, template_name='stat_site/prof_page.html', context=context)

def ret_demand_page(request):
    profession = Professions.objects.first()
    years_anatics = YaersAnalitics.objects.all()
    prof_years_anatics = ProfessionalYaersAnalitics.objects.filter(profession_id = profession.profession_id)
    
    profession_images = ProfessionImages.objects.filter(profession_id = profession.profession_id)
    years_prof_vacancies_image = profession_images.get(image_name='years_prof_vacancies')
    years_prof_salaries_image = profession_images.get(image_name = 'years_prof_salaries')
    years_salaries_image = ProfessionImages.objects.get(image_name = 'years_salaries')
    years_vacancies_image = ProfessionImages.objects.get(image_name = 'years_vacancies')

    context = {
        'years_analitics':years_anatics,
        'prof_years_anatics':prof_years_anatics,   
        'years_vacancies_image':years_vacancies_image,
        'years_prof_vacancies_image': years_prof_vacancies_image,
        'years_salaries_image': years_salaries_image,
        'years_prof_salaries_image': years_prof_salaries_image
    }
    
    return render(request, template_name="stat_site/demadn_page.html",context=context)

def ret_location_page(request):
    profession = Professions.objects.first()
    locations_anaticis = LocationAnalitics.objects.all()

    locations_by_salaries = locations_anaticis.order_by('-middle_salary')
    locations_by_vacancies = locations_anaticis.order_by('-vacancies_share')
    prof_location_analicis = LocationAnaliticsWithProfession.objects.filter(profession_id = profession.profession_id)
    prof_locations_by_salaries = prof_location_analicis.order_by('-middle_salary')
    prof_locations_by_vacancies = prof_location_analicis.order_by('-vacancies_share')


    city_prof_salaries = ProfessionImages.objects.get(image_name='cities_prof_salaries')
    city_prof_vacancies = ProfessionImages.objects.get(image_name='cities_prof_vacancies')
    cities_salaries = ProfessionImages.objects.get(image_name='cities_calaries')
    cities_vacancies = ProfessionImages.objects.get(image_name='cities_vacancies')

    context = {
        'locations_by_salaries': locations_by_salaries,
        'locations_by_vacancies': locations_by_vacancies,
        'prof_locations_by_salaries':prof_locations_by_salaries,
        'prof_locations_by_vacancies':prof_locations_by_vacancies,
        'cities_vacancies': cities_vacancies,
        'cities_salaries':cities_salaries,
        'cities_prof_vacancies':city_prof_vacancies,
        'cities_prof_salaries':city_prof_salaries,
    }

    return render(request, template_name="stat_site/locations_page.html", context=context)

def ret_skills_page(request):
    profession = Professions.objects.first()
    skills = ProfessionalSkillsByYear.objects.filter(profession_id = profession.profession_id)
    
    skills_by_year = [list(skills.filter(year = i).order_by('raiting_place')) for i in range(2015, 2023)]

    context = {'skills_by_year': skills_by_year}
    return render(request,"stat_site/skills_page.html",context=context)

def ret_last_vacancys_page(request):
    vac_list = []
    vacancies = search()
    for json_vacancy in vacancies:
        vac_name = json_vacancy['name']
        vac_url = json_vacancy['url']

        full_vacancy = requests.get(vac_url).json()
        description = re.sub(r'\<[^>]*\>', '',full_vacancy['description'])[0:300]+'...'
        skills = [ skill['name'] for skill in full_vacancy['key_skills']]
        employer_name = full_vacancy['employer']['name']
        salary_from = full_vacancy['salary']['from']
        salary_to = full_vacancy['salary']['to']
        salary_currency = full_vacancy['salary']['currency']
        salary = Salary(salary_from, salary_to, salary_currency)
        pub_date = full_vacancy['published_at']
        vac_list.append(Vacancy(vac_name, description, skills, salary, employer_name, pub_date))

    context = {
        'vacancies_list': vac_list
        }
    return render(request,"stat_site/last_vacncies.html", context=context)