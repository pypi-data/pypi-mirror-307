from sparrow import ConcurrentRequester
from typing import TYPE_CHECKING, Union
import asyncio
if TYPE_CHECKING:
    from sparrow.async_api.interface import RequestResult


class OpenAIClient:
    def __init__(self,
                 base_url: str,
                 api_key='EMPTY',
                 concurrency_limit=10,
                 timeout=600,
                 **kwargs):
        self._client = ConcurrentRequester(
            concurrency_limit=concurrency_limit,
            timeout=timeout,
        )
        self._headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {api_key}"}
        self._base_url = base_url.rstrip('/')
        self._api_key = api_key

    def wrap_to_request_params(self, messages: list, model: str, **kwargs):
        request_params = {
            'json': {
                'messages': messages,
                'model': model,
                'stream': False,
                **kwargs
            },
            'headers': self._headers,
            'meta': None
        }
        return request_params

    async def chat_completions(self, messages: list, model: str, return_raw=False, **kwargs) -> Union[str, "RequestResult"]:
        result, _ =  await self._client.process_requests(
            request_params=[self.wrap_to_request_params(messages, model, **kwargs)],
            url=f"{self._base_url}/chat/completions",
            method="POST",
            show_progress=False
        )
        if return_raw:
            return result[0]
        else:
            return result[0].data['choices'][0]['message']['content']

    def chat_completions_sync(self, messages: list, model: str, return_raw=False, **kwargs):
        return asyncio.run(self.chat_completions(messages, model, return_raw, **kwargs))


    async def chat_completions_batch(self, messages_list: list[list], model: str, return_raw=False, show_progress=True, **kwargs):
        results, _ =  await self._client.process_requests(
            request_params=[self.wrap_to_request_params(messages, model, **kwargs)
                            for messages in messages_list],
            url=f"{self._base_url}/chat/completions",
            method="POST",
            show_progress=show_progress
        )
        if return_raw:
            return results
        else:
            return [result.data['choices'][0]['message']['content'] for result in results]





