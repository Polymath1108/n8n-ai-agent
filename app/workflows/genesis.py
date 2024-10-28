from langgraph.graph import END, StateGraph
from app.states.supervisor import SupervisorState
from app.utils.state_helpers import get_last_message, join_graph
from app.nodes.genesis_supervisor import supervisor_node
from app.consts import PROJECT_MANAGER, SUPERVISOR, ADMINISTRATOR, FINISH


super_graph = StateGraph(SupervisorState)
super_graph.add_node(
    PROJECT_MANAGER, get_last_message | pm_chain | join_graph
)
super_graph.add_node(
    ADMINISTRATOR, get_last_message | admin_chain | join_graph
)
super_graph.add_node(SUPERVISOR, supervisor_node)

super_graph.add_edge(PROJECT_MANAGER, SUPERVISOR)
super_graph.add_edge(ADMINISTRATOR, SUPERVISOR)
super_graph.add_conditional_edges(
    SUPERVISOR,
    lambda x: x["next"],
    {
        PROJECT_MANAGER: PROJECT_MANAGER,
        ADMINISTRATOR: ADMINISTRATOR,
        FINISH: END,
    },
)
super_graph.set_entry_point(SUPERVISOR)
super_graph = super_graph.compile()