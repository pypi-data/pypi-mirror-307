from enum import unique
from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel, ChangeLoggedModel
from django.urls import reverse
from netbox.models.features import EventRulesMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import ObjectType
from django.db.models.signals import post_delete
from django.dispatch import receiver
from virtualization.models import VirtualMachine


class Risk(NetBoxModel):
    name = models.CharField(
        max_length=250,
        unique=True
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:risks:risk', args=[self.pk])


class RiskRelation(NetBoxModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        # return 'reskrel'
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:risks:riskrelation', args=[self.pk])


class RiskAssignment(ChangeLoggedModel, EventRulesMixin):
    object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='object_type',
        fk_field='object_id'
    )
    risk = models.ForeignKey(
        to='risks.Risk',
        on_delete=models.PROTECT,
        related_name='risk_assignments'
    )
    relation = models.ForeignKey(
        to='risks.RiskRelation',
        on_delete=models.PROTECT,
        related_name='risk_assignments'
    )

    clone_fields = ('object_type', 'object_id')

    class Meta:
        ordering = ['risk']
        unique_together = ('object_type', 'object_id',
                           'risk', 'relation')

    def __str__(self):
        return str(self.risk)

    def get_absolute_url(self):
        return reverse('plugins:risks:risk', args=[self.risk.pk])


@receiver(post_delete, sender=VirtualMachine, dispatch_uid='del_risk_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='virtualmachine').id
    instance_id = kwargs.get('instance').id
    objs = RiskAssignment.objects.filter(
        object_id=instance_id, object_type=object_type_id)
    objs.delete()
