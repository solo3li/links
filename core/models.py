from django.db import models

ICON_CHOICES = [
    ('fa-brands fa-facebook', 'فيسبوك (Facebook)'),
    ('fa-brands fa-twitter', 'تويتر/X (Twitter)'),
    ('fa-brands fa-instagram', 'انستجرام (Instagram)'),
    ('fa-brands fa-tiktok', 'تيك توك (TikTok)'),
    ('fa-brands fa-snapchat', 'سناب شات (Snapchat)'),
    ('fa-brands fa-youtube', 'يوتيوب (YouTube)'),
    ('fa-brands fa-telegram', 'تيليجرام (Telegram)'),
    ('fa-brands fa-whatsapp', 'واتساب (WhatsApp)'),
    ('fa-brands fa-github', 'جيت هب (GitHub)'),
    ('fa-brands fa-linkedin', 'لينكد إن (LinkedIn)'),
    ('fa-solid fa-envelope', 'بريد إلكتروني (Email)'),
    ('fa-solid fa-globe', 'موقع إلكتروني (Website)'),
    ('other', 'غير ذلك (إدخال يدوي)'),
]

class Profile(models.Model):
    name = models.CharField(max_length=100, verbose_name="الاسم")
    bio = models.TextField(blank=True, null=True, verbose_name="النبذة التعريفية")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="الصورة الشخصية")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "الملف الشخصي"
        verbose_name_plural = "الملفات الشخصية"

class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links', verbose_name="الملف الشخصي")
    title = models.CharField(max_length=100, verbose_name="عنوان الرابط")
    url = models.URLField(verbose_name="الرابط")
    icon_platform = models.CharField(max_length=50, choices=ICON_CHOICES, default='other', verbose_name="أيقونة المنصة")
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text="في حال اختيار 'غير ذلك'، أدخل فئة الأيقونة هنا (مثال: fa-brands fa-discord)", verbose_name="أيقونة مخصصة")
    bg_color = models.CharField(max_length=20, blank=True, null=True, verbose_name="لون خلفية الرابط", help_text="مثال: #ff3366 أو اسم اللون، اتركه فارغاً للافتراضي")
    text_color = models.CharField(max_length=20, blank=True, null=True, verbose_name="لون النص والأيقونة", help_text="مثال: #ffffff، اتركه فارغاً للافتراضي")
    order = models.IntegerField(default=0, verbose_name="الترتيب")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")
    is_highlighted = models.BooleanField(default=False, verbose_name="مميز", help_text="إذا كان مفعلاً سيظهر الرابط بتصميم مختلف (لفت الانتباه)")
    
    class Meta:
        ordering = ['order']
        verbose_name = "الرابط"
        verbose_name_plural = "الروابط"
        
    @property
    def final_icon(self):
        if self.icon_platform == 'other':
            return self.icon_class
        return self.icon_platform
        
    def __str__(self):
        return self.title
