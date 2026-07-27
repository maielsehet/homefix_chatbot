import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import clean, row_to_document

def test_clean():
    text = "  أهلاً بك  في خدمات صيانة المنزل!" 
    assert clean(text) == "أهلاً بك في خدمات صيانة المنزل!"

def test_clean_empty():
    import pandas as pd
    assert clean(pd.NA) == ""
    assert clean("") == ""

def test_row_to_document():
    row = {
        "category": "تكييف",
        "problem": "التكييف لا يبرد الغرفة",
        "solution": "تنظيف الفلاتر أو شحن الفريون"
    }
    
    doc = row_to_document(row, source_file="test_file.csv", row_id=0)
    
    assert "التكييف" in doc.page_content
    assert doc.metadata["category"] == "تكييف"
    assert doc.metadata["source"] == "test_file.csv" 

