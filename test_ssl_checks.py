import unittest
import ssl_checks
from datetime import datetime


class ExpirationDateTimeGoogle(unittest.TestCase):
    def test_ssl_expiration_datetime(self):
        self.assertTrue(ssl_checks.expiration_datetime("google.com"))
        self.assertIsInstance(
            ssl_checks.expiration_datetime("google.com"), datetime)


class DaysBeforeExpirationGoogle(unittest.TestCase):
    def test_get_ssl_expiry_datetime_v2(self):
        self.assertIsInstance(
            ssl_checks.days_before_expiration("google.com")[1], int)


class ExpirationDateTimeYandex(unittest.TestCase):
    def test_ssl_expiration_datetime(self):
        self.assertTrue(ssl_checks.expiration_datetime("ya.ru"))
        self.assertIsInstance(
            ssl_checks.expiration_datetime("ya.ru"), datetime)


class DaysBeforeExpirationYandex(unittest.TestCase):
    def test_get_ssl_expiry_datetime_v2(self):
        self.assertIsInstance(
            ssl_checks.days_before_expiration("ya.ru")[1], int)
