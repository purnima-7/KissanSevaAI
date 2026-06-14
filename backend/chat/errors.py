class KnowledgeNotFoundError(Exception):
    """Raised when no relevant information is found in the dataset"""
    pass


class TokenLimitExceededError(Exception):
    """Raised when API token or rate limit is exceeded"""
    pass


class LLMServiceError(Exception):
    """Raised for other LLM/API failures"""
    pass
