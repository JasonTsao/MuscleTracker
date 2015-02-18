from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("workouts.api",
			url(r"^(\d+)", "getWorkout"),
			url(r"^all", "getWorkouts"),
			url(r"^save", "saveWorkout"),
			url(r"^history/(\d+)", "getWorkoutHistory"),
			url(r"^history/all", "getWorkoutHistories"),
			url(r"^history/save", "saveWorkoutHistory"),
)

urlpatterns += patterns("workouts.views",
			url(r"^new", "newWorkout"),
			url(r"^history/new", "newWorkoutHistory"),
)