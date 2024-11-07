# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from ..core.request_options import RequestOptions
from ..types.eval_service_handlers_get_collection_response import EvalServiceHandlersGetCollectionResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.eval_service_handlers_create_collection_response import EvalServiceHandlersCreateCollectionResponse
from ..types.eval_service_handlers_update_collection_response import EvalServiceHandlersUpdateCollectionResponse
from ..types.eval_service_handlers_delete_collection_response import EvalServiceHandlersDeleteCollectionResponse
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class CollectionsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, collection_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> EvalServiceHandlersGetCollectionResponse:
        """
        Parameters
        ----------
        collection_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersGetCollectionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.collections.get(
            collection_id="collection_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersGetCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersGetCollectionResponse,  # type: ignore
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

    def create(
        self,
        *,
        collection_display_name: typing.Optional[str] = OMIT,
        collection_img_url: typing.Optional[str] = OMIT,
        collection_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EvalServiceHandlersCreateCollectionResponse:
        """
        Parameters
        ----------
        collection_display_name : typing.Optional[str]

        collection_img_url : typing.Optional[str]

        collection_description : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersCreateCollectionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.collections.create()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v2/collections",
            method="POST",
            json={
                "collection_display_name": collection_display_name,
                "collection_img_url": collection_img_url,
                "collection_description": collection_description,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersCreateCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersCreateCollectionResponse,  # type: ignore
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
        self,
        collection_id: str,
        *,
        collection_display_name: typing.Optional[str] = OMIT,
        collection_img_url: typing.Optional[str] = OMIT,
        collection_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EvalServiceHandlersUpdateCollectionResponse:
        """
        Parameters
        ----------
        collection_id : str

        collection_display_name : typing.Optional[str]

        collection_img_url : typing.Optional[str]

        collection_description : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersUpdateCollectionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.collections.update(
            collection_id="collection_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="PUT",
            json={
                "collection_display_name": collection_display_name,
                "collection_img_url": collection_img_url,
                "collection_description": collection_description,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersUpdateCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersUpdateCollectionResponse,  # type: ignore
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
        self, collection_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> EvalServiceHandlersDeleteCollectionResponse:
        """
        Delete a collection given a collection_id.

        Parameters
        ----------
        collection_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersDeleteCollectionResponse
            Successful Response

        Examples
        --------
        from scoutos import Scout

        client = Scout(
            api_key="YOUR_API_KEY",
        )
        client.collections.delete(
            collection_id="collection_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersDeleteCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersDeleteCollectionResponse,  # type: ignore
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


class AsyncCollectionsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(
        self, collection_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> EvalServiceHandlersGetCollectionResponse:
        """
        Parameters
        ----------
        collection_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersGetCollectionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.collections.get(
                collection_id="collection_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersGetCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersGetCollectionResponse,  # type: ignore
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

    async def create(
        self,
        *,
        collection_display_name: typing.Optional[str] = OMIT,
        collection_img_url: typing.Optional[str] = OMIT,
        collection_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EvalServiceHandlersCreateCollectionResponse:
        """
        Parameters
        ----------
        collection_display_name : typing.Optional[str]

        collection_img_url : typing.Optional[str]

        collection_description : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersCreateCollectionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.collections.create()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v2/collections",
            method="POST",
            json={
                "collection_display_name": collection_display_name,
                "collection_img_url": collection_img_url,
                "collection_description": collection_description,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersCreateCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersCreateCollectionResponse,  # type: ignore
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
        self,
        collection_id: str,
        *,
        collection_display_name: typing.Optional[str] = OMIT,
        collection_img_url: typing.Optional[str] = OMIT,
        collection_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EvalServiceHandlersUpdateCollectionResponse:
        """
        Parameters
        ----------
        collection_id : str

        collection_display_name : typing.Optional[str]

        collection_img_url : typing.Optional[str]

        collection_description : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersUpdateCollectionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.collections.update(
                collection_id="collection_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="PUT",
            json={
                "collection_display_name": collection_display_name,
                "collection_img_url": collection_img_url,
                "collection_description": collection_description,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersUpdateCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersUpdateCollectionResponse,  # type: ignore
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
        self, collection_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> EvalServiceHandlersDeleteCollectionResponse:
        """
        Delete a collection given a collection_id.

        Parameters
        ----------
        collection_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EvalServiceHandlersDeleteCollectionResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scoutos import AsyncScout

        client = AsyncScout(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.collections.delete(
                collection_id="collection_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/collections/{jsonable_encoder(collection_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    EvalServiceHandlersDeleteCollectionResponse,
                    construct_type(
                        type_=EvalServiceHandlersDeleteCollectionResponse,  # type: ignore
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
