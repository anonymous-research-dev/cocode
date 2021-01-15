from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler400, handler403, handler404, handler500
from django.urls import re_path, path, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    re_path(r'^documents\/(?P<path>[^\*]+\.md)$',
            views.core_document_show, name='document_show'),

    path('accounts/signup_agreements/', views.user_signup_agreements, name='signup_agreements'),
    path('accounts/signup/', views.UserCreateView.as_view(), name='signup'),
    path('accounts/edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),

    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:course_id>/',
         views.course_show, name='course_show'),
    path('courses/<str:course_id>/experiment',
         views.course_experiment, name='course_experiment'),
    path('courses/<str:course_id>/state_maps',
         views.course_state_maps, name='course_state_maps'),
    path('courses/<str:course_id>/materials/<str:material_id>/',
         views.material_show, name='material_show'),
    path('courses/<str:course_id>/materials/<str:material_id>/state/', 
         views.material_state, name='material_state'),
    path('courses/<str:course_id>/materials/<str:material_id>/files/',
         views.exercise_state_files, name='exercise_state_files'),
    re_path(r'^courses\/(?P<course_id>[\w\-_]+)\/materials\/(?P<material_id>[\w\-_]+)\/files\/(?P<path>[^\*]+)$',
         views.exercise_state_file, name='exercise_state_file'),
    path('courses/<str:course_id>/materials/<str:material_id>/seconds/',
         views.exercise_state_seconds, name='exercise_state_seconds'),
    path('courses/<str:course_id>/materials/<str:material_id>/reset/',
         views.exercise_state_reset, name='exercise_state_reset'),
    path('courses/<str:course_id>/materials/<str:material_id>/snaps/',
         views.exercise_snaps, name='exercise_snaps'),
    path('courses/<str:course_id>/materials/<str:material_id>/logs/',
         views.exercise_logs, name='exercise_logs'),
    path('courses/<str:course_id>/materials/<str:material_id>/survey_answers/',
         views.survey_answers, name='survey_answers'),

    path('', views.core_landing, name='landing'),
]
# handler400 = 'core.views.bad_request'
# handler403 = 'core.views.permission_denied'
# handler404 = 'core.views.page_not_found'
# handler500 = 'core.views.server_error'
