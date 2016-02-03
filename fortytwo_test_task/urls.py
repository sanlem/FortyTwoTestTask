from django.conf.urls import include, url, static
from django.contrib import admin
from apps.requests.views import RequestEntryListView
from django.conf import settings


admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'contacts.views.contacts_list', name="contacts_list"),
    url(r'^requests/', 'requests.views.requests_list', name="requests_list"),
    url(r'^requests_api/', RequestEntryListView.as_view(),
        name="requests_api"),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
