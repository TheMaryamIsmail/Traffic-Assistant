from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from graph import create_traffic_graph

app = FastAPI()

# Jinja2 Templates configuration
templates = Jinja2Templates(directory="templates")

# Compile LangGraph app
traffic_agent_app = create_traffic_graph()

@app.get("/")
async def home(request: Request):
    # Updated TemplateResponse syntax for newer Starlette/FastAPI versions
    return templates.TemplateResponse(
        request, "index.html", {"result": None}
    )

@app.post("/analyze")
async def analyze_commute(
    request: Request,
    origin: str = Form(...),
    destination: str = Form(...),
    transport_mode: str = Form(...)
):
    initial_state = {
        "origin": origin,
        "destination": destination,
        "transport_mode": transport_mode,
        "traffic_status": "",
        "delay_minutes": 0,
        "route_plan": ""
    }

    # Run the LangGraph AI Agent
    final_output = traffic_agent_app.invoke(initial_state)

    # Updated TemplateResponse syntax
    return templates.TemplateResponse(
        request, "index.html", {"result": final_output}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)