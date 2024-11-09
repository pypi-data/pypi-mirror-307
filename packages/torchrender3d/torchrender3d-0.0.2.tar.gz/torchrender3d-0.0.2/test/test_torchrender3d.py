import pytest
import torch
#import torchvision.models as models
#import src  # Replace with the actual module import if different
#from torchrender3d import PlotNetwork3D

def test_if_import_works():
     """Test if torchrender3d can be imported."""
     try:
         from torchrender3d import PlotNetwork3D         
         assert True
     except(ImportError):
         assert False

def main_code():
    import numpy as np
    import torch.nn as nn
    import torch.nn.functional as F
    from torchrender3d import PlotNetwork3D,LayerInfo
    #from ..example_nets.neural_network_models import SimpleCNN
    from torchvision import datasets, transforms 

    class SimpleCNN(nn.Module):
        def __init__(self):
            super(SimpleCNN, self).__init__()  
            
            self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
            self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)        
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):        
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))        
            x = x.view(-1, 64 * 7 * 7)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,)),  # Normalize grayscale images
        ]
    )
    test_dataset = datasets.MNIST(
        root="./data", train=False, download=True, transform=transform
    )
    test_data = np.array([test_dataset[i][0] for i in range(100)])

    network = SimpleCNN()
    info = LayerInfo.extract_forward_steps(network=network)
    [print(x) for x in info.items()]

    stored_network_params_path = "./example_nets/simplecnn.pth"
    network.load_state_dict(
        torch.load(
            stored_network_params_path, map_location=torch.device("cpu"), weights_only=True
        )
    )
    
    nn_plotter_engine = PlotNetwork3D(
        neural_network=network,
        stored_network_params_path=stored_network_params_path,
        normalize=False,
        plot_type="output",
        test_data=test_data,
        make_animation=False,
    )
    nn_plotter_engine(update_with_timer=None, timer_interval=1000,make_animation=None,close_automatically_window=True)    
    return True

def test_if_main_works():
    assert main_code() 
    
def main_code_for_gitlab():
    import numpy as np
    import torch.nn as nn
    import torch.nn.functional as F
    from torchrender3d import PlotNetwork3D,LayerInfo, PlotBuilderNN
    #from ..example_nets.neural_network_models import SimpleCNN
    from torchvision import datasets, transforms 

    class SimpleCNN(nn.Module):
        def __init__(self):
            super(SimpleCNN, self).__init__()  
            
            self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
            self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)        
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):        
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))        
            x = x.view(-1, 64 * 7 * 7)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,)),  # Normalize grayscale images
        ]
    )
    test_dataset = datasets.MNIST(
        root="./data", train=False, download=True, transform=transform
    )
    test_data = np.array([test_dataset[i][0] for i in range(100)])

    network = SimpleCNN()
    info = LayerInfo.extract_forward_steps(network=network)
    [print(x) for x in info.items()]

    stored_network_params_path = "./example_nets/simplecnn.pth"
    network.load_state_dict(
        torch.load(
            stored_network_params_path, map_location=torch.device("cpu"), weights_only=True
        )
    )
    if isinstance( test_data,(np.ndarray,list,torch.Tensor)):
            if isinstance(test_data,(np.ndarray,list)):
                test_data = torch.tensor(test_data,requires_grad=False)
                #test_data = test_data.unsqueeze(0)
                test_data = test_data
    else:
            input_image_dim=(1, 126, 126)
            test_data = torch.rand(input_image_dim)
    plot_builder = PlotBuilderNN(
            neural_network=network,
            input_image_dim=(1, 126, 126),
            network_param_path=stored_network_params_path,
            normalize=False,
            plot_type="output",
            test_data=test_data,
        )
    plot_builder()
     
    return True



def test_if_main_works_for_gitlab():
    assert main_code_for_gitlab() 
