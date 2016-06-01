from django.contrib.auth.models import User
from requests import Response
from rest_framework import generics
from rest_framework import permissions, renderers, parsers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippet.models import Snippet
from snippet.permissions import IsOwnerOrReadOnly
from snippet.serializers import SnippetSerializer, UserSerializer, AuthTokenSerializer


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})


class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

	permission_classes = (permissions.AllowAny,)


class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	permission_classes = (permissions.AllowAny,)

	def create(self, request, *args, **kwargs):
		response = super(UserList, self).create(request, args, kwargs)
		auth_token = Token.objects.get(user_id=response.data['id'])
		response.data['auth_token'] = auth_token.key
		return response


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	permission_classes = (permissions.IsAuthenticated,)


class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

	permission_classes = (permissions.IsAuthenticated,)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
	                      IsOwnerOrReadOnly,)


class ObtainAuthToken(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthTokenSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({'auth_token': token.key,
		                 'email': user.email,
		                 'id': user.id,
		                 'first_name': user.first_name,
		                 'last_name': user.last_name,
		                 })
