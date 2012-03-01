How to install this project:
----------------------------
1. Clone this project from github
2. cd into "polling" (the newly checkedout folder)
3. in your shell run: virtualenv -p /usr/bin/python2.7 venv --distribute
4. in your shell run: source venv/bin/activate
5. in your shell run: pip install -r requirements.txt
6. Create a file named "local_settings.py" fill in the DATABASES field for your django install.
```python
#Here is a sample local_settings.py
#No need for imports or anything, settings.py will bring it all in for you.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}
```

7. Phew, you're good to go! Run: ./manage.py runserver 0.0.0.0:XXXX to confirm

Working with virtual env
------------------------
* Before you start working on this project you should always run: source venv/bin/activate to active your virtualenv to have the correct libraries listed in requirements.txt
* To stop working with env and get your normal prompt back just simply run: "deactivate" from any directory.

