from starlette import status


class FriendlyException(Exception):

    def __init__(self, message: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, status_code: int = status.HTTP_200_OK, desc: str = None):
        self.message = message
        self.code = code
        self.desc = desc
        self.status_code = status_code
