# coding: utf-8

"""
    Terra Scientific Pipelines Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from teaspoons_client.models.get_pipelines_result import GetPipelinesResult

class TestGetPipelinesResult(unittest.TestCase):
    """GetPipelinesResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetPipelinesResult:
        """Test GetPipelinesResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetPipelinesResult`
        """
        model = GetPipelinesResult()
        if include_optional:
            return GetPipelinesResult(
                results = [
                    teaspoons_client.models.pipeline.Pipeline(
                        pipeline_name = '', 
                        display_name = '', 
                        description = '', )
                    ]
            )
        else:
            return GetPipelinesResult(
        )
        """

    def testGetPipelinesResult(self):
        """Test GetPipelinesResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
