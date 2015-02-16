from django.db import models
from accounts.models import Account


class MuscleLoad(models.Model):
	account = models.ForeignKey(Account)
	date = models.DateField()
	abdominals = models.IntegerField(default=0)
	abductors = models.IntegerField(default=0)
	adductors = models.IntegerField(default=0)
	biceps = models.IntegerField(default=0)
	calves = models.IntegerField(default=0)
	chest = models.IntegerField(default=0)
	forearms = models.IntegerField(default=0)
	glutes = models.IntegerField(default=0)
	hamstrings = models.IntegerField(default=0)
	lats = models.IntegerField(default=0)
	lower_back = models.IntegerField(default=0)
	middle_back = models.IntegerField(default=0)
	neck = models.IntegerField(default=0)
	obliques = models.IntegerField(default=0)
	quadriceps = models.IntegerField(default=0)
	shoulders = models.IntegerField(default=0)
	traps = models.IntegerField(default=0)
	triceps = models.IntegerField(default=0)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		unique_together = (('account', 'date'),)
	def __unicode__(self):
		return '{0} : {1}'.format(self.account.user_name, self.date)