from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import pytz


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Client(models.Model):
    """
    For multi tenancy
    timezone
    yyyy-mm-dd hh:mm am/pm
    nov, dd, 2016
    TODO datetime_format
    YYYY-MM-DDTHH:MM:SS+HH:MM
    """
    TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)
    DATETIME_FORMAT_CHOICES = (
        # '%d/%m/%y',
        ('%d %b %Y %I:%M%p', '25 Oct 2006 02:30PM'),
        ('%b %d, %Y %I:%M%p', 'Oct 25, 2006 02:30PM'),
        ('%B %d, %Y %I:%M%p', 'October 25, 2006 02:30PM'),
        ('%m/%d/%Y %I:%M%p', '10/25/2006 02:30PM'),
        ('%Y-%m-%d %H:%M', '2006-10-25 14:30'),
        ('%Y-%m-%d', '2006-10-25'),
        ('%m/%d/%Y %H:%M', '10/25/2006 14:30'),
        ('%m/%d/%Y', '10/25/2006'),
        ('%m/%d/%y %H:%M', '10/25/06 14:30'),
        ('%m/%d/%y', '10/25/06'),
    )
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    datetime_format = models.CharField(
        max_length=32, default='%m/%d/%Y %I:%M%p',choices=DATETIME_FORMAT_CHOICES)
    timezone = models.CharField(
        max_length=64, default='America/New_York', choices=TIMEZONE_CHOICES)
    address = models.TextField()
    # we want this to unique to each client eventually.
    twilio_number = models.CharField(max_length=16, default='+15702343621')
    office_hours = models.TextField()
    contact_details = models.TextField()

    def __str__(self):
        return self.name


class Facility(models.Model):
    """
    Where patients are appointed to.
    """
    client = models.ForeignKey('Client', models.PROTECT)
    name = models.CharField(max_length=255)
    # TODO shortform for sms?
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'facilities'
        unique_together = ('client', 'name')

    def __str__(self):
        return self.name


class Provider(models.Model):
    client = models.ForeignKey('Client', models.PROTECT)
    name = models.CharField(max_length=128)
    provider_id = models.CharField(max_length=64, null=True, blank=True)  #            physician id                    optional    string  employee number for the primary surgeon. must match to physician id in patient accounting system.
    provider_npi_id = models.CharField(max_length=64)  #        physician npi id                optional    string  national provider identification for the primary provider.
    provider_specialty = models.CharField(max_length=64, null=True, blank=True)  #   surgeon specialty               optional    string  specialty of the primary provider or surgeon on the appointment or case
    office_hours = models.TextField(null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)

    @property
    def get_office_hours(self):
        return self.office_hours or self.client.office_hours

    @property
    def get_contact_details(self):
        return self.contact_details or self.client.contact_details

    class Meta:
        unique_together = ('client', 'provider_npi_id')

    def __str__(self):
        return self.name