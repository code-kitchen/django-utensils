# encoding: utf-8
import hashlib
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Abstract models

class TimeStampedModel(models.Model):
    """
    Add a created and modified field to a model easily.
    
    The hash functions can be used to build file upload paths that aren't
    easily guessable or distribute large numbers of files between 1000
    directories by using the time_hash as the first folder in the upload
    path.
    """
    created = models.DateTimeField(_(u"created"), auto_now_add=True)
    modified = models.DateTimeField(_(u"modified"), auto_now=True)

    class Meta:
        abstract = True

    @property
    def date_hash(self):
        return hashlib.sha1(
            str(self.pk) + str(self.created)).hexdigest()[::2]

    @property
    def time_hash(self):
        return str(int(time.mktime(self.created.timetuple())))[-3:]

    @property
    def hash(self):
        return hashlib.sha1(self.date_hash + self.time_hash).hexdigest()

    def challenge_hash(self, challenger):
        return challenger == self.hash


class AddressedModel(models.Model):
    """
    Add common address fields to a model easily.
    """
    address_1 = models.CharField(
        _(u"address 1"), max_length=128, null=False, blank=True)
    address_2 = models.CharField(
        _(u"address 2"), max_length=128, null=False, blank=True)
    city = models.CharField(
        _(u"City/Town"), max_length=64, null=False, blank=True)
    county = models.CharField(
        _(u"county"), max_length=64, null=False, blank=True)
    postal_code = models.CharField(
        _(u"postal code"), max_length=16, null=False, blank=True)
    country = models.ForeignKey('countries_plus.Country', null=True, blank=True)

    class Meta:
        abstract = True
