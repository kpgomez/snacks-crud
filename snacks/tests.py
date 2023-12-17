from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack


# Create your tests here.
class SnacksCreateUpdateDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="password"
        )

        self.snack = Snack.objects.create(
            title="pickle", purchaser=self.user, description="vinegary"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "pickle")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "pickle")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(self.snack.description, "vinegary")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "pickle",
                "purchaser": self.user.id,
                "description": "vinegary",
            }, follow=True
        )

        # self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "pickle")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "updated title", "description": "new title", "purchaser": self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"), target_status_code=200)

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)


class SnacksReadTests(TestCase):
    def setUp(self):
        purchaser = get_user_model().objects.create(username="tester", password="password")
        Snack.objects.create(title="pickle", purchaser=purchaser)

    def test_list_page_status_code(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_page_template(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "snack_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_list_page_context(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        snacks = response.context["object_list"]
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].title, "pickle")
        self.assertEqual(snacks[0].description, "")
        self.assertEqual(snacks[0].purchaser.username, "tester")

    def test_detail_page_status_code(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "snack_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_detail_page_context(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.get(url)
        snack = response.context["snack"]
        self.assertEqual(snack.title, "pickle")
        self.assertEqual(snack.description, "")
        self.assertEqual(snack.purchaser.username, "tester")

