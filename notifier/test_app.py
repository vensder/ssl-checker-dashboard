import unittest
import app

class CheckResponseCode(unittest.TestCase):
    def check_response_code(self):
        self.assertEqual(app.post_message(app.webhook_url, "example.com", 5), 200)

