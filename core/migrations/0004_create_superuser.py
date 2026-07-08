from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@admin.com',
            password=make_password('admin123456'),
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

def remove_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_link_bg_color_link_text_color'),
    ]

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]
