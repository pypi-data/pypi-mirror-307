#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .FuckExcel import FuckExcel

name = "FuckExcel"


def getFuckExcel(excel_path):
    return FuckExcel(excel_path)
