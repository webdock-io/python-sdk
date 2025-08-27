import os
import unittest

from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock
load_dotenv()


class TestAccount(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))

    def test_account_info(self):
        account = self.client.account.info()
        self.assertIsInstance(account.get("body").get("userId"), int, "userId should be of type int")
