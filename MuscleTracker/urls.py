import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'accounts.views.signup'),
    # url(r'^$', 'MuscleTracker.views.home', name='home'),
    # url(r'^MuscleTracker/', include('MuscleTracker.foo.urls')),
    url(r'^acct/', include('accounts.urls')),
    url(r'^exercises/', include('exercises.urls')),
    url(r'^muscle_loads/', include('muscle_loads.urls')),
    url(r'^workouts/', include('workouts.urls')),
     url(r'^scripts/', include('scripts.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': settings.STATIC_ROOT, 'show_indexes':True}), 
)
