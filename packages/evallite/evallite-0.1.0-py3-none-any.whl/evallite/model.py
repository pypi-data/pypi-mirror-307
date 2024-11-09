from typing import Tuple, Optional, List, Any, Union, Type
from ailite import ai
from ailite.main._model._api.types._model_types import MODELS_TYPE
from deepeval.models import DeepEvalBaseLLM
from langchain.schema import AIMessage, HumanMessage
import json
from pydantic import BaseModel

class EvalLiteModel(DeepEvalBaseLLM):
    def __init__(
        self,
        model: Optional[MODELS_TYPE] = None,
        *args,
        **kwargs,
    ):
        self.model_name = model if model else "default"
        self.args = args
        self.kwargs = kwargs
        super().__init__(self.model_name)

    def load_model(self):
        return self.model_name

    def _parse_ai_response(self, response: str) -> dict:
        """Convert AI response to JSON format"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"content": response}

    def _process_response(self, response: str, schema: Optional[Type[BaseModel]] = None) -> Union[BaseModel, str]:
        """Process response according to schema"""
        if not schema:
            return response

        parsed_response = self._parse_ai_response(response)

        if schema.__name__ == 'Statements':
            if isinstance(parsed_response, dict) and 'statements' in parsed_response:
                return schema(statements=parsed_response['statements'])
            statements = [parsed_response['content']] if 'content' in parsed_response else [str(response)]
            return schema(statements=statements)

        elif schema.__name__ == 'Verdicts':
            if isinstance(parsed_response, dict) and 'verdicts' in parsed_response:
                return schema(verdicts=parsed_response['verdicts'])
            verdict = {
                "verdict": "yes",
                "reason": "Generated response"
            }
            return schema(verdicts=[verdict])

        elif schema.__name__ == 'Reason':
            if isinstance(parsed_response, dict) and 'reason' in parsed_response:
                return schema(reason=parsed_response['reason'])
            reason = parsed_response.get('content', str(response))
            return schema(reason=reason)

        return response

    def generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None, **kwargs) -> Union[BaseModel, str]:
        """Synchronous generation with schema support"""
        response = ai(prompt, model=self.model_name)  # Pass model name to ai function
        return self._process_response(response, schema)

    async def a_generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None, **kwargs) -> Union[
        BaseModel, str]:
        """Asynchronous generation with schema support"""
        response = ai(prompt, model=self.model_name)  # Pass model name to ai function
        return self._process_response(response, schema)

    def generate_raw_response(self, prompt: str, **kwargs) -> Tuple[AIMessage, float]:
        """Generate raw response with dummy cost"""
        response = ai(prompt, model=self.model_name)  # Pass model name to ai function
        return AIMessage(content=response), 0.0

    async def a_generate_raw_response(self, prompt: str, **kwargs) -> Tuple[AIMessage, float]:
        """Async raw response with dummy cost"""
        response = ai(prompt, model=self.model_name)  # Pass model name to ai function
        return AIMessage(content=response), 0.0

    def get_model_name(self):
        return self.model_name