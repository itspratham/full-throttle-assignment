import random
from datetime import *
from django.core.management.base import BaseCommand

from assignment.models import User, ActivityPeriod

import random, string
import names
import pytz
from random import randrange
from datetime import timedelta

class Command(BaseCommand):
    help = "Save randomly generated user record values."

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'number_of_user_records',
            type=int,
            help="Number of stock records to generate and save to database"
        )
    def get_timezone(self):
        random_timezone = pytz.all_timezones
        random_timezone = random.choice(random_timezone)
        return random_timezone

    def end_time(self,tz):
        end = datetime.strptime('2020-09-18 4:50 AM', '%Y-%m-%d %I:%M %p')
        end = end.astimezone(pytz.timezone(tz))
        return end

    def strt_time(self,tz):
        now_utc = datetime.now(pytz.timezone('UTC'))
        start = now_utc.astimezone(pytz.timezone(tz))
        return start

    def random_date(self,tz):
        start = self.strt_time(tz)
        end = self.end_time(tz)
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def get_name(self):
        gender_list = ["male", "female"]
        random_gender = random.choice(gender_list)
        name = names.get_full_name(gender=random_gender)
        return name

    def dummy_id(self):
        dumy_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
        return dumy_id

    def handle(self, *args, **options):
        size = options["number_of_user_records"]
        for _ in range(size):
            dummy_id = self.dummy_id()
            kwargs = {
                "user_id": dummy_id,
                "real_name": self.get_name(),
            }
            recordone = User(**kwargs)
            recordone.save()
            tz = self.get_timezone()
            gwargs = {
                "user_id" : recordone,
                "start_time": self.strt_time(tz),
                "end_time" : self.random_date(tz),
            }
            recordtwo = ActivityPeriod(**gwargs)
            recordtwo.save()
        self.stdout.write(self.style.SUCCESS('Stock records saved successfully.'))