# coding: utf-8

"""
    Terra Scientific Pipelines Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from teaspoons_client.models.pipeline_run_report import PipelineRunReport

class TestPipelineRunReport(unittest.TestCase):
    """PipelineRunReport unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PipelineRunReport:
        """Test PipelineRunReport
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PipelineRunReport`
        """
        model = PipelineRunReport()
        if include_optional:
            return PipelineRunReport(
                pipeline_name = '',
                pipeline_version = 56,
                wdl_method_version = '',
                outputs = {
                    'key' : None
                    }
            )
        else:
            return PipelineRunReport(
                pipeline_name = '',
                pipeline_version = 56,
                wdl_method_version = '',
        )
        """

    def testPipelineRunReport(self):
        """Test PipelineRunReport"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
