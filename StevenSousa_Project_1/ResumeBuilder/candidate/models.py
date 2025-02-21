from django.db import models

# Candidate model - Main user profile
class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    address = models.TextField(max_length=500, blank=True, null=True)


    # Education fields
    education = models.CharField(
        max_length=50,
        choices=[
            ('HS', 'High School'),
            ('BA', 'Bachelor\'s'),
            ('MA', 'Master\'s'),
            ('PHD', 'Ph.D.'),
        ],
        blank=True,
        null=True
    )
    major = models.CharField(max_length=100, blank=True, null=True)
    minor = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter GPA (e.g., 3.50)"
    )
    skills = models.TextField(blank=True, null=True)



    class Meta:
        db_table = 'django_candidate'
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Experience model - For candidate work experience
class Experience(models.Model):
    candidate = models.ForeignKey(
        Candidate,
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
        return f"{self.title} at {self.company} - {self.candidate}"


# Reference model - For candidate references
class Reference(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='references'
    )
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    relationship = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Relationship of reference to candidate"
    )

    class Meta:
        db_table = 'django_reference'
        verbose_name = 'Reference'
        verbose_name_plural = 'References'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Reference for {self.candidate}"


# Project model - For candidate projects
class Project(models.Model):
    candidate = models.ForeignKey(
        Candidate,
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
        return f"{self.title} - {self.candidate}"


# Course model - For candidate classes
class Course(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    course_name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        db_table = 'django_course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.course_name} - {self.candidate}"