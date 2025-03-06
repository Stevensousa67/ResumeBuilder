from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Reference, Project, Experience


# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Define fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'education', 'is_staff')
    # Define searchable fields
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'skills')
    # Define filters for the sidebar
    list_filter = ('education', 'is_staff', 'is_superuser', 'is_active')

    # Customize the fieldsets for the add/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'website', 'address')}),
        ('Education', {'fields': ('education', 'major', 'courses')}),
        ('Skills', {'fields': ('skills',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    ordering = ('email',)


# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_name', 'user', 'experience_count', 'project_count', 'reference_count')
    search_fields = ('profile_name', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user',)

    def experience_count(self, obj):
        return obj.experiences.count()
    experience_count.short_description = 'Experiences'

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'

    def reference_count(self, obj):
        return obj.references.count()
    reference_count.short_description = 'References'


# Reference Admin
@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'relationship', 'profile')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'relationship', 'profile__profile_name')
    list_filter = ('relationship', 'profile__user')


# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'profile')
    search_fields = ('title', 'description', 'profile__profile_name')
    list_filter = ('profile__user',)


# Experience Admin
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date', 'profile')
    search_fields = ('title', 'company', 'start_date', 'end_date', 'profile__profile_name')
    list_filter = ('company', 'profile__user')


# Ensure the custom User model is registered with the admin site
admin.site.unregister(User)  # Unregister default User if already registered
admin.site.register(User, UserAdmin)  # Register custom User with UserAdmin