# encoding: utf-8
from setuptools import setup, find_packages

import utensils


try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print "Warning: pypandoc module not found, could not convert Markdown to RST"
    read_md = lambda f: open(f, 'r').read()


readme = read_md('README.md')


with open('LICENSE') as f:
    license = f.read()


setup(
    name='django-utensils',
    version=utensils.__version__,
    description="Useful Django snippets.",
    long_description=readme,
    url='https://github.com/code-kitchen/django-utensils/',
    author='Ben Tappin',
    author_email='ben@mrben.co.uk',
    license=license,
    install_requires=[
        'django-bootstrap-form>=3.0',
        'django-braces<1.4.0',
        'django-countries-plus>=0.1.5',
        'django-storages>=1.1',
        'boto>=2.13.3',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    )
)
