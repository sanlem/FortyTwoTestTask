from django.conf.urls import include, url
from django.contrib import admin
from apps.requests.views import RequestEntryListView
from apps.contacts.views import ContactsUpdateView
from django.conf import settings
from django.contrib.staticfiles import views
from django.contrib.auth import views as auth_views


admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'contacts.views.contacts_list', name="contacts_list"),
    url(r'^edit/', ContactsUpdateView.as_view(), name="contacts_edit"),
    url(r'^requests/', 'requests.views.requests_list', name="requests_list"),
    url(r'^requests_api/', RequestEntryListView.as_view(),
        name="requests_api"),
    url(r'^login/', auth_views.login, { 'template_name': 'login.html' }, name="login"),
    url(r'^logout/', auth_views.logout, {'next_page': '/' }, name="logout"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
