from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    # Default field from AbstractUser: username, password, email, first_name, last_name
    # Add additional fields
    phone = models.CharField(max_length=20, blank=True, null=False)
    website = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    education = models.CharField(
        max_length=20,
        choices=[
            ('HS', 'High School'),
            ('GED', 'GED'),
            ('CERT', 'Certificate'),
            ('AA', 'Associate\'s'),
            ('BS', 'Bachelor\'s'),
            ('MA', 'Master\'s'),
            ('PHD', 'Ph.D.'),
            ],
        blank=True,
        null=True
    )
    major = models.CharField(max_length=100, blank=True, null=True)
    courses = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'django_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    profile_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'django_profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.profile_name} - {self.user}"

# # Candidate model - Main user profile
# class Candidate(models.Model):
#     candidate_id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     first_name = models.CharField(max_length=100, blank=False, null=False)
#     last_name = models.CharField(max_length=100, blank=False, null=False)
#     email = models.EmailField(unique=True, blank=False, null=False)
#     phone = models.CharField(max_length=20, blank=False, null=False)
#     website = models.URLField(max_length=200, blank=True, null=True)
#     skills = models.TextField(blank=True, null=True)
#     address = models.TextField(max_length=500, blank=True, null=True)
#
#     # Education fields
#     education = models.CharField(
#         max_length=50,
#         choices=[
#             ('HS', 'High School'),
#             ('GED', 'GED'),
#             ('CERT', 'Certificate'),
#             ('AA', 'Associate\'s'),
#             ('BA', 'Bachelor\'s'),
#             ('MA', 'Master\'s'),
#             ('PHD', 'Ph.D.'),
#         ],
#         blank=True,
#         null=True
#     )
#     major = models.CharField(max_length=100, blank=True, null=True)
#     courses = models.TextField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'django_candidate'
#         verbose_name = 'Candidate'
#         verbose_name_plural = 'Candidates'
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# Experience model - For candidate work experience
class Experience(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    title = models.CharField(max_length=125, blank=False, null=False)
    company = models.CharField(max_length=100, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'django_experience'
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return f"{self.title} at {self.company} - {self.profile}"


# Project model - For candidate projects
class Project(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=True, null=True)

    class Meta:
        db_table = 'django_project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.title} - {self.profile}"


# Reference model - For candidate references
class Reference(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='references'
    )
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'django_reference'
        verbose_name = 'Reference'
        verbose_name_plural = 'References'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Reference for {self.profile}"
