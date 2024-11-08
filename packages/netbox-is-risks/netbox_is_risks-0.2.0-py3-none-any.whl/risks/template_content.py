from netbox.plugins import PluginTemplateExtension
from core.models import ObjectType
from risks.models import RiskAssignment


class RiskVMPanel(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'

    def right_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        risk_ass = RiskAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        risks = []
        for r in risk_ass:
            risks.append({
                'assignment_id': r.id,
                'name': r.risk,
                'rel': r.relation.name
            })

        return self.render('risks/risk_panel.html', extra_context={
            'risks': risks
        })


class RiskAppSystemPanel(PluginTemplateExtension):
    model = 'netbox_app_systems.AppSystem'

    def right_page(self):
        app_system = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(
            model=app_system).id
        risk_ass = RiskAssignment.objects.filter(
            object_id=app_system.id, object_type=object_type_id)
        risks = []
        for r in risk_ass:
            risks.append({
                'assignment_id': r.id,
                'name': r.risk,
                'rel': r.relation.name
            })

        return self.render('risks/risk_panel.html', extra_context={
            'risks': risks
        })


class RiskDevicePanel(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        device = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=device).id
        risk_ass = RiskAssignment.objects.filter(
            object_id=device.id, object_type=object_type_id)
        risks = []
        for r in risk_ass:
            risks.append({
                'assignment_id': r.id,
                'name': r.risk,
                'rel': r.relation.name
            })

        return self.render('risks/risk_panel.html', extra_context={
            'risks': risks
        })


template_extensions = [RiskVMPanel, RiskDevicePanel, RiskAppSystemPanel]
