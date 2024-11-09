from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Tuple, Union, Dict
from pydantic import BaseModel, Field


class ImageFormat(str, Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    gif = "gif"
    bmp = "bmp"
    tiff = "tiff"
    tif = "tif"
    ppm = "ppm"
    ico = "ico"
    pdf = "pdf"
    webp = "webp"


class T2IOptions(BaseModel):
    prompt_2: Optional[Union[str, List[str]]] = Field(None, description="The prompt or prompts to be sent to the tokenizer_2 and text_encoder_2.")
    height: Optional[int] = Field(1024, description="The height in pixels of the generated image.")
    width: Optional[int] = Field(1024, description="The width in pixels of the generated image.")
    num_inference_steps: Optional[int] = Field(50, description="The number of denoising steps.")
    timesteps: Optional[List[int]] = Field(None, description="Custom timesteps to use for the denoising process.")
    sigmas: Optional[List[float]] = Field(None, description="Custom sigmas to use for the denoising process.")
    denoising_end: Optional[float] = Field(None, description="Fraction of the denoising process to be completed before termination.")
    guidance_scale: Optional[float] = Field(5.0, description="Guidance scale as defined in Classifier-Free Diffusion Guidance.")
    negative_prompt: Optional[Union[str, List[str]]] = Field(None, description="The prompt or prompts not to guide the image generation.")
    negative_prompt_2: Optional[Union[str, List[str]]] = Field(None, description="The prompt or prompts not to guide the image generation to be sent to tokenizer_2 and text_encoder_2.")
    #num_images_per_prompt: Optional[int] = Field(1, description="The number of images to generate per prompt.")
    eta: Optional[float] = Field(0.0, description="Corresponds to parameter eta (η) in the DDIM paper.")
    #generator: Optional[Union[torch.Generator, List[torch.Generator]]] = Field(None, description="One or a list of torch generator(s) to make generation deterministic.")
    #latents: Optional[torch.Tensor] = Field(None, description="Pre-generated noisy latents, sampled from a Gaussian distribution.")
    #prompt_embeds: Optional[torch.Tensor] = Field(None, description="Pre-generated text embeddings.")
    #negative_prompt_embeds: Optional[torch.Tensor] = Field(None, description="Pre-generated negative text embeddings.")
    # pooled_prompt_embeds: Optional[torch.Tensor] = Field(None, description="Pre-generated pooled text embeddings.")
    #negative_pooled_prompt_embeds: Optional[torch.Tensor] = Field(None, description="Pre-generated negative pooled text embeddings.")
    ip_adapter_image: Optional[str] = Field(None, description="Optional image input to work with IP Adapters.")
    #ip_adapter_image_embeds: Optional[List[torch.Tensor]] = Field(None, description="Pre-generated image embeddings for IP-Adapter.")
    #output_type: Optional[str] = Field("pil", description="The output format of the generated image.")
    return_dict: Optional[bool] = Field(True, description="Whether or not to return a dictionary instead of a plain tuple.")
    cross_attention_kwargs: Optional[Dict] = Field(None, description="A kwargs dictionary for the AttentionProcessor.")
    guidance_rescale: Optional[float] = Field(0.0, description="Guidance rescale factor.")
    original_size: Optional[Tuple[int, int]] = Field((1024, 1024), description="Original size of the image.")
    crops_coords_top_left: Optional[Tuple[int, int]] = Field((0, 0), description="Crop coordinates for generating the image.")
    target_size: Optional[Tuple[int, int]] = Field((1024, 1024), description="Target size of the generated image.")
    negative_original_size: Optional[Tuple[int, int]] = Field((1024, 1024), description="Negative condition for original image size.")
    negative_crops_coords_top_left: Optional[Tuple[int, int]] = Field((0, 0), description="Negative condition for crop coordinates.")
    negative_target_size: Optional[Tuple[int, int]] = Field((1024, 1024), description="Negative condition for target image size.")


class T2IRequest(BaseModel):
    prompt: str = Field(None, description="The prompt to guide the image generation.")
    output_type: ImageFormat = Field(ImageFormat.png, description="The output format of the generated image.")
    options: T2IOptions = T2IOptions()

    def extract_options(self):
        return self.options.model_dump(exclude_unset=True) if self.options else {}


class T2IResponse(BaseModel):
    created_at: datetime
    response_file: Annotated[str, Field(min_length=1)] = Field(..., description="Base64-encoded string of the image file to be transcribed.")
    response_file_format: Optional[str]
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
