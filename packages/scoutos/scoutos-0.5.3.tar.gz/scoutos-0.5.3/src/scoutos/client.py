# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import ScoutEnvironment
import os
import httpx
from .core.api_error import ApiError
from .core.client_wrapper import SyncClientWrapper
from .workflows.client import WorkflowsClient
from .environments.client import EnvironmentsClient
from .revisions.client import RevisionsClient
from .usage.client import UsageClient
from .workflow_logs.client import WorkflowLogsClient
from .copilots.client import CopilotsClient
from .collections.client import CollectionsClient
from .tables.client import TablesClient
from .documents.client import DocumentsClient
from .core.request_options import RequestOptions
from .types.response_model import ResponseModel
from .core.unchecked_base_model import construct_type
from json.decoder import JSONDecodeError
from .core.client_wrapper import AsyncClientWrapper
from .workflows.client import AsyncWorkflowsClient
from .environments.client import AsyncEnvironmentsClient
from .revisions.client import AsyncRevisionsClient
from .usage.client import AsyncUsageClient
from .workflow_logs.client import AsyncWorkflowLogsClient
from .copilots.client import AsyncCopilotsClient
from .collections.client import AsyncCollectionsClient
from .tables.client import AsyncTablesClient
from .documents.client import AsyncDocumentsClient


class Scout:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ScoutEnvironment
        The environment to use for requests from the client. from .environment import ScoutEnvironment



        Defaults to ScoutEnvironment.PROD



    api_key : typing.Optional[typing.Union[str, typing.Callable[[], str]]]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from scoutos import Scout

    client = Scout(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ScoutEnvironment = ScoutEnvironment.PROD,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("SCOUT_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(body="The client must be instantiated be either passing in api_key or setting SCOUT_API_KEY")
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.workflows = WorkflowsClient(client_wrapper=self._client_wrapper)
        self.environments = EnvironmentsClient(client_wrapper=self._client_wrapper)
        self.revisions = RevisionsClient(client_wrapper=self._client_wrapper)
        self.usage = UsageClient(client_wrapper=self._client_wrapper)
        self.workflow_logs = WorkflowLogsClient(client_wrapper=self._client_wrapper)
        self.copilots = CopilotsClient(client_wrapper=self._client_wrapper)
        self.collections = CollectionsClient(client_wrapper=self._client_wrapper)
        self.tables = TablesClient(client_wrapper=self._client_wrapper)
        self.documents = DocumentsClient(client_wrapper=self._client_wrapper)

    def list_source_archetypes_v_2_sources_get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ResponseModel:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ResponseModel
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.list_source_archetypes_v_2_sources_get()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v2/sources",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ResponseModel,
                    construct_type(
                        type_=ResponseModel,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncScout:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ScoutEnvironment
        The environment to use for requests from the client. from .environment import ScoutEnvironment



        Defaults to ScoutEnvironment.PROD



    api_key : typing.Optional[typing.Union[str, typing.Callable[[], str]]]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from scoutos import AsyncScout

    client = AsyncScout(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ScoutEnvironment = ScoutEnvironment.PROD,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("SCOUT_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(body="The client must be instantiated be either passing in api_key or setting SCOUT_API_KEY")
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.workflows = AsyncWorkflowsClient(client_wrapper=self._client_wrapper)
        self.environments = AsyncEnvironmentsClient(client_wrapper=self._client_wrapper)
        self.revisions = AsyncRevisionsClient(client_wrapper=self._client_wrapper)
        self.usage = AsyncUsageClient(client_wrapper=self._client_wrapper)
        self.workflow_logs = AsyncWorkflowLogsClient(client_wrapper=self._client_wrapper)
        self.copilots = AsyncCopilotsClient(client_wrapper=self._client_wrapper)
        self.collections = AsyncCollectionsClient(client_wrapper=self._client_wrapper)
        self.tables = AsyncTablesClient(client_wrapper=self._client_wrapper)
        self.documents = AsyncDocumentsClient(client_wrapper=self._client_wrapper)

    async def list_source_archetypes_v_2_sources_get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ResponseModel:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.list_source_archetypes_v_2_sources_get()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v2/sources",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ResponseModel,
                    construct_type(
                        type_=ResponseModel,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: ScoutEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
