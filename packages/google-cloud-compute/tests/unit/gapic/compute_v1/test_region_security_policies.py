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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    path_template,
)
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import extended_operation  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.compute_v1.services.region_security_policies import (
    RegionSecurityPoliciesClient,
    pagers,
    transports,
)
from google.cloud.compute_v1.types import compute


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


# Anonymous Credentials with universe domain property. If no universe domain is provided, then
# the default universe domain is "googleapis.com".
class _AnonymousCredentialsWithUniverseDomain(ga_credentials.AnonymousCredentials):
    def __init__(self, universe_domain="googleapis.com"):
        super(_AnonymousCredentialsWithUniverseDomain, self).__init__()
        self._universe_domain = universe_domain

    @property
    def universe_domain(self):
        return self._universe_domain


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert RegionSecurityPoliciesClient._get_default_mtls_endpoint(None) is None
    assert (
        RegionSecurityPoliciesClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert RegionSecurityPoliciesClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            RegionSecurityPoliciesClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            RegionSecurityPoliciesClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert RegionSecurityPoliciesClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert RegionSecurityPoliciesClient._get_client_cert_source(None, False) is None
    assert (
        RegionSecurityPoliciesClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        RegionSecurityPoliciesClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                RegionSecurityPoliciesClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                RegionSecurityPoliciesClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    RegionSecurityPoliciesClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RegionSecurityPoliciesClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = RegionSecurityPoliciesClient._DEFAULT_UNIVERSE
    default_endpoint = RegionSecurityPoliciesClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = RegionSecurityPoliciesClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == RegionSecurityPoliciesClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == RegionSecurityPoliciesClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == RegionSecurityPoliciesClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        RegionSecurityPoliciesClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        RegionSecurityPoliciesClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        RegionSecurityPoliciesClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        RegionSecurityPoliciesClient._get_universe_domain(None, None)
        == RegionSecurityPoliciesClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        RegionSecurityPoliciesClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
        ),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=_AnonymousCredentialsWithUniverseDomain())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # Test the case when there is a universe mismatch from the credentials.
    client = client_class(
        transport=transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain(
                universe_domain="foo.com"
            )
        )
    )
    with pytest.raises(ValueError) as excinfo:
        client._validate_universe_domain()
    assert (
        str(excinfo.value)
        == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
    )

    # Test the case when there is a universe mismatch from the client.
    #
    # TODO: Make this test unconditional once the minimum supported version of
    # google-api-core becomes 2.15.0 or higher.
    api_core_major, api_core_minor, _ = [
        int(part) for part in api_core_version.__version__.split(".")
    ]
    if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
        client = client_class(
            client_options={"universe_domain": "bar.com"},
            transport=transport_class(
                credentials=_AnonymousCredentialsWithUniverseDomain(),
            ),
        )
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RegionSecurityPoliciesClient, "rest"),
    ],
)
def test_region_security_policies_client_from_service_account_info(
    client_class, transport_name
):
    creds = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RegionSecurityPoliciesRestTransport, "rest"),
    ],
)
def test_region_security_policies_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RegionSecurityPoliciesClient, "rest"),
    ],
)
def test_region_security_policies_client_from_service_account_file(
    client_class, transport_name
):
    creds = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "compute.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://compute.googleapis.com"
        )


