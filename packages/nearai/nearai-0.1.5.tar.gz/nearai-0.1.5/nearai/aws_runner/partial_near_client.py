import re
from typing import List

from nearai.openapi_client import (
    BodyDownloadEnvironmentV1DownloadEnvironmentPost,
    BodyDownloadFileV1RegistryDownloadFilePost,
    BodyDownloadMetadataV1RegistryDownloadMetadataPost,
    BodyListFilesV1RegistryListFilesPost,
    BodyUploadMetadataV1RegistryUploadMetadataPost,
)
from nearai.openapi_client.api.agents_assistants_api import AgentsAssistantsApi
from nearai.openapi_client.api.registry_api import RegistryApi
from nearai.openapi_client.api_client import ApiClient
from nearai.openapi_client.configuration import Configuration
from nearai.openapi_client.models.entry_location import EntryLocation
from nearai.openapi_client.models.entry_metadata_input import EntryMetadataInput
from nearai.shared.auth_data import AuthData

ENVIRONMENT_FILENAME = "environment.tar.gz"


class PartialNearClient:
    """Wrap NearAI api registry methods, uses generated NearAI client."""

    def __init__(self, base_url: str, auth: AuthData):  # noqa: D107
        configuration = Configuration(access_token=f"Bearer {auth.model_dump_json()}", host=base_url)
        client = ApiClient(configuration)

        self._client = client
        self.entry_location_pattern = re.compile("^(?P<namespace>[^/]+)/(?P<name>[^/]+)/(?P<version>[^/]+)$")
        self.auth = auth

    def parse_location(self, entry_location: str) -> dict:
        """Create a EntryLocation from a string in the format namespace/name/version."""
        match = self.entry_location_pattern.match(entry_location)

        if match is None:
            raise ValueError(
                f"Invalid entry format: {entry_location}. Should have the format <namespace>/<name>/<version>"
            )

        return {
            "namespace": match.group("namespace"),
            "name": match.group("name"),
            "version": match.group("version"),
        }

    def get_file_from_registry(self, entry_location: dict, path: str):
        """Fetches a file from NearAI registry."""
        api_instance = RegistryApi(self._client)
        body = BodyDownloadFileV1RegistryDownloadFilePost.from_dict(
            dict(
                entry_location=entry_location,
                path=path,
            )
        )
        assert (
            body is not None
        ), f"Unable to create request body for file download. Entry location: {entry_location}, Path: {path}"
        result = api_instance.download_file_v1_registry_download_file_post(body)
        return result

    def list_files(self, entry_location: dict) -> List[str]:
        """List files in from an entry in the registry.

        Return the relative paths to all files with respect to the root of the entry.
        """
        api_instance = RegistryApi(self._client)
        body = BodyListFilesV1RegistryListFilesPost.from_dict(dict(entry_location=entry_location))
        assert body is not None, f"Unable to create request body for file listing. Entry location: {entry_location}"
        result = api_instance.list_files_v1_registry_list_files_post(body)
        return [file.filename for file in result]

    def get_files_from_registry(self, entry_location: dict):
        """Fetches all files from NearAI registry."""
        api_instance = RegistryApi(self._client)

        files = self.list_files(entry_location)
        results = []

        for path in files:
            body = BodyDownloadFileV1RegistryDownloadFilePost.from_dict(
                dict(
                    entry_location=entry_location,
                    path=path,
                )
            )
            assert (
                body is not None
            ), f"Unable to create request body for file download. Entry location: {entry_location}, Path: {path}"
            result = api_instance.download_file_v1_registry_download_file_post(body)
            results.append({"filename": path, "content": result})
        return results

    def get_agent_metadata(self, identifier: str) -> dict:
        """Fetches metadata for an agent from NearAI registry."""
        api_instance = RegistryApi(self._client)
        entry_location = self.parse_location(identifier)
        body = BodyDownloadMetadataV1RegistryDownloadMetadataPost.from_dict(dict(entry_location=entry_location))
        assert body is not None, f"Unable to create request body for agent metadata. Entry location: {entry_location}"
        result = api_instance.download_metadata_v1_registry_download_metadata_post(body)
        return result.to_dict()

    def get_agent(self, identifier):
        """Fetches an agent from NearAI registry."""
        entry_location = self.parse_location(identifier)
        # download all agent files
        return self.get_files_from_registry(entry_location)

    def get_environment(self, env_id):
        """Fetches an environment from NearAI registry."""
        entry_location = self.parse_location(env_id)
        api_instance = AgentsAssistantsApi(self._client)
        result = api_instance.download_environment_v1_download_environment_post(
            BodyDownloadEnvironmentV1DownloadEnvironmentPost.from_dict(
                dict(
                    entry_location=entry_location,
                    path=ENVIRONMENT_FILENAME,
                )
            ),
            _headers={"Accept": "application/gzip"},
        )
        return result

    def save_environment(self, file: bytes, metadata: dict) -> str:
        """Saves an environment to NearAI registry."""
        api_instance = RegistryApi(self._client)

        author = self.auth.account_id
        name = str(metadata.get("name"))
        entry_location: dict[str, str] = {"namespace": author, "name": name, "version": "0"}
        api_instance.upload_metadata_v1_registry_upload_metadata_post(
            BodyUploadMetadataV1RegistryUploadMetadataPost(
                metadata=EntryMetadataInput(**metadata), entry_location=EntryLocation(**entry_location)
            )
        )

        api_instance.upload_file_v1_registry_upload_file_post(
            path=ENVIRONMENT_FILENAME,
            file=file,
            namespace=entry_location["namespace"],
            name=entry_location["name"],
            version=entry_location["version"],
        )
        return f"{author}/{name}/0"
