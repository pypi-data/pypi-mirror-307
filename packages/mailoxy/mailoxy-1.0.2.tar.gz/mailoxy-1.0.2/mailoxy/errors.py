class MaiQrCodeError(ValueError):

    def __init__(self):
        super().__init__("Mai qrcode str must start with 'SGWCMAID'")


class GetUserIDError(RuntimeError):

    def __init__(self, errorID):
        super().__init__(f"errorID:{errorID}")


class MaiQrCodeTimeoutError(RuntimeError):
    def __init__(self):
        super().__init__("Mai qrcode time out")


class LoginError(RuntimeError):
    def __init__(self):
        super().__init__("登陆失败,请在微信“舞萌 | 中二”服务号上点击“玩家二维码”按钮后重试")


class IsLoginError(RuntimeError):
    def __init__(self):
        super().__init__("账号已登录")


class DivingFishError(Exception):
    def __init__(self,message):
        super().__init__(message)
