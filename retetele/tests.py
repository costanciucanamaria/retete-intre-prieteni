# retetele/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta

from .models import Retete, Comment, Like

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="mario",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="ana",
            password="12345678"
        )

        self.reteta1 = Retete.objects.create(
            nume="Pizza",
            ingrediente="Branza",
            preparare="Coace",
            user=self.user1,
            data_creare=timezone.now() - timedelta(days=1)
        )

        self.reteta2 = Retete.objects.create(
            nume="Burger",
            ingrediente="Carne",
            preparare="Prajeste",
            user=self.user2,
            data_creare=timezone.now()
        )


# =====================================
# AUTH TESTS
# =====================================

class AuthenticationTests(BaseTestCase):

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "mario",
            "password": "12345678"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "username": "mario",
            "password": "gresit"
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="mario", password="12345678")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


# =====================================
# CRUD TESTS
# =====================================

class RecipeCRUDTests(BaseTestCase):

    def test_create_recipe(self):
        self.client.login(username="mario", password="12345678")

        response = self.client.post(reverse("introducere_reteta"), {
            "nume": "Paste",
            "ingrediente": "Paste",
            "preparare": "Fierbe"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Retete.objects.count(), 3)

    def test_read_home_page(self):
        response = self.client.get(reverse("retete"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertContains(response, "Burger")

    def test_update_recipe(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(
            reverse("modificare_reteta", args=[self.reteta1.id]),
            {
                "nume": "Pizza Noua",
                "ingrediente": "Branza",
                "preparare": "Coace"
            }
        )

        self.reteta1.refresh_from_db()
        self.assertEqual(self.reteta1.nume, "Pizza Noua")

    def test_delete_recipe(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(
            reverse("stergere_reteta", args=[self.reteta1.id])
        )

        self.assertEqual(Retete.objects.count(), 1)


# =====================================
# PERMISSION TESTS
# =====================================

class PermissionTests(BaseTestCase):

    def test_create_requires_login(self):
        response = self.client.get(reverse("introducere_reteta"))
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_edit_other_recipe(self):
        self.client.login(username="ana", password="12345678")

        response = self.client.post(
            reverse("modificare_reteta", args=[self.reteta1.id]),
            {
                "nume": "Hack",
                "ingrediente": "Hack",
                "preparare": "Hack"
            }
        )

        self.reteta1.refresh_from_db()
        self.assertNotEqual(self.reteta1.nume, "Hack")


# =====================================
# SEARCH + SORT TESTS
# =====================================

class SearchSortTests(BaseTestCase):

    def test_search_recipe(self):
        response = self.client.get(reverse("cautare_retete"), {
            "q": "Pizza"
        })

        self.assertContains(response, "Pizza")
        self.assertNotContains(response, "Burger")

    def test_sort_alphabetic(self):
        response = self.client.get(reverse("retete"), {
            "sort": "nume"
        })

        self.assertEqual(response.status_code, 200)

    def test_sort_newest(self):
        response = self.client.get(reverse("retete"), {
            "sort": "-data_creare"
        })

        self.assertEqual(response.status_code, 200)


# =====================================
# COMMENTS TESTS
# =====================================

class CommentTests(BaseTestCase):

    def test_add_comment(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(
            reverse("adauga_comment", args=[self.reteta1.id]),
            {
                "text": "Super reteta!"
            }
        )

        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_saved_user(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(
            reverse("adauga_comment", args=[self.reteta1.id]),
            {
                "text": "Excelent"
            }
        )

        comment = Comment.objects.first()
        self.assertEqual(comment.user.username, "mario")


# =====================================
# LIKE TESTS
# =====================================

class LikeTests(BaseTestCase):

    def test_like_recipe(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(
            reverse("adauga_like", args=[self.reteta2.id])
        )

        self.assertEqual(Like.objects.count(), 1)

    def test_adauga_like_unlike(self):
        self.client.login(username="mario", password="12345678")

        self.client.post(reverse("adauga_like", args=[self.reteta2.id]))
        self.client.post(reverse("adauga_like", args=[self.reteta2.id]))

        self.assertEqual(Like.objects.count(), 0)


# =====================================
# IMAGE TESTS
# =====================================

class UploadImageTests(BaseTestCase):

    def test_upload_image(self):
        self.client.login(username="mario", password="12345678")

        image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        self.client.post(
            reverse("adauga_poza", args=[self.reteta1.id]),
            {"poza": image}
        )

        self.reteta1.refresh_from_db()
        self.assertTrue(bool(self.reteta1.poza))


# =====================================
# MODEL TESTS
# =====================================

class ModelTests(BaseTestCase):

    def test_recipe_str(self):
        self.assertEqual(str(self.reteta1), "Pizza")