# import torch
# from diffusers import FluxPipeline

# pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
# pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

prompt = "A cat holding a macbook showing i am a cat"
# image = pipe(
#     prompt,
#     guidance_scale=0.0,
#     num_inference_steps=4,
#     max_sequence_length=256,
#     generator=torch.Generator("cpu").manual_seed(0)
# ).images[0]
# # image.save("flux-schnell.png")

from huggingface_hub import InferenceClient

client = InferenceClient(
"black-forest-labs/FLUX.1-schnell",
token="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",
)

image = client.text_to_image(prompt=prompt)
image.save("old-man.png")
