from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import PTUEventRelation, PTUEvent, PTUEventAssignment, PTAppSystem, PTAppSystemAssignment, PTUsers, PTWorkstations, PTWorkstationsAssignment
from django.contrib.auth.models import ContentType
from drf_yasg.utils import swagger_serializer_method
from netbox.api.fields import ChoiceField, ContentTypeField
from utilities.api import get_serializer_for_model


class NestedPTUEventSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptuevent-detail'
    )

    class Meta:
        model = PTUEvent
        fields = ('id', 'display', 'url', 'name', 'description')


class PTUEventSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptuevent-detail'
    )

    class Meta:
        model = PTUEvent
        fields = ('id', 'url', 'display', 'name', 'description')


class NestedPTUEventRelationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptueventrelation-detail'
    )

    class Meta:
        model = PTUEventRelation
        fields = ('id', 'url', 'display', 'name', 'description')


class PTUEventRelationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptueventrelation-detail'
    )

    class Meta:
        model = PTUEventRelation
        fields = ('id', 'url', 'display', 'name', 'description')


class NestedPTUEventAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptueventassignment-detail')
    ptuevent = NestedPTUEventSerializer()
    relation = NestedPTUEventRelationSerializer

    class Meta:
        model = PTUEventAssignment
        fields = ['id', 'url', 'display', 'ptuevent', 'relation']


class PTUEventAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptueventassignment-detail')
    content_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    ptuevent = NestedPTUEventSerializer()
    relation = NestedPTUEventRelationSerializer(
        required=False, allow_null=True)

    class Meta:
        model = PTUEventAssignment
        fields = [
            'id', 'url', 'display', 'content_type', 'object_id', 'object', 'ptuevent', 'relation', 'created',
            'last_updated',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(
            instance.content_type.model_class(), prefix='Nested')
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data


class NestedPTAppSystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptappsystem-detail')

    class Meta:
        model = PTAppSystem
        fields = ('id', 'slug', 'url', 'display', 'name', 'tenant')


class PTAppSystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptappsystem-detail')

    class Meta:
        model = PTAppSystem
        fields = ('id', 'slug', 'url', 'display', 'name', "description",
                  'comments', 'tags', 'custom_fields', 'created', 'last_updated', 'tenant')


class NestedAPTppSystemAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptappsystemassignment-detail')
    app_system = NestedPTAppSystemSerializer()

    class Meta:
        model = PTAppSystemAssignment
        fields = ['id', 'url', 'display', 'PTAppSystem', 'relation']


class PTAppSystemAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptappsystemassignment-detail')
    content_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    app_system = NestedPTAppSystemSerializer()

    class Meta:
        model = PTAppSystemAssignment
        fields = [
            'id', 'url', 'display', 'content_type', 'object_id', 'object', 'app_system', 'created',
            'last_updated',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(
            instance.content_type.model_class(), prefix='Nested')
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data


class NestedPTUsersSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptusers-detail'
    )

    class Meta:
        model = PTUsers
        fields = ('id', 'url', 'display', 'name', 'description',
                  'firstname', 'lastname', 'status', 'sAMAccountName',
                  'ad_sid', 'vpnIPaddress', 'ad_description',
                  'position', 'department')


class PTUsersSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptusers-detail'
    )

    class Meta:
        model = PTUsers
        fields = ('id', 'url', 'display', 'name', 'description',
                  'firstname', 'lastname', 'status', 'sAMAccountName',
                  'ad_sid', 'vpnIPaddress', 'ad_description',
                  'position', 'department')


class NestedPTWorkstationsSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptworkstations-detail'
    )

    class Meta:
        model = PTWorkstations
        fields = ('id', 'url', 'display', 'name', 'description',
                  'CN', 'DistinguishedName', 'ad_sid', 'location', 'ad_description')


class PTWorkstationsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ptuevents-api:ptworkstations-detail'
    )

    class Meta:
        model = PTWorkstations
        fields = ('id', 'url', 'display', 'name', 'description',
                  'CN', 'DistinguishedName', 'ad_sid', 'location', 'ad_description')


class NestedPTWorkstationsAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='plugins-api:ptuevents-api:ptworkstations-detail')

    class Meta:
        model = PTWorkstations
        fields = ('id', 'url', 'display', 'name', 'description',
                  'CN', 'DistinguishedName', 'ad_sid', 'location', 'ad_description')


class PTWorkstationsAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='plugins-api:ptuevents-api:ptworkstationsassignment-detail')
    content_type = ContentTypeField(queryset=ContentType.objects.all())
    object = serializers.SerializerMethodField(read_only=True)
    pt_workstations = NestedPTWorkstationsAssignmentSerializer()

    class Meta:
        model = PTWorkstationsAssignment
        fields = [
            'id', 'url', 'display', 'content_type', 'object_id', 'object', 'pt_workstations', 'created', 'last_updated',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(
            instance.content_type.model_class(), prefix='Nested')
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data

