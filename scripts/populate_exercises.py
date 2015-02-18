import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from accounts.models import Account
from workouts.models import WorkoutHistory, Workout
from exercises.models import BodyPart, Muscle, Equipment, Exercise

from django.views.decorators.csrf import csrf_exempt


def populate(request):
	rtn_dict = {'success': False, "msg": ""}

	try:
		'''
			REMOVE ALL ROWS FROM TABLES
		'''
		Exercise.objects.all().delete()
		Equipment.objects.all().delete()
		Muscle.objects.all().delete()
		BodyPart.objects.all().delete()

		'''
			CREATE BODY PARTS
		'''

		print 'creating body parts'
		body_parts = ["chest", "arm", "core", "leg"]

		for body_part in body_parts:
			part = BodyPart(name=body_part)
			part.save()

		'''
			CREATE MUSCLES
		'''

		print 'creating muscles'
		chest_muscles = ["pectoral"]
		arm_muscles = ["bicep", "tricep", "forearm"]
		leg_muscles = ["calf", "quadracep", "gluteus"]
		core_muscles = ["abdominals", "back_lower", "back_upper", "lats"]
		muscles = {
			"chest": chest_muscles,
			"arm": arm_muscles,
			"leg": leg_muscles,
			"core": core_muscles
		}

		for k, v in muscles.items():
			for muscle_name in v:
				body_part = BodyPart.objects.get(name=k)
				muscle = Muscle(body_part=body_part, name=muscle_name)
				muscle.save()

		'''
			CREATE EQUIPMENT
		'''

		print 'creating equipment'
		equipment_list = ["dumbbell", "bench_press", "yoga_mat", "bench", "jump_rope", "treadmill"]

		for item in equipment_list:
			equipment = Equipment(name=item)
			equipment.save()

		'''
			CREATE EXERCISES
		'''

		print 'creating exercises'

		mu_pectoral = Muscle.objects.get(name="pectoral")
		mu_bicep = Muscle.objects.get(name="bicep")
		mu_tricep = Muscle.objects.get(name="tricep")
		mu_forearm = Muscle.objects.get(name="forearm")
		mu_calf = Muscle.objects.get(name="calf")
		mu_quadracep = Muscle.objects.get(name="quadracep")
		mu_gluteus = Muscle.objects.get(name="gluteus")
		mu_abdominals = Muscle.objects.get(name="abdominals")
		mu_back_lower = Muscle.objects.get(name="back_lower")
		mu_back_upper = Muscle.objects.get(name="back_upper")
		mu_lats = Muscle.objects.get(name="lats")

		eq_dumbbell = Equipment.objects.get(name="dumbbell")
		eq_treadmill = Equipment.objects.get(name="treadmill")
		eq_jump_rope = Equipment.objects.get(name="jump_rope")
		eq_bench = Equipment.objects.get(name="bench") 
		eq_bench_press = Equipment.objects.get(name="bench_press") 


		exercise_list = ["bench_press", "decline_press", "run_treadmill", "pushup_wide", "jogging_treadmill", "bicycling", "stairmaster", "jump_rope", "pull_down", "bicep_curl"]
		bench_press = Exercise(name="bench_press", equipment=eq_bench_press, main_muscle=mu_pectoral)
		decline_press = Exercise(name="decline_press", equipment=eq_bench_press, main_muscle=mu_pectoral)
		run_treadmill = Exercise(name="run_treadmill", equipment=eq_treadmill, main_muscle=mu_calf)
		bicep_curl = Exercise(name="bicep_curl", equipment=eq_dumbbell, main_muscle=mu_bicep)
		pushup_wide = Exercise(name="pushup_wide", main_muscle=mu_pectoral)
		jump_rope = Exercise(name="jump_rope", equipment=eq_jump_rope, main_muscle=mu_calf)

		bench_press.save()
		decline_press.save()
		bicep_curl.save()
		run_treadmill.save()
		pushup_wide.save()
		jump_rope.save()
		rtn_dict['success'] = True
		rtn_dict['msg'] = 'Successfully populated default exercises, muscles, bodyparts, and equipment'
	except Exception as e:
		print 'Error populating exercises, muscles, bodyparts, and equipment: {0}'.format(e)
		rtn_dict['msg'] = 'Error populating exercises, muscles, bodyparts, and equipment: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")