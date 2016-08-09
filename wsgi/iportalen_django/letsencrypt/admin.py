from utils.admin import iportalen_admin_site
from letsencrypt.models import LetsEncrypt

iportalen_admin_site.register(LetsEncrypt)