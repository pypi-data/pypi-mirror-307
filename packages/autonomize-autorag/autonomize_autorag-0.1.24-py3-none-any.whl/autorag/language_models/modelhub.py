"""Modelhub Embedding module implementation"""

# pylint: disable=line-too-long, duplicate-code

from typing import Any, Dict, List, Literal, Optional, Union, override

from autorag.core.credential import ModelhubCredential
from autorag.language_models.base import LanguageModel
from autorag.language_models.ollama import OllamaLanguageModel
from autorag.types.language_models import Generation
from autorag.utilities.logger import get_logger

logger = get_logger()


class ModelhubLanguageModel(LanguageModel):
    """
    Implementation of the LanguageModel abstract base class using Modelhub hosted models.

    This class utilizes Modelhubs's deployed language models' API to generate text data.
    It supports different models served using modelhub for text generation tasks like conversation
    and RAG systems.

    Example:
    .. code-block:: python

        from autorag.core.credential import ModelhubCredential
        from autorag.language_models.modelhub import ModelhubLanguageModel

        credential = ModelhubCredential()
        provider_name = "ollama"
        llm = ModelhubLanguageModel(credential=credential, provider="ollama")

        model_name = "llama3.1:8b-instruct-q8_0"
        llm.generate(
            messages=[{"role": "user", "content": "What is RAG?"}],
            model=model_name
        )
    """

    def __init__(
        self,
        credential: ModelhubCredential,
        provider_name: Literal["ollama"] = "ollama",
    ):
        """
        Initialize the ModelhubEmbedding instance.

        Args:
            credential ModelhubCredential: The credential object for authorizing with Modelhub.
            provider str: Which community provider to use for the language model.

        Raises:
            ValueError: If neither (client_id and client_secret) nor token is provided.
        """

        self._credential = credential
        self._get_provider(provider_name=provider_name)

    def _get_provider(self, provider_name: Literal["ollama"] = "ollama"):
        """
        Given the provider's name this method creates an instance of the provider deployed using modelhub.

        Args:
            provider_name (str): The name of the provider, for example:
        """
        if provider_name == "ollama":
            self._provider = OllamaLanguageModel(self._credential)

    def _generate(  # pylint: disable=too-many-locals
        self,
        messages: List[Dict[str, Any]],
        model: str,
        tool: Optional[Dict[str, Any]] = None,
        max_tokens: Optional[int] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        temperature: Optional[float] = None,
        num_ctx: Optional[int] = 8096,
        **kwargs: Any,
    ) -> Generation:
        """
        Generates a response based on the provided messages and model settings.

        Args:
            messages (List[Dict[str, Any]]): A list of dictionaries containing the conversation history or prompts.
            model (str): The model identifier to use for text generation.
            tool (Optional[Dict[str, Any]]): A dictionary containing tool definition, if applicable.
            max_tokens (Optional[int]): Maximum number of tokens to generate. Defaults to no limit.
            frequency_penalty (Optional[float]): Penalizes new tokens based on their frequency in the generated text.
            presence_penalty (Optional[float]): Penalizes new tokens based on whether they appear in the generated text.
            seed (Optional[int]): Random seed for reproducibility of results.
            stop (Optional[Union[str, List[str]]]): String or list of strings to end the generation when encountered.
            temperature (Optional[float]): Controls randomness in the generation.
            Higher values (e.g., 1.0) make output more random, lower values (e.g., 0.2) make it more deterministic.
            num_ctx (Optional[int]): Sets the size of the context window used to generate the next token.
            (Default: 8096)
            **kwargs (Any): Additional optional arguments for further customization.

        Returns:
            Generation: Generated response based on the input messages and model parameters.
        """
        output = self._provider.generate(
            messages,
            model,
            tool,
            max_tokens,
            frequency_penalty,
            presence_penalty,
            seed,
            stop,
            temperature,
            num_ctx=num_ctx,
            **kwargs,
        )

        return output

    @override
    async def agenerate(  # pylint: disable=too-many-locals
        self,
        messages: List[Dict[str, Any]],
        model: str,
        tool: Optional[Dict[str, Any]] = None,
        max_tokens: Optional[int] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        temperature: Optional[float] = None,
        num_ctx: Optional[int] = 8096,
        **kwargs: Any,
    ) -> Generation:
        """
        Asynchronously generates a response based on the provided messages and model settings.

        Args:
            messages (List[Dict[str, Any]]): A list of dictionaries containing the conversation history or prompts.
            model (str): The model identifier to use for text generation.
            tool (Optional[Dict[str, Any]]): A dictionary containing tool definition, if applicable.
            max_tokens (Optional[int]): Maximum number of tokens to generate. Defaults to no limit.
            frequency_penalty (Optional[float]): Penalizes new tokens based on their frequency in the generated text.
            presence_penalty (Optional[float]): Penalizes new tokens based on whether they appear in the generated text.
            seed (Optional[int]): Random seed for reproducibility of results.
            stop (Optional[Union[str, List[str]]]): String or list of strings to end the generation when encountered.
            temperature (Optional[float]): Controls randomness in the generation.
            Higher values (e.g., 1.0) make output more random, lower values (e.g., 0.2) make it more deterministic.
            num_ctx (Optional[int]): Sets the size of the context window used to generate the next token.
            (Default: 8096)
            **kwargs (Any): Additional optional arguments for further customization.

        Returns:
            Generation: Generated response based on the input messages and model parameters.
        """
        output = await self._provider.agenerate(
            messages,
            model,
            tool,
            max_tokens,
            frequency_penalty,
            presence_penalty,
            seed,
            stop,
            temperature,
            num_ctx=num_ctx,
            **kwargs,
        )
        return output
