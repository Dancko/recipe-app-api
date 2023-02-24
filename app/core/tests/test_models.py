"""
Tests for models.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Tests for models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with the email successful."""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if new user's email is normalized."""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['test3@example.COM', 'test3@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a new user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email='sample@example.com',
            password='sample123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipies successfully."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        recipe = models.Recipe.create(
            user=user,
            title='Sample recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)
