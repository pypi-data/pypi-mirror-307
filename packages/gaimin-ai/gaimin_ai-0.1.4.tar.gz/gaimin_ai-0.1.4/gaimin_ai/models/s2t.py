from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Optional, Union
import base64

class AudioFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    AAC = "aac"
    MP4 = "mp4"
    WEBM = "webm"


class S2TWhisperOptions(BaseModel):
    language: Optional[Annotated[str, Field(min_length=2, max_length=2)]] = Field(None, description="Language code for the audio, e.g., 'en'.")
    temperature: Optional[Annotated[float, Field(ge=0.0, le=1.0)]] = Field(0.7, description="Temperature for randomness in the model's output.")
    compression_ratio_threshold: Optional[float] = 2.4
    logprob_threshold: Optional[float] = -1
    no_speech_threshold: Optional[float] = 0.6
    condition_on_previous_text: Optional[bool] = True
    initial_prompt: Optional[str] = None
    prepend_punctuations: Optional[str] = Field(
        default=None, example="\"'“¿([{-", pattern=r'^[\"\'“¿\(\[\{\-]*$')
    append_punctuations: Optional[str] = Field(
        default=None, example="\"'.。,，!！?？:：”)]}、", pattern=r'^[\"\'.。,，!！?？:：”)}、]*$')
    clip_timestamps: Optional[Union[str, List[float]]] = "0"
    hallucination_silence_threshold: Optional[float] = None


class S2TWhisperRequest(BaseModel):
    input_file: Annotated[str, Field(min_length=1)] = Field(..., description="Base64-encoded string of the audio file to be transcribed.")
    input_format: AudioFormat = Field(..., description="Format of the audio file (e.g., 'wav', 'mp3', 'mp4').")
    model_size: Optional[Annotated[str, Field(pattern=r'^(tiny|base|small|medium|large)$')]] = Field(..., description="Size of the Whisper model to use.")
    options: Optional[S2TWhisperOptions] = Field(default_factory=S2TWhisperOptions, description="Optional parameters for the Whisper model.")

    class Config:
        protected_namespaces = ()

    def extract_options(self):
        return self.options.model_dump(exclude_unset=True) if self.options else {}

    @field_validator('input_file')
    def validate_base64(cls, v):
        try:
            # Validate base64 string
            base64.b64decode(v, validate=True)
        except Exception:
            raise ValueError('input_file must be a valid base64-encoded string')
        return v


class S2TWhisperResponse(BaseModel):
    created_at: datetime
    message: str
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }