from django.db import models
from django.db import models
from django.utils import timezone
import random

# دالة لحفظ الفيديوهات والصور داخل مجلد باسم النشاط
def activity_video_path(instance, filename):
    return f"activities/{instance.activity.title}/videos/{filename}"

def activity_image_path(instance, filename):
    return f"activities/{instance.activity.title}/images/{filename}"


class Activity(models.Model):
    COLOR_CHOICES = [
        ("from-yellow-400 to-orange-500", "أصفر → برتقالي"),
        ("from-cyan-400 to-blue-500", "سماوي → أزرق"),
        ("from-indigo-400 to-purple-500", "نيلي → بنفسجي"),
        ("from-purple-400 to-pink-500", "بنفسجي → وردي"),
        ("from-green-400 to-blue-500", "أخضر → أزرق"),
        ("from-orange-400 to-red-500", "برتقالي → أحمر"),
    ]
    STATUS_CHOICES = [
        # ("معلق", "معلق"),
        ("قادم", "قادم"),
        ("مكتمل", "مكتمل"),
    ]

    id = models.AutoField(primary_key=True, verbose_name="المعرف")
    title = models.CharField(max_length=255, verbose_name="العنوان")
    date = models.DateField(default=timezone.now,verbose_name="التاريخ") # يمكنك تغييره DateField
    location = models.CharField(default='Aïn El Kebira', max_length=255, verbose_name="المكان")
    participants = models.PositiveIntegerField(verbose_name="عدد المشاركين",null=True, blank=True)
    duration = models.CharField(max_length=50,null=True, blank=True, verbose_name="المدة")
    category = models.CharField(max_length=100, verbose_name="الفئة",null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name="الحالة")
    description = models.TextField(verbose_name="الوصف")

    class Meta:
        verbose_name = "نشاط"
        verbose_name_plural = "الأنشطة"

    def __str__(self):
        return self.title


class ActivityHighlights(models.Model):
    name = models.CharField(max_length=100, verbose_name="النقطة المميزة")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="highlights", verbose_name="النشاط")

    class Meta:
        verbose_name = "ميزة النشاط"
        verbose_name_plural = "مميزات النشاط"

    def __str__(self):
        return self.name


class ActivityAchievements(models.Model):
    name = models.CharField(max_length=100, verbose_name="الإنجاز")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="achievements", verbose_name="النشاط")

    class Meta:
        verbose_name = "إنجاز النشاط"
        verbose_name_plural = "إنجازات النشاط"

    def __str__(self):
        return self.name


class ActivityVideo(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="videos", verbose_name="النشاط")
    video = models.FileField(upload_to=activity_video_path, verbose_name="الفيديو")

    class Meta:
        verbose_name = "فيديو النشاط"
        verbose_name_plural = "فيديوهات النشاط"

    def __str__(self):
        return f"🎥 {self.activity.title}"


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="images", verbose_name="النشاط")
    image = models.ImageField(upload_to=activity_image_path, verbose_name="الصورة")

    class Meta:
        verbose_name = "صورة النشاط"
        verbose_name_plural = "صور النشاط"

    def __str__(self):
        return f"🖼️ {self.activity.title}"
    
# * ---------------------------------------------------------->
def news_image_path(instance, filename):
    return f"news/{instance.title}/images/{filename}"

class News(models.Model):
    # أنواع الأخبار (Type)
    TYPE_CHOICES = [
        ("announcement", "إعلان"),       # خبر أو إعلان رسمي
        ("achievement", "إنجاز"),        # خبر يخص إنجاز أو نجاح
        ("reminder", "تذكير"),          # تذكير بحدث أو موعد
        ("workshop", "ورشة عمل"),       # خبر يخص ورشة أو تدريب
        ("initiative", "مبادرة"),        # خبر عن مبادرة جديدة
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="العنوان")
    excerpt = models.TextField(verbose_name="ملخص قصير")
    content = models.TextField(verbose_name="المحتوى")
    date = models.DateField(verbose_name="التاريخ")
    time = models.TimeField(verbose_name="الوقت")
    author = models.ForeignKey(
        "Members",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"type": "admin"},  # يجيب فقط الأعضاء الإداريين
        verbose_name="الكاتب"
    )

    # category = models.CharField(max_length=100, verbose_name="التصنيف")
    category = models.CharField(max_length=100, choices=TYPE_CHOICES, verbose_name="نوع الخبر")

    image = models.ImageField(upload_to=news_image_path, verbose_name="الصورة")  
    views = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    likes = models.PositiveIntegerField(default=0, verbose_name="عدد الإعجابات")
    featured = models.BooleanField(default=False, verbose_name="مميز")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "الخبر"
        verbose_name_plural = "الاخبار"

