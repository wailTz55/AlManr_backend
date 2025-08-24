# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Activity
# from .serializers import ActivitySerializer

# @api_view(['GET'])
# def get_activities(request):
#     activities = Activity.objects.all()
#     serializer = ActivitySerializer(activities, many=True)
#     return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity, News, Members
from .serializers import ActivitySerializer, NewsSerializer, MembersSerializer

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import *
class ApplicationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)