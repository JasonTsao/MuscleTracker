from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
#from django.views.decorators.csrf import csrf_exempt
#from accounts.api import saveEmail

urlpatterns = patterns("accounts.api",
                        url(r"^register$", "registerUser"),
                        url(r"^login$", "login"),
                        url(r'logout', "logoutUser"),
                        url(r'email/save', "saveEmail"),
)

urlpatterns += patterns("accounts.views",
			url(r"^email/new", "signup"),
)