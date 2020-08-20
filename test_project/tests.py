# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from builtins import str
from django.test import TestCase, TransactionTestCase
from djangoplicity.actions.models import Action, ActionParameter, ActionLog
from djangoplicity.actions.plugins import ActionPlugin
from test_project.models import SimpleAction, SimpleError, SomeListTest, SomeEventAction, SomeMergeTest
from django.core.cache import cache

import traceback

# Create your tests here.
class ActionsTestCase(TestCase):

    def createNewAction(self):
        Action.objects.all().delete()
        a = Action(plugin='test_project.models.SimpleAction', name='Simple action')
        a.register_plugin(SimpleAction)
        a.save()
        return a
    
    def createNewActionParameter(self, action):
        ActionParameter.objects.all().delete()
        p = ActionParameter.objects.create(action=action ,name='test', value='value test')
        p.save()
        return p

    # to test EventActions
    def createList(self):
        l,created = SomeListTest.objects.get_or_create( api_key='INVALID', list_id='INVALID', web_id='INVALID', connected=True )
        l.save()
        return l

    # add new action, register it and get choices list for this action
    def test_list_choices(self):
        a = self.createNewAction()
        list_choices = a.get_plugin_choices()
        self.assertEquals(list_choices, [(SimpleAction.get_class_path(), SimpleAction.action_name)] )
    
    # get plugin class registered
    def test_get_class_registered(self):
        a = self.createNewAction()
        self.assertEquals(a.get_plugincls(), SimpleAction)

    # Get an instance of the plug-in for this action
    def test_get_plugin(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        self.assertIsInstance(a.get_plugin(), SimpleAction)
    
    # get list of parameters for action
    def test_get_parameters(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        self.assertEquals(a.get_parameters(), {u'test': u'value test'})

    def test_dispatch(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        a.dispatch()
        #self.assertTrue(SimpleAction.successful())
        a.post_save_handler()

    # get_value method get value of the parameter 
    def test_get_value(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        self.assertEquals(p.get_value(), u'value test')

    def test_create_actionLog(self):
            a = ActionLog(plugin='test_project.tests.SimpleAction', name='Simple action')
            self.assertEquals(a.name, u'Simple action')
    
    def test_on_success(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        log = a.get_plugin()
        log.on_success(retval=None, task_id=None, args=({u"message": u"hello", u"name": u"world"}, {u"message": u"hello", u"name": u"world"}), kwargs={u"message": u"hello", u"name": u"world"})
        # self.assertEquals(a.name, u'Simple action')

    def test_on_failure(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        log = a.get_plugin()
        
        args=({u"message": u"hello", u"name": u"world"}, {u"message": u"hello", u"name": u"world"})
        kwargs={u"message": u"hello", u"name": u"world"}
        try:
            raise RuntimeError('something bad happened!')
        except RuntimeError as inst:
            info=traceback.format_exc()
            einfo=SimpleError(info)
        log.on_failure(exc=None, task_id=None, args=args, kwargs=kwargs, einfo=einfo)
        # self.assertEquals(a.name, u'Simple action')
    
    def test_get_arguments(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        log = a.get_plugin()
        args = log.get_arguments(u"message", u"hello", u"world", a = u"hello")
        self.assertEquals(args, ((u'hello', u'world'), {'a': u'hello'}))

    def test_get_class_path(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        log = a.get_plugin()
        path = log.get_class_path()
        self.assertEquals(path, SimpleAction.get_class_path())
    
    def test_register(self):
        Action.objects.all().delete()
        SimpleAction.register()
        list_register={'test_project.models.SimpleAction':SimpleAction}
        self.assertEquals(Action._plugins, list_register)
            
    def test_run(self):
        Action.objects.all().delete()
        a=SimpleAction()
        a.run('test')
        self.assertEquals(u'test', a.action_run_test)
    
    def test_get_key(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        l = self.createList()
        SomeEventAction( action=a, on_event='on_unsubscribe', model_object=l ).save()
        self.assertEquals(SomeEventAction._get_key(), u'djangoplicity.mailinglists.action_cache')
    
    def test_delete_cache(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        l = self.createList()
        SomeEventAction( action=a, on_event='on_unsubscribe', model_object=l ).save()
        SomeEventAction.clear_cache()
        self.assertIsNone(cache.get( SomeEventAction._key ))
    
    def test_create_get_cache(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        l = self.createList()
        SomeEventAction( action=a, on_event='on_unsubscribe', model_object=l ).save()
        self.assertEquals(SomeEventAction.create_cache(), SomeEventAction.get_cache())

    def test_get_actions(self):
        a = self.createNewAction()
        p = self.createNewActionParameter(a)
        l = self.createList()
        (tag_objid,created) = SomeMergeTest.objects.get_or_create( list=l, name='Object ID' )
        l.primary_key_field = tag_objid
        l.save()
        SomeEventAction( action=a, on_event='on_unsubscribe', model_object=l ).save()
        action_cache = SomeEventAction.get_cache()
        actions = action_cache[ str( l.pk ) ]
        self.assertEquals(SomeEventAction.get_actions(l.pk), actions)
    
    def test_get_actions_for_event(self):
            a = self.createNewAction()
            p = self.createNewActionParameter(a)
            l = self.createList()
            (tag_objid,created) = SomeMergeTest.objects.get_or_create( list=l, name='Object ID' )
            l.primary_key_field = tag_objid
            l.save()
            SomeEventAction( action=a, on_event='on_unsubscribe', model_object=l ).save()
            action_cache = SomeEventAction.get_cache()
            actions = action_cache[ 'on_unsubscribe' ]
            self.assertEquals(SomeEventAction.get_actions_for_event(on_event='on_unsubscribe'), actions)
        