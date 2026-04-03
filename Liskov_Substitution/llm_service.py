from src.services.llm.openai_factory import OpenAIFactory 

class LLMInitializationError(Exception):
    pass

class LLMModelProvider:
    def __init__(self):
        self._factory = OpenAIFactory()
        self._model = None

    @property
    def model(self):
        if self._model is not None:
            return self._model

        try:
            self._model = self._factory.create_llm()
        except Exception as e:
            raise LLMInitializationError(f"Failed to initialize LLM model: {e}") from e

        if self._model is None:
            raise LLMInitializationError("LLM factory returned None")

        return self._model

llm_model_provider = LLMModelProvider()
