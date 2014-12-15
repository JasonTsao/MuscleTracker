from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("exercises.api",
			url(r"^(\d+)", "getExercise"),
			url(r"^all", "getExercises"),
			url(r"^history/(\d+)", "getExerciseHistory"),
			url(r"^history/all", "getExerciseHistories"),
			url(r"^history/add", "addExerciseHistoryToWorkout"),
			url(r"^history/edit/(\d+)", "editExerciseHistory"),

)