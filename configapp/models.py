from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    title = models.CharField(max_length=200, verbose_name="Lavozim")
    short_bio = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qisqacha ma'lumot")
    detailed_bio = models.TextField(verbose_name="Batafsil ma'lumot")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="Profil rasmi")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan sana")
    website = models.URLField(max_length=200, blank=True, verbose_name="Veb sayt")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    city = models.CharField(max_length=100, verbose_name="Shahar")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    degree = models.CharField(max_length=100, blank=True, null=True, verbose_name="Daraja")
    age = models.IntegerField(blank=True, null=True, verbose_name="Yosh")
    freelance_available = models.BooleanField(default=True, verbose_name="Freelance mavjud")
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="CV fayli")

    telegram = models.URLField(blank=True, verbose_name="Telegram Link")
    instagram = models.URLField(blank=True, verbose_name="Instagram Link")
    github = models.URLField(blank=True, verbose_name="GitHub Link")
    gmail = models.EmailField(blank=True, verbose_name="Gmail")
    linkedin = models.URLField(blank=True, null=True)
    leetcode = models.URLField(blank=True, null=True)

    hero_background = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name="Hero fon rasm")
    hero_title = models.CharField(max_length=100, blank=True, verbose_name="Hero sarlavha")
    hero_subtitles = models.TextField(help_text="Herotda ko'rinadigan kasblar. Har birini vergul bilan ajrating",
                                      verbose_name="Hero kasblar")

    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.full_name

    def get_subtitles_list(self):
        if self.hero_subtitles:
            return [subtitle.strip() for subtitle in self.hero_subtitles.split(',')]
        return ['Designer', 'Developer', 'Freelancer', 'Photographer']

    def save(self, *args, **kwargs):
        # Age ni avtomatik hisoblash
        if self.birth_date:
            today = timezone.now().date()
            age = today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            self.age = age
        super().save(*args, **kwargs)


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('technical', 'Texnik'),
        ('soft', 'Soft Skill'),
        ('language', 'Tillar'),
        ('framework', 'Frameworklar'),
    ]

    name = models.CharField(max_length=100, verbose_name="Skill nomi")
    percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Foiz"
    )
    category = models.CharField(max_length=50, default='technical',
                                choices=SKILL_CATEGORIES, verbose_name="Kategoriya")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skilllar"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Service(models.Model):
    icon_class = models.CharField(max_length=50,
                                  help_text="Bootstrap icon class. Masalan: bi bi-briefcase",
                                  verbose_name="Icon class")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    filter_name = models.CharField(max_length=50,
                                   help_text="Isotope filter uchun class nomi",
                                   verbose_name="Filter nomi")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Portfolio Kategoriya"
        verbose_name_plural = "Portfolio Kategoriyalari"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE,
                                 related_name='items', verbose_name="Kategoriya")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    short_description = models.CharField(max_length=200, verbose_name="Qisqacha tavsif")
    detailed_description = models.TextField(blank=True, verbose_name="Batafsil tavsif")
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True,
                              verbose_name="Rasm")
    date_created = models.DateField(default=timezone.now, verbose_name="Yaratilgan sana")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    github_link = models.URLField(blank=True, verbose_name="GitHub Repository Link")
    live_demo_link = models.URLField(blank=True, verbose_name="Live Demo Link")
    technologies_used = models.CharField(max_length=300, blank=True,
                                         help_text="Foydalanilgan texnologiyalar (vergul bilan ajratilgan)",
                                         verbose_name="Foydalanilgan texnologiyalar")

    class Meta:
        verbose_name = "Portfolio Loyiha"
        verbose_name_plural = "Portfolio Loyihalari"
        ordering = ['order', '-date_created']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """Texnologiyalarni ro'yxat ko'rinishida qaytaradi"""
        if self.technologies_used:
            return [tech.strip() for tech in self.technologies_used.split(',')]
        return []


class Experience(models.Model):
    EXPERIENCE_TYPE = [
        ('work', 'Ish Tajribasi'),
        ('education', "Ta'lim"),
        ('summary', 'Qisqacha ma\'lumot'),
        ('certificate', 'Sertifikatlar'),
    ]

    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE,
                                       verbose_name="Tajriba turi")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    company = models.CharField(max_length=200, blank=True, verbose_name="Kompaniya/Ta'lim muassasi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(null=True, blank=True, verbose_name="Tugash sanasi")
    current = models.BooleanField(default=False, verbose_name="Hozirgi ish")
    description = models.TextField(verbose_name="Tavsif")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Tajriba"
        verbose_name_plural = "Tajribalar"
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.title} - {self.company if self.company else ''}"


