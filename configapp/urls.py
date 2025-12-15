# configapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # PUBLIC URLS
    path('', views.home, name='home'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ADMIN PANEL URLS - BARCHASI admin-panel/ OSTIDA
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/edit-home-about/', views.edit_home_about, name='edit_home_about'),
    path('admin-panel/edit-skills/', views.edit_skills, name='edit_skills'),
    path('admin-panel/edit-services/', views.edit_services, name='edit_services'),
    path('admin-panel/edit-portfolio/', views.edit_portfolio, name='edit_portfolio'),
    path('admin-panel/edit-experiences/', views.edit_experiences, name='edit_experiences'),
    path('admin-panel/edit-contact/', views.edit_contact, name='edit_contact'),
]