# create_env.py
import secrets
import os


def generate_secret_key():
    """Yangi secret key yaratish"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for i in range(50))


def create_env_file():
    """.env faylini avtomatik yaratish"""
    env_content = f"""# Django Settings
SECRET_KEY={generate_secret_key()}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=jurayevmarat23@gmail.com
EMAIL_HOST_PASSWORD=azvh sizw prhb ajbm

# reCAPTCHA (Test keys)
RECAPTCHA_PUBLIC_KEY=6LdtLRwsAAAAABp2xbzkwnH0sqjmby5833Md8G4D
RECAPTCHA_PRIVATE_KEY=6LdtLRwsAAAAANgA4Vm0Nz2ZafdEMRojP4D6j1bV

# Database (optional)
# DATABASE_URL=sqlite:///db.sqlite3
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    print("✅ .env fayli muvaffaqiyatli yaratildi!")
    print("📁 Fayl manzili:", os.path.abspath('.env'))


if __name__ == "__main__":
    create_env_file()