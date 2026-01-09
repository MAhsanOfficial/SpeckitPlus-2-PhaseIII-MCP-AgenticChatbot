"""
AI Agent for Phase III Chatbot using Gemini 2.5 Flash.

This module implements the HabitChatAgent that:
- Processes user messages using Gemini 2.5 Flash
- Orchestrates MCP tool calls for habit operations
- Generates friendly, conversational responses
"""
import os
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import google.generativeai as genai

from src.mcp.tools.habits import get_habit_tools
from src.mcp.tools.base import BaseMCPTool

logger = logging.getLogger(__name__)

# System prompt for the habit tracking assistant
SYSTEM_PROMPT = """You are a friendly and helpful habit tracking assistant. Your role is to help users:
- Create and manage their habits
- Log daily habit completions
- Check their streak progress
- Get motivated to maintain their habits

Guidelines:
- Be warm, encouraging, and supportive
- Celebrate user achievements (streaks, completions)
- Provide brief, actionable responses
- When users complete habits, acknowledge their progress
- If users miss habits, be understanding and encouraging
- Always confirm actions you've taken (created habit, logged completion, etc.)

Available actions you can take:
- List all habits for the user
- Create new habits
- Log habit completions for specific dates
- Get streak information
- Get habit summaries and analytics

When users ask about their habits or want to track progress, use the appropriate tools.
When users want to create habits, use the habit_create tool.
When users say they completed a habit, use the habit_log_completion tool.
"""


@dataclass
class AgentResponse:
    """Response from the AI agent."""
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


class HabitChatAgent:
    """
    AI agent for habit tracking conversations using Gemini 2.5 Flash.
    
    This agent:
    - Processes natural language messages
    - Calls MCP tools for habit operations
    - Returns conversational responses
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agent with Gemini API key."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-preview-05-20",
            system_instruction=SYSTEM_PROMPT,
            tools=self._build_tools()
        )
        self.tools = {tool.name: tool for tool in get_habit_tools()}
    
    def _build_tools(self) -> List[genai.protos.Tool]:
        """Build Gemini function declarations from MCP tools."""
        function_declarations = []
        
        for tool in get_habit_tools():
            # Convert MCP tool schema to Gemini function declaration
            properties = {}
            required = []
            
            schema = tool.input_schema
            if "properties" in schema:
                for prop_name, prop_def in schema["properties"].items():
                    # Skip jwt_token as it's injected by the system
                    if prop_name == "jwt_token":
                        continue
                    
                    prop_type = prop_def.get("type", "string")
                    gemini_type = self._map_type(prop_type)
                    
                    properties[prop_name] = genai.protos.Schema(
                        type=gemini_type,
                        description=prop_def.get("description", "")
                    )
                
                # Get required fields (excluding jwt_token)
                required = [r for r in schema.get("required", []) if r != "jwt_token"]
            
            func_decl = genai.protos.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties=properties,
                    required=required
                ) if properties else None
            )
            function_declarations.append(func_decl)
        
        return [genai.protos.Tool(function_declarations=function_declarations)]
    
    def _map_type(self, json_type: str) -> genai.protos.Type:
        """Map JSON schema type to Gemini type."""
        type_map = {
            "string": genai.protos.Type.STRING,
            "number": genai.protos.Type.NUMBER,
            "integer": genai.protos.Type.INTEGER,
            "boolean": genai.protos.Type.BOOLEAN,
            "array": genai.protos.Type.ARRAY,
            "object": genai.protos.Type.OBJECT,
        }
        return type_map.get(json_type, genai.protos.Type.STRING)
    
    async def process_message(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        jwt_token: str
    ) -> AgentResponse:
        """
        Process a user message and return a response.
        
        Args:
            user_message: The user's message
            history: Previous conversation messages
            jwt_token: JWT token for authenticating MCP tool calls
            
        Returns:
            AgentResponse with content, tool calls, and suggestions
        """
        try:
            # Build conversation history for Gemini
            gemini_history = self._build_history(history)
            
            # Start chat with history
            chat = self.model.start_chat(history=gemini_history)
            
            # Send user message
            response = chat.send_message(user_message)
            
            # Process response and handle tool calls
            tool_calls = []
            tool_results = []
            final_response = response
            
            # Handle function calls if present
            while response.candidates[0].content.parts:
                has_function_call = False
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_call = True
                        func_call = part.function_call
                        tool_name = func_call.name
                        tool_args = dict(func_call.args) if func_call.args else {}
                        
                        logger.info(f"Tool call: {tool_name} with args: {tool_args}")
                        
                        # Record tool call
                        tool_calls.append({
                            "name": tool_name,
                            "arguments": tool_args
                        })
                        
                        # Execute the tool
                        result = await self._execute_tool(tool_name, tool_args, jwt_token)
                        tool_results.append({
                            "name": tool_name,
                            "result": result
                        })
                        
                        # Send tool result back to model
                        response = chat.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=tool_name,
                                        response={"result": result}
                                    )
                                )]
                            )
                        )
                        final_response = response
                
                if not has_function_call:
                    break
            
            # Extract text response
            content = ""
            for part in final_response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    content += part.text
            
            # Generate suggestions based on context
            suggestions = self._generate_suggestions(user_message, tool_calls)
            
            return AgentResponse(
                content=content or "I'm here to help with your habits! What would you like to do?",
                tool_calls=tool_calls if tool_calls else None,
                tool_results=tool_results if tool_results else None,
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return AgentResponse(
                content="I'm having trouble processing that right now. Please try again.",
                suggestions=["Show my habits", "Help"]
            )
    
    def _build_history(self, history: List[Dict[str, str]]) -> List[genai.protos.Content]:
        """Convert conversation history to Gemini format."""
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append(
                genai.protos.Content(
                    role=role,
                    parts=[genai.protos.Part(text=msg["content"])]
                )
            )
        return gemini_history
    
    async def _execute_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        jwt_token: str
    ) -> Dict[str, Any]:
        """Execute an MCP tool and return the result."""
        tool = self.tools.get(tool_name)
        if not tool:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            # Add JWT token to args for authentication
            args["jwt_token"] = jwt_token
            result = await tool.execute(**args)
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            return {"error": str(e)}
    
    def _generate_suggestions(
        self,
        user_message: str,
        tool_calls: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate follow-up suggestions based on context."""
        suggestions = []
        
        # Default suggestions
        default_suggestions = [
            "Show my habits",
            "What's my streak?",
            "Create a new habit"
        ]
        
        # Context-aware suggestions
        message_lower = user_message.lower()
        
        if any(tc["name"] == "habit_create" for tc in tool_calls):
            suggestions = [
                "Show my habits",
                "Log a completion",
                "Create another habit"
            ]
        elif any(tc["name"] == "habit_log_completion" for tc in tool_calls):
            suggestions = [
                "What's my streak?",
                "Show my habits",
                "Log another completion"
            ]
        elif any(tc["name"] == "habit_list" for tc in tool_calls):
            suggestions = [
                "What's my streak?",
                "Create a new habit",
                "Log a completion"
            ]
        elif any(tc["name"] == "habit_streak" for tc in tool_calls):
            suggestions = [
                "Show my habits",
                "Log a completion",
                "Get habit summary"
            ]
        elif "help" in message_lower:
            suggestions = [
                "Show my habits",
                "Create habit: Morning meditation",
                "What's my streak?"
            ]
        else:
            suggestions = default_suggestions
        
        return suggestions


def get_habit_agent() -> HabitChatAgent:
    """Factory function to create a HabitChatAgent instance."""
    return HabitChatAgent()
