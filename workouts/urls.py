from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("workouts.api",
			url(r"^(\d+)", "getWorkout"),
)