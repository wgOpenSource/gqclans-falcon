import falcon

from tests import BaseTestCase


class PingQueryTest(BaseTestCase):
    url = '/graphql'

    def test_get_ok(self):
        """
        Should return 200 OK and expected body, encoded with JSON.
        """
        expected_body = {
            'data': {
                'ping': 'ok'
            }
        }
        params = {
            'query': '{ ping }'
        }

        response = self.client.get(self.url, query_string=params)

        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, response.body)
        self.assertEqual('application/json; charset=UTF-8', response.headers['content-type'])

    def test_post_ok(self):
        """
        Should return 200 OK and expected body, encoded with JSON.
        """
        expected_body = {
            'data': {
                'ping': 'ok'
            }
        }
        params = {
            'query': '{ ping }'
        }

        response = self.client.post(self.url, data=params)

        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, response.body)
        self.assertEqual('application/json; charset=UTF-8', response.headers['content-type'])

    def test_put_not_allower(self):
        """
        Should return 405 Not Allowed for methods differ from GET and POST
        """
        for method in ('PUT', 'PATCH', 'DELETE'):
            func = getattr(self.client, method.lower())
            response = func(self.url)
            self.assertEqual(falcon.HTTP_405, response.status)
