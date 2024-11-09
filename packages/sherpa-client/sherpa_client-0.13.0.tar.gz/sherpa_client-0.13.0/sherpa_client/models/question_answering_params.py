from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionAnsweringParams")


@attr.s(auto_attribs=True)
class QuestionAnsweringParams:
    """Question answering parameters

    Attributes:
        enabled (Union[Unset, bool]): Generate answer to the question
        generator (Union[Unset, str]): Answer generator to be used
    """

    enabled: Union[Unset, bool] = False
    generator: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        generator = self.generator

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if generator is not UNSET:
            field_dict["generator"] = generator

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        generator = d.pop("generator", UNSET)

        question_answering_params = cls(
            enabled=enabled,
            generator=generator,
        )

        return question_answering_params
