import jsonschema
import mock
import requests

from unittest import skip

from django.conf import settings
from django.test import TestCase

from openldap.api import user_api
from openldap.tests.test_api import OpenLDAPBaseAPITests
from users.tests.test_models import CustomUserTests


class OpenLDAPUserAPITests(OpenLDAPBaseAPITests):

    @mock.patch('requests.get')
    def test_list_users_query(self, get_mock):
        """
        Retrieve a list of all users.
        """
        jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wbG'
               'UuY29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MDk4O'
               'DY4LCJuYmYiOjE1MjcwOTgyNjgsImRhdGEiOnsiMCI6Inguam9lLmJsb2dncyIsImVycm9yIjoiIiwi'
               'Y291bnQiOjF9fQ.0Ah3-tL3sf_Nb1o7PkIvPlJ6P3q19_o7BK8Vbv_vGo4')
        get_mock.return_value = self._mock_response(
            status=200,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527098868,
            "nbf": 1527098268,
            "data": {
                "0": "x.joe.bloggs",
                "error": "",
                "count": 1
            }
        }
        result = user_api.list_users()
        self.assertEqual(result, expected_response)

    @mock.patch('requests.post')
    def test_create_user_query(self, post_mock):
        """
        Create a User.
        """
        jwt = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wbGUuY2'
               '9tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MTAwMTQxLCJuY'
               'mYiOjE1MjcwOTk1NDEsImRhdGEiOnsiY24iOiJ4LmpvZS5ibG9nZ3MiLCJzbiI6IkJsb2dncyIsImdpZG51'
               'bWJlciI6IjUwMDAwMDEiLCJnaXZlbm5hbWUiOiJKb2UiLCJkaXNwbGF5TmFtZSI6Ik1yIEpvZSBCbG9nZ3M'
               'iLCJ0aXRsZSI6Ik1yIiwiaG9tZWRpcmVjdG9yeSI6Ii9ob21lL3guam9lLmJsb2dncyIsImxvZ2luc2hlbG'
               'wiOiIvYmluL2Jhc2giLCJvYmplY3RjbGFzcyI6WyJpbmV0T3JnUGVyc29uIiwicG9zaXhBY2NvdW50Iiwid'
               'G9wIl0sInRlbGVwaG9uZW51bWJlciI6IjAwMDAwLTAwMC0wMDAiLCJtYWlsIjoiam9lLmJsb2dnc0BiYW5n'
               'b3IuYWMudWsiLCJ1aWQiOiJ4LmpvZS5ibG9nZ3MiLCJ1aWRudW1iZXIiOiI1MDAwMDAxIn19.LDxd6hvdqC'
               '8CdG17ucNrD7Dy5Q4T7k-B-vHOTLOWs7Q')
        post_mock.return_value = self._mock_response(
            status=201,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527100141,
            "nbf": 1527099541,
            "data": {
                "cn": "x.joe.bloggs",
                "sn": "Bloggs",
                "gidnumber": "5000001",
                "givenname": "Joe",
                "displayName": "Mr Joe Bloggs",
                "title": "Mr",
                "homedirectory": "/home/x.joe.bloggs",
                "loginshell": "/bin/bash",
                "objectclass": [
                    "inetOrgPerson",
                    "posixAccount",
                    "top",
                ],
                "telephonenumber": "00000-000-000",
                "mail": "joe.bloggs@bangor.ac.uk",
                "uid": "x.joe.bloggs",
                "uidnumber": "5000001"
            }
        }
        result = user_api.create_user(user=self.user)
        self.assertEqual(result, expected_response)

        # Verify the user's profile information was updated correctly.
        self.assertEqual("5000001", self.user.profile.uid_number)
        self.assertEqual("x.joe.bloggs", self.user.profile.scw_username)

    @mock.patch('requests.get')
    def test_get_user_by_id_query(self, get_mock):
        """
        Get an existing user by id.
        """
        jwt = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wbGUuY'
               '29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MDk4OTIwLCJ'
               'uYmYiOjE1MjcwOTgzMjAsImRhdGEiOnsiMCI6eyJ1aWQiOnsiMCI6Inguam9lLmJsb2dncyIsImNvdW50I'
               'joxfSwibWFpbCI6eyIwIjoiam9lLmJsb2dnc0BiYW5nb3IuYWMudWsiLCJjb3VudCI6MX0sImRpc3BsYXl'
               'uYW1lIjp7IjAiOiJNciBKb2UgQmxvZ2dzIiwiY291bnQiOjF9LCJnaWRudW1iZXIiOnsiMCI6Ijk5OTk5O'
               'TkiLCJjb3VudCI6MX0sInVpZG51bWJlciI6eyIwIjoiOTk5OTk5OSIsImNvdW50IjoxfSwidGVsZXBob25'
               'lIjoiMDAwMDAtMDAwMDAwIn0sImVycm9yIjoiIiwiY291bnQiOjF9fQ.WG4MhgveQEn0vXult3RbOze2CB'
               'AzE3OwLqmnfGl0GLg')
        get_mock.return_value = self._mock_response(
            status=200,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527098920,
            "nbf": 1527098320,
            "data": {
                "0": {
                    "uid": {
                        "0": "x.joe.bloggs",
                        "count": 1
                    },
                    "mail": {
                        "0": "joe.bloggs@bangor.ac.uk",
                        "count": 1
                    },
                    "displayname": {
                        "0": "Mr Joe Bloggs",
                        "count": 1
                    },
                    "gidnumber": {
                        "0": "9999999",
                        "count": 1
                    },
                    "uidnumber": {
                        "0": "9999999",
                        "count": 1
                    },
                    "telephone": "00000-000000"
                },
                "error": "",
                "count": 1
            }
        }
        result = user_api.get_user_by_id(user_id='x.joe.bloggs')
        self.assertEqual(result, expected_response)

    @mock.patch('requests.get')
    def test_get_user_by_email_address_query(self, get_mock):
        """
        Get an existing user by email address.
        """
        jwt = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wbGUuY'
               '29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MDk4OTIwLCJ'
               'uYmYiOjE1MjcwOTgzMjAsImRhdGEiOnsiMCI6eyJ1aWQiOnsiMCI6Inguam9lLmJsb2dncyIsImNvdW50I'
               'joxfSwibWFpbCI6eyIwIjoiam9lLmJsb2dnc0BiYW5nb3IuYWMudWsiLCJjb3VudCI6MX0sImRpc3BsYXl'
               'uYW1lIjp7IjAiOiJNciBKb2UgQmxvZ2dzIiwiY291bnQiOjF9LCJnaWRudW1iZXIiOnsiMCI6Ijk5OTk5O'
               'TkiLCJjb3VudCI6MX0sInVpZG51bWJlciI6eyIwIjoiOTk5OTk5OSIsImNvdW50IjoxfSwidGVsZXBob25'
               'lIjoiMDAwMDAtMDAwMDAwIn0sImVycm9yIjoiIiwiY291bnQiOjF9fQ.WG4MhgveQEn0vXult3RbOze2CB'
               'AzE3OwLqmnfGl0GLg')
        get_mock.return_value = self._mock_response(
            status=200,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527098920,
            "nbf": 1527098320,
            "data": {
                "0": {
                    "uid": {
                        "0": "x.joe.bloggs",
                        "count": 1
                    },
                    "mail": {
                        "0": "joe.bloggs@bangor.ac.uk",
                        "count": 1
                    },
                    "displayname": {
                        "0": "Mr Joe Bloggs",
                        "count": 1
                    },
                    "gidnumber": {
                        "0": "9999999",
                        "count": 1
                    },
                    "uidnumber": {
                        "0": "9999999",
                        "count": 1
                    },
                    "telephone": "00000-000000"
                },
                "error": "",
                "count": 1
            }
        }
        result = user_api.get_user_by_email_address(email_address='joe.bloggs@bangor.ac.uk')
        self.assertEqual(result, expected_response)

    @skip("Pending OpenLDAP fix")
    @mock.patch('requests.delete')
    def test_deactivate_user_account_query(self, delete_mock):
        """
        Deactivate an existing user's OpenDLAP account
        """
        jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wb'
               'GUuY29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MTA'
               'wNTk3LCJuYmYiOjE1MjcwOTk5OTcsImRhdGEiOnsiZGVsZXRlIjoibW92ZWQgdG8gY249eC5qb2UuY'
               'mxvZ2dzLG91PVVzZXJzLG91PUluYWN0aXZlLGRjPWV4YW1wbGUsZGM9YWMsZGM9dWsifX0.KIac7dO'
               'JHfhPGPFJrSkKAtd5bIIOKBQaO9_82rB1pkA')
        delete_mock.return_value = self._mock_response(
            status=204,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527100597,
            "nbf": 1527099997,
            "data": {
                "delete": "moved to cn=x.joe.bloggs,ou=Users,ou=Inactive,dc=example,dc=ac,dc=uk"
            }
        }
        result = user_api.deactivate_user_account(user=self.user)
        self.assertEqual(result, expected_response)

    @mock.patch('requests.post')
    def test_reset_user_password_query(self, post_mock):
        """
        Reset a user's password.
        """
        jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wbGU'
               'uY29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI5MjQ5MjM'
               'zLCJuYmYiOjE1MjkyNDg2MzMsImRhdGEiOnsicGFzc3dvcmQiOiJTdWNjZXNzZnVsbHkgcmVzZXQgcGF'
               'zc3dvcmQifX0.ZC9yWYpDwszRs3TIt1naWmg0BSbl3U5SiW1LJ_hVEwM')
        post_mock.return_value = self._mock_response(
            status=201,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1529249233,
            "nbf": 1529248633,
            "data": {
                "password": "Successfully reset password"
            }
        }
        result = user_api.reset_user_password(user=self.user, password=12345678)
        self.assertEqual(result, expected_response)

    @mock.patch('requests.put')
    def test_activate_user_account_query(self, put_mock):
        """
        Activate an existing user's OpenLDAP account.
        """
        jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL29wZW5sZGFwLmV4YW1wb'
               'GUuY29tLyIsImF1ZCI6Imh0dHBzOi8vb3BlbmxkYXAuZXhhbXBsZS5jb20vIiwiaWF0IjoxNTI3MTA'
               'wNTE0LCJuYmYiOjE1MjcwOTk5MTQsImRhdGEiOnsiZW5hYmxlIjoibW92ZWQgdG8gY249eC5qb2UuY'
               'mxvZ2dzLG91PUV4YW1wbGVVbml2ZXJzaXR5LG91PUluc3RpdHV0aW9ucyxvdT1Vc2VycyxkYz1leGF'
               'tcGxlLGRjPWFjLGRjPXVrIn19.w4JBxjvITyGPDRw2crT2S4ZwNyzGUFWL1JRhcLGdxA8')
        put_mock.return_value = self._mock_response(
            status=200,
            content=jwt.encode(),
        )
        expected_response = {
            "iss": settings.OPENLDAP_JWT_ISSUER,
            "aud": settings.OPENLDAP_JWT_AUDIENCE,
            "iat": 1527100514,
            "nbf": 1527099914,
            "data": {
                "enable":
                "moved to cn=x.joe.bloggs,ou=ExampleUniversity,ou=Institutions,ou=Users,dc=example,dc=ac,dc=uk"
            }
        }
        result = user_api.activate_user_account(user=self.user)
        self.assertEqual(result, expected_response)

    def test_query_exceptions(self):
        """
        Ensure each query raises the correct error/exception.
        """
        queries = [
            (user_api.list_users, None),
            (user_api.create_user, {
                'user': self.user,
            }),
            (user_api.get_user_by_id, {
                'user_id': 'x.joe.bloggs'
            }),
            (user_api.get_user_by_email_address, {
                'email_address': 'joe.bloggs@bangor.ac.uk'
            }),
            (user_api.reset_user_password, {
                'user': self.user,
                'password': '1234567',
            }),
            #(user_api.deactivate_user_account, {
            #    'user': self.user,
            #}),
            (user_api.activate_user_account, {
                'user': self.user,
            }),
        ]
        for query, query_kwargs in queries:
            self._test_query_with_invalid_json_schema(query, query_kwargs)
            self._test_query_with_connection_error(query, query_kwargs)
            self._test_query_with_http_error(query, query_kwargs)
            self._test_query_with_timeout_error(query, query_kwargs)
