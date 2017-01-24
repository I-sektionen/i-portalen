from django.db import models
from django.db.models.query_utils import Q
from django.utils import timezone
from utils.time import six_months_back


class EventManager(models.Manager):
    def published(self):
        return self.filter(
                Q(status=self.model.APPROVED)|
                Q(status=self.model.BEING_CANCELD),

                visible_from__lte=timezone.now(),
                end__gte=timezone.now()
                ).order_by('-start')

    def events_by_user(self, user):
        """Returns the events a specific user is preregistered to.
        :param user: A django user.
        """
        r = self.filter(entryaspreregistered__user=user)
        return r

    def user(self, user):
        user_events = user.event_set.filter(
            end__gte=timezone.now()-timezone.timedelta(days=7)).order_by('-visible_from')
        user_org = user.get_organisations()

        for o in user_org:
            user_events |= o.event_set.filter(
                end__gte=timezone.now()-timezone.timedelta(days=7)).order_by('-visible_from')
        return user_events

class EntryAsPreRegisteredManager(models.Manager):
    def get_noshow(self, user):
        return self.filter(user=user, no_show=True, timestamp__gte=six_months_back)


