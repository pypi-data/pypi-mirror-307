#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2024] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.

from typing import Any, Dict


class BaseInfo:
    """Base structure of information."""

    def __init__(self, **kwarg: Dict[str, Any]) -> None:
        self.kwargs = kwarg
        for key in kwarg:
            setattr(self, key, kwarg[key])

    def __repr__(self) -> str:
        """Representation"""
        result_str = ", ".join(f"{key}={value}" for key, value in self.kwargs.items())
        return f"{self.__class__.__name__}({result_str})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the BaseInfo object.
        """
        return self.kwargs
