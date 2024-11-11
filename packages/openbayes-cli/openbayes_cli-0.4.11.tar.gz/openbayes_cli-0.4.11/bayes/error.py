
class Error(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def credential_notfound_error(name: str) -> Exception:
    return Exception(f"配置名 '{name}' 不存在, 使用 bayes switch '{name}' -e {{endpoint}} 设置")