def test_region_security_policies_client_get_transport_class():
    transport = RegionSecurityPoliciesClient.get_transport_class()
    available_transports = [
        transports.RegionSecurityPoliciesRestTransport,
    ]
    assert transport in available_transports

    transport = RegionSecurityPoliciesClient.get_transport_class("rest")
    assert transport == transports.RegionSecurityPoliciesRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    RegionSecurityPoliciesClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RegionSecurityPoliciesClient),
)
def test_region_security_policies_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(RegionSecurityPoliciesClient, "get_transport_class") as gtc:
        transport = transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(RegionSecurityPoliciesClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
            "true",
        ),
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    RegionSecurityPoliciesClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RegionSecurityPoliciesClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_region_security_policies_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [RegionSecurityPoliciesClient])
@mock.patch.object(
    RegionSecurityPoliciesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegionSecurityPoliciesClient),
)
def test_region_security_policies_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [RegionSecurityPoliciesClient])
@mock.patch.object(
    RegionSecurityPoliciesClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(RegionSecurityPoliciesClient),
)
def test_region_security_policies_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = RegionSecurityPoliciesClient._DEFAULT_UNIVERSE
    default_endpoint = RegionSecurityPoliciesClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = RegionSecurityPoliciesClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=_AnonymousCredentialsWithUniverseDomain(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=_AnonymousCredentialsWithUniverseDomain())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=_AnonymousCredentialsWithUniverseDomain())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
    else:
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
        ),
    ],
)
def test_region_security_policies_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            RegionSecurityPoliciesClient,
            transports.RegionSecurityPoliciesRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_region_security_policies_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AddRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_add_rule_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_rule_resource"] = {
        "action": "action_value",
        "description": "description_value",
        "header_action": {
            "request_headers_to_adds": [
                {
                    "header_name": "header_name_value",
                    "header_value": "header_value_value",
                }
            ]
        },
        "kind": "kind_value",
        "match": {
            "config": {
                "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"]
            },
            "expr": {
                "description": "description_value",
                "expression": "expression_value",
                "location": "location_value",
                "title": "title_value",
            },
            "versioned_expr": "versioned_expr_value",
        },
        "network_match": {
            "dest_ip_ranges": ["dest_ip_ranges_value1", "dest_ip_ranges_value2"],
            "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
            "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
            "src_asns": [861, 862],
            "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
            "src_ports": ["src_ports_value1", "src_ports_value2"],
            "src_region_codes": ["src_region_codes_value1", "src_region_codes_value2"],
            "user_defined_fields": [
                {"name": "name_value", "values": ["values_value1", "values_value2"]}
            ],
        },
        "preconfigured_waf_config": {
            "exclusions": [
                {
                    "request_cookies_to_exclude": [
                        {"op": "op_value", "val": "val_value"}
                    ],
                    "request_headers_to_exclude": {},
                    "request_query_params_to_exclude": {},
                    "request_uris_to_exclude": {},
                    "target_rule_ids": [
                        "target_rule_ids_value1",
                        "target_rule_ids_value2",
                    ],
                    "target_rule_set": "target_rule_set_value",
                }
            ]
        },
        "preview": True,
        "priority": 898,
        "rate_limit_options": {
            "ban_duration_sec": 1680,
            "ban_threshold": {"count": 553, "interval_sec": 1279},
            "conform_action": "conform_action_value",
            "enforce_on_key": "enforce_on_key_value",
            "enforce_on_key_configs": [
                {
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "enforce_on_key_type": "enforce_on_key_type_value",
                }
            ],
            "enforce_on_key_name": "enforce_on_key_name_value",
            "exceed_action": "exceed_action_value",
            "exceed_redirect_options": {
                "target": "target_value",
                "type_": "type__value",
            },
            "rate_limit_threshold": {},
        },
        "redirect_options": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.AddRuleRegionSecurityPolicyRequest.meta.fields[
        "security_policy_rule_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_rule_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["security_policy_rule_resource"][field])
                ):
                    del request_init["security_policy_rule_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["security_policy_rule_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_rule_rest_required_fields(
    request_type=compute.AddRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.add_rule(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_add_rule_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.add_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("validateOnly",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyRuleResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_add_rule_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_add_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_add_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.AddRuleRegionSecurityPolicyRequest.pb(
            compute.AddRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.AddRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.add_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_add_rule_rest_bad_request(
    transport: str = "rest", request_type=compute.AddRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_rule(request)


def test_add_rule_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.add_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/addRule"
            % client.transport._host,
            args[1],
        )


def test_add_rule_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_rule(
            compute.AddRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )


def test_add_rule_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.AddRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_add_rule_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_rule_resource"] = {
        "action": "action_value",
        "description": "description_value",
        "header_action": {
            "request_headers_to_adds": [
                {
                    "header_name": "header_name_value",
                    "header_value": "header_value_value",
                }
            ]
        },
        "kind": "kind_value",
        "match": {
            "config": {
                "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"]
            },
            "expr": {
                "description": "description_value",
                "expression": "expression_value",
                "location": "location_value",
                "title": "title_value",
            },
            "versioned_expr": "versioned_expr_value",
        },
        "network_match": {
            "dest_ip_ranges": ["dest_ip_ranges_value1", "dest_ip_ranges_value2"],
            "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
            "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
            "src_asns": [861, 862],
            "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
            "src_ports": ["src_ports_value1", "src_ports_value2"],
            "src_region_codes": ["src_region_codes_value1", "src_region_codes_value2"],
            "user_defined_fields": [
                {"name": "name_value", "values": ["values_value1", "values_value2"]}
            ],
        },
        "preconfigured_waf_config": {
            "exclusions": [
                {
                    "request_cookies_to_exclude": [
                        {"op": "op_value", "val": "val_value"}
                    ],
                    "request_headers_to_exclude": {},
                    "request_query_params_to_exclude": {},
                    "request_uris_to_exclude": {},
                    "target_rule_ids": [
                        "target_rule_ids_value1",
                        "target_rule_ids_value2",
                    ],
                    "target_rule_set": "target_rule_set_value",
                }
            ]
        },
        "preview": True,
        "priority": 898,
        "rate_limit_options": {
            "ban_duration_sec": 1680,
            "ban_threshold": {"count": 553, "interval_sec": 1279},
            "conform_action": "conform_action_value",
            "enforce_on_key": "enforce_on_key_value",
            "enforce_on_key_configs": [
                {
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "enforce_on_key_type": "enforce_on_key_type_value",
                }
            ],
            "enforce_on_key_name": "enforce_on_key_name_value",
            "exceed_action": "exceed_action_value",
            "exceed_redirect_options": {
                "target": "target_value",
                "type_": "type__value",
            },
            "rate_limit_threshold": {},
        },
        "redirect_options": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.AddRuleRegionSecurityPolicyRequest.meta.fields[
        "security_policy_rule_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_rule_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["security_policy_rule_resource"][field])
                ):
                    del request_init["security_policy_rule_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["security_policy_rule_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_add_rule_unary_rest_required_fields(
    request_type=compute.AddRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.add_rule_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_add_rule_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.add_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("validateOnly",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyRuleResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_add_rule_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_add_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_add_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.AddRuleRegionSecurityPolicyRequest.pb(
            compute.AddRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.AddRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.add_rule_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_add_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.AddRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_rule_unary(request)


def test_add_rule_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.add_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/addRule"
            % client.transport._host,
            args[1],
        )


def test_add_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_rule_unary(
            compute.AddRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )


def test_add_rule_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_delete_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_rest_required_fields(
    request_type=compute.DeleteRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_delete"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_delete"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.DeleteRegionSecurityPolicyRequest.pb(
            compute.DeleteRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.delete(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete(request)


def test_delete_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}"
            % client.transport._host,
            args[1],
        )


def test_delete_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_delete_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.DeleteRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_delete_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_delete_unary_rest_required_fields(
    request_type=compute.DeleteRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_delete"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_delete"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.DeleteRegionSecurityPolicyRequest.pb(
            compute.DeleteRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.DeleteRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.delete_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_unary(request)


def test_delete_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_delete_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.GetRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_get_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicy(
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            fingerprint="fingerprint_value",
            id=205,
            kind="kind_value",
            label_fingerprint="label_fingerprint_value",
            name="name_value",
            region="region_value",
            self_link="self_link_value",
            type_="type__value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.SecurityPolicy)
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.label_fingerprint == "label_fingerprint_value"
    assert response.name == "name_value"
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.type_ == "type__value"


def test_get_rest_required_fields(request_type=compute.GetRegionSecurityPolicyRequest):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.SecurityPolicy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.SecurityPolicy.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.get._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_get"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_get"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.GetRegionSecurityPolicyRequest.pb(
            compute.GetRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.SecurityPolicy.to_json(
            compute.SecurityPolicy()
        )

        request = compute.GetRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.SecurityPolicy()

        client.get(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get(request)


def test_get_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicy()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_get_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.GetRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_get_rule_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicyRule(
            action="action_value",
            description="description_value",
            kind="kind_value",
            preview=True,
            priority=898,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicyRule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.SecurityPolicyRule)
    assert response.action == "action_value"
    assert response.description == "description_value"
    assert response.kind == "kind_value"
    assert response.preview is True
    assert response.priority == 898


def test_get_rule_rest_required_fields(
    request_type=compute.GetRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("priority",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.SecurityPolicyRule()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.SecurityPolicyRule.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_rule(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rule_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.get_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("priority",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rule_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_get_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_get_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.GetRuleRegionSecurityPolicyRequest.pb(
            compute.GetRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.SecurityPolicyRule.to_json(
            compute.SecurityPolicyRule()
        )

        request = compute.GetRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.SecurityPolicyRule()

        client.get_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_rule_rest_bad_request(
    transport: str = "rest", request_type=compute.GetRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_rule(request)


def test_get_rule_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicyRule()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicyRule.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/getRule"
            % client.transport._host,
            args[1],
        )


def test_get_rule_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule(
            compute.GetRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_get_rule_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InsertRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_insert_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request_init["security_policy_resource"] = {
        "adaptive_protection_config": {
            "layer7_ddos_defense_config": {
                "enable": True,
                "rule_visibility": "rule_visibility_value",
                "threshold_configs": [
                    {
                        "auto_deploy_confidence_threshold": 0.339,
                        "auto_deploy_expiration_sec": 2785,
                        "auto_deploy_impacted_baseline_threshold": 0.4121,
                        "auto_deploy_load_threshold": 0.2768,
                        "name": "name_value",
                    }
                ],
            }
        },
        "advanced_options_config": {
            "json_custom_config": {
                "content_types": ["content_types_value1", "content_types_value2"]
            },
            "json_parsing": "json_parsing_value",
            "log_level": "log_level_value",
            "user_ip_request_headers": [
                "user_ip_request_headers_value1",
                "user_ip_request_headers_value2",
            ],
        },
        "creation_timestamp": "creation_timestamp_value",
        "ddos_protection_config": {"ddos_protection": "ddos_protection_value"},
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "id": 205,
        "kind": "kind_value",
        "label_fingerprint": "label_fingerprint_value",
        "labels": {},
        "name": "name_value",
        "recaptcha_options_config": {"redirect_site_key": "redirect_site_key_value"},
        "region": "region_value",
        "rules": [
            {
                "action": "action_value",
                "description": "description_value",
                "header_action": {
                    "request_headers_to_adds": [
                        {
                            "header_name": "header_name_value",
                            "header_value": "header_value_value",
                        }
                    ]
                },
                "kind": "kind_value",
                "match": {
                    "config": {
                        "src_ip_ranges": [
                            "src_ip_ranges_value1",
                            "src_ip_ranges_value2",
                        ]
                    },
                    "expr": {
                        "description": "description_value",
                        "expression": "expression_value",
                        "location": "location_value",
                        "title": "title_value",
                    },
                    "versioned_expr": "versioned_expr_value",
                },
                "network_match": {
                    "dest_ip_ranges": [
                        "dest_ip_ranges_value1",
                        "dest_ip_ranges_value2",
                    ],
                    "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
                    "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
                    "src_asns": [861, 862],
                    "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
                    "src_ports": ["src_ports_value1", "src_ports_value2"],
                    "src_region_codes": [
                        "src_region_codes_value1",
                        "src_region_codes_value2",
                    ],
                    "user_defined_fields": [
                        {
                            "name": "name_value",
                            "values": ["values_value1", "values_value2"],
                        }
                    ],
                },
                "preconfigured_waf_config": {
                    "exclusions": [
                        {
                            "request_cookies_to_exclude": [
                                {"op": "op_value", "val": "val_value"}
                            ],
                            "request_headers_to_exclude": {},
                            "request_query_params_to_exclude": {},
                            "request_uris_to_exclude": {},
                            "target_rule_ids": [
                                "target_rule_ids_value1",
                                "target_rule_ids_value2",
                            ],
                            "target_rule_set": "target_rule_set_value",
                        }
                    ]
                },
                "preview": True,
                "priority": 898,
                "rate_limit_options": {
                    "ban_duration_sec": 1680,
                    "ban_threshold": {"count": 553, "interval_sec": 1279},
                    "conform_action": "conform_action_value",
                    "enforce_on_key": "enforce_on_key_value",
                    "enforce_on_key_configs": [
                        {
                            "enforce_on_key_name": "enforce_on_key_name_value",
                            "enforce_on_key_type": "enforce_on_key_type_value",
                        }
                    ],
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "exceed_action": "exceed_action_value",
                    "exceed_redirect_options": {
                        "target": "target_value",
                        "type_": "type__value",
                    },
                    "rate_limit_threshold": {},
                },
                "redirect_options": {},
            }
        ],
        "self_link": "self_link_value",
        "type_": "type__value",
        "user_defined_fields": [
            {
                "base": "base_value",
                "mask": "mask_value",
                "name": "name_value",
                "offset": 647,
                "size": 443,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.InsertRegionSecurityPolicyRequest.meta.fields[
        "security_policy_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["security_policy_resource"][field])):
                    del request_init["security_policy_resource"][field][i][subfield]
            else:
                del request_init["security_policy_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_insert_rest_required_fields(
    request_type=compute.InsertRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "validateOnly",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicyResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_insert"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_insert"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.InsertRegionSecurityPolicyRequest.pb(
            compute.InsertRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.InsertRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.insert(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_insert_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert(request)


def test_insert_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "region": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies"
            % client.transport._host,
            args[1],
        )


def test_insert_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )


def test_insert_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.InsertRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_insert_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request_init["security_policy_resource"] = {
        "adaptive_protection_config": {
            "layer7_ddos_defense_config": {
                "enable": True,
                "rule_visibility": "rule_visibility_value",
                "threshold_configs": [
                    {
                        "auto_deploy_confidence_threshold": 0.339,
                        "auto_deploy_expiration_sec": 2785,
                        "auto_deploy_impacted_baseline_threshold": 0.4121,
                        "auto_deploy_load_threshold": 0.2768,
                        "name": "name_value",
                    }
                ],
            }
        },
        "advanced_options_config": {
            "json_custom_config": {
                "content_types": ["content_types_value1", "content_types_value2"]
            },
            "json_parsing": "json_parsing_value",
            "log_level": "log_level_value",
            "user_ip_request_headers": [
                "user_ip_request_headers_value1",
                "user_ip_request_headers_value2",
            ],
        },
        "creation_timestamp": "creation_timestamp_value",
        "ddos_protection_config": {"ddos_protection": "ddos_protection_value"},
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "id": 205,
        "kind": "kind_value",
        "label_fingerprint": "label_fingerprint_value",
        "labels": {},
        "name": "name_value",
        "recaptcha_options_config": {"redirect_site_key": "redirect_site_key_value"},
        "region": "region_value",
        "rules": [
            {
                "action": "action_value",
                "description": "description_value",
                "header_action": {
                    "request_headers_to_adds": [
                        {
                            "header_name": "header_name_value",
                            "header_value": "header_value_value",
                        }
                    ]
                },
                "kind": "kind_value",
                "match": {
                    "config": {
                        "src_ip_ranges": [
                            "src_ip_ranges_value1",
                            "src_ip_ranges_value2",
                        ]
                    },
                    "expr": {
                        "description": "description_value",
                        "expression": "expression_value",
                        "location": "location_value",
                        "title": "title_value",
                    },
                    "versioned_expr": "versioned_expr_value",
                },
                "network_match": {
                    "dest_ip_ranges": [
                        "dest_ip_ranges_value1",
                        "dest_ip_ranges_value2",
                    ],
                    "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
                    "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
                    "src_asns": [861, 862],
                    "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
                    "src_ports": ["src_ports_value1", "src_ports_value2"],
                    "src_region_codes": [
                        "src_region_codes_value1",
                        "src_region_codes_value2",
                    ],
                    "user_defined_fields": [
                        {
                            "name": "name_value",
                            "values": ["values_value1", "values_value2"],
                        }
                    ],
                },
                "preconfigured_waf_config": {
                    "exclusions": [
                        {
                            "request_cookies_to_exclude": [
                                {"op": "op_value", "val": "val_value"}
                            ],
                            "request_headers_to_exclude": {},
                            "request_query_params_to_exclude": {},
                            "request_uris_to_exclude": {},
                            "target_rule_ids": [
                                "target_rule_ids_value1",
                                "target_rule_ids_value2",
                            ],
                            "target_rule_set": "target_rule_set_value",
                        }
                    ]
                },
                "preview": True,
                "priority": 898,
                "rate_limit_options": {
                    "ban_duration_sec": 1680,
                    "ban_threshold": {"count": 553, "interval_sec": 1279},
                    "conform_action": "conform_action_value",
                    "enforce_on_key": "enforce_on_key_value",
                    "enforce_on_key_configs": [
                        {
                            "enforce_on_key_name": "enforce_on_key_name_value",
                            "enforce_on_key_type": "enforce_on_key_type_value",
                        }
                    ],
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "exceed_action": "exceed_action_value",
                    "exceed_redirect_options": {
                        "target": "target_value",
                        "type_": "type__value",
                    },
                    "rate_limit_threshold": {},
                },
                "redirect_options": {},
            }
        ],
        "self_link": "self_link_value",
        "type_": "type__value",
        "user_defined_fields": [
            {
                "base": "base_value",
                "mask": "mask_value",
                "name": "name_value",
                "offset": 647,
                "size": 443,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.InsertRegionSecurityPolicyRequest.meta.fields[
        "security_policy_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["security_policy_resource"][field])):
                    del request_init["security_policy_resource"][field][i][subfield]
            else:
                del request_init["security_policy_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_insert_unary_rest_required_fields(
    request_type=compute.InsertRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "validateOnly",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicyResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_insert_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_insert"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_insert"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.InsertRegionSecurityPolicyRequest.pb(
            compute.InsertRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.InsertRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.insert_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_insert_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert_unary(request)


def test_insert_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "region": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )


def test_insert_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.ListRegionSecurityPoliciesRequest,
        dict,
    ],
)
def test_list_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicyList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicyList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"


def test_list_rest_required_fields(
    request_type=compute.ListRegionSecurityPoliciesRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_results",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.SecurityPolicyList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.SecurityPolicyList.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxResults",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(
            (
                "project",
                "region",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_list"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_list"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.ListRegionSecurityPoliciesRequest.pb(
            compute.ListRegionSecurityPoliciesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.SecurityPolicyList.to_json(
            compute.SecurityPolicyList()
        )

        request = compute.ListRegionSecurityPoliciesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.SecurityPolicyList()

        client.list(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListRegionSecurityPoliciesRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list(request)


def test_list_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SecurityPolicyList()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "region": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.SecurityPolicyList.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListRegionSecurityPoliciesRequest(),
            project="project_value",
            region="region_value",
        )


def test_list_rest_pager(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.SecurityPolicyList(
                items=[
                    compute.SecurityPolicy(),
                    compute.SecurityPolicy(),
                    compute.SecurityPolicy(),
                ],
                next_page_token="abc",
            ),
            compute.SecurityPolicyList(
                items=[],
                next_page_token="def",
            ),
            compute.SecurityPolicyList(
                items=[
                    compute.SecurityPolicy(),
                ],
                next_page_token="ghi",
            ),
            compute.SecurityPolicyList(
                items=[
                    compute.SecurityPolicy(),
                    compute.SecurityPolicy(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.SecurityPolicyList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1", "region": "sample2"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.SecurityPolicy) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_patch_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_resource"] = {
        "adaptive_protection_config": {
            "layer7_ddos_defense_config": {
                "enable": True,
                "rule_visibility": "rule_visibility_value",
                "threshold_configs": [
                    {
                        "auto_deploy_confidence_threshold": 0.339,
                        "auto_deploy_expiration_sec": 2785,
                        "auto_deploy_impacted_baseline_threshold": 0.4121,
                        "auto_deploy_load_threshold": 0.2768,
                        "name": "name_value",
                    }
                ],
            }
        },
        "advanced_options_config": {
            "json_custom_config": {
                "content_types": ["content_types_value1", "content_types_value2"]
            },
            "json_parsing": "json_parsing_value",
            "log_level": "log_level_value",
            "user_ip_request_headers": [
                "user_ip_request_headers_value1",
                "user_ip_request_headers_value2",
            ],
        },
        "creation_timestamp": "creation_timestamp_value",
        "ddos_protection_config": {"ddos_protection": "ddos_protection_value"},
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "id": 205,
        "kind": "kind_value",
        "label_fingerprint": "label_fingerprint_value",
        "labels": {},
        "name": "name_value",
        "recaptcha_options_config": {"redirect_site_key": "redirect_site_key_value"},
        "region": "region_value",
        "rules": [
            {
                "action": "action_value",
                "description": "description_value",
                "header_action": {
                    "request_headers_to_adds": [
                        {
                            "header_name": "header_name_value",
                            "header_value": "header_value_value",
                        }
                    ]
                },
                "kind": "kind_value",
                "match": {
                    "config": {
                        "src_ip_ranges": [
                            "src_ip_ranges_value1",
                            "src_ip_ranges_value2",
                        ]
                    },
                    "expr": {
                        "description": "description_value",
                        "expression": "expression_value",
                        "location": "location_value",
                        "title": "title_value",
                    },
                    "versioned_expr": "versioned_expr_value",
                },
                "network_match": {
                    "dest_ip_ranges": [
                        "dest_ip_ranges_value1",
                        "dest_ip_ranges_value2",
                    ],
                    "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
                    "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
                    "src_asns": [861, 862],
                    "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
                    "src_ports": ["src_ports_value1", "src_ports_value2"],
                    "src_region_codes": [
                        "src_region_codes_value1",
                        "src_region_codes_value2",
                    ],
                    "user_defined_fields": [
                        {
                            "name": "name_value",
                            "values": ["values_value1", "values_value2"],
                        }
                    ],
                },
                "preconfigured_waf_config": {
                    "exclusions": [
                        {
                            "request_cookies_to_exclude": [
                                {"op": "op_value", "val": "val_value"}
                            ],
                            "request_headers_to_exclude": {},
                            "request_query_params_to_exclude": {},
                            "request_uris_to_exclude": {},
                            "target_rule_ids": [
                                "target_rule_ids_value1",
                                "target_rule_ids_value2",
                            ],
                            "target_rule_set": "target_rule_set_value",
                        }
                    ]
                },
                "preview": True,
                "priority": 898,
                "rate_limit_options": {
                    "ban_duration_sec": 1680,
                    "ban_threshold": {"count": 553, "interval_sec": 1279},
                    "conform_action": "conform_action_value",
                    "enforce_on_key": "enforce_on_key_value",
                    "enforce_on_key_configs": [
                        {
                            "enforce_on_key_name": "enforce_on_key_name_value",
                            "enforce_on_key_type": "enforce_on_key_type_value",
                        }
                    ],
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "exceed_action": "exceed_action_value",
                    "exceed_redirect_options": {
                        "target": "target_value",
                        "type_": "type__value",
                    },
                    "rate_limit_threshold": {},
                },
                "redirect_options": {},
            }
        ],
        "self_link": "self_link_value",
        "type_": "type__value",
        "user_defined_fields": [
            {
                "base": "base_value",
                "mask": "mask_value",
                "name": "name_value",
                "offset": 647,
                "size": 443,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.PatchRegionSecurityPolicyRequest.meta.fields[
        "security_policy_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["security_policy_resource"][field])):
                    del request_init["security_policy_resource"][field][i][subfield]
            else:
                del request_init["security_policy_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_rest_required_fields(
    request_type=compute.PatchRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "updateMask",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_patch"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_patch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.PatchRegionSecurityPolicyRequest.pb(
            compute.PatchRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.patch(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch(request)


def test_patch_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}"
            % client.transport._host,
            args[1],
        )


def test_patch_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch(
            compute.PatchRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )


def test_patch_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_patch_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_resource"] = {
        "adaptive_protection_config": {
            "layer7_ddos_defense_config": {
                "enable": True,
                "rule_visibility": "rule_visibility_value",
                "threshold_configs": [
                    {
                        "auto_deploy_confidence_threshold": 0.339,
                        "auto_deploy_expiration_sec": 2785,
                        "auto_deploy_impacted_baseline_threshold": 0.4121,
                        "auto_deploy_load_threshold": 0.2768,
                        "name": "name_value",
                    }
                ],
            }
        },
        "advanced_options_config": {
            "json_custom_config": {
                "content_types": ["content_types_value1", "content_types_value2"]
            },
            "json_parsing": "json_parsing_value",
            "log_level": "log_level_value",
            "user_ip_request_headers": [
                "user_ip_request_headers_value1",
                "user_ip_request_headers_value2",
            ],
        },
        "creation_timestamp": "creation_timestamp_value",
        "ddos_protection_config": {"ddos_protection": "ddos_protection_value"},
        "description": "description_value",
        "fingerprint": "fingerprint_value",
        "id": 205,
        "kind": "kind_value",
        "label_fingerprint": "label_fingerprint_value",
        "labels": {},
        "name": "name_value",
        "recaptcha_options_config": {"redirect_site_key": "redirect_site_key_value"},
        "region": "region_value",
        "rules": [
            {
                "action": "action_value",
                "description": "description_value",
                "header_action": {
                    "request_headers_to_adds": [
                        {
                            "header_name": "header_name_value",
                            "header_value": "header_value_value",
                        }
                    ]
                },
                "kind": "kind_value",
                "match": {
                    "config": {
                        "src_ip_ranges": [
                            "src_ip_ranges_value1",
                            "src_ip_ranges_value2",
                        ]
                    },
                    "expr": {
                        "description": "description_value",
                        "expression": "expression_value",
                        "location": "location_value",
                        "title": "title_value",
                    },
                    "versioned_expr": "versioned_expr_value",
                },
                "network_match": {
                    "dest_ip_ranges": [
                        "dest_ip_ranges_value1",
                        "dest_ip_ranges_value2",
                    ],
                    "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
                    "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
                    "src_asns": [861, 862],
                    "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
                    "src_ports": ["src_ports_value1", "src_ports_value2"],
                    "src_region_codes": [
                        "src_region_codes_value1",
                        "src_region_codes_value2",
                    ],
                    "user_defined_fields": [
                        {
                            "name": "name_value",
                            "values": ["values_value1", "values_value2"],
                        }
                    ],
                },
                "preconfigured_waf_config": {
                    "exclusions": [
                        {
                            "request_cookies_to_exclude": [
                                {"op": "op_value", "val": "val_value"}
                            ],
                            "request_headers_to_exclude": {},
                            "request_query_params_to_exclude": {},
                            "request_uris_to_exclude": {},
                            "target_rule_ids": [
                                "target_rule_ids_value1",
                                "target_rule_ids_value2",
                            ],
                            "target_rule_set": "target_rule_set_value",
                        }
                    ]
                },
                "preview": True,
                "priority": 898,
                "rate_limit_options": {
                    "ban_duration_sec": 1680,
                    "ban_threshold": {"count": 553, "interval_sec": 1279},
                    "conform_action": "conform_action_value",
                    "enforce_on_key": "enforce_on_key_value",
                    "enforce_on_key_configs": [
                        {
                            "enforce_on_key_name": "enforce_on_key_name_value",
                            "enforce_on_key_type": "enforce_on_key_type_value",
                        }
                    ],
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "exceed_action": "exceed_action_value",
                    "exceed_redirect_options": {
                        "target": "target_value",
                        "type_": "type__value",
                    },
                    "rate_limit_threshold": {},
                },
                "redirect_options": {},
            }
        ],
        "self_link": "self_link_value",
        "type_": "type__value",
        "user_defined_fields": [
            {
                "base": "base_value",
                "mask": "mask_value",
                "name": "name_value",
                "offset": 647,
                "size": 443,
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.PatchRegionSecurityPolicyRequest.meta.fields[
        "security_policy_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["security_policy_resource"][field])):
                    del request_init["security_policy_resource"][field][i][subfield]
            else:
                del request_init["security_policy_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_patch_unary_rest_required_fields(
    request_type=compute.PatchRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "updateMask",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_patch"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_patch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.PatchRegionSecurityPolicyRequest.pb(
            compute.PatchRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.patch_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_unary(request)


def test_patch_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
            compute.PatchRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_resource=compute.SecurityPolicy(
                adaptive_protection_config=compute.SecurityPolicyAdaptiveProtectionConfig(
                    layer7_ddos_defense_config=compute.SecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
                        enable=True
                    )
                )
            ),
        )


def test_patch_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_patch_rule_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_rule_resource"] = {
        "action": "action_value",
        "description": "description_value",
        "header_action": {
            "request_headers_to_adds": [
                {
                    "header_name": "header_name_value",
                    "header_value": "header_value_value",
                }
            ]
        },
        "kind": "kind_value",
        "match": {
            "config": {
                "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"]
            },
            "expr": {
                "description": "description_value",
                "expression": "expression_value",
                "location": "location_value",
                "title": "title_value",
            },
            "versioned_expr": "versioned_expr_value",
        },
        "network_match": {
            "dest_ip_ranges": ["dest_ip_ranges_value1", "dest_ip_ranges_value2"],
            "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
            "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
            "src_asns": [861, 862],
            "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
            "src_ports": ["src_ports_value1", "src_ports_value2"],
            "src_region_codes": ["src_region_codes_value1", "src_region_codes_value2"],
            "user_defined_fields": [
                {"name": "name_value", "values": ["values_value1", "values_value2"]}
            ],
        },
        "preconfigured_waf_config": {
            "exclusions": [
                {
                    "request_cookies_to_exclude": [
                        {"op": "op_value", "val": "val_value"}
                    ],
                    "request_headers_to_exclude": {},
                    "request_query_params_to_exclude": {},
                    "request_uris_to_exclude": {},
                    "target_rule_ids": [
                        "target_rule_ids_value1",
                        "target_rule_ids_value2",
                    ],
                    "target_rule_set": "target_rule_set_value",
                }
            ]
        },
        "preview": True,
        "priority": 898,
        "rate_limit_options": {
            "ban_duration_sec": 1680,
            "ban_threshold": {"count": 553, "interval_sec": 1279},
            "conform_action": "conform_action_value",
            "enforce_on_key": "enforce_on_key_value",
            "enforce_on_key_configs": [
                {
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "enforce_on_key_type": "enforce_on_key_type_value",
                }
            ],
            "enforce_on_key_name": "enforce_on_key_name_value",
            "exceed_action": "exceed_action_value",
            "exceed_redirect_options": {
                "target": "target_value",
                "type_": "type__value",
            },
            "rate_limit_threshold": {},
        },
        "redirect_options": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.PatchRuleRegionSecurityPolicyRequest.meta.fields[
        "security_policy_rule_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_rule_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["security_policy_rule_resource"][field])
                ):
                    del request_init["security_policy_rule_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["security_policy_rule_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_rule_rest_required_fields(
    request_type=compute.PatchRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "priority",
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_rule(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_rule_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.patch_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "priority",
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyRuleResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_rule_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_patch_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_patch_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.PatchRuleRegionSecurityPolicyRequest.pb(
            compute.PatchRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.patch_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_rule_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_rule(request)


def test_patch_rule_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/patchRule"
            % client.transport._host,
            args[1],
        )


def test_patch_rule_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_rule(
            compute.PatchRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )


def test_patch_rule_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.PatchRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_patch_rule_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request_init["security_policy_rule_resource"] = {
        "action": "action_value",
        "description": "description_value",
        "header_action": {
            "request_headers_to_adds": [
                {
                    "header_name": "header_name_value",
                    "header_value": "header_value_value",
                }
            ]
        },
        "kind": "kind_value",
        "match": {
            "config": {
                "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"]
            },
            "expr": {
                "description": "description_value",
                "expression": "expression_value",
                "location": "location_value",
                "title": "title_value",
            },
            "versioned_expr": "versioned_expr_value",
        },
        "network_match": {
            "dest_ip_ranges": ["dest_ip_ranges_value1", "dest_ip_ranges_value2"],
            "dest_ports": ["dest_ports_value1", "dest_ports_value2"],
            "ip_protocols": ["ip_protocols_value1", "ip_protocols_value2"],
            "src_asns": [861, 862],
            "src_ip_ranges": ["src_ip_ranges_value1", "src_ip_ranges_value2"],
            "src_ports": ["src_ports_value1", "src_ports_value2"],
            "src_region_codes": ["src_region_codes_value1", "src_region_codes_value2"],
            "user_defined_fields": [
                {"name": "name_value", "values": ["values_value1", "values_value2"]}
            ],
        },
        "preconfigured_waf_config": {
            "exclusions": [
                {
                    "request_cookies_to_exclude": [
                        {"op": "op_value", "val": "val_value"}
                    ],
                    "request_headers_to_exclude": {},
                    "request_query_params_to_exclude": {},
                    "request_uris_to_exclude": {},
                    "target_rule_ids": [
                        "target_rule_ids_value1",
                        "target_rule_ids_value2",
                    ],
                    "target_rule_set": "target_rule_set_value",
                }
            ]
        },
        "preview": True,
        "priority": 898,
        "rate_limit_options": {
            "ban_duration_sec": 1680,
            "ban_threshold": {"count": 553, "interval_sec": 1279},
            "conform_action": "conform_action_value",
            "enforce_on_key": "enforce_on_key_value",
            "enforce_on_key_configs": [
                {
                    "enforce_on_key_name": "enforce_on_key_name_value",
                    "enforce_on_key_type": "enforce_on_key_type_value",
                }
            ],
            "enforce_on_key_name": "enforce_on_key_name_value",
            "exceed_action": "exceed_action_value",
            "exceed_redirect_options": {
                "target": "target_value",
                "type_": "type__value",
            },
            "rate_limit_threshold": {},
        },
        "redirect_options": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = compute.PatchRuleRegionSecurityPolicyRequest.meta.fields[
        "security_policy_rule_resource"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "security_policy_rule_resource"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["security_policy_rule_resource"][field])
                ):
                    del request_init["security_policy_rule_resource"][field][i][
                        subfield
                    ]
            else:
                del request_init["security_policy_rule_resource"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_patch_rule_unary_rest_required_fields(
    request_type=compute.PatchRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).patch_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "priority",
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_rule_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_rule_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.patch_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "priority",
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "project",
                "region",
                "securityPolicy",
                "securityPolicyRuleResource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_patch_rule_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_patch_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_patch_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.PatchRuleRegionSecurityPolicyRequest.pb(
            compute.PatchRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.PatchRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.patch_rule_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_patch_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_rule_unary(request)


def test_patch_rule_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.patch_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/patchRule"
            % client.transport._host,
            args[1],
        )


def test_patch_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_rule_unary(
            compute.PatchRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
            security_policy_rule_resource=compute.SecurityPolicyRule(
                action="action_value"
            ),
        )


def test_patch_rule_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.RemoveRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_remove_rule_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_rule(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, extended_operation.ExtendedOperation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_remove_rule_rest_required_fields(
    request_type=compute.RemoveRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("priority",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_rule(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_rule_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.remove_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("priority",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_rule_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_remove_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_remove_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.RemoveRuleRegionSecurityPolicyRequest.pb(
            compute.RemoveRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.RemoveRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.remove_rule(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_remove_rule_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_rule(request)


def test_remove_rule_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.remove_rule(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/removeRule"
            % client.transport._host,
            args[1],
        )


def test_remove_rule_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_rule(
            compute.RemoveRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_remove_rule_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        compute.RemoveRuleRegionSecurityPolicyRequest,
        dict,
    ],
)
def test_remove_rule_unary_rest(request_type):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_rule_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)


def test_remove_rule_unary_rest_required_fields(
    request_type=compute.RemoveRuleRegionSecurityPolicyRequest,
):
    transport_class = transports.RegionSecurityPoliciesRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["security_policy"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_rule._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["securityPolicy"] = "security_policy_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_rule._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("priority",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "securityPolicy" in jsonified_request
    assert jsonified_request["securityPolicy"] == "security_policy_value"

    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = compute.Operation.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_rule_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_rule_unary_rest_unset_required_fields():
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.remove_rule._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("priority",))
        & set(
            (
                "project",
                "region",
                "securityPolicy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_rule_unary_rest_interceptors(null_interceptor):
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.RegionSecurityPoliciesRestInterceptor(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "post_remove_rule"
    ) as post, mock.patch.object(
        transports.RegionSecurityPoliciesRestInterceptor, "pre_remove_rule"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = compute.RemoveRuleRegionSecurityPolicyRequest.pb(
            compute.RemoveRuleRegionSecurityPolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = compute.Operation.to_json(compute.Operation())

        request = compute.RemoveRuleRegionSecurityPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = compute.Operation()

        client.remove_rule_unary(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_remove_rule_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveRuleRegionSecurityPolicyRequest
):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "security_policy": "sample3",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_rule_unary(request)


def test_remove_rule_unary_rest_flattened():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "security_policy": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = compute.Operation.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.remove_rule_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/compute/v1/projects/{project}/regions/{region}/securityPolicies/{security_policy}/removeRule"
            % client.transport._host,
            args[1],
        )


def test_remove_rule_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_rule_unary(
            compute.RemoveRuleRegionSecurityPolicyRequest(),
            project="project_value",
            region="region_value",
            security_policy="security_policy_value",
        )


def test_remove_rule_unary_rest_error():
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = RegionSecurityPoliciesClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = RegionSecurityPoliciesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegionSecurityPoliciesClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegionSecurityPoliciesClient(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = RegionSecurityPoliciesClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RegionSecurityPoliciesRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    client = RegionSecurityPoliciesClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RegionSecurityPoliciesRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = RegionSecurityPoliciesClient.get_transport_class(transport_name)(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    assert transport.kind == transport_name


def test_region_security_policies_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RegionSecurityPoliciesTransport(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            credentials_file="credentials.json",
        )


def test_region_security_policies_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.region_security_policies.transports.RegionSecurityPoliciesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RegionSecurityPoliciesTransport(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "add_rule",
        "delete",
        "get",
        "get_rule",
        "insert",
        "list",
        "patch",
        "patch_rule",
        "remove_rule",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_region_security_policies_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.region_security_policies.transports.RegionSecurityPoliciesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport = transports.RegionSecurityPoliciesTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_region_security_policies_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.region_security_policies.transports.RegionSecurityPoliciesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport = transports.RegionSecurityPoliciesTransport()
        adc.assert_called_once()


def test_region_security_policies_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        RegionSecurityPoliciesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_region_security_policies_http_transport_client_cert_source_for_mtls():
    cred = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.RegionSecurityPoliciesRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_region_security_policies_host_no_port(transport_name):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_region_security_policies_host_with_port(transport_name):
    client = RegionSecurityPoliciesClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "compute.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://compute.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_region_security_policies_client_transport_session_collision(transport_name):
    creds1 = _AnonymousCredentialsWithUniverseDomain()
    creds2 = _AnonymousCredentialsWithUniverseDomain()
    client1 = RegionSecurityPoliciesClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = RegionSecurityPoliciesClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.add_rule._session
    session2 = client2.transport.add_rule._session
    assert session1 != session2
    session1 = client1.transport.delete._session
    session2 = client2.transport.delete._session
    assert session1 != session2
    session1 = client1.transport.get._session
    session2 = client2.transport.get._session
    assert session1 != session2
    session1 = client1.transport.get_rule._session
    session2 = client2.transport.get_rule._session
    assert session1 != session2
    session1 = client1.transport.insert._session
    session2 = client2.transport.insert._session
    assert session1 != session2
    session1 = client1.transport.list._session
    session2 = client2.transport.list._session
    assert session1 != session2
    session1 = client1.transport.patch._session
    session2 = client2.transport.patch._session
    assert session1 != session2
    session1 = client1.transport.patch_rule._session
    session2 = client2.transport.patch_rule._session
    assert session1 != session2
    session1 = client1.transport.remove_rule._session
    session2 = client2.transport.remove_rule._session
    assert session1 != session2


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RegionSecurityPoliciesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = RegionSecurityPoliciesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionSecurityPoliciesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = RegionSecurityPoliciesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = RegionSecurityPoliciesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionSecurityPoliciesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = RegionSecurityPoliciesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = RegionSecurityPoliciesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionSecurityPoliciesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = RegionSecurityPoliciesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = RegionSecurityPoliciesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionSecurityPoliciesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = RegionSecurityPoliciesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = RegionSecurityPoliciesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionSecurityPoliciesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RegionSecurityPoliciesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RegionSecurityPoliciesClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RegionSecurityPoliciesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RegionSecurityPoliciesClient.get_transport_class()
        transport = transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = RegionSecurityPoliciesClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = RegionSecurityPoliciesClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (RegionSecurityPoliciesClient, transports.RegionSecurityPoliciesRestTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
