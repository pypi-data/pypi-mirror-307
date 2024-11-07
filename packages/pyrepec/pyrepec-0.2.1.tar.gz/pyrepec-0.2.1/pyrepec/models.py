# -*- coding: utf-8 -*-

"""Data Models for pyrepec."""

from typing import List, Optional, Union

from pydantic import BaseModel


class RepecError(BaseModel):
    """
    Pydantic model class for errors issued by Repec API services.

    :param code: Numerical error code
    :type code: int or None
    :param message: Description of the error
    :type message: str
    :param function: Repec method that has originated the error
    :type function: str
    :param url: Full URL of Repec API that as been called
    :type url: str or None
    """

    code: Union[int, None] = None
    message: Optional[str] = "Unknown Exception"
    function: Optional[str] = "N/A"
    url: Optional[str] = None


class RepecResultList(BaseModel):
    """
    Pydantic model class for results returned by REPEC API services.

    :param data: List of result items
    :type data: List of dicts
    :param error: Error issued by Repec API services (if any)
    :type error: :class:`models.RepecError` or None
    """

    data: List[dict]
    error: Union[Optional[RepecError], None]


class RepecSingleResult(BaseModel):
    """
    Pydantic model class for results returned by REPEC API services.

    :param data: Result item
    :type data: dict
    :param error: Error issued by Repec API services (if any)
    :type error: :class:`models.RepecError` or None
    """

    data: dict
    error: Union[Optional[RepecError], None]


class RepecJelResult(BaseModel):
    """
    Pydantic model class for JEL codes returned by REPEC API services.

    :param data: List of JEL codes
    :type data: List of str
    :param error: Error issued by Repec API services (if any)
    :type error: :class:`models.RepecError` or None
    """

    data: list[str]
    error: Union[Optional[RepecError], None]
