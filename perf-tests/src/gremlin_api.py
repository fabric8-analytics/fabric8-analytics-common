"""Class representing Gremlin API."""

import re
import requests

from api import *

from gremlin_package_generator import *
from gremlin_query import *


class GremlinApi(Api):
    """Class representing Gremlin API."""

    def __init__(self, url):
        """Set the API endpoint."""
        super().__init__(url)
        # initialize generators of ecosystem+package and ecosystem+package+version tuples
        self._package_generator = GremlinPackageGenerator.package_generator()
        self._package_version_generator = GremlinPackageGenerator.package_version_generator()

    @staticmethod
    def check_and_get_attribute(node, attribute_name):
        """Check the attribute presence and if the attribute is found, return its value."""
        assert attribute_name in node, \
            "'%s' attribute is expected in the node, " \
            "found: %s attributes " % (attribute_name, ", ".join(node.keys()))
        return node[attribute_name]

    @staticmethod
    def check_gremlin_status_node(data):
        """Check the basic structure of the 'status' node in Gremlin response."""
        status = GremlinApi.check_and_get_attribute(data, "status")
        message = GremlinApi.check_and_get_attribute(status, "message")
        code = GremlinApi.check_and_get_attribute(status, "code")
        attributes = GremlinApi.check_and_get_attribute(status, "attributes")

        assert message == ""
        assert code == 200

        # this node should be empty
        assert not attributes

    @staticmethod
    def check_gremlin_result_node(data):
        """Check the basic structure of the 'result' node in Gremlin response."""
        result = GremlinApi.check_and_get_attribute(data, "result")
        data = GremlinApi.check_and_get_attribute(result, "data")
        meta = GremlinApi.check_and_get_attribute(result, "meta")

        assert type(data) is list
        assert type(meta) is dict

    @staticmethod
    def check_uuid(uuid):
        """Check if the string contains a proper UUID.

        Supported format: 71769af6-0a39-4242-94be-1f84f04c8a56
        """
        regex = re.compile(
            '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
            re.I)
        match = regex.match(uuid)
        return bool(match)

    @staticmethod
    def check_request_id_value_in_json_response(data, attribute_name):
        """Check the request ID attribute in the JSON response.

        Check if ID is stored in a format like: '71769af6-0a39-4242-94be-1f84f04c8a56'
        """
        assert data is not None

        id_attribute = GremlinApi.check_and_get_attribute(data, attribute_name)

        assert id_attribute is not None
        assert GremlinApi.check_uuid(id_attribute)

    @staticmethod
    def check_valid_gremlin_response_data(data):
        """Check that the Gremlin response is valid."""
        assert data, "Gremlin does not send a proper response"

        GremlinApi.check_request_id_value_in_json_response(data, "requestId")
        GremlinApi.check_gremlin_status_node(data)
        GremlinApi.check_gremlin_result_node(data)

    def post_query(self, query):
        """Post the already constructed query to the Gremlin."""
        data = {"gremlin": str(query)}
        print(data)
        response = requests.post(self.url, json=data)
        print(response.json())
        return response

    def query_package(self, ecosystem, package):
        """Try to find the package in the selected ecosystem."""
        query = GremlinQuery().has("ecosystem", ecosystem).has("name", package)
        return self.post_query(query)

    def query_package_version(self, ecosystem, package, version):
        """Try to find the package with version in the selected ecosystem."""
        query = GremlinQuery().has("pecosystem", ecosystem).has("pname", package).has(
            "version", version)
        return self.post_query(query)

    def package_query(self, i, thread=None):
        """Query the package metadata stored in the graph database."""
        ecosystem, package = next(self._package_generator)
        # print(ecosystem, package)
        response = self.query_package(ecosystem, package)
        return response

    def package_version_query(self, i, thread=None):
        """Query the package+version metadata stored in the graph database."""
        ecosystem, package, version = next(self._package_version_generator)
        print(ecosystem, package, version)
        response = self.query_package_version(ecosystem, package, version)
        return response

    def check_gremlin_response(self, response):
        """Check the sanity of Gremlin response."""
        try:
            assert response.status_code == 200
            data = response.json()
            assert data is not None
            self.check_valid_gremlin_response_data(data)
            return True
        except e:
            print(e)
            return False
