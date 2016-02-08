from . import models
from utils.admin import HiddenModelAdmin, iportalen_admin_site

iportalen_admin_site.register(models.QuestionGroup, HiddenModelAdmin)
iportalen_admin_site.register(models.Question, HiddenModelAdmin)
iportalen_admin_site.register(models.Option, HiddenModelAdmin)


iportalen_admin_site.register(models.Vote, HiddenModelAdmin)
iportalen_admin_site.register(models.HasVoted, HiddenModelAdmin)