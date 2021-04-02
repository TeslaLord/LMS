from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ForeignKey(
        "Section", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=2000, blank=True)
    skills = models.CharField(max_length=2000, blank=True)
    aoi = models.CharField(max_length=2000, blank=True)
    github = models.CharField(max_length=200, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Grade(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    ut1 = models.CharField(max_length=200, blank=True)
    ut2 = models.CharField(max_length=200, blank=True)
    ut3 = models.CharField(max_length=200, blank=True)

    ut1p = models.ImageField(upload_to='plots', blank=True)
    ut2p = models.ImageField(upload_to='plots', blank=True)
    ut3p = models.ImageField(upload_to='plots', blank=True)

    ut1pb = models.ImageField(upload_to='plots', blank=True)
    ut2pb = models.ImageField(upload_to='plots', blank=True)
    ut3pb = models.ImageField(upload_to='plots', blank=True)

    ut12 = models.ImageField(upload_to='plots', blank=True)
    ut13 = models.ImageField(upload_to='plots', blank=True)
    ut23 = models.ImageField(upload_to='plots', blank=True)


class Section(models.Model):
    section = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.section


class Question(models.Model):
    section = models.ForeignKey(
        "Section", on_delete=models.CASCADE, null=True, blank=True)
    question_field = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.question_field


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_field = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"{self.user} answered {self.answer_field}"
