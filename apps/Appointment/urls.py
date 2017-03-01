from django.conf.urls import url
# Controller - route methods
from . import views
urlpatterns = [
	url(r"^dashboard$", views.dashboard, name="dashboard"),
	url(r'^logout$', views.logout, name = 'logout'),
    url(r"^create_appt$", views.create_appt, name="create_appt"),
	url(r"^edit_appt/(?P<appt_id>\d+)$", views.edit_appt, name="edit_appt"),
	url(r"^update_appt/(?P<appt_id>\d+)$", views.update_appt, name="update_appt"),
    url(r"^delete_appt/(?P<appt_id>\d+)$", views.delete_appt, name="delete_appt"),
]
