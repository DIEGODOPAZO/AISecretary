from .token_manager import TokenManager


class MicrosoftBaseRequest:
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager