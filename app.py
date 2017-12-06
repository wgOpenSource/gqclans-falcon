from logging import getLogger

import falcon

from resources import GraphQLResource

logger = getLogger(f'api.{__name__}')


app = falcon.API()
app.req_options.keep_blank_qs_values = True
app.req_options.auto_parse_form_urlencoded = True
app.add_route('/graphql', GraphQLResource())
