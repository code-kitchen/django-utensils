To get going with the example:

```
pip install -r dev_requirements.txt
PYTHONPATH=. django-admin.py syncdb --settings=example.settings
PYTHONPATH=. django-admin.py runserver --settings=example.settings
```

It is assumed that you have a virtualenv setup for the example project.