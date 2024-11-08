import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Risk, RiskRelation, RiskAssignment


class RiskTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    # default_action = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Risk
        fields = ('pk', 'name', 'description')
        default_columns = ('name', 'description')


class RiskRelationTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = RiskRelation
        fields = ('pk', 'name', 'description')
        default_columns = ('name', 'description')


class RiskAssignmentTable(NetBoxTable):
    object_type = columns.ContentTypeColumn(
        verbose_name='Object Type'
    )
    object = tables.Column(
        linkify=True,
        orderable=False
    )
    risk = tables.Column(
        linkify=True
    )
    relation = tables.Column(
        linkify=True
    )
    actions = columns.ActionsColumn(
        # actions=('edit', 'delete')
        actions = {
            'edit': set(),
            'delete': set(),
        }
    )

    class Meta(NetBoxTable.Meta):
        model = RiskAssignment
        fields = ('pk', 'object_type', 'object',
                  'risk', 'relation', 'actions')
        default_columns = ('pk', 'object_type', 'object',
                           'risk', 'relation')
