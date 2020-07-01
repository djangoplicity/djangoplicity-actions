# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from djangoplicity.actions.models import Action
from djangoplicity.actions.plugins import ActionPlugin

# Create your tests here.
class ActionsTestCase(TestCase):

    #add new action, register it and get choices list for this action
    def test_action(self):
        action = Action(plugin='Simple action', name='test')
        simpleAction = SimpleAction()
        action.register_plugin(SimpleAction)
        list_choices = action.get_plugin_choices()
        self.assertEquals(list_choices, [(SimpleAction.get_class_path(), SimpleAction.action_name)] )


class SimpleAction( ActionPlugin ):
    action_name = 'Simple action'

    def run( self, conf ):
        print "Run"