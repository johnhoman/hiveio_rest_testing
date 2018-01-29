import unittest
import sys
import json
import urllib3
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(0, "../")

from connect_manager import HiveApi

class AuthenticationTest(unittest.TestCase):

    _endpoint = "i2.hiveio.com:1443/api"

    def test_authentication_token(self):

        token = HiveApi.get_token(self._endpoint)
        self.assertNotEqual(token, None)


class GuestResponseTest(unittest.TestCase):
    """ goals
    1. Get the guest inventory
    2. Get guest by name through endpoint /guest/{name}
    """
    _endpoint = "i2.hiveio.com:1443/api/"
    
    def test_guest_inventory_get(self):
        """
            1. Get authentication token from HiveApi.connect
            2. Make sure a non empty inventory is returned
        """
        guests = HiveApi.guest_inventory_get(self._endpoint)

        self.assertNotEqual(guests, [])
        self.assertEqual(isinstance(guests, list), True)
        self.assertEqual(all(isinstance(i, dict) for i in guests), True)

    def test_guest_attributes(self):

        guest_keys = HiveApi.guest_names_get(self._endpoint)
        print(guest_keys)

    def test_guest_get_by_name(self):

        guests = HiveApi.guest_names_get(self._endpoint)
        guest = HiveApi.guest_get_by_name(self._endpoint, guests[0])

        self.assertEqual(isinstance(guest, dict), True)
        pprint(guest)


if __name__ == '__main__':
    unittest.main()