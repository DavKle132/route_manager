from django.db import models

from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first = models.CharField(max_langth=25)
#     last = models.CharField(max_length=25)

class Route(models.Model):
    route_name = models.CharField(max_length=200, unique=True)
    route_length = models.DecimalField(max_digits=10, decimal_places=1)
    active_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    workflows = models.ManyToManyField('Workflow', through='RouteWorkflow', related_name='routes')

    def __str__(self):
        return self.route_name

@receiver(post_save, sender=Route, dispatch_uid="route_post_save")
def route_post_save(sender, instance, **kwargs):
    """Argument explanation:

       sender - The model class. (MyModel)
       instance - The actual instance being saved.
       created - Boolean; True if a new record was created.

       *args, **kwargs - Capture the unneeded `raw` and `using`(1.3) arguments.
    """
    workflow = Workflow.objects.filter(workflow_name='WF1').first()
    rw = RouteWorkflow.objects.create(route=instance, workflow=workflow)
    rw.save()


class Note(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_frame = models.IntegerField(default=0)
    end_frame = models.IntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return str(self.route) + ' ' + str(self.message)[0:5] + '...'

class Workflow(models.Model):
    workflow_name = models.CharField(max_length=200)

    def __str__(self):
        return self.workflow_name

class RouteWorkflow(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.route) + ' ' + str(self.workflow) + ' ' + str(self.status)

class RouteLog(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return ''

# class Role(models.Model):
#     PROCESSOR = 1
#     QC = 2
#     SUPERVISOR = 3
#     ROLE_CHOICES = (
#         (PROCESSOR, 'processor'),
#         (QC, 'qc'),
#         (SUPERVISOR, 'supervisor'),
#     )

#     id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

#     users = models.ManyToManyField(User)

    
    
    

