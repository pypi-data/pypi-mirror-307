from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import uuid

from pydantic import BaseModel, Field, model_validator


class T2TOptions(BaseModel):
    num_keep: Optional[int] = None
    seed: Optional[int] = None
    num_predict: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    min_p: Optional[float] = None
    tfs_z: Optional[float] = None
    typical_p: Optional[float] = None
    repeat_last_n: Optional[int] = None
    temperature: Optional[float] = None
    repeat_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    mirostat: Optional[int] = None
    mirostat_tau: Optional[float] = None
    mirostat_eta: Optional[float] = None
    penalize_newline: Optional[bool] = None
    stop: Optional[List[str]] = None
    numa: Optional[bool] = None
    num_ctx: Optional[int] = None
    num_batch: Optional[int] = None
    num_gpu: Optional[int] = None
    main_gpu: Optional[int] = None
    low_vram: Optional[bool] = None
    f16_kv: Optional[bool] = None
    vocab_only: Optional[bool] = None
    use_mmap: Optional[bool] = None
    use_mlock: Optional[bool] = None
    num_thread: Optional[int] = None


class T2TGenerateRequest(BaseModel):
    model: str
    prompt: Optional[str] = None
    suffix: Optional[str] = None
    images: Optional[List[str]] = None
    format: Optional[str] = Field(None, pattern="^json$")
    options: Optional[T2TOptions] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[str] = None
    stream: Optional[bool] = False
    raw: Optional[bool] = None
    keep_alive: Optional[Union[str, int]] = "300m"
    id: uuid.UUID = Field(default_factory=uuid.uuid4) 


class T2TGenerateResponse(BaseModel):
    model: str
    created_at: datetime
    response: str
    done: bool
    done_reason: Optional[str] = None
    context: Optional[List[int]] = None  # Assuming context is a list of integers
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class T2TEmbeddingRequest(BaseModel):
    model: str = Field(..., description="Name of the model to generate embeddings from")
    input: Optional[Union[str, List[str]]] = Field(None, description="Text or list of text to generate embeddings for")
    prompt: Optional[Union[str, List[str]]] = Field(None, description="Prompt or list of prompts to generate embeddings for")
       
    truncate: bool = Field(True, description="Truncates the end of each input to fit within context length. Returns error if false and context length is exceeded.")
    options: Optional[T2TOptions] = Field(None, description="Additional model parameters listed in the documentation for the Modelfile such as temperature")
    keep_alive: Optional[str] = Field("1m", description="Controls how long the model will stay loaded into memory following the request")
    
    @model_validator(mode="before")
    def check_input_or_prompt(cls, values):
        input_val = values.get('input')
        prompt_val = values.get('prompt')
        if input_val is None and prompt_val is None:
            raise ValueError('Either "input" or "prompt" must be provided.')
        if input_val is not None and prompt_val is not None:
            raise ValueError('Only one of "input" or "prompt" can be provided.')
        return values


class T2TEmbeddingResponse(BaseModel):
    embedding: List[float]


class T2TToolParameters(BaseModel):
    location: str
    format: str


class T2TToolFunction(BaseModel):
    name: str
    description: str
    parameters: T2TToolParameters


class T2TTool(BaseModel):
    type: str
    function: T2TToolFunction


class T2TMessage(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None  # Assuming base64-encoded images
    tool_calls: Optional[List[T2TTool]] = None


class T2TChatRequest(BaseModel):
    model: str
    messages: List[T2TMessage]
    tools: Optional[List[T2TTool]] = None
    format: Optional[str] = Field(None, pattern="^json$")
    options: Optional[T2TOptions] = None
    stream: Optional[bool] = False
    keep_alive: Optional[str] = "5m"


class T2TToolCall(BaseModel):
    function: T2TToolFunction
    arguments: T2TToolParameters


class T2TChatResponseMessage(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None  # Assuming base64-encoded images
    tool_calls: Optional[List[T2TToolCall]] = None


class T2TChatResponse(BaseModel):
    model: str
    created_at: datetime
    message: T2TChatResponseMessage
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None    


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class T2TPullModelRequest(BaseModel):
    name: str
    stream: Optional[bool] = False


class T2TPullModelResponse(BaseModel):
    status: str
    digest: Optional[str] = None
    total: Optional[int] = None
    completed: Optional[int] = None


class T2TShowModelInformationRequest(BaseModel):
    name: str
    verbose: Optional[bool] = False


class T2TShowModelInformationResponse(BaseModel):
    license: str
    modelfile: str
    parameters: str
    template: str
    details: Dict[str, Any]
    model_info: Dict[str, Any]
    modified_at: str

    class Config:
        protected_namespaces = ()


class T2TModelDetails(BaseModel):
    parent_model: Optional[str] = None
    format: Optional[str] = None
    family: Optional[str] = None
    families: Optional[List[str]] = None
    parameter_size: Optional[str] = None
    quantization_level: Optional[str] = None


class T2TLocalModel(BaseModel):
    name: str
    model: str
    modified_at: Optional[str] = None
    size: int
    digest: str
    details: Optional[T2TModelDetails] = None
    expires_at: Optional[str] = None
    size_vram: Optional[int] = None


class T2TListModelsResponse(BaseModel):
    models: List[T2TLocalModel]
