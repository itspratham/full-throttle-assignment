import random
from datetime import *
from django.core.management.base import BaseCommand

from assignment.models import User, ActivityPeriod

import random, string
import names
import pytz
from random import randrange ,randint
from datetime import timedelta

class Command(BaseCommand):
    help = "Save randomly generated user record values."

    def random_number(self):
        return random.randint(1, 5)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'number_of_user_records',
            type=int,
            help="Number of user records to generate and save to database"
        )
    def get_timezone(self):
        random_timezone = pytz.all_timezones
        random_timezone = random.choice(random_timezone)
        return random_timezone

    def end_time(self):
        end = datetime(2020, 6, 30, 7, 1, 8, 475874,tzinfo=pytz.timezone("UTC"))
        return end

    def strt_time(self):
        start = datetime.now(tz=pytz.timezone("UTC"))
        return start

    def random_date(self):
        start = self.strt_time()
        end = self.end_time()
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta,22222222)
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
                "tz": self.get_timezone()
            }
            recordone = User(**kwargs)
            recordone.save()
            # gwargs = {
            #     "user_id" : recordone,
            #     "start_time": self.strt_time(),
            #     "end_time" : self.random_date(),
            # }
            gwargs = []
            for i in range(self.random_number()):
                gwargs.append(ActivityPeriod(user_id = recordone,
                    start_time= self.strt_time(),
                    end_time = self.random_date()))
            recordtwo = ActivityPeriod.objects.bulk_create(gwargs)
            #recordtwo.save()
        self.stdout.write(self.style.SUCCESS('User records saved successfully.'))