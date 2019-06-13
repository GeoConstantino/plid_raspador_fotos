import pytest
import os
import pandas as pd

from process import lista_rgs

def test_lista_rgs():
    file_csv = os.getcwd()+"/in/test_lista_rgs.csv"
    assert lista_rgs(file_csv) == [[130015340,6],[98255060,10]]

