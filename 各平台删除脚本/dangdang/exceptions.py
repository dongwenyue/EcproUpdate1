"""异常处理类"""


class OpenApiError(Exception):
    """开发平台错误基类"""

    error_code: int
    error_msg: str

    def __init__(self, **kwargs):
        """初始化"""
        super().__init__()
        self.__dict__ = kwargs

    def __str__(self) -> str:
        return f"【当当】开放平台错误, error_code: {self.error_code}, error_msg: {self.error_msg}"
