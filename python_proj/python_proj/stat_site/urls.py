from django.urls import path
from . import views
urlpatterns = [
    path('profession', views.ret_main_page, name='profession'),
    path('demand', views.ret_demand_page, name='demand'),
    path('locations',views.ret_location_page, name='locations'),
    path('skills',views.ret_skills_page,name='skills'),
    path('last_vacancies',views.ret_last_vacancys_page,name='last_vacancies'),
    path('', views.ret_welcome_page, name='welcome')
]