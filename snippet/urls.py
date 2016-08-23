from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from snippet import views

# API endpoints
urlpatterns = [
	url(r'^$', views.api_root),
	url(r'^snippet/$', views.SnippetList.as_view(), name='snippet-list'),
	url(r'^snippet/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
	url(r'^snippet/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),
	url(r'^users/$', views.UserList.as_view(), name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
	url(r'^api-token-auth/', views.ObtainAuthToken.as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)

# Login and logout views for the browsable API
urlpatterns += [
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
