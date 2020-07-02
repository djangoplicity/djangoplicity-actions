# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from djangoplicity.actions.models import Action, ActionParameter, ActionLog
from djangoplicity.actions.plugins import ActionPlugin

# Create your tests here.
class ActionsTestCase(TestCase):

    def createAction(self):
        action = Action(plugin='SimpleAction', name='Simple action')
        action.register_plugin(SimpleAction)
        return action
    
    def createActionParameter(self):
        action = self.createAction()
        action.save()
        action_parameter = ActionParameter.objects.create(action=action ,name='test', value='str', help_text='test')
        
        return action_parameter

    #add new action, register it and get choices list for this action
    def test_list_choices(self):
        action = self.createAction()
        list_choices = action.get_plugin_choices()
        self.assertEquals(list_choices, [(SimpleAction.get_class_path(), SimpleAction.action_name)] )
        # self.assertIsNone(None)
    
    def test_other(self):
        actionParameter = self.createActionParameter()
        return actionParameter


class SimpleAction( ActionPlugin ):
    action_name = 'Simple action'

    action_parameters = [
            ( '<param name>', '<param help text>', '<value type:str|int|bool|date>' ),
            ( 'password', 'Admin password for list', 'str' ),
            ( 'somenum', 'Some num', 'int' ),
        ]

    def run( self, conf ):
        pass