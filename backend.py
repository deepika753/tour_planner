import nest_asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
import openai
import requests

# Initialize FastAPI app
app = FastAPI()

# Configure OpenAI API Key
openai.api_key = "<YOUR_OPENAI_API_KEY>"

# Configure Neo4j Driver
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test"))

# Apply nest_asyncio
nest_asyncio.apply()

class UserPreferences(BaseModel):
    user_id: str
    city: str
    date: str
    start_time: str
    end_time: str
    interests: list
    budget: float
    starting_point: str = None

class ItineraryResponse(BaseModel):
    itinerary: list
    weather: dict
    message: str

def save_user_memory(preferences: UserPreferences):
    with driver.session() as session:
        session.run("""
            MERGE (u:User {id: $user_id})
            MERGE (c:City {name: $city})
            MERGE (u)-[:PLANS]->(t:Trip {date: $date, budget: $budget})
            MERGE (t)-[:TO]->(c)
            MERGE (t)-[:STARTS_AT]->(s:Location {name: $starting_point})
        """, {
            "user_id": preferences.user_id,
            "city": preferences.city,
            "date": preferences.date,
            "budget": preferences.budget,
            "starting_point": preferences.starting_point or preferences.city
        })

@app.post("/collect_preferences/")
async def collect_preferences(preferences: UserPreferences):
    save_user_memory(preferences)
    return {"message": "Preferences saved successfully!"}

@app.post("/generate_itinerary/", response_model=ItineraryResponse)
async def generate_itinerary(preferences: UserPreferences):
    prompt = f"Plan a one-day itinerary in {preferences.city} based on interests: {', '.join(preferences.interests)}, budget: ${preferences.budget}."
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=500)
    itinerary = response.choices[0].text.strip().split('\n')
    return {"itinerary": itinerary, "message": "Itinerary generated successfully!"}
