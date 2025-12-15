# configapp/context_processors.py
from .models import Profile, ContactInfo
from django.conf import settings


def profile_processor(request):
    """Barcha template'lar uchun profile ma'lumotlarini qaytaradi"""
    context = {}

    try:
        # Profile ma'lumotlari
        profile = Profile.objects.filter(is_active=True).first()
        if profile:
            context['profile'] = profile

            # Social links
            social_links = []
            if profile.telegram:
                social_links.append({'platform': 'telegram', 'url': profile.telegram, 'icon': 'bi-telegram'})
            if profile.instagram:
                social_links.append({'platform': 'instagram', 'url': profile.instagram, 'icon': 'bi-instagram'})
            if profile.github:
                social_links.append({'platform': 'github', 'url': profile.github, 'icon': 'bi-github'})
            if profile.email:
                social_links.append({'platform': 'email', 'url': f'mailto:{profile.email}', 'icon': 'bi-envelope'})

            context['social_links'] = social_links
            context['has_resume'] = bool(profile.resume_file)
    except:
        pass

    try:
        # Contact info
        contact_info = ContactInfo.objects.filter(is_active=True).first()
        if contact_info:
            context['contact_info'] = contact_info
    except:
        pass

    # Recaptcha kaliti
    context['RECAPTCHA_SITE_KEY'] = getattr(settings, 'RECAPTCHA_SITE_KEY', '')

    return context