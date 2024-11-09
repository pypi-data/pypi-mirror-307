from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FilteringParams")


@attr.s(auto_attribs=True)
class FilteringParams:
    """Filtering parameters

    Attributes:
        query_filter (Union[Unset, str]): Optional Lucene query string to filter on, e.g.: '+annotations:*'
        selected_facets (Union[Unset, List[str]]):
    """

    query_filter: Union[Unset, str] = UNSET
    selected_facets: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        query_filter = self.query_filter
        selected_facets: Union[Unset, List[str]] = UNSET
        if not isinstance(self.selected_facets, Unset):
            selected_facets = self.selected_facets

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if query_filter is not UNSET:
            field_dict["queryFilter"] = query_filter
        if selected_facets is not UNSET:
            field_dict["selectedFacets"] = selected_facets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_filter = d.pop("queryFilter", UNSET)

        selected_facets = cast(List[str], d.pop("selectedFacets", UNSET))

        filtering_params = cls(
            query_filter=query_filter,
            selected_facets=selected_facets,
        )

        return filtering_params
