# Snippet API with Django Rest Framework

This Django REST API project is the companion of a [Snippet Andorid App](https://github.com/manthansharma/snippet-app).

## Setup

1. Add "polls" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = [
            ...
            'snippet-api',
        ]

2. Include the polls URLconf in your project urls.py like this:
        
        url(r'^snippet/', include('snippet-api.urls')),

3. Run `python manage.py migrate` to create the snippet models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/snippet/ to create your snippet.
