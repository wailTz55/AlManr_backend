from rest_framework import serializers
from .models import *

class ActivitySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    highlights = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'title', 'date', 'location', 'participants', 
                'duration', 'category', 'status', 'description', 
                'images', 'videos', 'achievements', 'highlights']
    
    def get_images(self, obj):
        # إرجاع مسارات الصور كمصفوفة نصوص
        return [image.image.url for image in obj.images.all()]
    
    def get_videos(self, obj):
        # إرجاع مسارات الفيديوهات كمصفوفة نصوص  
        return [video.video.url for video in obj.videos.all()]
    
    def get_achievements(self, obj):
        # إرجاع أسماء الإنجازات كمصفوفة نصوص
        return [achievement.name for achievement in obj.achievements.all()]
    
    def get_highlights(self, obj):
        # إرجاع أسماء المميزات كمصفوفة نصوص
        return [highlight.name for highlight in obj.highlights.all()]
    
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
