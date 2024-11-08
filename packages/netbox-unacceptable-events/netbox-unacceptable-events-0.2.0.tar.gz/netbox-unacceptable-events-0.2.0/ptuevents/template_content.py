from netbox.plugins import PluginTemplateExtension
from core.models import ObjectType
from .models import PTUEventAssignment, PTAppSystemAssignment


class PTUEventVMPanel(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'

    def right_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        PTUEvent_ass = PTUEventAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        PTUEvents = []
        for r in PTUEvent_ass:
            PTUEvents.append({
                'assignment_id': r.id,
                'name': r.ptuevent,
                'rel': r.relation.name
            })

        return self.render('ptuevents/ptuevent_panel.html', extra_context={
            'PTUEvents': PTUEvents
        })



# class PTUEventAppSystemPanel(PluginTemplateExtension):
#     model = 'PTUEvents.PTAppSystem'

#     def right_page(self):
#         app_system = self.context['object']
#         object_type_id = ObjectType.objects.get_for_model(
#             model=app_system).id
#         PTUEvent_ass = PTUEventAssignment.objects.filter(
#             object_id=app_system.id, object_type=object_type_id)
#         PTUEvents = []
#         for r in PTUEvent_ass:
#             PTUEvents.append({
#                 'assignment_id': r.id,
#                 'name': r.PTUEvent,
#                 'rel': r.relation.name
#             })

#         return self.render('PTUEvents/PTUEvent_panel.html', extra_context={
#             'PTUEvents': PTUEvents
#         })


class PTUEventDevicePanel(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        device = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=device).id
        PTUEvent_ass = PTUEventAssignment.objects.filter(
            object_id=device.id, object_type=object_type_id)
        PTUEvents = []
        for r in PTUEvent_ass:
            PTUEvents.append({
                'assignment_id': r.id,
                'name': r.PTUEvent,
                'rel': r.relation.name
            })

        return self.render('ptuevents/ptuevent_panel.html', extra_context={
            'PTUEvents': PTUEvents
        })


class AppSystemVMPanel(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'
    # model = 'dcim.device'

    def left_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        app_systems = PTAppSystemAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        # print(vars(AppSystem_ass))
        # print(AppSystem_ass)
        AppSystems = []
        for s in app_systems:
            AppSystems.append({
                'id': s.id,
                'app_system': s.app_system})
            # print(s.__dict__)

        # print(AppSystems)
        return self.render('ptuevents/appsystem_panel.html', extra_context={
            'app_systems': AppSystems
        })


class AppSystemDevicePanel(PluginTemplateExtension):
    model = 'dcim.device'

    def left_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        app_systems = PTAppSystemAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        AppSystems = []
        for s in app_systems:
            AppSystems.append({
                'id': s.id,
                'app_system': s.app_system})
            # print(s.__dict__)

        return self.render('ptuevents/appsystem_panel.html', extra_context={
            'app_systems': AppSystems
        })


template_extensions = [AppSystemVMPanel, AppSystemDevicePanel, PTUEventVMPanel,
                       PTUEventDevicePanel]

