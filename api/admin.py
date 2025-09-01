from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib import messages
from .models import Application, Members


class ActivityHighlightsInline(admin.TabularInline):
    model = ActivityHighlights
    extra = 1

class ActivityAchievementsInline(admin.TabularInline):
    model = ActivityAchievements
    extra = 1

class ActivityVideoInline(admin.TabularInline):
    model = ActivityVideo
    extra = 1

class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "status", "participants", "category")
    list_filter = ("status", "category")
    search_fields = ("title", "location", "description")

    inlines = [ActivityHighlightsInline, ActivityAchievementsInline, ActivityVideoInline, ActivityImageInline]# class ActivityAdmin(admin.ModelAdmin):




# * Members
# إنجازات العضو (Inline)
class MemberAchievementInline(admin.TabularInline):
    model = MemberAchievement
    extra = 1   # عدد الصفوف الفارغة الجاهزة للإضافة


# مهارات العضو (Inline)
class MemberSkillInline(admin.TabularInline):
    model = MemberSkill
    extra = 1


# صفحة العضو في الأدمن
@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "type", "email", "phone", "joinDate")
    list_filter = ("role", "type")
    search_fields = ("name", "role", "email", "phone")

    inlines = [MemberAchievementInline, MemberSkillInline]

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "author", "category", "featured")  # الأعمدة في القائمة
    list_filter = ("category", "featured", "date",)          # الفلاتر الجانبية
    search_fields = ("title", "excerpt", "content")                         # البحث
    ordering = ("-date", "-time")       
    exclude = ("views", "likes")

@admin.action(description="المصادقة ونقل إلى الأعضاء")
def approve_and_add_to_members(modeladmin, request, queryset):
    for application in queryset:
        # نتأكد ما إذا كان العضو موجود أصلاً
        if Members.objects.filter(name=application.fullName).exists():
            messages.warning(request, f"⚠ {application.fullName} موجود مسبقاً كعضو.")
            continue

        # إنشاء عضو جديد بناءً على بيانات الطلب
        member = Members.objects.create(
            name=application.fullName,
            email=application.email,
            phone=application.phone,
            image=application.photo,   # ننقل الصورة
            role="normal",             # تعيين افتراضي (يمكن تغييره لاحقاً من الإدارة)
            type="normal"
        )
        messages.success(request, f"✅ تمت إضافة {application.fullName} إلى الأعضاء بنجاح.")

        # بعد المصادقة نحذف الطلب من جدول Application
        application.delete()

        # (اختياري) إذا تحب تحذف الطلب بعد المصادقة
        # application.delete()

# تسجيل الأكشن داخل لوحة الإدارة
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicationId", "fullName", "email", "phone", "submitted_at")
    search_fields = ("applicationId", "fullName", "email", "phone")
    list_filter = ("age", "submitted_at")
    readonly_fields = ("submitted_at",) 
    actions = [approve_and_add_to_members]

        # نجعل كل الحقول للقراءة فقط
    readonly_fields = ("applicationId", "fullName", "email", "phone", "age", "submitted_at")

    # منع الإضافة
    def has_add_permission(self, request):
        return False



