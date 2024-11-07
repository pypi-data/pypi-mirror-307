# coding: utf-8

"""
    Terra Scientific Pipelines Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from teaspoons_client.models.error_report import ErrorReport
from teaspoons_client.models.job_report import JobReport
from teaspoons_client.models.pipeline_run_report import PipelineRunReport
from typing import Optional, Set
from typing_extensions import Self

class AsyncPipelineRunResponse(BaseModel):
    """
    Result of an asynchronous pipeline run request.
    """ # noqa: E501
    job_report: JobReport = Field(alias="jobReport")
    error_report: Optional[ErrorReport] = Field(default=None, alias="errorReport")
    pipeline_run_report: PipelineRunReport = Field(alias="pipelineRunReport")
    __properties: ClassVar[List[str]] = ["jobReport", "errorReport", "pipelineRunReport"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AsyncPipelineRunResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of job_report
        if self.job_report:
            _dict['jobReport'] = self.job_report.to_dict()
        # override the default output from pydantic by calling `to_dict()` of error_report
        if self.error_report:
            _dict['errorReport'] = self.error_report.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pipeline_run_report
        if self.pipeline_run_report:
            _dict['pipelineRunReport'] = self.pipeline_run_report.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AsyncPipelineRunResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "jobReport": JobReport.from_dict(obj["jobReport"]) if obj.get("jobReport") is not None else None,
            "errorReport": ErrorReport.from_dict(obj["errorReport"]) if obj.get("errorReport") is not None else None,
            "pipelineRunReport": PipelineRunReport.from_dict(obj["pipelineRunReport"]) if obj.get("pipelineRunReport") is not None else None
        })
        return _obj


