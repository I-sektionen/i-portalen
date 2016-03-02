from django.test import TestCase
from django.utils import timezone
from course_evaluations.models import Year
from user_managements.models import IUser


class SpeakerListTests (TestCase):
    def setUp(self):
        """
        This set up creates users: Event admin, speaker1..5
        Sets up an event
        :return:
        """
        # Normal user with no special permissions
        self.admin = IUser.objects.create_user(username="admin001")

    def test_add_periods(self):
        year = Year(year=2016)
        vt1_start = timezone.now()
        vt2_start = timezone.now() + timezone.timedelta(days=30)
        vt2_end = timezone.now() + timezone.timedelta(days=60)
        ht1_start = timezone.now() + timezone.timedelta(days=90)
        ht2_start = timezone.now() + timezone.timedelta(days=120)
        ht2_end = timezone.now() + timezone.timedelta(days=150)
        year.add_periods(vt1_start, vt2_start, vt2_end, ht1_start, ht2_start, ht2_end)
        year.save()

    def test_get_year(self):
        pass

    def test_clean(self):
        pass

    def test_get_free_courses(self):
        pass

    def test_update_courses_from_list(self):
        pass

    def test_copy_last_year(self):
        pass
