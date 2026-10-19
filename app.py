from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import sqlite3
from pathlib import Path
app=FastAPI(title="Natural Language to SQL Analytics Agent",version="0.1.0")
DB=Path(__file__).parent/"analytics.db"
def initialize():
 c=sqlite3.connect(DB); c.execute("CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY,region TEXT,product TEXT,amount REAL)")
 if c.execute("SELECT COUNT(*) FROM sales").fetchone()[0]==0:c.executemany("INSERT INTO sales(region,product,amount) VALUES(?,?,?)",[("North","Widget",120),("South","Widget",80),("North","Gadget",200),("West","Gadget",150)])
 c.commit();c.close()
initialize()
def plan(q):
 q=q.lower()
 if "total" in q and "region" in q:return ("sales_by_region","SELECT region, SUM(amount) AS total_amount FROM sales GROUP BY region ORDER BY total_amount DESC LIMIT 100")
 if "total" in q and "product" in q:return ("sales_by_product","SELECT product, SUM(amount) AS total_amount FROM sales GROUP BY product ORDER BY total_amount DESC LIMIT 100")
 if "average" in q or "avg" in q:return ("average_sale","SELECT AVG(amount) AS average_amount FROM sales LIMIT 1")
 if "list" in q or "show" in q or "all sales" in q:return ("list_sales","SELECT id,region,product,amount FROM sales ORDER BY id LIMIT 100")
 raise ValueError("Unsupported question. Try total by region/product, average sale, or list sales.")
def run_query(q):
 intent,sql=plan(q)
 c=sqlite3.connect(f"file:{DB}?mode=ro",uri=True);c.row_factory=sqlite3.Row
 try: rows=[dict(x) for x in c.execute(sql).fetchmany(100)]
 finally:c.close()
 return {"intent":intent,"sql":sql,"rows":rows,"row_limit":100,"read_only":True}
class Request(BaseModel):
 question:str=Field(min_length=3,max_length=500)
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/schema")
def schema():return {"tables":{"sales":["id INTEGER","region TEXT","product TEXT","amount REAL"]}}
@app.post("/query")
def endpoint(r:Request):
 try:return run_query(r.question)
 except ValueError as e:raise HTTPException(status_code=400,detail=str(e))
