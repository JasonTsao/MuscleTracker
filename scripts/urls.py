from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("scripts.populate_exercises",
			url(r"^populate", "populate"),
)

urlpatterns += patterns("scripts.send_emails",
			url(r"^beta_emails/send", "sendBetaAppEmails"),
)