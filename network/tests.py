from django.test import Client, TestCase

from .models import User, Post


class NetworkTestCase(TestCase):

    def setUp(self):
        # Create users.
        u1 = User.objects.create(username="Harry", password="Potter")
        u2 = User.objects.create(username="Ron", password="Weasley")

        # Create posts.
        p1 = Post.objects.create(poster=u1, body="Malfoy is a jerk")
        p2 = Post.objects.create(poster=u2, body="Gryffindor rules!")
        p3 = Post.objects.create(poster=u1, body="Why is Snape such a jerk?")

    def test_posts_count(self):
        u = User.objects.get(username="Harry")
        self.assertEqual(u.posts.count(), 2)
