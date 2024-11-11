import requests
import json
import httpx
import pytgpt.exceptions as exceptions
from pytgpt.utils import Optimizers
from pytgpt.utils import Conversation
from pytgpt.utils import AwesomePrompts
from pytgpt.base import Provider, AsyncProvider
from typing import AsyncGenerator

session = requests.Session()

default_model = "meta/llama-2-70b-chat"


class LLAMA2(Provider):
    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 800,
        temperature: float = 0.75,
        presence_penalty: int = 0,
        frequency_penalty: int = 0,
        top_p: float = 0.9,
        model: str = default_model,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
    ):
        """Instantiates LLAMA2

        Args:
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 800.
            temperature (float, optional): Charge of the generated text's randomness. Defaults to 0.75.
            presence_penalty (int, optional): Chances of topic being repeated. Defaults to 0.
            frequency_penalty (int, optional): Chances of word being repeated. Defaults to 0.
            top_p (float, optional): Sampling threshold during inference time. Defaults to 0.9.
            model (str, optional): LLM model name. Defaults to "meta/llama-2-70b-chat".
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
        """
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.model = model
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.top_p = top_p
        self.chat_endpoint = "https://www.llama2.ai/api"
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://www.llama2.ai/",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.llama2.ai",
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        session.headers.update(self.headers)
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        session.proxies = proxies

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict:
        """Chat with AI

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
           dict : {}
        ```json
        {
           "text" : "How may I help you today?"
        }
        ```
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )
        session.headers.update(self.headers)

        payload = {
            "prompt": f"{conversation_prompt}<s>[INST] {prompt} [/INST]",
            "model": self.model,
            "systemPrompt": "You are a helpful assistant.",
            "temperature": self.temperature,
            "topP": self.top_p,
            "maxTokens": self.max_tokens_to_sample,
            "image": None,
            "audio": None,
        }

        def for_stream():
            response = session.post(
                self.chat_endpoint, json=payload, stream=True, timeout=self.timeout
            )
            if (
                not response.ok
                or not response.headers.get("Content-Type")
                == "text/plain; charset=utf-8"
            ):
                raise exceptions.FailedToGenerateResponseError(
                    f"Failed to generate response - ({response.status_code}, {response.reason})"
                )

            message_load: str = ""
            for value in response.iter_lines(
                decode_unicode=True,
                delimiter="\n",
                chunk_size=self.stream_chunk_size,
            ):
                try:
                    if bool(value.strip()):
                        message_load += value + "\n"
                        resp: dict = dict(text=message_load)
                        yield value if raw else resp
                        self.last_response.update(resp)
                except json.decoder.JSONDecodeError:
                    pass
            self.conversation.update_chat_history(
                prompt, self.get_message(self.last_response)
            )

        def for_non_stream():
            for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            ):
                yield self.get_message(response)

        def for_non_stream():
            return self.get_message(
                self.ask(
                    prompt,
                    False,
                    optimizer=optimizer,
                    conversationally=conversationally,
                )
            )

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (str): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response["text"]


class AsyncLLAMA2(AsyncProvider):
    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 800,
        temperature: float = 0.75,
        presence_penalty: int = 0,
        frequency_penalty: int = 0,
        top_p: float = 0.9,
        model: str = default_model,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
    ):
        """Instantiates LLAMA2

        Args:
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 800.
            temperature (float, optional): Charge of the generated text's randomness. Defaults to 0.75.
            presence_penalty (int, optional): Chances of topic being repeated. Defaults to 0.
            frequency_penalty (int, optional): Chances of word being repeated. Defaults to 0.
            top_p (float, optional): Sampling threshold during inference time. Defaults to 0.9.
            model (str, optional): LLM model name. Defaults to "meta/llama-2-70b-chat".
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
        """
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.model = model
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.top_p = top_p
        self.chat_endpoint = "https://www.llama2.ai/api"
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://www.llama2.ai/",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.llama2.ai",
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        self.session = httpx.AsyncClient(
            headers=self.headers,
            proxies=proxies,
        )

    async def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict | AsyncGenerator:
        """Chat with AI asynchronously.

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
           dict|AsyncGeneraror[dict] : ai content
        ```json
        {
           "text" : "How may I help you today?"
        }
        ```
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        payload = {
            "prompt": f"{conversation_prompt}<s>[INST] {prompt} [/INST]",
            "model": self.model,
            "systemPrompt": "You are a helpful assistant.",
            "temperature": self.temperature,
            "topP": self.top_p,
            "maxTokens": self.max_tokens_to_sample,
            "image": None,
            "audio": None,
        }

        async def for_stream():
            async with self.session.stream(
                "POST", self.chat_endpoint, json=payload, timeout=self.timeout
            ) as response:
                if (
                    not response.is_success
                    or not response.headers.get("Content-Type")
                    == "text/plain; charset=utf-8"
                ):
                    raise exceptions.FailedToGenerateResponseError(
                        f"Failed to generate response - ({response.status_code}, {response.reason_phrase})"
                    )
                message_load: str = ""
                async for value in response.aiter_lines():
                    try:
                        if bool(value.strip()):
                            message_load += value + "\n"
                            resp: dict = dict(text=message_load)
                            yield value if raw else resp
                            self.last_response.update(resp)
                    except json.decoder.JSONDecodeError:
                        pass
            self.conversation.update_chat_history(
                prompt, await self.get_message(self.last_response)
            )

        async def for_non_stream():
            async for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else await for_non_stream()

    async def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str | AsyncGenerator:
        """Generate response `str` asynchronously.
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str|AsyncGenerator: Response generated
        """

        async def for_stream():
            async_ask = await self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            )
            async for response in async_ask:
                yield await self.get_message(response)

        async def for_non_stream():
            return await self.get_message(
                await self.ask(
                    prompt,
                    False,
                    optimizer=optimizer,
                    conversationally=conversationally,
                )
            )

        return for_stream() if stream else await for_non_stream()

    async def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (str): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response["text"]


if __name__ == "__main__":
    bot = LLAMA2()

    def main():
        resp = bot.ask("hello")
        for value in resp:
            print(value)

    async def asyncmain():
        bot = AsyncLLAMA2()
        resp = await bot.chat("hello", True)
        # print(resp)
        async for value in resp:
            print(value)

    # main()
    import asyncio

    asyncio.run(asyncmain())
