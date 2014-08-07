# encoding: utf-8
from setuptools import setup, find_packages

import utensils


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='django-utensils',
    version=utensils.__version__,
    description="Useful Django snippets.",
    long_description=readme,
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
