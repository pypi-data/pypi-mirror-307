from typing import Tuple, Optional, List, Any, Union, Type
from ailite import ai
from ailite.main._model._api.types._model_types import MODELS_TYPE
from deepeval.models import DeepEvalBaseLLM
import json
from pydantic import BaseModel



class Steps(BaseModel):
    steps: List[str]


class ReasonScore(BaseModel):
    reason: str
    score: int


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
        self.evaluation_cost = 0  # Initialize evaluation cost
        super().__init__(self.model_name)

    def load_model(self):
        return self.model_name

    def _parse_ai_response(self, response: str) -> dict:
        """Convert AI response to JSON format with better error handling"""
        try:
            # Remove markdown code block if present
            response = response.replace('```json', '').replace('```', '').strip()
            return json.loads(response)
        except json.JSONDecodeError:
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return self._create_structured_response(response)
            except:
                return self._create_structured_response(response)

    def _create_structured_response(self, response: str) -> dict:
        """Create structured response based on content type"""
        lines = [line.strip() for line in response.split('\n') if line.strip()]

        # Try to identify steps format
        if any(line.startswith(str(i) + '.') for i in range(1, 10) for line in lines):
            steps = [line for line in lines if any(line.startswith(str(i) + '.') for i in range(1, 10))]
            return {"steps": steps}

        # Try to identify score/reason format
        import re
        score_match = re.search(r'\b([0-9]|10)\b', response)
        if score_match:
            score = int(score_match.group())
            reason = response.replace(score_match.group(), '').strip()
            return {"score": score, "reason": reason}

        return {"content": response}

    def _process_response(self, response: str, schema: Optional[Type[BaseModel]] = None) -> Union[BaseModel, str]:
        """Process response according to schema with improved handling"""
        if not schema:
            return response

        parsed_response = self._parse_ai_response(response)

        if schema.__name__ == 'Steps':
            if isinstance(parsed_response, dict) and 'steps' in parsed_response:
                return Steps(steps=parsed_response['steps'])
            return Steps(steps=[str(response)])

        elif schema.__name__ == 'ReasonScore':
            if isinstance(parsed_response, dict) and 'score' in parsed_response and 'reason' in parsed_response:
                return ReasonScore(score=parsed_response['score'], reason=parsed_response['reason'])
            # Handle non-standard response format
            score = parsed_response.get('score', 5)
            reason = parsed_response.get('reason', str(response))
            return ReasonScore(score=score, reason=reason)

        return response

    def generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None, **kwargs) -> Union[BaseModel, str]:
        """Synchronous generation with schema support"""
        response = ai(prompt, model=self.model_name)
        processed_response = self._process_response(response, schema)
        return processed_response

    async def a_generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None, **kwargs) -> Union[
        BaseModel, str]:
        """Asynchronous generation"""
        response = ai(prompt, model=self.model_name)
        processed_response = self._process_response(response, schema)
        return processed_response

    def get_model_name(self):
        return self.model_name