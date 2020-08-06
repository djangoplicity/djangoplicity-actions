from django.db import models
from djangoplicity.actions.models import EventAction
from djangoplicity.actions.plugins import ActionPlugin


class SomeListTest(models.Model):
    api_key = models.CharField(max_length=255, verbose_name="API key")
    list_id = models.CharField(unique=True, max_length=50)
    web_id = models.CharField(blank=True, max_length=255)
    connected = models.BooleanField(default=False)

ACTION_EVENTS = (
    ('on_subscribe', 'On subscribe'),
    ('on_unsubscribe', 'On unsubscribe'),
    ('on_upemail', 'On update email'),
    ('on_profile', 'On profile update'),
    ('on_cleaned', 'On cleaned'),
    ('on_campaign', 'On campaign'),
)
class SomeEventAction(EventAction):
    '''
    Define actions to be executed when a event occurs for a list (e.g. sub,
    unsub, clean etc.)
    '''
    def __init__(self, *args, **kwargs):
        super(SomeEventAction, self).__init__(*args, **kwargs)
        self._meta.get_field('on_event')._choices = ACTION_EVENTS

    model_object = models.ForeignKey(SomeListTest)

    _key = 'djangoplicity.mailinglists.action_cache'

    @classmethod
    def _get_key( cls ):
        return cls._key

class SomeMergeTest(models.Model):
    '''
    Store information about mailchimp mergefields for each list.
    Merge vars are now named Merge fields, but the class name was kept
    '''
    list = models.ForeignKey(SomeListTest)
    name = models.CharField(max_length=255)


class SimpleAction( ActionPlugin ):
    action_name = 'Simple action'
    action_run_test = ''

    action_parameters = [
            ('name', 'list name', 'str'),
            ( 'password', 'Admin password for list', 'str' ),
            ( 'somenum', 'Some num', 'int' ),
        ]
    abstract = True

    def __init__(self, *args, **kwargs):
        pass

    def run( self, conf ):
        self.action_run_test = conf

class SimpleError():
    def __init__(self, traceback):
        self.traceback=traceback