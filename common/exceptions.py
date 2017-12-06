import falcon


class BaseApplicationError(Exception):
    additional_data = None
    code = 500
    title = None
    message = falcon.HTTP_500
    description = None
