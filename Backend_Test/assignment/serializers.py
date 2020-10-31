from rest_framework import serializers
from .models import User,ActivityPeriod
from dateutil import parser
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = User
        fields = ('user_id', 'real_name', 'tz')

    def get_user_id(self, obj):
        return obj.user_id

class ActivityPeriodSerializer(serializers.ModelSerializer):
    # user_id = serializers.CharField(source='user_id.user_id')
    # real_name = serializers.CharField(source='user_id.real_name')
    # tz = serializers.CharField(source='user_id.tz')
    # start_time = serializers.SerializerMethodField('get_start_time')
    # end_time = serializers.SerializerMethodField('get_end_time')

    class Meta:
        model = ActivityPeriod
        fields = ('start_time', 'end_time')

    # def get_start_time(self, obj):
    #     date = parser.isoparse(obj)
    #     return datetime.strftime(date, '%B %d %Y %I:%M%p')
    #
    # def get_end_time(self, obj):
    #     date = parser.isoparse(obj)
    #     return datetime.strftime(date, '%B %d %Y %I:%M%p')