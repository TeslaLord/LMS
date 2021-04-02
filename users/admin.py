from django.contrib import admin
from .models import Grade, Question, Answer, Section, Profile


class adminGrade(admin.ModelAdmin):
    fields = ('user', 'ut1', 'ut2', 'ut3')


class adminQuestion(admin.ModelAdmin):
    fields = ['question_field', 'section']


admin.site.register(Grade, adminGrade)
admin.site.register(Question, adminQuestion)
admin.site.register(Answer)
admin.site.register(Section)
admin.site.register(Profile)
