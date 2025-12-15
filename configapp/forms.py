from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
            }
        ),
        error_messages={'required': 'Iltimos, robot emasligingizni tasdiqlang!'}
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name-field',
                'placeholder': 'Ismingiz',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email-field',
                'placeholder': 'Email manzilingiz',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'subject-field',
                'placeholder': 'Mavzu',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message-field',
                'rows': 10,
                'placeholder': 'Xabaringiz',
                'required': True
            }),
        }
        labels = {
            'name': 'Ism',
            'email': 'Email',
            'subject': 'Mavzu',
            'message': 'Xabar'
        }
        error_messages = {
            'name': {'required': 'Ismingizni kiriting!'},
            'email': {'required': 'Email manzilingizni kiriting!'},
            'subject': {'required': 'Mavzuni kiriting!'},
            'message': {'required': 'Xabar matnini kiriting!'}
        }


class DownloadResumeForm(forms.Form):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
            }
        ),
        error_messages={'required': 'Iltimos, robot emasligingizni tasdiqlang!'}
    )


class HomeAboutForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'title', 'short_bio', 'detailed_bio',
            'profile_image', 'birth_date', 'website', 'phone',
            'city', 'email', 'degree', 'age', 'freelance_available',
            'resume_file', 'telegram', 'instagram', 'github', 'gmail',
            'hero_background', 'hero_title', 'hero_subtitles', 'is_active'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Toʻliq ism'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Backend Developer'}),
            'short_bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qisqacha maʼlumot'}),
            'detailed_bio': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Batafsil maʼlumot'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 00 000 00 00'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shahringiz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Bachelor'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 120}),
            'telegram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Telegram havola'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram havola'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub havola'}),
            'gmail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Gmail manzili'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hero sarlavha'}),
            'hero_subtitles': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Developer, Designer, Freelancer'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'hero_background': forms.FileInput(attrs={'class': 'form-control'}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control'}),
            'freelance_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'telegram': 'Telegram',
            'instagram': 'Instagram',
            'linkedin': 'LinkedIn',
            'leetcode': 'LeetCode',
            'github': 'GitHub',
            'gmail': 'Gmail',
            'freelance_available': 'Freelance mavjud',
            'is_active': 'Faol'
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'percentage', 'category', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: Python, Django, JavaScript'
            }),
            'percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Skill nomi',
            'percentage': 'Foiz (%)',
            'category': 'Kategoriya',
            'order': 'Tartib raqami',
            'is_active': 'Faol'
        }
        help_texts = {
            'percentage': '0 dan 100 gacha bo\'lishi kerak',
            'order': 'Kichik raqamlar birinchi ko\'rinadi'
        }

    def clean_percentage(self):
        """Percentage ni 0-100 oralig'ida tekshirish"""
        percentage = self.cleaned_data['percentage']
        if percentage < 0 or percentage > 100:
            raise forms.ValidationError("Foiz 0 dan 100 gacha bo'lishi kerak!")
        return percentage


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['experience_type', 'title', 'company', 'start_date',
                  'end_date', 'current', 'description', 'order', 'is_active']
        widgets = {
            'experience_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lavozim yoki ta\'lim darajasi'}),
            'company': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Kompaniya yoki ta\'lim muassasi'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Tavsif'}),
            'current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'experience_type': 'Tajriba turi',
            'title': 'Sarlavha',
            'company': 'Kompaniya/Ta\'lim muassasi',
            'start_date': 'Boshlanish sanasi',
            'end_date': 'Tugash sanasi',
            'current': 'Hozirgi ish',
            'description': 'Tavsif',
            'order': 'Tartib raqami',
            'is_active': 'Faol'
        }

    def clean(self):
        cleaned_data = super().clean()
        current = cleaned_data.get('current')
        end_date = cleaned_data.get('end_date')

        if current and end_date:
            raise forms.ValidationError("Agar 'Hozirgi ish' belgilangan bo'lsa, tugash sanasini bo'sh qoldiring")

        if not current and not end_date:
            raise forms.ValidationError("Tugash sanasini kiriting yoki 'Hozirgi ish'ni belgilang")

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = PortfolioCategory
        fields = ['name', 'filter_name', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoriya nomi'
            }),
            'filter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Filter nomi (masalan: filter-web)'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nomi',
            'filter_name': 'Filter nomi',
            'order': 'Tartib raqami',
            'is_active': 'Faol'
        }
        help_texts = {
            'filter_name': 'Isotope filter uchun class nomi (masalan: filter-web, filter-app)'
        }


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['category', 'title', 'short_description', 'detailed_description',
                  'image', 'date_created', 'order', 'is_featured', 'is_active',
                  'github_link', 'live_demo_link', 'technologies_used']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Loyiha nomi'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qisqacha tavsif'
            }),
            'detailed_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Batafsil tavsif'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'date_created': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project'
            }),
            'live_demo_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://demo.example.com'
            }),
            'technologies_used': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Django, React, PostgreSQL, ...'
            }),
        }
        labels = {
            'category': 'Kategoriya',
            'title': 'Sarlavha',
            'short_description': 'Qisqacha tavsif',
            'detailed_description': 'Batafsil tavsif',
            'image': 'Rasm',
            'date_created': 'Yaratilgan sana',
            'order': 'Tartib raqami',
            'is_featured': 'Tavsiya etilgan',
            'is_active': 'Faol',
            'github_link': 'GitHub Link',
            'live_demo_link': 'Live Demo Link',
            'technologies_used': 'Texnologiyalar'
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon_class', 'title', 'description', 'order', 'is_active']
        widgets = {
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'bi bi-briefcase yoki fas fa-cog'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xizmat nomi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Xizmat haqida batafsil tavsif'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'icon_class': 'Icon Class',
            'title': 'Sarlavha',
            'description': 'Tavsif',
            'order': 'Tartib raqami',
            'is_active': 'Faol'
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone', 'email', 'map_embed_code', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Toʻliq manzil'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 90 123 45 67',
                'pattern': '^\+?[0-9\s\-\(\)]{7,20}$'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'map_embed_code': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '<iframe src="https://www.google.com/maps/embed?..."></iframe>'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'address': 'Manzil',
            'phone': 'Telefon',
            'email': 'Email',
            'map_embed_code': 'Google Maps Embed Kodi',
            'is_active': 'Faol'
        }
        help_texts = {
            'map_embed_code': 'Google Maps dan olingan embed kodini joylang'
        }