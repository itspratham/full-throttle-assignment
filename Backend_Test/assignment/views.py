from django.shortcuts import render

# Create your views here.

from rest_framework import views
from .serializers import ActivityPeriodSerializer, UserSerializer
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

    def get_user_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_user_length(self):
        return len(User.objects.all())

    def get_activity_object(self):
        try:
            return ActivityPeriod.objects.all()
        except ActivityPeriod.DoesNotExist:
            raise Http404

    def get(self, request):
        data = {"ok": "true",}
        print(self.get_user_length())
        list1 = []
        for i in range(1,self.get_user_length()+1):
            snippet1 = self.get_user_object(i)
            serializer1 = UserSerializer(snippet1)
            snippet2  = ActivityPeriod.objects.filter(user_id = i)
            serializer2 = ActivityPeriodSerializer(snippet2, many=True)
            list1.append({"id":serializer1.data["user_id"],
                          "real_name":serializer1.data["real_name"],
                          "tz": serializer1.data["tz"],
                           "activity_periods": [{"start_time": self.get_date(serializer2.data[j]["start_time"]),
                                   "end_time": self.get_date(serializer2.data[j]["end_time"])
                                   } for j in range(0, len(snippet2))]
                          })
        data["members"] = list1
        return Response(data=data,status=status.HTTP_200_OK)
