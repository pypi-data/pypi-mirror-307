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

import ptuevents.models


class PTUEvent(NetBoxModel):
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
        verbose_name_plural = 'Unacceptable events'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptuevent', args=[self.pk])


class PTUEventRelation(NetBoxModel):
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
        verbose_name_plural = 'Event relationship'

    def __str__(self):
        # return 'reskrel'
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptueventrelation', args=[self.pk])

class PTUEventAssignment(ChangeLoggedModel, EventRulesMixin):
    object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='object_type',
        fk_field='object_id'
    )
    ptuevent = models.ForeignKey(
        to='ptuevents.ptuevent',
        on_delete=models.PROTECT,
        related_name='ptuevent_assignments'
    )
    relation = models.ForeignKey(
        to='ptuevents.PTUEventRelation',
        on_delete=models.PROTECT,
        related_name='ptuevent_assignments'
    )

    clone_fields = ('object_type', 'object_id')

    class Meta:
        ordering = ['ptuevent']
        unique_together = ('object_type', 'object_id',
                           'ptuevent', 'relation')

    def __str__(self):
        return str(self.ptuevent)

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptuevent', args=[self.ptuevent.pk])


@receiver(post_delete, sender=VirtualMachine, dispatch_uid='del_PTUEvent_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='virtualmachine').id
    instance_id = kwargs.get('instance').id
    objs = PTUEventAssignment.objects.filter(
        object_id=instance_id, object_type=object_type_id)
    objs.delete()


class PTAppSystem(NetBoxModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='ptappsystem',
        blank=False,
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptappsystem', args=[self.pk])

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Application systems'


class PTAppSystemAssignment(ChangeLoggedModel, EventRulesMixin):
    object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='object_type',
        fk_field='object_id'
    )
    app_system = models.ForeignKey(
        to='ptuevents.PTAppSystem',
        on_delete=models.PROTECT,
        related_name='ptappsystem_assignments'
    )

    clone_fields = ('object_type', 'object_id')

    class Meta:
        ordering = ['app_system']
        unique_together = ('object_type', 'object_id',
                           'app_system')

    def __str__(self):
        return str(self.app_system)

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptappsystem', args=[self.app_system.pk])


@receiver(post_delete, sender=VirtualMachine, dispatch_uid='del_appsystem_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='virtualmachine').id
    instance_id = kwargs.get('instance').id
    objs = PTAppSystemAssignment.objects.filter(
        object_id=instance_id, object_type=object_type_id)
    objs.delete()


class PTUsers(NetBoxModel):
    name = models.CharField(
        max_length=250,
    )

    firstname = models.CharField(
        max_length=250,
        blank=True,
    )
    lastname = models.CharField(
        max_length=250,
        blank=True,
    )

    ENABLED = 'enabled'
    DISABLED = 'disabled'
    DELETED = 'deleted'
    NEEDACTION = 'need action'

    CHOICES = (
        (ENABLED, ENABLED),
        (DISABLED, DISABLED),
        (DELETED, DELETED),
        (NEEDACTION, NEEDACTION),
    )

    status = models.CharField(
        max_length=250,
        unique=False,
        choices=CHOICES,
        default=ENABLED
    )

    sAMAccountName = models.CharField(
        max_length=250,
        unique=True,
        blank=False,
    )

    ad_sid = models.CharField(
        max_length=250,
        blank=False,
        unique=True,
    )

    vpnIPaddress = models.CharField(
        max_length=250,
        blank=True,
    )
    ad_description = models.CharField(
        max_length=250,
        blank=True,
    )
    position = models.CharField(
        max_length=250,
        blank=True,
    )
    department = models.CharField(
        max_length=250,
        blank=True,
    )
    comment = models.CharField(
        max_length=250,
        blank=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptusers', args=[self.pk])

    # Запрет изменения поля ad_sid
    def save(self, *args, **kwargs):
        if self.pk:
            original = PTUsers.objects.get(pk=self.pk)
            self.ad_sid = original.ad_sid
        super(PTUsers, self).save(*args, **kwargs)


class PTWorkstations(NetBoxModel):

    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
    )

    CN = models.CharField(
        max_length=250,
        blank=False,
    )

    DistinguishedName = models.CharField(
        max_length=500,
        unique=True,
        blank=False,
    )

    ad_sid = models.CharField(
        max_length=250,
        blank=False,
        unique=True,
    )

    ad_description = models.CharField(
        max_length=500,
        blank=True,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Workstations'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptworkstations', args=[self.pk])

    # Запрет изменения поля ad_sid
    def save(self, *args, **kwargs):
        if self.pk:
            original = PTWorkstations.objects.get(pk=self.pk)
            self.ad_sid = original.ad_sid
        super(PTWorkstations, self).save(*args, **kwargs)


@receiver(post_delete, sender=PTUsers, dispatch_uid='del_PTUEvent_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='ptusers').id
    instance_id = kwargs.get('instance').id
    objs = PTUEventAssignment.objects.filter(
        object_id=instance_id, object_type=object_type_id)
    objs.delete()


@receiver(post_delete, sender=PTWorkstations, dispatch_uid='del_PTUEvent_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='ptworkstations').id
    instance_id = kwargs.get('instance').id
    objs = PTUEventAssignment.objects.filter(
            object_id=instance_id, object_type=object_type_id)
    objs.delete()


class PTWorkstationsAssignment(ChangeLoggedModel, EventRulesMixin):
    object_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='object_type',
        fk_field='object_id'
    )
    pt_workstations = models.ForeignKey(
        to='ptuevents.PTWorkstations',
        on_delete=models.PROTECT,
        related_name='ptworkstations_assignments'
    )

    clone_fields = ('object_type', 'object_id')

    class Meta:
        ordering = ['pt_workstations']
        unique_together = ('object_type', 'object_id', 'pt_workstations')

    def __str__(self):
        return str(self.pt_workstations)

    def get_absolute_url(self):
        return reverse('plugins:ptuevents:ptworkstations', args=[self.pt_workstations.pk])


@receiver(post_delete, sender=PTUsers, dispatch_uid='del_workstations_assignment')
def del_assignments(sender, **kwargs):
    object_type_id = ObjectType.objects.get(model='ptusers').id
    instance_id = kwargs.get('instance').id
    objs = PTWorkstationsAssignment.objects.filter(
        object_id=instance_id, object_type=object_type_id)
    objs.delete()
