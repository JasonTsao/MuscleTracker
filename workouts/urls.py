from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("workouts.api",
			url(r"^(\d+)", "getWorkout"),
			url(r"^all", "getWorkouts"),
			url(r"^history/(\d+)", "getWorkoutHistory"),
			url(r"^history/all", "getWorkoutHistories"),
)