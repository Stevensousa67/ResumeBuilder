from django.contrib import admin
from .models import Candidate, Reference, Project, Experience, Course

# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'education', 'major',
                    'minor', 'gpa', 'skills')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'education', 'major', 'minor', 'gpa',
                     'skills')
    list_filter = ('education', 'major', 'minor', 'gpa')


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'relationship')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'relationship')
    list_filter = ('relationship',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    search_fields = ('title', 'company', 'start_date', 'end_date')
    list_filter = ('company',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name',)
    search_fields = ('course_name',)
    list_filter = ('course_name',)
