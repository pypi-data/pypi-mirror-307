# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.apps_service_handlers_list_workflow_revisions_response import (
    AppsServiceHandlersListWorkflowRevisionsResponse,
)
from ..core.jsonable_encoder import jsonable_encoder
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.apps_service_handlers_promote_workflow_revision_response import (
    AppsServiceHandlersPromoteWorkflowRevisionResponse,
)
from ..types.apps_service_handlers_delete_workflow_revision_response import (
    AppsServiceHandlersDeleteWorkflowRevisionResponse,
)
from ..core.client_wrapper import AsyncClientWrapper


class RevisionsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list(
        self, workflow_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersListWorkflowRevisionsResponse:
        """
        List all app revisions in the organization

        Parameters
        ----------
        workflow_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersListWorkflowRevisionsResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.revisions.list(
            workflow_id="workflow_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersListWorkflowRevisionsResponse,
                    construct_type(
                        type_=AppsServiceHandlersListWorkflowRevisionsResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update(
        self, workflow_id: str, revision_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersPromoteWorkflowRevisionResponse:
        """
        Parameters
        ----------
        workflow_id : str

        revision_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersPromoteWorkflowRevisionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.revisions.update(
            workflow_id="workflow_id",
            revision_id="revision_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions/{jsonable_encoder(revision_id)}/promote",
            method="PUT",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersPromoteWorkflowRevisionResponse,
                    construct_type(
                        type_=AppsServiceHandlersPromoteWorkflowRevisionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, workflow_id: str, revision_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersDeleteWorkflowRevisionResponse:
        """
        Parameters
        ----------
        workflow_id : str

        revision_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersDeleteWorkflowRevisionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.revisions.delete(
            workflow_id="workflow_id",
            revision_id="revision_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions/{jsonable_encoder(revision_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersDeleteWorkflowRevisionResponse,
                    construct_type(
                        type_=AppsServiceHandlersDeleteWorkflowRevisionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncRevisionsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list(
        self, workflow_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersListWorkflowRevisionsResponse:
        """
        List all app revisions in the organization

        Parameters
        ----------
        workflow_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersListWorkflowRevisionsResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.revisions.list(
                workflow_id="workflow_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersListWorkflowRevisionsResponse,
                    construct_type(
                        type_=AppsServiceHandlersListWorkflowRevisionsResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update(
        self, workflow_id: str, revision_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersPromoteWorkflowRevisionResponse:
        """
        Parameters
        ----------
        workflow_id : str

        revision_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersPromoteWorkflowRevisionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.revisions.update(
                workflow_id="workflow_id",
                revision_id="revision_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions/{jsonable_encoder(revision_id)}/promote",
            method="PUT",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersPromoteWorkflowRevisionResponse,
                    construct_type(
                        type_=AppsServiceHandlersPromoteWorkflowRevisionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete(
        self, workflow_id: str, revision_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AppsServiceHandlersDeleteWorkflowRevisionResponse:
        """
        Parameters
        ----------
        workflow_id : str

        revision_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AppsServiceHandlersDeleteWorkflowRevisionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.revisions.delete(
                workflow_id="workflow_id",
                revision_id="revision_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/workflows/{jsonable_encoder(workflow_id)}/revisions/{jsonable_encoder(revision_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    AppsServiceHandlersDeleteWorkflowRevisionResponse,
                    construct_type(
                        type_=AppsServiceHandlersDeleteWorkflowRevisionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
