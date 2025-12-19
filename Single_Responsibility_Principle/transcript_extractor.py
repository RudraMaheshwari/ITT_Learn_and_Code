from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from src.services.llm_service import llm_model_provider
from src.utils.logger import logger

class TranscriptSchema(BaseModel):
    business_intent: Optional[str] = Field(None)
    purchase_intent: Optional[str] = Field(None)
    conversation_stage: Optional[str] = Field(None)
    objection_types: List[str] = Field(default_factory=list)
    email: Optional[str] = Field(None)
    email_consent: Optional[bool] = None
    email_verified: Optional[bool] = None
    reschedule: Optional[bool] = None
    name: Optional[str] = None
    name_verified: Optional[bool] = None
    conversation_summary: Optional[str] = None

class TranscriptExtractor:
    def extract_conversation_state(self, transcript: List[Dict]) -> Dict[str, Any]:
        try:
            transcript_text = self._format_transcript(transcript)
            extracted = self._extract_with_llm(transcript_text)
            return extracted if extracted else {}
        except Exception:
            return {}

    def _format_transcript(self, messages: List[Dict]) -> str:
        formatted = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            formatted.append(f"{role.upper()}: {content}")
        return "\n".join(formatted)

    def _extract_with_llm(self, transcript: str) -> Dict:
        prompt = f"""Extract the following information from this sales conversation transcript:

            REQUIRED FIELDS:
                - business_intent: one of [growth, sale, succession, unclear] or null
                - purchase_intent: one of [ready_to_nurture, not_ready_to_buy] or null
                - conversation_stage: one of [initial_rapport, business_discovery, sbr_pitch, objection_handling, nurture, purchase, conversation_closing] or null
                - objection_types: list of [price, timing, value, other]
                - email: extract if mentioned, but only save if email_verified is true
                - email_consent: boolean - did user consent to receive emails?
                - email_verified: boolean - did user confirm/verify their email?
                - reschedule: boolean - did user request to reschedule?
                - name: extract if mentioned in conversation
                - name_verified: boolean - did user confirm their name?
                - conversation_summary: 2–3 sentences summarizing the conversation

            TRANSCRIPT:
            {transcript}

            Return only valid JSON with these fields.
        """

        llm = llm_model_provider.model.with_structured_output(TranscriptSchema)
        messages = [
            SystemMessage(content="Extract structured fields from the transcript."),
            HumanMessage(content=prompt)
        ]

        try:
            result = llm.invoke(messages)
            data = result.dict() if hasattr(result, "dict") else result
            return data
        except Exception as e:
            logger.error(f"Structured output extraction failed: {e}")
            return {}
