# configapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import *
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import traceback
import json
from datetime import datetime


# ==================== PUBLIC VIEWS ====================

def home(request):
    """Bosh sahifa"""
    try:
        profile = Profile.objects.filter(is_active=True).first()
    except:
        profile = None

    skills = Skill.objects.filter(is_active=True).order_by('order')
    services = Service.objects.filter(is_active=True).order_by('order')
    portfolio_categories = PortfolioCategory.objects.filter(is_active=True).order_by('order')
    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('order')
    work_experiences = Experience.objects.filter(experience_type='work', is_active=True).order_by('order')
    educations = Experience.objects.filter(experience_type='education', is_active=True).order_by('order')
    contact_info = ContactInfo.objects.filter(is_active=True).first()

    context = {
        'profile': profile,
        'skills': skills,
        'services': services,
        'portfolio_categories': portfolio_categories,
        'portfolio_items': portfolio_items,
        'work_experiences': work_experiences,
        'educations': educations,
        'contact_info': contact_info,
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_SITE_KEY', ''),
        'form': ContactForm()
    }

    return render(request, 'index.html', context)


def portfolio_detail(request, pk):
    """Portfolio loyiha batafsil sahifasi"""
    portfolio_item = get_object_or_404(PortfolioItem, pk=pk, is_active=True)
    context = {'item': portfolio_item}
    return render(request, 'portfolio_detail.html', context)


@require_POST
@csrf_exempt
def contact_submit(request):
    """Contact form ma'lumotlarini qabul qilish"""
    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()

        # Email yuborish
        try:
            admin_email = getattr(settings, 'EMAIL_HOST_USER', '')
            if admin_email:
                send_mail(
                    f"Yangi xabar: {contact_message.subject}",
                    f"Ism: {contact_message.name}\nEmail: {contact_message.email}\n\nXabar:\n{contact_message.message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=True,
                )
        except:
            pass

        return JsonResponse({'success': True, 'message': 'Xabaringiz muvaffaqiyatli yuborildi!'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})


# ==================== PDF GENERATOR FUNCTIONS ====================

def wrap_text(text, max_chars):
    """Textni qatorlarga ajratish"""
    if not text:
        return []
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def verify_recaptcha_v2(token):
    """reCAPTCHA v2 tekshirish"""
    try:
        recaptcha_secret = getattr(settings, 'RECAPTCHA_SECRET_KEY', '')
        if not recaptcha_secret:
            return True, []  # Test mode

        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': recaptcha_secret, 'response': token},
            timeout=10
        )
        result = response.json()
        return result.get('success', False), result.get('error-codes', [])

    except:
        return False, ['verification-error']


