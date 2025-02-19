from huggingface_hub import InferenceClient

client = InferenceClient(
"black-forest-labs/FLUX.1-schnell",
token="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",
)

image = client.text_to_image(prompt="create a background type image displaying computer on which lady is working and searhing the product. make it suitable for e-commerece site for background image for search section. making its width 50% higher than heigth size can be 100vw and 30vh")
image.save("product-search.png")
