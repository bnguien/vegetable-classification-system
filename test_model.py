import tensorflow as tf

model_path = "models/final_resnet50_model.keras"
model = tf.keras.models.load_model(model_path)
print("Layers in the model:")
for idx, layer in enumerate(model.layers[:10]):
    print(f"Layer {idx}: name={layer.name}, class={layer.__class__.__name__}")
    if hasattr(layer, 'layers'):
        print(f"  Inner layers count: {len(layer.layers)}")
        for j, inner_layer in enumerate(layer.layers[:5]):
            print(f"    Inner layer {j}: name={inner_layer.name}, class={inner_layer.__class__.__name__}")
