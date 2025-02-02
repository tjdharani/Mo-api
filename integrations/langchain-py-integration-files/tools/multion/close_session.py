from typing import TYPE_CHECKING, Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools.base import BaseTool
import asyncio

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    import multion
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        import multion
    except ImportError:
        pass


class CloseSessionSchema(BaseModel):
    """Input for UpdateSessionTool."""

    tabId: str = Field(
        ..., description="The tabID, received from one of the createSessions or updateSessions run before"
    )
   


class MultionCloseSession(BaseTool):
    """Tool that closes an existing Multion Browser Window with provided fields.

    Attributes:
        name: The name of the tool. Default: "close_multion_session"
        description: The description of the tool.
        args_schema: The schema for the tool's arguments. Default: UpdateSessionSchema
    """

    name: str = "close_multion_session"
    description: str = """Use this tool to close \
an existing corresponding Multion Browser Window with provided fields. \
Note: TabId must be received from previous Browser window creation."""
    args_schema: Type[CloseSessionSchema] = CloseSessionSchema
    tabId: str = ""

    def _run(
        self,
        tabId: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        try:
            try:
                response = multion.close_session(tabId)
            except Exception as e:
                print(f"{e}, retrying...")
                return {"error": f"{e}", "Response": "retrying..."}
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    async def _arun(
        self,
        tabId: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._run, tabId)

        return result
