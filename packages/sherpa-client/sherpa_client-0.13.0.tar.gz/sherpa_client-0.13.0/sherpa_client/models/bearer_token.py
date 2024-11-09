from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BearerToken")


@attr.s(auto_attribs=True)
class BearerToken:
    """
    Attributes:
        access_token (str):
        email (Union[Unset, str]):
    """

    access_token: str
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        email = d.pop("email", UNSET)

        bearer_token = cls(
            access_token=access_token,
            email=email,
        )

        return bearer_token
