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

        # Follow users.
        u2.following.add(u1)

    def test_posts_count(self):
        u = User.objects.get(username="Harry")
        self.assertEqual(u.posts.count(), 2)

    def test_following_count(self):
        u1 = User.objects.get(username="Harry")
        u2 = User.objects.get(username="Ron")

        self.assertEqual(u1.following.count(), 0)
        self.assertEqual(u2.following.count(), 1)

    def test_followers_count(self):
        u1 = User.objects.get(username="Harry")
        u2 = User.objects.get(username="Ron")

        self.assertEqual(u1.followers.count(), 1)
        self.assertEqual(u2.followers.count(), 0)