def generate_complete_cv_pdf():
    """To'liq CV PDF yaratish"""
    buffer = BytesIO()

    # Data olish
    profile = Profile.objects.filter(is_active=True).first()
    skills = Skill.objects.filter(is_active=True).order_by('order')
    work_experiences = Experience.objects.filter(experience_type='work', is_active=True).order_by('-start_date')
    educations = Experience.objects.filter(experience_type='education', is_active=True).order_by('-start_date')
    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('-date_created')[:5]

    # PDF yaratish
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    story = []
    styles = getSampleStyleSheet()

    # Custom style yaratish
    styles.add(ParagraphStyle(
        name='NameStyle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=10,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#374151'),
        spaceAfter=20,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=10,
        spaceBefore=20,
        borderBottom=1,
        borderColor=colors.HexColor('#D1D5DB')
    ))

    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='SkillText',
        parent=styles['Normal'],
        fontSize=9,
        leftIndent=10
    ))

    # 1. Sarlavha
    if profile:
        story.append(Paragraph(profile.full_name.upper(), styles['NameStyle']))
        story.append(Paragraph(profile.title, styles['TitleStyle']))

        # Kontakt ma'lumotlari
        contact_info = []
        if profile.phone:
            contact_info.append(f"📞 {profile.phone}")
        if profile.email:
            contact_info.append(f"✉️ {profile.email}")
        if profile.city:
            contact_info.append(f"📍 {profile.city}")
        if profile.website:
            contact_info.append(f"🌐 {profile.website}")

        if contact_info:
            story.append(Paragraph(" | ".join(contact_info), ParagraphStyle(
                name='ContactStyle',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=30
            )))

    # 2. Profil ma'lumoti
    story.append(Paragraph("PROFIL", styles['SectionTitle']))
    if profile and profile.short_bio:
        story.append(Paragraph(profile.short_bio, styles['BodyText']))
    story.append(Spacer(1, 12))

    # 3. Ko'nikmalar
    if skills.exists():
        story.append(Paragraph("KO'NIKMALAR", styles['SectionTitle']))

        # Skills jadvali
        skill_data = []
        for skill in skills:
            skill_data.append([
                Paragraph(skill.name, styles['SkillText']),
                f"{skill.percentage}%"
            ])

        if skill_data:
            skill_table = Table(skill_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
            skill_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(skill_table)
            story.append(Spacer(1, 12))

    # 4. Ish tajribasi
    if work_experiences.exists():
        story.append(Paragraph("ISH TAJRIBASI", styles['SectionTitle']))

        for exp in work_experiences:
            # Ish nomi va vaqti
            period = f"{exp.start_date.strftime('%b %Y')} - "
            if exp.current:
                period += "Present"
            elif exp.end_date:
                period += exp.end_date.strftime('%b %Y')

            story.append(Paragraph(f"<b>{exp.title}</b> | {exp.company} | {period}", styles['BodyText']))

            # Tavsif
            if exp.description:
                story.append(Paragraph(exp.description, ParagraphStyle(
                    name='ExpDesc',
                    parent=styles['Normal'],
                    fontSize=9,
                    leftIndent=20,
                    spaceAfter=8
                )))

            story.append(Spacer(1, 8))

    # 5. Ta'lim
    if educations.exists():
        story.append(PageBreak())
        story.append(Paragraph("TA'LIM", styles['SectionTitle']))

        for edu in educations:
            period = f"{edu.start_date.strftime('%b %Y')} - "
            if edu.current:
                period += "Present"
            elif edu.end_date:
                period += edu.end_date.strftime('%b %Y')

            story.append(Paragraph(f"<b>{edu.title}</b> | {edu.company} | {period}", styles['BodyText']))

            if edu.description:
                story.append(Paragraph(edu.description, ParagraphStyle(
                    name='EduDesc',
                    parent=styles['Normal'],
                    fontSize=9,
                    leftIndent=20,
                    spaceAfter=8
                )))

            story.append(Spacer(1, 8))

    # 6. Portfolio loyihalar
    if portfolio_items.exists():
        story.append(Paragraph("PORTFOLIO LOYIHALAR", styles['SectionTitle']))

        for project in portfolio_items:
            story.append(Paragraph(f"<b>{project.title}</b>", styles['BodyText']))

            if project.short_description:
                story.append(Paragraph(project.short_description, ParagraphStyle(
                    name='ProjDesc',
                    parent=styles['Normal'],
                    fontSize=9,
                    leftIndent=20,
                    spaceAfter=4
                )))

            if project.technologies_used:
                techs = project.get_technologies_list()
                if techs:
                    story.append(Paragraph(
                        f"<i>Texnologiyalar: {', '.join(techs)}</i>",
                        ParagraphStyle(
                            name='TechList',
                            parent=styles['Normal'],
                            fontSize=8,
                            leftIndent=20,
                            textColor=colors.HexColor('#6B7280'),
                            spaceAfter=8
                        )
                    ))

            story.append(Spacer(1, 8))

    # 7. Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#9CA3AF')
        )
    ))

    # PDF ni build qilish
    doc.build(story)
    buffer.seek(0)

    return buffer


def download_resume(request):
    """CV yuklab olish"""
    token = request.GET.get('token', '')

    # reCAPTCHA tekshirish
    if token:
        success, errors = verify_recaptcha_v2(token)
        if not success:
            return JsonResponse({
                'success': False,
                'error': 'Robot tekshiruvi muvaffaqiyatsiz.'
            }, status=400)

    try:
        # To'liq CV PDF yaratish
        pdf_buffer = generate_complete_cv_pdf()

        # Profile ma'lumotlari
        profile = Profile.objects.filter(is_active=True).first()
        filename = f"{profile.full_name.replace(' ', '_')}_CV.pdf" if profile else "Resume.pdf"

        # Response yaratish
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(pdf_buffer.getvalue())

        return response

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'PDF yaratishda xatolik: {str(e)}'
        }, status=500)


# ==================== AUTH VIEWS ====================

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Xush kelibsiz!")
            return redirect('admin_panel')
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri!')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Muvaffaqiyatli chiqildi!")
    return redirect('home')


# ==================== ADMIN VIEWS ====================

@login_required
def admin_panel(request):
    stats = {
        'profile': Profile.objects.count(),
        'skills': Skill.objects.count(),
        'services': Service.objects.count(),
        'portfolio_items': PortfolioItem.objects.count(),
        'messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'experiences': Experience.objects.count(),
    }

    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'recent_messages': recent_messages,
        'django_version': '4.2.10',
        'python_version': '3.x'
    }
    return render(request, 'admin.html', context)


@login_required
def edit_home_about(request):
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(
            full_name="Ismingiz",
            title="Lavozimingiz",
            phone="+998 00 000 00 00",
            city="Shahringiz",
            email="example@email.com"
        )

    if request.method == 'POST':
        form = HomeAboutForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profil ma'lumotlari saqlandi!")
            return redirect('edit_home_about')
    else:
        form = HomeAboutForm(instance=profile)

    return render(request, 'edit_home_about.html', {'form': form, 'profile': profile})


