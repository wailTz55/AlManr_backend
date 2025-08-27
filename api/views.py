
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity, News, Members
from .serializers import *

@api_view(['GET'])
def get_all_data(request):
    activities = Activity.objects.all()
    news = News.objects.all()
    members = Members.objects.all()

    activities_serializer = ActivitySerializer(activities, many=True)
    news_serializer = NewsSerializer(news, many=True)
    members_serializer = MembersSerializer(members, many=True)

    return Response({
        "activities": activities_serializer.data,
        "news": news_serializer.data,
        "members": members_serializer.data
    })



class ApplicationView(APIView):
    def post(self, request, *args, **kwargs):

        full_name = request.data.get("fullName")
        email = request.data.get("email")
        phone = request.data.get("phone")

        if Application.objects.filter(fullName=full_name).exists() :
            return Response(
                {"message": "⚠️ هذا الاسم مسجّل من قبل"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif Application.objects.filter(email=email).exists() :
            return Response(
                {"message": "⚠️ هذا البريد الإلكتروني مسجّل من قبل"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif Application.objects.filter(phone=phone).exists() :
            return Response(
                {"message": "⚠️ هذا الرقم مسجّل من قبل"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        contactReason = request.data.get("contactReason")

        # تحقق من البيانات المكررة (مثال حسب الحاجة)
        if Contact.objects.filter(phone=phone, message=request.data.get("message")).exists():
            return Response(
                {"message": "⚠️ لقد أرسلت نفس الرسالة من قبل"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # التحقق من صحة السبب
        valid_reasons = [choice[0] for choice in Contact.REASON_CHOICES]
        if contactReason not in valid_reasons:
            return Response(
                {"message": "⚠️ السبب غير صالح"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # استخدام Serializer
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "✅ تم إرسال الرسالة بنجاح", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)