from typing import Dict, Any, Callable

from aws_lambda_powertools import Logger
from src.use_cases.llm.user.get_user_tool_use_case import get_user_tool_llm_use_case

logger = Logger("OpenAITools")


class OpenAITools:
    def __init__(self):
        # Map function names to actual methods
        self.strategies: Dict[str, Callable] = {
            "get_all_users": self.get_all_users,
        }

    def execute(self, f_name, context: Dict[str, Any] = None, **kwargs):
        # Dynamically call the function based on the strategy name
        if f_name in self.strategies:
            return self.strategies[f_name](context or {}, **kwargs)
        else:
            raise ValueError(f"Strategy '{f_name}' not found.")

    def get_all_users(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Get all users."""
        try:
            business_id = context.get("business_id")
            if not business_id:
                raise ValueError("Business ID is required")

            users = get_user_tool_llm_use_case(business_id)

            return {
                "success": True,
                "message": "Users retrieved successfully",
                "data": users,
            }
        except Exception as e:
            logger.error("Error getting all users: %s", e)
            return {"sucess": False, "message": "Error getting all users"}


if __name__ == "__main__":
    tools = OpenAITools()
    result = tools.execute("get_all_users")
    print(result)
