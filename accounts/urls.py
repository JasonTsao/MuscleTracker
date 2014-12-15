from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

urlpatterns = patterns("accounts.api",
                        url(r"^login", "login"),
)