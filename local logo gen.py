import torch
from diffusers import StableDiffusionXLPipeline

# download form hugging face directly

lora_path = "./models/models--artificialguybr--LogoRedmond-LogoLoraForSDXL-V2/snapshots/8dd804b93747318e75063d49c29593d5deba736e" 
sdxl_path = "./models/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/462165984030d82259a11f4367a4eed129e94a7b"  

# Load SDXL Base 1.0
pipe = StableDiffusionXLPipeline.from_pretrained(sdxl_path, torch_dtype=torch.float16)
pipe.to("cuda")  # Move to GPU

# Load LoRA weights for logo design
pipe.load_lora_weights(lora_path, weight_name="LogoRedmondV2-Logo-LogoRedmAF.safetensors") #LogoRedmondV2-Logo-LogoRedmAF.safetensors
# Fuse LoRA into the model
pipe.fuse_lora(lora_scale=0.8)

# Generate a logo
prompt = "modern tiger logo"
image = pipe(prompt, num_inference_steps=25, guidance_scale=3.5).images[0]

# Save the generated logo
image.save("generated_logo.png")
