from . import models
from utils.admin import iportalen_admin_site, iportalen_superadmin_site

iportalen_admin_site.register(models.Groupings)
iportalen_admin_site.register(models.Course)
iportalen_admin_site.register(models.Exam)
iportalen_admin_site.register(models.ExamResult)

iportalen_superadmin_site.register(models.Groupings)
iportalen_superadmin_site.register(models.Course)
iportalen_superadmin_site.register(models.Exam)
iportalen_superadmin_site.register(models.ExamResult)
