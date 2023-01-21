from django.db import models
from django.db.models.functions import Length
import datetime

models.CharField.register_lookup(Length)

class Professions(models.Model):
    profession_name = models.CharField(max_length=40)
    profession_id = models.CharField(max_length = 5, primary_key=True)
    title = models.CharField(max_length=40,verbose_name='название')
    desription = models.TextField(verbose_name='описание')
    
    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
        constraints = [
            models.CheckConstraint(name='profession_id_check',check=models.Q(profession_id__length__gte=5))
        ]

class ProfessionalYaersAnalitics(models.Model):
    year = models.IntegerField(choices=[(year,year) for year in range(2000, datetime.datetime.now().year)],verbose_name='год')
    profession_id = models.ForeignKey(Professions, db_column='profession_id',on_delete=models.CASCADE)
    middle_salary = models.IntegerField(verbose_name='средняя зарплата за год')
    vacancies_num = models.IntegerField(verbose_name='количество вакансий за год по выбранной профессии')

    class Meta:
        verbose_name = f'аналитка за год для выбранной профессии'
        verbose_name_plural = f'аналитика за все года для выбранной профессии'
        constraints = [
            models.CheckConstraint(name='prof_year_check',check=models.Q(year__gte=0)),
            models.CheckConstraint(name='prof_salary_check',check=models.Q(middle_salary__gte=0)),
            models.CheckConstraint(name='prof_vacancies_check',check=models.Q(vacancies_num__gte=0))
        ]

class ProfessionalSkillsByYear(models.Model):
    year = models.IntegerField(choices=[(year,year) for year in range(2000, datetime.datetime.now().year)],verbose_name='год')
    raiting_place = models.IntegerField(choices=[(place, place) for place in range(1, 11)],verbose_name='мемто в рейтенге топовых навыков')
    profession_id = models.ForeignKey(Professions, db_column='profession_id',on_delete=models.CASCADE)
    description = models.TextField(verbose_name='описание навыка')

    class Meta:
        verbose_name = 'навык и его место в рейтенге в этом году'
        verbose_name_plural = 'навыки за каждый год с их местом в рейтенге'

class LocationAnaliticsWithProfession(models.Model):
    location = models.CharField(max_length=40,verbose_name='название города/страны')
    profession_id = models.ForeignKey(Professions, db_column='profession_id',on_delete=models.CASCADE)
    vacancies_share = models.FloatField(verbose_name='доля вакансий в городе/стране по этойп профессии')
    middle_salary = models.IntegerField(verbose_name='средняя зп в городе/стране по этой профессии')
    
    class Meta:
        verbose_name = 'аналитика по городу/стране для выбранной профессии'
        verbose_name_plural = 'общая аналитика по городам/странам для выбранной профессии'
        constraints=[
            models.CheckConstraint(name='location_prof_salary_check',check=models.Q(middle_salary__gte=0)),
            models.CheckConstraint(name='location_prof_vacancies_check',check=models.Q(vacancies_share__gte=0))
        ]
class ProfessionImages(models.Model):
    profession_id = models.ForeignKey(Professions, db_column='profession_id',on_delete=models.CASCADE)
    image_name = models.CharField(max_length=40) 
    image = models.ImageField()

class LocationAnalitics(models.Model):

    location = models.CharField(max_length=40,verbose_name='название города/страны')
    vacancies_share = models.FloatField(verbose_name='доля вакансий в этом городе/стране')
    middle_salary = models.IntegerField(verbose_name='средняя зп в этом городе/стране')
    
    class Meta:
        verbose_name = 'общая аналитика по городу/стране'
        verbose_name_plural = 'общая аналитика по всем городам/странам'
        constraints=[
            models.CheckConstraint(name='location_salary', check=models.Q(middle_salary__gte=0)),
            models.CheckConstraint(name='location_vacancies',check=models.Q(vacancies_share__gte=0))
        ]

class YaersAnalitics(models.Model):
    year = models.IntegerField(choices=[(year,year) for year in range(2000, datetime.datetime.now().year)], verbose_name='год')
    middle_salary = models.IntegerField(verbose_name='средняя зп за этот год')
    vacancies_num = models.IntegerField(verbose_name='количество вакансий в этом году')
    
    class Meta:
        verbose_name = 'общая аналитка за год'
        verbose_name_plural = 'общая аналитика по всем годам'
        constraints=[
            models.CheckConstraint(name='year_salary', check=models.Q(middle_salary__gte=0)),
            models.CheckConstraint(name='year_vacancies', check=models.Q(vacancies_num__gte=0))
        ]
