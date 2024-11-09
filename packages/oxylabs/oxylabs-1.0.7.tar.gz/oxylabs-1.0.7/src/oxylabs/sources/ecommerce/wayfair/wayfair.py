from typing import Optional

from oxylabs.sources.ecommerce.response import EcommerceResponse
from oxylabs.utils.types import source
from oxylabs.utils.utils import prepare_config


class Wayfair:
    def __init__(self, ecommerce_instance) -> None:
        """
        Initializes an instance of the Wayfair class.

        Args:
            ecommerce_instance: The Ecommerce instance associated with the
            Wayfair class.
        """
        self._ecommerce_instance = ecommerce_instance

    def scrape_search(
        self,
        query: str,
        start_page: Optional[int] = None,
        pages: Optional[int] = None,
        limit: Optional[int] = None,
        user_agent_type: Optional[str] = None,
        callback_url: Optional[str] = None,
        request_timeout: Optional[int] = 165,
        **kwargs
    ) -> EcommerceResponse:
        """
        Scrapes Wayfair search results for a given query.

        Args:
            query (str): The search query.
            start_page (Optional[int]): The starting page number.
            pages (Optional[int]): The number of pages to scrape.
            limit (Optional[int]): Number of results to retrieve in each page.
            user_agent_type (Optional[str]): Device type and browser.
            callback_url (Optional[str]): URL to your callback endpoint.
            parsing_instructions (Optional[dict]): Instructions for parsing the results.
            request_timeout (int | 165, optional): The interval in seconds for
            the request to time out if no response is returned.
            Defaults to 165.

        Returns:
            EcommerceResponse: The response from the server after the job is completed.
        """

        config = prepare_config(request_timeout=request_timeout)
        payload = {
            "source": source.WAYFAIR_SEARCH,
            "query": query,
            "start_page": start_page,
            "pages": pages,
            "limit": limit,
            "user_agent_type": user_agent_type,
            "callback_url": callback_url,
            **kwargs,
        }
        response = self._ecommerce_instance._get_resp(payload, config)
        return response

    def scrape_url(
        self,
        url: str,
        user_agent_type: Optional[str] = None,
        callback_url: Optional[str] = None,
        request_timeout: Optional[int] = 165,
        **kwargs
    ) -> EcommerceResponse:
        """
        Scrapes Wayfair search results for a given URL.

        Args:
            url (str): The URL to be scraped.
            user_agent_type (Optional[str]): Device type and browser.
            callback_url (Optional[str]): URL to your callback endpoint.
            parsing_instructions (Optional[dict]): Instructions for parsing the results.
            request_timeout (int | 165, optional): The interval in seconds for
            the request to time out if no response is returned.
            Defaults to 165.

        Returns:
            EcommerceResponse: The response from the server after the job is completed.
        """

        config = prepare_config(request_timeout=request_timeout)
        payload = {
            "source": source.WAYFAIR,
            "url": url,
            "user_agent_type": user_agent_type,
            "callback_url": callback_url,
            **kwargs,
        }
        response = self._ecommerce_instance._get_resp(payload, config)
        return response


class WayfairAsync:
    def __init__(self, ecommerce_async_instance) -> None:
        """
        Initializes an instance of the WayfairAsync class.

        Args:
            ecommerce_async_instance: The EcommerceAsync instance associated
            with the WayfairAsync class.
        """
        self._ecommerce_async_instance = ecommerce_async_instance

    async def scrape_search(
        self,
        query: str,
        start_page: Optional[int] = None,
        pages: Optional[int] = None,
        limit: Optional[int] = None,
        user_agent_type: Optional[str] = None,
        callback_url: Optional[str] = None,
        request_timeout: Optional[int] = 165,
        job_completion_timeout: Optional[int] = None,
        poll_interval: Optional[int] = None,
        **kwargs
    ) -> EcommerceResponse:
        """
        Asynchronously scrapes Wayfair search results for a given query.

        Args:
            query (str): The search query.
            start_page (Optional[int]): The starting page number.
            pages (Optional[int]): The number of pages to scrape.
            limit (Optional[int]): Number of results to retrieve in each page
            user_agent_type (Optional[str]): Device type and browser.
            callback_url (Optional[str]): URL to your callback endpoint.
            parsing_instructions (Optional[dict]): Instructions for parsing the results.
            request_timeout (int | 165, optional): The interval in seconds for
            the request to time out if no response is returned.
            Defaults to 165.
            poll_interval (int | 5, optional): The interval in seconds to poll
            the server for a response. Defaults to 5
            job_completion_timeout (int | 50, optional): The interval in
            seconds for the job to time out if no response is returned.
            Defaults to 50

        Returns:
            EcommerceResponse: The response from the server after the job is completed.
        """

        config = prepare_config(
            request_timeout=request_timeout,
            poll_interval=poll_interval,
            job_completion_timeout=job_completion_timeout,
            async_integration=True,
        )
        payload = {
            "source": source.WAYFAIR_SEARCH,
            "query": query,
            "start_page": start_page,
            "pages": pages,
            "limit": limit,
            "user_agent_type": user_agent_type,
            "callback_url": callback_url,
            **kwargs,
        }
        response = await self._ecommerce_async_instance._get_resp(
            payload, config
        )
        return response

    async def scrape_url(
        self,
        url: str,
        user_agent_type: Optional[str] = None,
        callback_url: Optional[str] = None,
        request_timeout: Optional[int] = 165,
        job_completion_timeout: Optional[int] = None,
        poll_interval: Optional[int] = None,
        **kwargs
    ) -> EcommerceResponse:
        """
        Asynchronously scrapes Wayfair search results for a given URL.

        Args:
            url (str): The URL to be scraped.
            user_agent_type (Optional[str]): Device type and browser.
            callback_url (Optional[str]): URL to your callback endpoint.
            parsing_instructions (Optional[dict]): Instructions for parsing the results.
            request_timeout (int | 165, optional): The interval in seconds for
            the request to time out if no response is returned.
            Defaults to 165.
            poll_interval (int | 5, optional): The interval in seconds to poll
            the server for a response. Defaults to 5
            job_completion_timeout (int | 50, optional): The interval in
            seconds for the job to time out if no response is returned.
            Defaults to 50

        Returns:
            EcommerceResponse: The response from the server after the job is completed.
        """

        config = prepare_config(
            request_timeout=request_timeout,
            poll_interval=poll_interval,
            job_completion_timeout=job_completion_timeout,
            async_integration=True,
        )
        payload = {
            "source": source.WAYFAIR,
            "url": url,
            "user_agent_type": user_agent_type,
            "callback_url": callback_url,
            **kwargs,
        }
        response = await self._ecommerce_async_instance._get_resp(
            payload, config
        )
        return response
