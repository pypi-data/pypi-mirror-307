from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Risk, RiskRelation, RiskAssignment
from core.models import ObjectType
from drf_yasg.utils import swagger_serializer_method
from netbox.api.fields import ChoiceField, ContentTypeField
from utilities.api import get_serializer_for_model


class RiskSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:risks-api:risk-detail'
    )

    class Meta:
        model = Risk
        fields = ('id', 'url', 'display', 'name', 'description')


class RiskRelationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:risks-api:riskrelation-detail'
    )

    class Meta:
        model = RiskRelation
        fields = ('id', 'url', 'display', 'name', 'description')


class NestedRiskAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:risks-api:riskassignment-detail')
    risk = RiskSerializer(nested=True)
    relation = RiskRelationSerializer(nested=True)

    class Meta:
        model = RiskAssignment
        fields = ['id', 'url', 'display', 'risk', 'relation']


class RiskAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:risks-api:riskassignment-detail')
    object_type = ContentTypeField(
        queryset=ObjectType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    risk = RiskSerializer(nested=True)
    relation = RiskRelationSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = RiskAssignment
        fields = [
            'id', 'url', 'display', 'object_type', 'object_id', 'object', 'risk', 'relation', 'created',
            'last_updated',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(
            instance.object_type.model_class(), prefix='Nested')
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data
