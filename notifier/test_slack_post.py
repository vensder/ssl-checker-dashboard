import unittest
import slack_post as sp

webhook_url = environ["secrets.SLACK_WEBHOOK_URL"]

class CheckResponseCode(unittest.TestCase):
    def test_response_code(self):
        self.assertEqual(sp.post_message(webhook_url, "example.com", 5), 200)

