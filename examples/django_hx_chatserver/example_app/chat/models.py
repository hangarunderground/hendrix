from django.db import models
from django.utils import timezone
from django.template import Context, loader

from hendrix.contrib.async.signals import message_signal
# Create your models here.


class ChatMessage(models.Model):
    """
        a model that stores chat history
    """

    sender = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, db_index=True)
    content = models.TextField('enter a message')
    date_created = models.DateTimeField(default=timezone.now)


def save_chat_message(*args, **kwargs):

    """
    kwargs will always include:
    {
     'data': # will always be exactly what your client sent on the socket
        # in this case...
        {u'message': u'hi', u'sender': u'anonymous', u'channel': u'homepage'},
     'dispatcher': # the dispatcher that will allow for broadcasting a response
      <hendrix.contrib.async.messaging.MessageDispatcher object at 0x10ddb1c10>,
    }
    """

    data = kwargs.get('data')
    if data.get('message') and data.get('channel'):

        cm = ChatMessage.objects.create(
            sender=data.get('sender'),
            content=data.get('message'),
            channel=data.get('channel')
        )

        t = loader.get_template('message.html')

        kwargs.get('dispatcher').send(cm.channel, {
            'html': t.render(Context({'message': cm}))
        })

message_signal.connect(save_chat_message)