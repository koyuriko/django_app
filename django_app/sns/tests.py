from django.test import TestCase

from django.contrib.auth.models import User
from .models import Message

class SnsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr = cls.create_user()
        cls.create_message(usr)

    @classmethod
    def create_user(cls):
        #Create testuser
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)

    @classmethod
    def create_message(cls, usr):
        #create test message
        Message(content='this is test message.', owner_id=usr.id).save()
        Message(content='test', owner_id=usr.id).save()
        Message(content="ok", owner_id=usr.id).save()
        Message(content="ng", owner_id=usr.id).save()
        Message(content='finish', owner_id=usr.id).save()

    def test_check(self):
        usr = User.objects.first()
        self.assertIsNotNone(usr)
        msg = Message.objects.first()
        self.assertIsNotNone(msg)











# class SnsTests(TestCase):
#     def test_check(self):
#         x = True
#         self.assertTrue(x)
#         y = 100
#         self.assertGreater(y, 0)
#         arr = [10, 20, 30]
#         self.assertIn(20, arr)
#         nn = None
#         self.assertIsNone(nn)
