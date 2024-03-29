from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("muscle_loads.api",
			url(r"^(\d+)", "getLatestMuscleLoad"),
			url(r"^(\d+-\d+-\d+)/(\d+-\d+-\d+)", "getMuscleLoads"),
			url(r"^save", "saveMuscleLoad"),

)