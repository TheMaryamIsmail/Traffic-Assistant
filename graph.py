from langgraph.graph import StateGraph, START, END
from state import CommuteState
from nodes import (
    input_parser_node,
    traffic_fetcher_node,
    decision_routing_node,
    alternative_route_node,
    standard_route_node,
    response_synthesizer_node
)

def check_traffic_delay(state: CommuteState):
    if state["delay_minutes"] > 20:
        return "heavy_delay"
    else:
        return "normal_traffic"

def create_traffic_graph():
    workflow = StateGraph(CommuteState)

    # Add Nodes
    workflow.add_node("parser", input_parser_node)
    workflow.add_node("fetch_traffic", traffic_fetcher_node)
    workflow.add_node("decision", decision_routing_node)
    workflow.add_node("alt_route", alternative_route_node)
    workflow.add_node("std_route", standard_route_node)
    workflow.add_node("synthesizer", response_synthesizer_node)

    # Add Edges & Flow
    workflow.add_edge(START, "parser")
    workflow.add_edge("parser", "fetch_traffic")
    workflow.add_edge("fetch_traffic", "decision")

    workflow.add_conditional_edges(
        "decision",
        check_traffic_delay,
        {
            "heavy_delay": "alt_route",
            "normal_traffic": "std_route"
        }
    )

    workflow.add_edge("alt_route", "synthesizer")
    workflow.add_edge("std_route", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()