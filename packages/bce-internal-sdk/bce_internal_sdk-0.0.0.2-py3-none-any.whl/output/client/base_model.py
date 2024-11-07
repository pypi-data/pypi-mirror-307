#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/11/1
# @Author  : zhoubohan
# @File    : base_model.py
"""
from pydantic import BaseModel as BM
from enum import Enum


class BaseModel(BM):
    """
    Base Model contains the common configuration for all pydantic models
    """

    class Config:
        """
        Config contains the common configuration for all pydantic models
        """
        allow_population_by_field_name = True
        protected_namespaces = []

    def json(self, **kwargs):
        """
        Override the json method to convert Enum to its value
        """
        original_dict = super().dict(**kwargs)
        for key, value in original_dict.items():
            if isinstance(value, Enum):
                original_dict[key] = value.value
        return super().json(
            by_alias=True,
            exclude_unset=True, **kwargs)