@login_required
def edit_skills(request):
    skills = Skill.objects.all().order_by('order')

    if request.method == 'POST':
        if 'add_skill' in request.POST:
            form = SkillForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Skill qo'shildi!")
                return redirect('edit_skills')
        elif 'edit_skill' in request.POST:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)
            form = SkillForm(request.POST, instance=skill)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Skill yangilandi!")
                return redirect('edit_skills')
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)
            skill.delete()
            messages.success(request, "✅ Skill o'chirildi!")
            return redirect('edit_skills')
    else:
        form = SkillForm()

    return render(request, 'edit_skills.html', {'skills': skills, 'form': form})


@login_required
def edit_experiences(request):
    experiences = Experience.objects.all().order_by('order', '-start_date')

    if request.method == 'POST':
        if 'add_experience' in request.POST:
            form = ExperienceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Tajriba qo'shildi!")
                return redirect('edit_experiences')
        elif 'edit_experience' in request.POST:
            exp_id = request.POST.get('experience_id')
            experience = get_object_or_404(Experience, id=exp_id)
            form = ExperienceForm(request.POST, instance=experience)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Tajriba yangilandi!")
                return redirect('edit_experiences')
        elif 'delete_experience' in request.POST:
            exp_id = request.POST.get('experience_id')
            experience = get_object_or_404(Experience, id=exp_id)
            experience.delete()
            messages.success(request, "✅ Tajriba o'chirildi!")
            return redirect('edit_experiences')
    else:
        form = ExperienceForm()

    return render(request, 'edit_experiences.html', {
        'experiences': experiences,
        'form': form
    })


@login_required
def edit_portfolio(request):
    categories = PortfolioCategory.objects.all().order_by('order')
    portfolios = PortfolioItem.objects.all().order_by('order')

    if request.method == 'POST':
        # Category operations
        if 'add_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Kategoriya qo'shildi!")
                return redirect('edit_portfolio')
        elif 'edit_category' in request.POST:
            cat_id = request.POST.get('category_id')
            category = get_object_or_404(PortfolioCategory, id=cat_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Kategoriya yangilandi!")
                return redirect('edit_portfolio')
        elif 'delete_category' in request.POST:
            cat_id = request.POST.get('category_id')
            category = get_object_or_404(PortfolioCategory, id=cat_id)
            category.delete()
            messages.success(request, "✅ Kategoriya o'chirildi!")
            return redirect('edit_portfolio')

        # Portfolio operations
        elif 'add_portfolio' in request.POST:
            form = PortfolioForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Portfolio qo'shildi!")
                return redirect('edit_portfolio')
        elif 'edit_portfolio' in request.POST:
            port_id = request.POST.get('portfolio_id')
            portfolio = get_object_or_404(PortfolioItem, id=port_id)
            form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Portfolio yangilandi!")
                return redirect('edit_portfolio')
        elif 'delete_portfolio' in request.POST:
            port_id = request.POST.get('portfolio_id')
            portfolio = get_object_or_404(PortfolioItem, id=port_id)
            portfolio.delete()
            messages.success(request, "✅ Portfolio o'chirildi!")
            return redirect('edit_portfolio')
    else:
        form = PortfolioForm()

    return render(request, 'edit_portfolio.html', {
        'categories': categories,
        'portfolios': portfolios,
        'form': form
    })


@login_required
def edit_services(request):
    services = Service.objects.all().order_by('order')

    if request.method == 'POST':
        if 'add_service' in request.POST:
            form = ServiceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Xizmat qo'shildi!")
                return redirect('edit_services')
        elif 'edit_service' in request.POST:
            service_id = request.POST.get('service_id')
            service = get_object_or_404(Service, id=service_id)
            form = ServiceForm(request.POST, instance=service)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Xizmat yangilandi!")
                return redirect('edit_services')
        elif 'delete_service' in request.POST:
            service_id = request.POST.get('service_id')
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            messages.success(request, "✅ Xizmat o'chirildi!")
            return redirect('edit_services')
    else:
        form = ServiceForm()

    return render(request, 'edit_services.html', {'services': services, 'form': form})


@login_required
def edit_contact(request):
    contact_info = ContactInfo.objects.first()

    if not contact_info:
        contact_info = ContactInfo.objects.create(
            address="Manzilingiz",
            phone="+998 00 000 00 00",
            email="example@email.com"
        )

    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Kontakt ma'lumotlari saqlandi!")
            return redirect('edit_contact')
    else:
        form = ContactInfoForm(instance=contact_info)

    return render(request, 'edit_contact.html', {
        'form': form,
        'contact_info': contact_info
    })