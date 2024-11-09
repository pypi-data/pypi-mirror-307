# <span style="color:#EE4C2C">TorchRender3D </span>


<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/logo.png" alt= “PackageLogo” width=15% height=15%>


**<span style="color:#EE4C2C">TorchRender3D</span>** is a visualization tool for neural networks, utilizing VTK (Visualization Toolkit) for 3D rendering. This tool enables users to visually inspect and analyze the internal structure of neural networks in real-time.

## Features

- Visualize neural network parameters in a 3D space.
- Interactive rendering with support for keyboard and mouse events.
- Capture and save rendered frames as TIFF images for animation purposes.
- Support for different neural network architectures.
- Easy-to-use interface for integrating with existing PyTorch models.

Below is a simple render example of the learnable parameter space of a simple CNN:

<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/3d_animate.gif" alt= “feature_example” width=30% height=30%>

## Installation

- Clone from gitlab repo as

```bash
git clone https://gitlab.com/ml-ppa-derivatives/torchrender3d.git
```

- Create a virtual environment (recomended but can be skipped) as and activate it

```bash
python -m venv <venv_name>
```

```bash
source <venv_name>/bin/activate
```

- Install using pip from local as 

```bash
pip install -e .
```

## Implementation

- Define or import your own neural network developed using pytorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchrender3d import PlotNetwork3D

#: Define a simple neural net or import your own model
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()        
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1) 
        self.flatten_method = nn.Flatten()       
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):        
        x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14 after pool
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7 after pool       
        x = self.flatten_method(x)
        x = F.relu(self.fc1(x))               # Fully connected layer
        x = self.fc2(x)                       # Output layer
        return x

stored_network_params_path = 'path_to_trained_model'
torch.save(model.state_dict(), stored_network_params_path)
```

- Instantiate the model and the model plotter

```python
model = SimpleCNN()    
stored_network_params_path = './example_nets/simplecnn'
torch.save(model.state_dict(), stored_network_params_path)

model_plotter = PlotNetwork3D(
                              neural_network=model,
                              stored_network_params_path=stored_network_params_path, #: can be a random string, but required a valid path for updating feature
                              normalize=False,
                              plot_type='param', # if 'output' then plots the output of each steps in the forward method; elif 'param' then shows the learnable parameters
                              )

```
- Call model plotter to show the plot in 3D

```python
model_plotter()
```
<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/simple_cnn_param.gif" alt= “cnn_output” width=30% height=30%>
</div>

- Visualize network parameter evolution during training
```python
#: call it with the 'update_with_timer' parameter and 'timer_interval' (if True) else can be updating by clicking 'u'
model_plotter(update_with_timer = True,timer_interval: int = 5000) 
```

- The plots during each update can be stored as tiff file format, later to visualize as an animation
```python
#: if make_animation==True, then instantiate the model_plotter with 'output_anim_folder' set to a valid path
model_plotter(update_with_timer = True,timer_interval: int = 5000,make_animation=True) 
```

- Same strategy can be used also to visualize the outputs from each steps of the forward method of the neural net by instatiating the model_plotter with the parameter plot_type='output'. An example is shown below

<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/cnn_output.gif" alt= “cnn_output” width=30% height=30%>
</div>

## Requirements

- Python 3.x
- VTK
- NumPy
- PyTorch

## Authors and acknowledgment
**Authors**: Tanumoy Saha   
**Acknowledgment**: We would like to acknowledge PUNCH4NFDI and InterTwin consortium for the funding and the members of TA5 for their valuable support 

## Project 
Initial stage of development (Version: 0.1). 