class ContactInfo(models.Model):
    address = models.TextField(verbose_name="Manzil")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(verbose_name="Email")
    map_embed_code = models.TextField(help_text="Google Maps embed kodi",
                                      verbose_name="Xarita kodi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kontakt Ma'lumot"
        verbose_name_plural = "Kontakt Ma'lumotlari"

    def __str__(self):
        return "Kontakt Ma'lumotlari"

    def save(self, *args, **kwargs):
        # Faqat bitta kontakt ma'lumoti bo'lishini ta'minlash
        if not self.pk and ContactInfo.objects.exists():
            # Mavjud obyektni yangilash
            existing = ContactInfo.objects.first()
            existing.address = self.address
            existing.phone = self.phone
            existing.email = self.email
            existing.map_embed_code = self.map_embed_code
            existing.is_active = self.is_active
            return existing.save(*args, **kwargs)
        return super().save(*args, **kwargs)


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('read', "O'qilgan"),
        ('replied', 'Javob berilgan'),
        ('spam', 'Spam'),
    ]

    name = models.CharField(max_length=200, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new',
                              verbose_name="Status")

    class Meta:
        verbose_name = "Kontakt Xabari"
        verbose_name_plural = "Kontakt Xabarlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Testimonial(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ism")
    position = models.CharField(max_length=200, verbose_name="Lavozim")
    company = models.CharField(max_length=200, verbose_name="Kompaniya")
    content = models.TextField(verbose_name="Fikr")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True,
                              verbose_name="Rasm")
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 verbose_name="Reyting")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Fikr-Mulohaza"
        verbose_name_plural = "Fikr-Mulohazalar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.position}"


class Project(models.Model):
    TYPE_CHOICES = [
        ('personal', 'Shaxsiy loyiha'),
        ('client', 'Mijoz loyihasi'),
        ('open_source', 'Ochiq manba'),
    ]

    title = models.CharField(max_length=200, verbose_name="Loyiha nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Tavsif")
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='personal',
                                    verbose_name="Loyiha turi")
    client_name = models.CharField(max_length=200, blank=True, verbose_name="Mijoz nomi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(blank=True, null=True, verbose_name="Tugash sanasi")
    technologies = models.TextField(help_text="Foydalanilgan texnologiyalar (vergul bilan ajratilgan)",
                                    verbose_name="Texnologiyalar")
    github_link = models.URLField(blank=True, verbose_name="GitHub Link")
    live_link = models.URLField(blank=True, verbose_name="Live Link")
    featured_image = models.ImageField(upload_to='projects/', verbose_name="Asosiy rasm")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []


class Education(models.Model):
    DEGREE_CHOICES = [
        ('bachelor', "Bakalavr"),
        ('master', "Magistr"),
        ('phd', "PhD"),
        ('diploma', "Diploma"),
        ('certificate', "Sertifikat"),
    ]

    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="Daraja")
    field_of_study = models.CharField(max_length=200, verbose_name="Yo'nalish")
    institution = models.CharField(max_length=200, verbose_name="Ta'lim muassasi")
    start_year = models.IntegerField(verbose_name="Boshlanish yili")
    end_year = models.IntegerField(blank=True, null=True, verbose_name="Tugash yili")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_current = models.BooleanField(default=False, verbose_name="Joriy ta'lim")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Ta'lim"
        verbose_name_plural = "Ta'lim"
        ordering = ['order', '-start_year']

    def __str__(self):
        return f"{self.get_degree_display()} in {self.field_of_study} - {self.institution}"


class Certificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="Sertifikat nomi")
    issuing_organization = models.CharField(max_length=200, verbose_name="Tashkilot")
    issue_date = models.DateField(verbose_name="Berilgan sana")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Muddati")
    credential_id = models.CharField(max_length=100, blank=True, verbose_name="Sertifikat ID")
    credential_url = models.URLField(blank=True, verbose_name="Sertifikat linki")
    image = models.ImageField(upload_to='certificates/', blank=True, null=True,
                              verbose_name="Sertifikat rasmi")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        ordering = ['order', '-issue_date']

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('skype', 'Skype'),
        ('stackoverflow', 'Stack Overflow'),
        ('medium', 'Medium'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
        ('codepen', 'CodePen'),
        ('leetcode', 'LeetCode'),
        ('hackerrank', 'HackerRank'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="Platforma")
    url = models.URLField(verbose_name="Link")
    icon_class = models.CharField(max_length=50, blank=True,
                                  help_text="Bootstrap icon class. Masalan: bi bi-github",
                                  verbose_name="Icon class")
    order = models.IntegerField(default=0, verbose_name="Tartibi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Ijtimoiy Tarmoq"
        verbose_name_plural = "Ijtimoiy Tarmoqlar"
        ordering = ['order', 'platform']

    def __str__(self):
        return self.get_platform_display()

    def save(self, *args, **kwargs):
        # Avtomatik icon class qo'shish
        if not self.icon_class:
            self.icon_class = f'bi bi-{self.platform}'
        super().save(*args, **kwargs)