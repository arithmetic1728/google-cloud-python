# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.dataflow_v1beta3.types import messages

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import MessagesV1Beta3Transport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class MessagesV1Beta3RestInterceptor:
    """Interceptor for MessagesV1Beta3.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MessagesV1Beta3RestTransport.

    .. code-block:: python
        class MyCustomMessagesV1Beta3Interceptor(MessagesV1Beta3RestInterceptor):
            def pre_list_job_messages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_job_messages(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MessagesV1Beta3RestTransport(interceptor=MyCustomMessagesV1Beta3Interceptor())
        client = MessagesV1Beta3Client(transport=transport)


    """

    def pre_list_job_messages(
        self,
        request: messages.ListJobMessagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[messages.ListJobMessagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_job_messages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MessagesV1Beta3 server.
        """
        return request, metadata

    def post_list_job_messages(
        self, response: messages.ListJobMessagesResponse
    ) -> messages.ListJobMessagesResponse:
        """Post-rpc interceptor for list_job_messages

        Override in a subclass to manipulate the response
        after it is returned by the MessagesV1Beta3 server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MessagesV1Beta3RestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MessagesV1Beta3RestInterceptor


class MessagesV1Beta3RestTransport(MessagesV1Beta3Transport):
    """REST backend transport for MessagesV1Beta3.

    The Dataflow Messages API is used for monitoring the progress
    of Dataflow jobs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dataflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MessagesV1Beta3RestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataflow.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or MessagesV1Beta3RestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _ListJobMessages(MessagesV1Beta3RestStub):
        def __hash__(self):
            return hash("ListJobMessages")

        def __call__(
            self,
            request: messages.ListJobMessagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> messages.ListJobMessagesResponse:
            r"""Call the list job messages method over HTTP.

            Args:
                request (~.messages.ListJobMessagesRequest):
                    The request object. Request to list job messages. Up to max_results messages
                will be returned in the time range specified starting
                with the oldest messages first. If no time range is
                specified the results with start with the oldest
                message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.messages.ListJobMessagesResponse:
                    Response to a request to list job
                messages.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs/{job_id}/messages",
                },
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/jobs/{job_id}/messages",
                },
            ]
            request, metadata = self._interceptor.pre_list_job_messages(
                request, metadata
            )
            pb_request = messages.ListJobMessagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = messages.ListJobMessagesResponse()
            pb_resp = messages.ListJobMessagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_job_messages(resp)
            return resp

    @property
    def list_job_messages(
        self,
    ) -> Callable[[messages.ListJobMessagesRequest], messages.ListJobMessagesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobMessages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MessagesV1Beta3RestTransport",)
