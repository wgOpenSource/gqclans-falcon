import os

import falcon


class StaticGraphiQLResource:
    def on_get(self, req, resp, static_file=None):
        if static_file is None:
            static_file = 'graphiql.html'
            resp.content_type = 'text/html; charset=UTF-8'
        elif static_file == 'graphiql.css':
            resp.content_type = 'text/css; charset=UTF-8'
        else:
            resp.content_type = 'application/javascript; charset=UTF-8'

        resp.status = falcon.HTTP_200
        resp.stream = open(os.path.join('static', 'graphiql', static_file), 'rb')
