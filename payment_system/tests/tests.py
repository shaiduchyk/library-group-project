from datetime import timedelta
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from payment_system.models import Payment, PaymentStatus, PaymentType
from borrowings.models import Borrowing
from books_service.models import Book
from payment_system.services.stripe_services import create_payment_session
from user.models import User


class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Covers.HARD,
            inventory=1,
            daily_fee=10.00,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )
        self.payment = Payment.objects.create(
            status=PaymentStatus.PENDING,
            type=PaymentType.PAYMENT,
            borrowing=self.borrowing,
            session_url="http://test.com",
            session_id="123456",
            money_to_pay=100.00,
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.payment),
            f"|Status: {self.payment.status} | "
            f"Type: {self.payment.type} | "
            f"Money to pay: {self.payment.money_to_pay}|",
        )


class PaymentViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="testpass"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Covers.HARD,
            inventory=1,
            daily_fee=10.00,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )
        self.payment = Payment.objects.create(
            status=PaymentStatus.PENDING,
            type=PaymentType.PAYMENT,
            borrowing=self.borrowing,
            session_url="http://test.com",
            session_id="123456",
            money_to_pay=100.00,
        )

    def test_list_payments(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("payments:payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("payments:payments-detail", kwargs={"pk": self.payment.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

    def test_list_payments_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse("payments:payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("payments:payments-detail", kwargs={"pk": self.payment.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="password123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="password123",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Covers.HARD,
            inventory=1,
            daily_fee=10.00,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
            is_active=True,
        )
        self.payment = Payment.objects.create(
            status=PaymentStatus.PENDING,
            type=PaymentType.PAYMENT,
            borrowing=self.borrowing,
            session_url="http://test.com",
            session_id="123456",
            money_to_pay=100.00,
        )

    def test_payments_listed(self):
        url = reverse("admin:payment_system_payment_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.payment.status)
        self.assertContains(res, self.payment.type)

    def test_payment_change_page(self):
        url = reverse(
            "admin:payment_system_payment_change",
            args=[self.payment.id]
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_payment_page(self):
        url = reverse("admin:payment_system_payment_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class PaymentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="testuser@test.com",
            password="12345"
        )

        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Covers.HARD,
            inventory=10,
            daily_fee=1.00
        )

        borrow_date = timezone.now().date()
        expected_return_date = borrow_date + timedelta(days=10)
        self.borrowing = Borrowing.objects.create(
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
            book=book,
            user=user
        )

    def test_create_payment_session(self):
        payment = create_payment_session(self.borrowing)
        self.assertEqual(payment.money_to_pay, 10.00)
        self.assertIsNotNone(payment.session_url)
        self.assertIsNotNone(payment.session_id)
