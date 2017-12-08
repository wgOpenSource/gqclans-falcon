from logging import getLogger

import falcon

from resources import GraphQLResource, StaticGraphiQLResource

logger = getLogger(f'api.{__name__}')


app = falcon.API()
app.req_options.keep_blank_qs_values = True
app.req_options.auto_parse_form_urlencoded = True
app.add_route('/graphql', GraphQLResource())
app.add_route('/graphiql', StaticGraphiQLResource())
app.add_route('/graphiql/{static_file}', StaticGraphiQLResource())