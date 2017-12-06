import json
from collections import OrderedDict
from contextlib import redirect_stdout
from os.path import devnull

import falcon

from queries.default import default_schema


def set_graphql_allow_header(req, resp, resource):
    resp.set_header('Allow', 'GET, POST, OPTIONS')


@falcon.after(set_graphql_allow_header)
class GraphQLResource:
    def on_options(self, req, resp):
        resp.status = falcon.HTTP_204
        pass

    def on_head(self, req, resp):
        pass

    def on_get(self, req, resp):
        if req.params and 'query' in req.params and req.params['query']:
            query = str(req.params['query'])
        else:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(
                {'errors': [{'message': 'Must provide query string.'}]},
                separators=(',', ':')
            )
            return

        if 'variables' in req.params and req.params['variables']:
            try:
                variables = json.loads(str(req.params['variables']), object_pairs_hook=OrderedDict)
            except json.decoder.JSONDecodeError:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'Variables are invalid JSON.'}]},
                    separators=(',', ':')
                )
                return
        else:
            variables = ''

        operation_name = (
            str(req.params['operationName']) if 'operationName' in req.params and req.params['operationName'] else None
        )

        with open(devnull, 'w') as f:
            with redirect_stdout(f):
                result = (
                    default_schema.execute(query, variable_values=variables) if operation_name is None else
                    default_schema.execute(query, variable_values=variables, operation_name=operation_name)
                )

        if result.data:
            data_ret = {'data': result.data}
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(data_ret, separators=(',', ':'))
            return
        elif result.errors:
            err_msgs = [{'message': str(i)} for i in result.errors]
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'errors': err_msgs}, separators=(',', ':'))
            return
        else:
            raise RuntimeError

    def on_post(self, req, resp):
        if req.params and 'query' in req.params and req.params['query']:
            query = str(req.params['query'])
        else:
            query = None

        if 'variables' in req.params and req.params['variables']:
            try:
                variables = json.loads(str(req.params['variables']), object_pairs_hook=OrderedDict)
            except json.decoder.JSONDecodeError:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'Variables are invalid JSON.'}]},
                    separators=(',', ':')
                )
                return
        else:
            variables = None

        operation_name = (
            str(req.params['operationName']) if 'operationName' in req.params and req.params['operationName'] else None
        )

        if req.content_type and 'application/json' in req.content_type:
            if req.content_length in (None, 0):
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'POST body sent invalid JSON.'}]},
                    separators=(',', ':')
                )
                return

            raw_json = req.stream.read()
            try:
                req.context['post_data'] = json.loads(
                    raw_json.decode('utf-8'),
                    object_pairs_hook=OrderedDict
                )
            except json.decoder.JSONDecodeError:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'POST body sent invalid JSON.'}]},
                    separators=(',', ':')
                )
                return

            if (query is None and req.context['post_data'] and
                'query' in req.context['post_data']):
                query = str(req.context['post_data']['query'])
            elif query is None:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'Must provide query string.'}]},
                    separators=(',', ':')
                )
                return

            if (variables is None and req.context['post_data'] and
                'variables' in req.context['post_data'] and
                req.context['post_data']['variables']):
                variables = str(req.context['post_data']['variables'])
                try:
                    json_str = str(req.context['post_data']['variables'])
                    variables = json.loads(json_str, object_pairs_hook=OrderedDict)
                except json.decoder.JSONDecodeError:
                    resp.status = falcon.HTTP_400
                    resp.body = json.dumps(
                        {'errors': [
                            {'message': 'Variables are invalid JSON.'}
                        ]},
                        separators=(',', ':')
                    )
                    return
            elif variables is None:
                variables = ''

            if (
                operation_name is None and
                'operationName' in req.context['post_data'] and
                req.context['post_data']['operationName']
            ):
                operation_name = str(req.context['post_data']['operationName'])

        elif req.content_type and 'application/graphql' in req.content_type:
            req.context['post_data'] = req.stream.read().decode('utf-8')

            if query is None and req.context['post_data']:
                query = str(req.context['post_data'])

            elif query is None:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {'errors': [{'message': 'Must provide query string.'}]},
                    separators=(',', ':')
                )
                return

        elif query is None:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(
                {'errors': [{'message': 'Must provide query string.'}]},
                separators=(',', ':')
            )
            return

        with open(devnull, 'w') as f:
            with redirect_stdout(f):
                result = (
                    default_schema.execute(query, variable_values=variables) if operation_name is None else
                    default_schema.execute(query, variable_values=variables, operation_name=operation_name)
                )

        if result.data:
            data_ret = {'data': result.data}
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(data_ret, separators=(',', ':'))
            return
        elif result.errors:
            err_msgs = [{'message': str(i)} for i in result.errors]
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'errors': err_msgs}, separators=(',', ':'))
            return
        else:
            raise RuntimeError

    def on_put(self, req, resp):
        self.prepare_not_found_response(resp)

    def on_patch(self, req, resp):
        self.prepare_not_found_response(resp)

    def on_delete(self, req, resp):
        self.prepare_not_found_response(resp)

    @staticmethod
    def prepare_not_found_response(resp):
        resp.status = falcon.HTTP_405
        resp.body = json.dumps(
            {'errors': [
                {'message': 'GraphQL only supports GET and POST requests.'}
            ]},
            separators=(',', ':')
        )
