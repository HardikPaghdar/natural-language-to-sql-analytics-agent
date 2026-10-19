from app import plan,run_query
import pytest
def test_query_uses_approved_select():
 intent,sql=plan("show total sales by region")
 assert intent=="sales_by_region" and sql.startswith("SELECT")
def test_sample_data_query_is_read_only():
 r=run_query("list all sales")
 assert r["read_only"] and len(r["rows"])>0
def test_unsupported_query_rejected():
 with pytest.raises(ValueError): plan("delete all sales")
