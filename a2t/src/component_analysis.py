"""Component analysis benchmarks.

Copyright (c) 2019 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
from time import time
import json
import re
from urllib.parse import urljoin

from api import Api


# directory where the API results needs to be dumped
API_RESULTS_DIRECTORY = "api_results"


class ComponentAnalysis(Api):
    """Implementation of component analysis."""

    def __init__(self, url, token, user_key, dump_json_responses):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token, user_key)
        self._dump_json_responses = dump_json_responses

    def analysis_url(self, ecosystem, component, version):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                      c=component,
                                                                      v=version))

    def check_auth_token_validity(self):
        """Check that the authorization token is valid by calling the API and check HTTP code."""
        endpoint = self.url + 'api/v1/readiness'
        response = self.perform_get_request(endpoint)

        if response.status_code != 200:
            self.print_error_response(response, "error")
        return response.status_code == 200

    def dump_analysis(self, ecosystem, component, version, json_response):
        """Dump the component analysis result into a file."""
        timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        filename = API_RESULTS_DIRECTORY + "/"
        filename += "component_analysis_{e}_{c}_{v}_{t}.json".format(e=ecosystem,
                                                                     c=component,
                                                                     v=version,
                                                                     t=timestamp_str)
        with open(filename, 'w') as fout:
            json.dump(json_response, fout)

    def check_analysis(self, analysis, ecosystem, package, version):
        """Check the results of component analysis."""
        try:
            assert analysis is not None, "Analysis not available"
            assert "result" in analysis, "Can not find the 'result' node."
            result = analysis["result"]
            self.check_recommendation_part(result)
            self.check_data_part(result, ecosystem, package, version)
            return "OK"
        except Exception as e:
            return "Failed: " + str(e)

    def check_recommendation_part(self, result):
        """Check the recommendation part of component analysis."""
        assert "recommendation" in result, "Can not find the 'recommendation' node."
        recommendation = result["recommendation"]
        assert recommendation == {} or "component-analyses" in recommendation, \
            "Wrong content of recommendation node"
        if "component_analyses" in recommendation:
            self.check_component_analyses_recommendation(recommendation)

    def check_component_analyses_recommendation(self, recommendation):
        """Check the recommendation node in the component analysis."""
        assert "change_to" in recommendation, "Expected node 'change_to'"
        assert "message" in recommendation, "Expected node 'message'"
        assert "component_analyses" in recommendation, "Expected node 'component-analyses'"
        component_analyses = recommendation["component_analyses"]
        assert "cve" in component_analyses
        self.check_cves(component_analyses)

    def check_cves(self, component_analyses):
        """Check CVEs that might be part of component analyses."""
        cves = component_analyses["cve"]
        for c in cves:
            assert "id" in c
            assert "cvss" in c
            self.check_cve_value(c["id"])

    def get_cve_pattern(self, with_score):
        """Return the CVE pattern."""
        if with_score:
            # please note that in graph DB, the CVE entries have the following format:
            # CVE-2012-1150:5.0
            # don't ask me why, but the score is stored in one field together with ID itself
            # the : character is used as a separator
            return r"CVE-(\d{4})-\d{4,}:(\d+\.\d+)"
        else:
            return r"CVE-(\d{4})-\d{4,}"

    def check_cve_value(self, cve, with_score=False):
        """Check CVE values in CVE records."""
        pattern = self.get_cve_pattern(with_score)

        match = re.fullmatch(pattern, cve)
        assert match is not None, "Improper CVE number %s" % cve

        year = int(match.group(1))
        current_year = datetime.datetime.utcnow().year

        # well the lower limit is a bit arbitrary
        # (according to SRT guys it should be 1999)
        assert year >= 1999 and year <= current_year, "Improper year of CVE"

        if with_score:
            score = float(match.group(2))
            assert score >= 0.0 and score <= 10.0, "Improper score value of CVE"

    def check_data_part(self, result, ecosystem, package, version):
        """Check the data part of component analysis."""
        assert "data" in result, "Can not find the 'data' node."
        data = result["data"]
        assert len(data) >= 0, "At least one package expected in analysis"
        for node in data:
            self.check_package_version(node, ecosystem, package, version)

    def check_package_version(self, node, ecosystem, package, version):
        """Check the package in component analysis."""
        assert "package" in node, "'package' node is expected"
        assert "version" in node, "'version' node is expected"
        self.check_package_part(node, ecosystem, package)
        self.check_version_part(node, ecosystem, package, version)
        # TODO: add more thorough checks

    def compare_ecosystems(self, e, ecosystem):
        """Compare two ecosystems: the setup one and the checked one."""
        assert e is not None, "Missing ecosystem to compare"
        assert ecosystem is not None, "Missing ecosystem to compare"
        assert e == ecosystem, "Unexpected ecosystem found {}".format(e)
        # TODO: add more thorough checks

    def compare_packages(self, p, package):
        """Compare two packages: the setup one and the checked one."""
        assert p is not None, "Missing package to compare"
        assert package is not None, "Missing package to compare"
        assert p == package, "Unexpected component name found {}".format(p)
        # TODO: add more thorough checks

    def compare_versions(self, v, version):
        """Compare two versions: the setup one and the checked one."""
        assert v is not None, "Missing version to compare"
        assert version is not None, "Missing version to compare"
        assert v == version, "Unexpected version found {}".format(v)
        # TODO: add more thorough checks

    def check_ecosystem(self, node):
        """Check the 'ecosystem' attribute in a node."""
        assert "ecosystem" in node, "Package node does not contain attribute 'ecosystem'"
        assert len(node["ecosystem"]) >= 1, "Expecting at least one 'ecosystem' value"
        # TODO: add more thorough checks

    def check_name(self, node):
        """Check the 'name' attribute in a node."""
        assert "name" in node, "Package node does not contain attribute 'node'"
        assert len(node["name"]) >= 1, "Expecting at least one 'name' value"
        # TODO: add more thorough checks

    def check_package_part(self, node, ecosystem, package):
        """Self package part of E/P analysis response."""
        package_node = node["package"]
        # check the ecosystem and name attributes that are required for a package
        self.check_ecosystem(package_node)
        self.check_name(package_node)

        # compare with expected values
        e = package_node["ecosystem"][0]
        p = package_node["name"][0]
        self.compare_ecosystems(e, ecosystem)
        self.compare_packages(p, package)

    def check_pecosystem(self, node):
        """Check the 'pecosystem' attribute in a node."""
        assert "pecosystem" in node, "Version node does not contain attribute 'pecosystem'"
        assert len(node["pecosystem"]) >= 1, "Expecting at least one 'pecosystem' value"
        # TODO: add more thorough checks

    def check_pname(self, node):
        """Check the 'pname' attribute in a node."""
        assert "pname" in node, "Version node does not contain attribute 'pname'"
        assert len(node["pname"]) >= 1, "Expecting at least one 'pname' value"
        # TODO: add more thorough checks

    def check_version(self, node):
        """Check the 'version' attribute in a node."""
        assert "version" in node, "Version node does not contain attribute 'version'"
        assert len(node["version"]) >= 1, "Expecting at least one 'version' value"
        # TODO: add more thorough checks

    def check_version_part(self, node, ecosystem, package, version):
        """Self version part of E/P/V analysis response."""
        version_node = node["version"]
        # check the ecosystem, version, and name attributes that are required for a version
        self.check_pecosystem(version_node)
        self.check_pname(version_node)
        self.check_version(version_node)

        # compare with expected values
        e = version_node["pecosystem"][0]
        p = version_node["pname"][0]
        v = version_node["version"][0]
        self.compare_ecosystems(e, ecosystem)
        self.compare_packages(p, package)
        self.compare_versions(v, version)

    def dump_response_if_enabled(self, ecosystem, component, version, response):
        """Dump response gathered from server, but only if dumping is enabled."""
        if self._dump_json_responses:
            try:
                self.dump_analysis(ecosystem, component, version, response.json())
            except Exception:
                self.print_error_response(response, "error")
                # not need to fail there - we'll fail later properly

    def start(self, thread_id=None, ecosystem=None, component=None, version=None, queue=None):
        """Start the component analysis and check the status code."""
        start_time = time()
        endpoint = self.analysis_url(ecosystem, component, version)
        response = self.perform_get_request(endpoint)

        self.dump_response_if_enabled(ecosystem, component, version, response)

        status_code = response.status_code
        end_time = time()
        duration = end_time - start_time

        json_response = ""
        check = "N/A"

        try:
            json_response = response.json()
            if status_code == 200:
                check = self.check_analysis(json_response, ecosystem, component, version)
            else:
                check = "N/A, analysis in progress"
        except Exception:
            pass

        r = {"name": "component_analysis",
             "method": "GET",
             "ecosystem": ecosystem,
             "package": component,
             "version": version,
             "thread_id": thread_id,
             "status_code": status_code,
             "json": json_response,
             "started": start_time,
             "finished": end_time,
             "duration": duration,
             "analysis": check,
             "manifest": "N/A"
             }

        if queue is not None:
            queue.put(r)

        # return both component analysis status and debug data (durations) as well
        return r
