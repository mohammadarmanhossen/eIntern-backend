from django.db import models

class SubjectType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ToolsType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StipendType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ProjectType(models.Model):    
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Internship(models.Model):
    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("running", "Running"),
        ("completed", "Completed"),
    )

    title = models.CharField(max_length=200)
    details = models.TextField(default="No details provided")
    mode_type = models.CharField(max_length=20) 
    working_hours = models.CharField(max_length=50)
    office_location = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    certificate = models.CharField(max_length=50)
    mentorship = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )


    subject_type = models.ForeignKey(SubjectType, on_delete=models.SET_NULL, null=True)
    stipend_type = models.ForeignKey(StipendType, on_delete=models.SET_NULL, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True)
    tools_type = models.ManyToManyField(ToolsType, blank=True)


    def __str__(self):
        return f"{self.title} ({self.mode_type})"




class Arman(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)