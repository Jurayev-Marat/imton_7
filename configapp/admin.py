# configapp/admin.py
from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'city', 'is_active')
    list_filter = ('is_active', 'city')
    search_fields = ('full_name', 'title', 'email')
    readonly_fields = ('age', 'created_at', 'updated_at')

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'title', 'short_bio', 'detailed_bio', 'profile_image')
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('birth_date', 'age', 'website', 'phone', 'city', 'email', 'degree', 'resume_file')
        }),
        ('Ijtimoiy tarmoqlar', {
            'fields': ('telegram', 'instagram', 'github', 'gmail', 'linkedin', 'leetcode')
        }),
        ('Hero bo\'limi', {
            'fields': ('hero_background', 'hero_title', 'hero_subtitles')
        }),
        ('Holat', {
            'fields': ('freelance_available', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'category', 'order', 'is_active')
    list_editable = ('percentage', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'filter_name', 'order', 'is_active')
    list_editable = ('filter_name', 'order', 'is_active')
    search_fields = ('name',)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'is_featured', 'order', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'date_created')
    search_fields = ('title', 'short_description', 'detailed_description')
    list_editable = ('order', 'is_featured', 'is_active')
    readonly_fields = ('date_created',)

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'category', 'short_description', 'detailed_description')
        }),
        ('Media va sanalar', {
            'fields': ('image', 'date_created')
        }),
        ('Havolalar va texnologiyalar', {
            'fields': ('github_link', 'live_demo_link', 'technologies_used')
        }),
        ('Tartib va holat', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'experience_type', 'start_date', 'end_date', 'current', 'is_active')
    list_filter = ('experience_type', 'current', 'is_active')
    search_fields = ('title', 'company', 'description')
    date_hierarchy = 'start_date'
    list_editable = ('is_active',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'is_active')
    list_editable = ('is_active',)

    def has_add_permission(self, request):
        # Faqat bitta kontakt ma'lumoti bo'lishi kerak
        if ContactInfo.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'status')
    list_filter = ('is_read', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read', 'status')

    def has_add_permission(self, request):
        return False


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('field_of_study', 'institution', 'degree', 'start_year', 'end_year', 'is_active')
    list_filter = ('degree', 'is_active')
    search_fields = ('field_of_study', 'institution', 'description')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'is_active')
    list_filter = ('is_active', 'issue_date')
    search_fields = ('name', 'issuing_organization')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'start_date', 'is_featured', 'is_active')
    list_filter = ('project_type', 'is_featured', 'is_active')
    search_fields = ('title', 'description', 'client_name')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'position', 'company', 'content')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('platform', 'is_active')