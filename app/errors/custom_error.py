
class Errors:
    class BaseException(Exception):
        msg = "Base Exeption"
        reason = ""

        def __init__(self, request=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if request:
                self.request = request

        def __str__(self):
            return f'{self.__class__.__name__}-{self.msg}'

    class ChainIdNotSupported(BaseException):
        msg = "Network not Supported"
        status_code = 40410

    @property
    @classmethod
    def POSSIBLE_SERVER_ERRORS(cls):
        return [i.__name__ for i in dir(cls)]

    @classmethod
    def POSSIBLE_SERVER_ERRORS_DETAILS(cls):
        res = []
        for i in dir(cls):
            item = getattr(cls, i)
            try:
                res.append(
                    {
                        "name": item.__name__,
                        "reason": item.msg,
                        "status_code": item.status_code
                    }
                )
            except:
                pass
        return res

    UNHANDELED_ERRORS_STATUS_CODE = 50000
