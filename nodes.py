import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from state import CommuteState

# Load environment variables
# Load environment variables
load_dotenv()

# .env file mein aapne GEMINI_API_KEY rakha hai, isliye yahan wahi naam dein
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in the .env file!")

llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2, google_api_key=api_key)

def input_parser_node(state: CommuteState):
    print("--- 1. INPUT PARSER NODE ---")
    return state

def traffic_fetcher_node(state: CommuteState):
    print("--- 2. TRAFFIC FETCHER NODE ---")
    origin = state.get("origin", "").lower()
    destination = state.get("destination", "").lower()
    
    # Karachi-based traffic simulation logic
    if "pechs" in origin and "chundrigar" in destination:
        state["traffic_status"] = "Heavy Jam / Construction at Saddar & Sharea Faisal"
        state["delay_minutes"] = 35
    elif "gulshan" in origin or "university" in destination:
        state["traffic_status"] = "Moderate Congestion at NIPA Chowrangi"
        state["delay_minutes"] = 18
    else:
        state["traffic_status"] = "Smooth Traffic Flow"
        state["delay_minutes"] = 5
        
    return state

def decision_routing_node(state: CommuteState):
    print("--- 3. DECISION ROUTING NODE ---")
    return state

def alternative_route_node(state: CommuteState):
    print("--- 4. ALTERNATIVE ROUTE NODE (Heavy Delay) ---")
    prompt = f"The traffic from {state['origin']} to {state['destination']} has a delay of {state['delay_minutes']} minutes due to {state['traffic_status']}. Suggest a smart alternative route and transport mode in 3 bullet points."
    response = llm.invoke([HumanMessage(content=prompt)])
    state["route_plan"] = response.content
    return state

def standard_route_node(state: CommuteState):
    print("--- 4. STANDARD ROUTE NODE (Normal Flow) ---")
    state["route_plan"] = f"Take the primary direct route from {state['origin']} to {state['destination']} using your selected {state['transport_mode']}. Estimated arrival is on time."
    return state

def response_synthesizer_node(state: CommuteState):
    print("--- 5. RESPONSE SYNTHESIZER NODE ---")
    return state