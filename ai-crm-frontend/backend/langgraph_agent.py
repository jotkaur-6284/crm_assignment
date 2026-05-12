import os
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import START, StateGraph

from services.ai_service import extract_interaction_from_text

load_dotenv()

GROQ_MODEL = os.getenv('GROQ_MODEL', 'gemma2-9b-it')
LLAMA_MODEL = os.getenv('LLAMA_MODEL', 'llama-3.3-70b-versatile')


class InteractionState(TypedDict):
    text: str
    extracted: dict


class HCPInteractionAgent:
    """LangGraph agent for managing HCP interactions across sales workflows.

    This agent uses a small state graph to parse incoming chat text, extract
    entities and structured fields, summarize interactions, and expose tools for
    logging, editing, follow up, and HCP profile lookup.
    """

    def __init__(self):
        self.graph = self._build_graph()
        self.tools = self._build_tools()

    def describe_role(self) -> str:
        return (
            "The LangGraph agent manages HCP interactions by extracting key details "
            "from conversational and form input, creating summarizations, and offering "
            "sales tools for logging, editing, follow-up guidance, and profile lookup."
        )

    def _build_graph(self):
        graph = StateGraph(InteractionState)
        graph.add_node('parse_interaction', self._parse_interaction_node)
        graph.add_node('summarize_interaction', self._summarize_interaction_node)
        graph.add_edge(START, 'parse_interaction')
        graph.add_edge('parse_interaction', 'summarize_interaction')
        return graph.compile()

    def _parse_interaction_node(self, state: InteractionState) -> dict:
        return {'extracted': extract_interaction_from_text(state['text'])}

    def _summarize_interaction_node(self, state: InteractionState) -> dict:
        extracted = state.get('extracted', {})
        return {
            'extracted': {
                **extracted,
                'summary': extracted.get('summary') or extracted.get('topics', ''),
            }
        }

    def _build_tools(self):
        return [
            {
                'name': 'Log Interaction',
                'description': 'Capture HCP interaction details from chat or form text.',
                'action': self.log_interaction_tool,
            },
            {
                'name': 'Edit Interaction',
                'description': 'Update an existing saved HCP interaction.',
                'action': self.edit_interaction_tool,
            },
            {
                'name': 'Summarize Interaction',
                'description': 'Create a compact interaction summary for field notes.',
                'action': self.summarize_interaction_tool,
            },
            {
                'name': 'Follow Up Suggestion',
                'description': 'Recommend the next sales action after an HCP visit.',
                'action': self.follow_up_tool,
            },
            {
                'name': 'Search HCP Profile',
                'description': 'Lookup HCP profile details and historical engagement.',
                'action': self.search_hcp_tool,
            },
        ]

    def parse_chat(self, text: str) -> dict:
        result = self.graph.invoke({'text': text})
        return result.get('extracted', {})

    def log_interaction_tool(self, text: str) -> dict:
        parsed = self.parse_chat(text)
        return {
            'tool': 'Log Interaction',
            'model': GROQ_MODEL,
            'data': parsed,
        }

    def edit_interaction_tool(self, interaction_id: int, updates: dict) -> dict:
        return {
            'tool': 'Edit Interaction',
            'interaction_id': interaction_id,
            'updates': updates,
        }

    def summarize_interaction_tool(self, text: str) -> dict:
        extracted = self.parse_chat(text)
        return {
            'tool': 'Summarize Interaction',
            'summary': extracted.get('summary', extracted.get('topics', '')),
        }

    def follow_up_tool(self, text: str) -> dict:
        return {
            'tool': 'Follow Up Suggestion',
            'suggestion': 'Recommend a follow-up call or sample delivery based on the interaction summary.',
            'context': text,
        }

    def search_hcp_tool(self, hcp_name: str) -> dict:
        return {
            'tool': 'Search HCP Profile',
            'hcp_name': hcp_name,
            'result': f'Lookup for {hcp_name} will return historical notes and sample status.',
        }

    def list_tools(self) -> list:
        return [
            {
                'name': tool['name'],
                'description': tool['description'],
            }
            for tool in self.tools
        ]

    def run_tool(self, tool_name: str, **kwargs) -> dict:
        tool_map = {tool['name'].lower(): tool['action'] for tool in self.tools}
        action = tool_map.get(tool_name.lower())
        if action is None:
            return {
                'tool': tool_name,
                'error': f'Unknown tool "{tool_name}". Available tools: {[t["name"] for t in self.tools]}',
            }
        return action(**kwargs)