# * --------------------------------------------------------



from django.core.exceptions import ValidationError

class Members(models.Model):
    ROLE_CHOICES = [
        ("president", "رئيس"),
        ("vice1", "نائب أول"),
        ("vice2", "نائب ثاني"),
        ("general_secretary", "الكاتب العام"),
        ("vice_secretary", "نائب الكاتب العام"),
        ("treasurer", "أمين المال"),
        ("vice_treasurer", "نائب أمين المال"),
        ("member1", "عضو أول"),
        ("member2", "عضو ثاني"),
        ("social_committee", "رئيس لجنة الشؤون الاجتماعية"),
        ("culture_committee", "رئيس لجنة النشاطات الثقافية"),
        ("sports_committee", "رئيس لجنة النشاطات الرياضية"),
        ("normal", "عادي"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="الاسم الكامل")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, verbose_name="الدور")
    image = models.ImageField(upload_to="members_images/", blank=True, null=True, verbose_name="الصورة")
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة قصيرة")
    joinDate = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="تاريخ الانضمام")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="الهاتف")
    education = models.CharField(max_length=255, blank=True, null=True, verbose_name="المستوى التعليمي")

    TYPE_CHOICES = [
        ("admin", "عضو إداري"),
        ("normal", "عضو عادي"),
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="normal", verbose_name="نوع العضو")

    def save(self, *args, **kwargs):
        # المناصب الحصرية (يسمح لعضو واحد فقط)
        unique_roles = [
            "president", "vice1", "vice2",
            "general_secretary", "vice_secretary",
            "treasurer", "vice_treasurer",
            "member1", "member2",
            "social_committee", "culture_committee", "sports_committee"
        ]

        if self.role in unique_roles:
            exists = Members.objects.filter(role=self.role).exclude(id=self.id).exists()
            if exists:
                raise ValidationError(f"المنصب '{dict(self.ROLE_CHOICES)[self.role]}' محجوز بالفعل ولا يمكن تكراره.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "الاعضاء"



# جدول الإنجازات (مرتبط بعضو)
class MemberAchievement(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=255, verbose_name="الإنجاز")
    def __str__(self):
        return f"{self.title} - {self.member.name}"


# جدول المهارات (مرتبط بعضو)
class MemberSkill(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=255, verbose_name="المهارة")

    def __str__(self):
        return f"{self.name} - {self.member.name}"

def Application_photo_path(instance, filename):
    return f"applications_photos/{instance.applicationId}/photo{filename}"
def Application_id_card_path(instance, filename):
    return f"applications_photos/{instance.applicationId}/id_card{filename}"

class Application(models.Model):
    applicationId = models.AutoField(primary_key=True, verbose_name="المعرف")
    photo = models.ImageField(
        upload_to=Application_photo_path, 
        verbose_name="الصورة الشخصية"
    )
    id_card = models.ImageField(
        blank=True, # remove
        null=True,  # remove
        upload_to=Application_id_card_path, 
        verbose_name="صورة بطاقة الهوية"
    )
    fullName = models.CharField(
        max_length=255, 
        verbose_name="الاسم الكامل",
        unique=True

    )
    email = models.EmailField(
        max_length=255, 
        verbose_name="البريد الإلكتروني"
    )
    phone = models.CharField(
        max_length=50, 
        verbose_name="رقم الهاتف"
    )
    age = models.PositiveIntegerField(
        verbose_name="العمر"
    )
    interests = models.TextField(
        verbose_name="الاهتمامات"
    )
    experience = models.TextField(
        blank=True, null=True, 
        verbose_name="الخبرات السابقة"
    )
    motivation = models.TextField(
        verbose_name="الدافع للانضمام"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="تاريخ التقديم"
    )

    class Meta:
        verbose_name = "طلب الانضمام"
        verbose_name_plural = "طلبات الانضمام"

    def __str__(self):
        return f"{self.fullName} - {self.applicationId}"


class Contact(models.Model):

    REASON_CHOICES = [
        ("membership", "استفسار عن العضوية"),
        ("activities", "الأنشطة والفعاليات"),
        ("partnership", "شراكة أو تعاون"),
        ("complaint", "شكوى أو اقتراح"),
        ("other", "أخرى"),
    ]



    name = models.CharField(max_length=100, verbose_name="الاسم")
    email = models.EmailField(max_length=100, verbose_name="البريد الإلكتروني",null=True,blank=True)
    contactReason = models.CharField(max_length=20, choices=REASON_CHOICES)  # 👈 هنا السبب
    phone = models.CharField(max_length=10, verbose_name="رقم الهاتف")
    subject = models.CharField(max_length=200, verbose_name="الموضوع")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.reason}"
