from django.shortcuts import render

# Create your views here.

from rest_framework import views
from .serializers import UserSerializer,ActivityPeriodSerializer
from .models import User,ActivityPeriod
from django.http import Http404
from rest_framework.response import Response
from datetime import datetime
from dateutil import parser
from rest_framework import status
import json

class UserDataView(views.APIView):

    def get_date(self,date_serial):
        date = parser.isoparse(date_serial)
        return datetime.strftime(date,'%B %d %Y %I:%M%p')

    def get_user_object(self):
        try:
            return User.objects.all()
        except User.DoesNotExist:
            raise Http404
    def get_activity_object(self):
        try:
            return ActivityPeriod.objects.all()
        except ActivityPeriod.DoesNotExist:
            raise Http404

    def get(self, request):
        data = {"ok": "true",}
        list1 = []
        snippet1 = self.get_user_object()
        snippet2 = self.get_activity_object()
        serializer1 = UserSerializer(snippet1,many = True)
        serializer2 = ActivityPeriodSerializer(snippet2,many= True)
        set1={}
        for i in range(len(serializer1.data)):
            list_to_be_appended = {"start_time": self.get_date(serializer2.data[i]["start_time"]),
                                   "end_time": self.get_date(serializer2.data[i]["end_time"])
                                   }
            if serializer1.data[i]["user_id"] in User.objects.all():
                set1[serializer1.data[i]["user_id"]].append(list_to_be_appended)
            else:
                set1[serializer1.data[i]["user_id"]] =[]
                set1[serializer1.data[i]["user_id"]].append(list_to_be_appended)
            list1.append({"id":serializer1.data[i]["user_id"],
                          "real_name":serializer1.data[i]["real_name"],
                          "tz": serializer1.data[i]["tz"],
                           "activity_periods":set1[serializer1.data[i]["user_id"]],
                          })
        data["members"] = list1
        return Response(data=data,status=status.HTTP_200_OK)
