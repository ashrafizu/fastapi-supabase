from enum import Enum

from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException, Path, Body, Query
from fastapi.encoders import jsonable_encoder

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# You can give your API a title and add additional metadata such as a description, version number, etc.
# The description also supports markdown formatting.
app = FastAPI(
    title="Ashraf's FastAPI and Supabase Project",
    description="This is just a trial and error phase",
    version="0.1.0",
)

# Docstrings of classes will be reflected in the API documentation in the 'Schemas' section
class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


# You can add metadata to attributes using the Field class.
# This information will also be shown in the auto-generated documentation.
class Item(BaseModel):
    """Representation of an item in the system."""
    name: str = Field(description="Name of the item.")
    price: float = Field(description="Price of the item in RM.")
    count: int = Field(description="Amount of instances of this item in stock.")
    id: int = Field(description="Unique integer that specifies this item.")
    category: Category = Field(description="Category this item belongs to.")

class Fuel(BaseModel):
    date: str
    ron95: float
    ron97: float
    diesel: float
    series_type: str


@app.get("/fuel-price")
def get_fuel_data():
    fuel_price = supabase.table("fuel_price").select("*").execute()
    return fuel_price

Selection = dict[
    str, str | int | float | Category | None
]  # dictionary containing the user's query arguments


@app.post("/fuel-price")
def add_fuel_data(payload: Fuel):
    check_date_exist = supabase.table("fuel_price_string").select("date").eq("date", payload.date).execute()
    for item in check_date_exist.data:
        if item["date"] == payload.date:
            raise HTTPException(status_code=400, detail=f"Fuel price data with date '{payload.date}' already exists.")
        
    fuel_price = supabase.table("fuel_price_string").insert(payload.model_dump()).execute()
    return {"added": fuel_price}

class Update_Body(BaseModel):
    ron95: float
    ron97: float
    diesel: float
    series_type: str   

# The 'responses' keyword allows you to specify which responses a user can expect from this endpoint.
@app.put(
        "/fuel-price/update/{fuel_date}",
        responses={
            404: {"description": "Item not found"},
            400: {"description": "No arguments specified"}
        },
)
# The Query and Path classes also allow us to add documentation to query and path parameters.
def update_fuel_price_by_date(
    fuel_date: str = Path(title="Date", description="in 'YYYY-MM-DDDD' format"),
    payload: dict = Body(title="Details to update", description="in JSON format", example={"ron95":0, "ron97":0, "diesel":0, "series_type":"string"})
):
    check_date_exist = supabase.table("fuel_price_string").select("date").eq("date", fuel_date).execute()
    if check_date_exist.data == []:
        raise HTTPException(status_code=404, detail=f"Fuel price data with date '{fuel_date}' does not exist.")
    
    json_body = list(payload)
    for param in json_body:
        if param not in ("ron95", "ron97", "diesel", "series_type"):
            raise HTTPException(status_code=400, detail=f"Parameter '{param}' is not recognized.")
    if json_body == []:
        raise HTTPException(status_code=400, detail="No parameter given.")

    fuel_price = supabase.table("fuel_price_string").update(payload).eq("date", fuel_date).execute()
    return {"updated": fuel_price}


@app.delete("/fuel-price/delete/{fuel_date}")
def delete_fuel_data_by_date(fuel_date: str):
    fuel_price = supabase.table("fuel_price_string").delete().eq("date",fuel_date).execute()
    if fuel_price.data == []:
        raise HTTPException(status_code=404, detail=f"Fuel price data with date '{fuel_date}' does not exist.")
    return {"deleted": fuel_price}