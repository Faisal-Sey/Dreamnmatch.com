from django.db import models
from django.shortcuts import reverse
from django.conf import settings
import datetime


# Create your models here.


class Qualities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    Age_group = models.CharField(max_length=30)
    Region = models.CharField(max_length=255, blank=True)
    Purpose = models.CharField(max_length=50, blank=True)
    Gender = models.CharField(max_length=20, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Qualities'

    def __str__(self):
        return '{}'.format(self.user)

    def get_age(self):
        return int((datetime.date.today() - self.other.Date_of_Birth).days / 365.25)


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    Profile_pic = models.ImageField(blank=True, null=True)
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    First_name = models.CharField(max_length=80)
    Status = models.CharField(max_length=80, default="Single")
    Last_name = models.CharField(max_length=80)
    Date_of_Birth = models.DateField(blank=True, null=True)
    Country = models.CharField(max_length=255)
    Region = models.CharField(max_length=255)
    Phone = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True)
    Gender = models.CharField(max_length=40)
    Description = models.TextField(max_length=4000)
    Occupation = models.CharField(max_length=100, blank=True, null=True)
    Birthplace = models.CharField(max_length=100, blank=True, null=True)
    Interest_shows = models.CharField(max_length=255, blank=True, null=True)
    Interest_bands = models.CharField(max_length=255, blank=True, null=True)
    Interest_movies = models.CharField(max_length=255, blank=True, null=True)
    Interest_games = models.CharField(max_length=255, blank=True, null=True)
    Jobs_title = models.CharField(max_length=255, blank=True, null=True)
    Jobs_started = models.CharField(max_length=255, blank=True, null=True)
    Jobs_end = models.CharField(max_length=255, blank=True, null=True)
    Jobs_description = models.TextField(max_length=4000, blank=True, null=True)
    Jobs_title1 = models.CharField(max_length=255, blank=True, null=True)
    Jobs_started1 = models.CharField(max_length=255, blank=True, null=True)
    Jobs_end1 = models.CharField(max_length=255, blank=True, null=True)
    Jobs_description1 = models.TextField(max_length=4000, blank=True, null=True)
    Height = models.CharField(max_length=50, blank=True, null=True)
    Eye_color = models.CharField(max_length=50, blank=True, null=True)
    Hair_color = models.CharField(max_length=50, blank=True, null=True)
    Weight = models.CharField(max_length=50, blank=True, null=True)
    Body_type = models.CharField(max_length=50, blank=True, null=True)
    Ethnicity = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    Recovery_email = models.CharField(max_length=255, blank=True, null=True)
    Recovery_phone = models.CharField(max_length=50, blank=True, null=True)
    Question_1 = models.CharField(max_length=100, blank=True, null=True)
    Question_2 = models.CharField(max_length=100, blank=True, null=True)
    Answer_1 = models.CharField(max_length=100, blank=True, null=True)
    Answer_2 = models.CharField(max_length=100, blank=True, null=True)

    other = models.ForeignKey(Qualities, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    subscription = models.CharField(max_length=40, default="Free")
    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.First_name)

    def get_age(self):
        new_date = self.Date_of_Birth
        return int((datetime.date.today() - new_date).days / 365.25)


class Payment(models.Model):
    Email = models.EmailField(blank=True)
    Amount = models.IntegerField(blank=True, null=True)


class MessageDetail(models.Model):
    From = models.CharField(max_length=50)
    To = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.From)

    def get_absolute_url(self):
        return reverse("current", kwargs={
            'slug': self.slug
        })


class Messaging(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    label = models.IntegerField(blank=True, null=True)
    detail = models.ManyToManyField(MessageDetail)
    time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.user)

    def get_absolute_url(self):
        return reverse("current", kwargs={
            'slug': self.slug
        })


class StatusImage(models.Model):
    image = models.ImageField(blank=True, null=True)
    objects = models.Manager()


class Status(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4000, null=True, blank=True)
    stats = models.ManyToManyField(StatusImage)
    slug = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.user)




