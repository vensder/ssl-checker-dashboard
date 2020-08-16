import unittest
import slack_post as sp


class CheckResponseCode(unittest.TestCase):
    def test_response_code(self):
        self.assertEqual(sp.post_message(sp.webhook_url, "example.com", 5), 200)
