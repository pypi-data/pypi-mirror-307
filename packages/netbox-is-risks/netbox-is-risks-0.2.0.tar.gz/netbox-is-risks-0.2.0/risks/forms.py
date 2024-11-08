from netbox.forms import NetBoxModelForm
from pyrsistent import v
from .models import Risk, RiskRelation, RiskAssignment
from utilities.forms.fields import DynamicModelChoiceField
from django import forms


class RiskForm(NetBoxModelForm):
    class Meta:
        model = Risk
        fields = ('name', 'description', 'comments')


class RiskRelationForm(NetBoxModelForm):
    class Meta:
        model = RiskRelation
        fields = ('name', 'description')


class RiskAssignmentForm(forms.ModelForm):
    risk = DynamicModelChoiceField(
        queryset=Risk.objects.all()
    )
    relation = DynamicModelChoiceField(
        queryset=RiskRelation.objects.all()
    )

    class Meta:
        model = RiskAssignment
        fields = (
            'risk', 'relation',
        )
