# configapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('download-resume/', views.download_resume, name='download_resume'),

    # Auth URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Admin URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin/edit-home-about/', views.edit_home_about, name='edit_home_about'),
    path('admin/edit-skills/', views.edit_skills, name='edit_skills'),
    path('admin/edit-experiences/', views.edit_experiences, name='edit_experiences'),
    path('admin/edit-portfolio/', edit_portfolio, name='edit_portfolio'),
    path('admin/edit-services/', edit_services, name='edit_services'),
    path('admin/edit-contact/', views.edit_contact, name='edit_contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)