from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'contacts.views.contacts_list', name="contacts_list"),
    url(r'^requests/', 'requests.views.requests_list', name="requests_list")
)
