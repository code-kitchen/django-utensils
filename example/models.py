from django.db import models

from utensils.models import AddressedModel, TimeStampedModel


class Author(AddressedModel):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    middle_names = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        ordering = ('last_name',)

    def __unicode__(self):
        return u"{}, {}".format(self.last_name, self.first_name)


class Book(TimeStampedModel):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=255, null=False, blank=False)
    publication_date = models.PositiveSmallIntegerField()
    in_stock = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
