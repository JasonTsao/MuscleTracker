from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("exercises.api",
			url(r"^(\d+)", "getExcercise"),

)