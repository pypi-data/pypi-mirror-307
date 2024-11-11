class APIError(Exception):
    def __init__(self, message: str, response):
        try:
            body = response.json()
        except:
            body = response.text
        msg = f"{message}: {body['detail']}" if "detail" in body else message
        super().__init__(msg)