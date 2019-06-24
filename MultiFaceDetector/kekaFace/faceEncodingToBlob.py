# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 16:37:46 2019

@author: krish
"""
import numpy as np
import io
import sqlite3
def adaptArray(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convertArray(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)