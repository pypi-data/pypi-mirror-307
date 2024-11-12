import torch
import coremltools as ct
import open_clip


# Define a wrapper to handle the forward pass and any output adjustments
class VisionModelWrapper(torch.nn.Module):
    def __init__(self, vision_model):
        super(VisionModelWrapper, self).__init__()
        self.vision_model = vision_model

        # Assuming the encode_image method returns a 512-dimensional vector
        self.output_layer = torch.nn.Linear(512, 512)  # Adjust to your target dimension if necessary

    def forward(self, input_image):
        vision_outputs = self.vision_model.encode_image(input_image)
        return self.output_layer(vision_outputs)

def init_config(config):
    '''set default config values if config has null value'''
    defaults = {
        'package_path': '',
    }

    return {key: config.get(key, default) for key, default in defaults.items()}

def main(config):
    config = init_config(config)
    # Load and wrap the MobileCLIP model
    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('ViT-B-32')
    wrapped_vision_model = VisionModelWrapper(model)

    # Set the model to evaluation mode
    wrapped_vision_model.eval()

    # Dummy input for tracing in the correct format (3, 224, 224)
    dummy_input = torch.ones((1, 3, 224, 224))

    # Trace the model
    traced_model = torch.jit.trace(wrapped_vision_model, dummy_input)

    # Convert to Core ML format
    mlmodel = ct.convert(
        traced_model,
        inputs=[ct.ImageType(shape=(1, 3, 224, 224), scale=1/255.0, bias=[0, 0, 0])],
    )

    # Save the model as an mlpackage
    mlmodel.save(config['package_path'])

if __name__ == '__main__':
    pass
