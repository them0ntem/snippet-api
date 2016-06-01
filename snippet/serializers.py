import time

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from human_dates import time_ago_in_words
from rest_framework import serializers
from rest_framework.reverse import reverse

from snippet.models import Snippet


class SnippetPrevNextHyperlink(serializers.HyperlinkedIdentityField):
	def __init__(self, *args, **kwargs):
		self.lookup_fields = kwargs.pop('lookup_fields')
		self.next = kwargs.pop('next')
		super(SnippetPrevNextHyperlink, self).__init__(*args, **kwargs)

	def get_url(self, obj, view_name, request, format):
		if hasattr(obj, 'pk') and obj.pk in (None, ''):
			return None

		lookup_value = getattr(obj, self.lookup_fields)

		try:
			if self.next:
				lookup_value = Snippet.objects.get(pk=lookup_value).get_next_by_created().pk
			else:
				lookup_value = Snippet.objects.get(pk=lookup_value).get_previous_by_created().pk
		except Snippet.DoesNotExist:
			return "None"

		kwargs = {self.lookup_url_kwarg: lookup_value}
		return reverse(view_name, kwargs=kwargs, request=request, format=format)


class UserSerializer(serializers.ModelSerializer):
	snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'snippets')
		extra_kwargs = {
			'password': {'write_only': True},
			'username': {'required': False},
			'first_name': {'required': True},
			'last_name': {'required': True},
			'email': {'required': True},
		}
		read_only_fields = ('id',)

	def create(self, validated_data):
		user = User.objects.create(
			username=self.get_unique_username(),
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

	def get_unique_username(self):
		username = (self.validated_data['first_name'] + self.validated_data['last_name']).replace(' ', '').lower()

		while True:
			username += str(int(time.time() * 1000))
			if User.objects.filter(username=username).exists():
				username += str(int(time.time() * 1000))
			else:
				break
		return username

	def validate_email(self, value):
		if value in User.objects.values_list('email', flat=True):
			raise serializers.ValidationError("A user with that email already exists.")
		return value


class SnippetSerializer(serializers.ModelSerializer):
	highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
	owner = serializers.ReadOnlyField(source='owner.username')
	next = SnippetPrevNextHyperlink(view_name="snippet-detail", lookup_fields='pk', next=True, read_only=True)
	prev = SnippetPrevNextHyperlink(view_name="snippet-detail", lookup_fields='pk', next=False, read_only=True)
	days_ago = serializers.SerializerMethodField()

	class Meta:
		model = Snippet
		fields = (
			'id', 'title', 'code', 'linenos', 'language', 'style', 'owner', 'highlight', 'next', 'prev', 'days_ago')

	def get_days_ago(self, obj):
		return time_ago_in_words(obj.created)


def validate_email_bool(email):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
		return True
	except ValidationError:
		return False


class AuthTokenSerializer(serializers.Serializer):
	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass

	email = serializers.CharField(label=_("Email"))
	password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

	def validate(self, attrs):
		email_or_username = attrs.get('email')
		password = attrs.get('password')

		if email_or_username and password:
			if validate_email_bool(email_or_username):
				try:
					user_request = User.objects.get(email=email_or_username)
				except User.DoesNotExist:
					msg = _('Unable to log in with provided credentials.')
					raise serializers.ValidationError(msg)
				email_or_username = user_request.username
			user = authenticate(username=email_or_username, password=password)

			if user:
				if not user.is_active:
					msg = _('User account is disabled.')
					raise serializers.ValidationError(msg)
			else:
				msg = _('Unable to log in with provided credentials.')
				raise serializers.ValidationError(msg)

		else:
			msg = _('Must include "email" and "password".')
			raise serializers.ValidationError(msg)

		attrs['user'] = user
		return attrs
