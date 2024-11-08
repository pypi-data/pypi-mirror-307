# ruff: noqa: D102

"""
Provides the WeaverController class for managing HTTP requests.

This module extends the functionality of the Client class to handle artifact retrieval,
release management, and various graph operations. It adds specific methods to
interact with API endpoints related to artifacts, releases, and graph data traversal.
"""

from __future__ import annotations

from gobtools.utils.client import Client


class WeaverController(Client):
    """
    A controller for managing HTTP requests related to artifacts, releases, and graphs.

    This class extends the Client class, adding methods specific to handling artifact
    retrieval, graph operations, and release management.
    """

    def __init__(self, path_root: str) -> None:
        """
        Initialize the WeaverController with a base URL.

        Arguments:
        ---------
            path_root (str): The base URL for HTTP requests.

        """
        super().__init__(path_root)

    def __post_with_added_values(
        self,
        path: str,
        data: dict,
        added_values: list[str] | None = None,
    ) -> dict:
        if added_values:
            data["addedValues"] = added_values
        else:
            data["addedValues"] = []
        return self.post_dict(path, data)

    def __post_releases(
        self,
        path: str,
        group_id: str,
        artifact_id: str,
        version: str,
        added_values: list[str] | None = None,
    ) -> dict:
        data = {"groupId": group_id, "artifactId": artifact_id, "version": version}
        return self.__post_with_added_values(path, data, added_values)

    def __post_graph(
        self,
        path: str,
        releases: list[dict],
        added_values: list[str] | None = None,
    ) -> dict:
        data = {"releases": releases}
        return self.__post_with_added_values(path, data, added_values)

    def __post_artifact(
        self,
        path: str,
        group_id: str,
        artifact_id: str,
        added_values: list[str] | None = None,
    ) -> dict:
        data = {"groupId": group_id, "artifactId": artifact_id}
        return self.__post_with_added_values(path, data, added_values)

    def get_release(
        self,
        group_id: str,
        artifact_id: str,
        version: str,
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_releases(
            "/release",
            group_id,
            artifact_id,
            version,
            added_values,
        )

    def get_release_new_versions(
        self,
        group_id: str,
        artifact_id: str,
        version: str,
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_releases(
            "/release/newVersions",
            group_id,
            artifact_id,
            version,
            added_values,
        )

    def get_dependents(
        self,
        group_id: str,
        artifact_id: str,
        version: str,
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_releases(
            "/release/dependents",
            group_id,
            artifact_id,
            version,
            added_values,
        )

    def get_graph_traversing(
        self,
        start_releases_gav: list[str],
        lib_to_expands_ga: list[str],
        filters: list[str],
        added_values: list[str] | None = None,
    ) -> dict:
        data = {
            "startReleasesGav": start_releases_gav,
            "libToExpandsGa": lib_to_expands_ga,
            "filters": filters,
        }
        return self.__post_with_added_values("/graph/traversing", data, added_values)

    def get_graph_rooted_graph(
        self,
        releases: list[dict],
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_graph("/graph/rootedGraph", releases, added_values)

    def get_graph_direct_possibilities_rooted(
        self,
        releases: list[dict],
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_graph(
            "/graph/directPossibilitiesRooted",
            releases,
            added_values,
        )

    def get_cypher(self, query: str, added_values: list[str] | None = None) -> dict:
        data = {"query": query}
        return self.__post_with_added_values("/cypher", data, added_values)

    def get_artifact(
        self,
        group_id: str,
        artifact_id: str,
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_artifact("/artifact", group_id, artifact_id, added_values)

    def get_artifact_releases(
        self,
        group_id: str,
        artifact_id: str,
        added_values: list[str] | None = None,
    ) -> dict:
        return self.__post_artifact(
            "/artifact/releases",
            group_id,
            artifact_id,
            added_values,
        )
