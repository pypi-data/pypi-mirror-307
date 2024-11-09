#import time
import numpy as np
import torch
import torch.fx as fx
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
#import vtk
#from IPython.display import display

# import matplotlib.pyplot as plt
#from copy import copy, deepcopy
#from tqdm import tqdm
from typing import Callable

class LayerInfo:
    @staticmethod
    def normalize_mat(mat: np.ndarray|torch.Tensor, rng: tuple = (-1, 1)):
        mat = mat - np.min(mat.flatten())
        if np.max(mat.flatten()) != 0:
            mat = mat / np.max(mat.flatten())
            mat = mat * (rng[1] - rng[0]) - (rng[1] - rng[0]) / 2
        return mat

    @staticmethod
    def extract_cnn_params(
        layer: nn.Conv1d | nn.Conv2d | nn.ConvTranspose1d | nn.ConvTranspose2d,
        normalize: bool = True,
    ):
        if isinstance(layer, nn.Conv2d) or isinstance(layer, nn.ConvTranspose2d):
            num_kernels = layer.out_channels
            depth = layer.in_channels
            height = layer.kernel_size[0]
            width = height
            weight = layer.weight.detach().numpy()
            if layer.bias != None:
                bias = layer.bias.detach().numpy()
            else:
                bias = None
        elif isinstance(layer, nn.Conv1d) or isinstance(layer, nn.ConvTranspose1d):
            num_kernels = layer.out_channels
            depth = layer.in_channels
            height = 1
            width = layer.kernel_size[0]
            weight = layer.weight.detach().numpy()
            weight = np.expand_dims(weight, axis=2)
            if layer.bias != None:
                bias = layer.bias.detach().numpy()
            else:
                bias = None
        else:
            print(f"layer type {type(layer)} is not a cnn in 1 and 2d")
            raise ValueError

        # max_weight = np.max(weight.flatten())
        # min_weight = np.min(weight.flatten())

        # weight = weight - min_weight
        # weight = weight/np.max(weight.flatten())*2
        # weight = weight-1
        if normalize:
            weight = LayerInfo.normalize_mat(mat=weight)
            if layer.bias != None:
                bias = LayerInfo.normalize_mat(mat=bias)

        return num_kernels, depth, height, width, weight, bias

    @staticmethod
    def calculate_cnn_layer_output(
        layer: nn.Conv1d | nn.Conv2d | nn.ConvTranspose1d | nn.ConvTranspose2d,
        input_mat: torch.Tensor,
        normalize: bool = True,
    ):
        #: input image dimension should be in format: btch x channels x height x width
        #print(f'Debug400 normalize set to {normalize}')
        if isinstance(input_mat, torch.Tensor) and (
            isinstance(layer, (nn.Conv2d, nn.ConvTranspose2d))
        ):
            #print(f'debug403 input_mat_shape {input_mat.shape}')
            # if len(input_mat.shape)==2:
            #     input_mat.squeeze()
            output = layer(input_mat).detach().numpy()
            #print(f'Debug407 normalize set to {normalize}')
            if normalize==True:
                #print()
                output = LayerInfo.normalize_mat(mat=output)
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            num_outputs = output.shape[1]
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        elif isinstance(input_mat, torch.Tensor) and (
            isinstance(layer, (nn.Conv1d, nn.ConvTranspose1d))
        ):
            output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            # reshaped_array = output.reshape(1, 10, 1, 128)
            output = output.reshape(1, output.shape[2], 1, output.shape[3])
            num_outputs = output.shape[1]
            # print(output.shape)
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        else:
            print("input is not a tensor or layer is not a cnn")
            raise ValueError
        return feature_maps

    @staticmethod
    def extract_bn_params(
        layer: nn.BatchNorm1d | nn.BatchNorm2d, normalize: bool = True
    ):
        if isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
            weight = layer.weight.detach().numpy()
            bias = layer.bias.detach().numpy()
        else:
            print(f"layer type {type(layer)} is not a batchnorm in 1 and 2d")
            raise ValueError
        if normalize:
            weight = LayerInfo.normalize_mat(mat=weight)
            bias = LayerInfo.normalize_mat(mat=bias)
        return weight, bias

    @staticmethod
    def extract_linear_params(layer: nn.Linear, normalize: bool = True):
        if isinstance(layer, nn.Linear):
            in_neurons = layer.in_features
            out_neurons = layer.out_features
            weight = layer.weight.detach().numpy()
            bias = layer.bias.detach().numpy()
        else:
            print(f"layer type {type(layer)} is not a linear")
            raise ValueError
        if normalize:
            weight = LayerInfo.normalize_mat(mat=weight)
            bias = LayerInfo.normalize_mat(mat=bias)
        return in_neurons, out_neurons, weight, bias

    @staticmethod
    def calculate_activation_layer_output(
        layer: (
            nn.ReLU
            | nn.LeakyReLU
            | nn.Sigmoid
            | nn.Tanh
            | nn.Softmax
            | nn.ELU
            | nn.SELU
            | nn.GELU
        ),
        input_mat: torch.Tensor,
        normalize: bool = True,
        output:torch.Tensor=None
    ):
        if isinstance(
            layer,
            (
                nn.ReLU,
                nn.LeakyReLU,
                nn.Sigmoid,
                nn.Tanh,
                nn.Softmax,
                nn.ELU,
                nn.SELU,
                nn.GELU,
            ),
        ):
            if output==None:
                output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            num_outputs = output.shape[1]
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        else:
            print("input is not a tensor or layer is not a cnn")
            raise ValueError
        return feature_maps

    @staticmethod
    def calculate_pool_layer_output(
        layer: nn.MaxPool1d | nn.MaxPool2d,
        input_mat: torch.Tensor,
        normalize: bool = True,
        output:torch.Tensor=None
    ):
        if isinstance(layer, (nn.MaxPool1d, nn.MaxPool2d)):
            if output==None:
                output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            num_outputs = output.shape[1]
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        else:
            print("input is not a tensor or layer is not a cnn")
            raise ValueError
        return feature_maps

    @staticmethod
    def calculate_bn_layer_output(
        layer: nn.BatchNorm1d | nn.BatchNorm2d,
        input_mat: torch.Tensor,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        if isinstance(layer, (nn.BatchNorm1d, nn.BatchNorm2d)):
            if output==None:
                output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            num_outputs = output.shape[1]
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        else:
            print("input is not a tensor or layer is not a cnn")
            raise ValueError
        return feature_maps

    @staticmethod
    def calculate_layer_output_non_linear(
        layer: (
            nn.BatchNorm1d
            | nn.BatchNorm2d
            | nn.MaxPool1d
            | nn.MaxPool2d
            | nn.ReLU
            | nn.LeakyReLU
            | nn.Sigmoid
            | nn.Tanh
            | nn.Softmax
            | nn.ELU
            | nn.SELU
            | nn.GELU
            | nn.Conv1d
            | nn.Conv2d
            | nn.ConvTranspose1d
            | nn.ConvTranspose2d
        ),
        input_mat: torch.Tensor,
        normalize: bool = True,
        output:torch.Tensor=None
    ):
        if isinstance(
            layer,
            (
                nn.BatchNorm1d,
                nn.BatchNorm2d,
                nn.MaxPool1d,
                nn.MaxPool2d,
                nn.ReLU,
                nn.LeakyReLU,
                nn.Sigmoid,
                nn.Tanh,
                nn.Softmax,
                nn.ELU,
                nn.SELU,
                nn.GELU,
                nn.Conv2d,
                nn.ConvTranspose2d,
            ),
        ):
            if output==None:
                output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            num_outputs = output.shape[1]
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        elif isinstance(input_mat, torch.Tensor) and (
            isinstance(layer, (nn.Conv1d, nn.ConvTranspose1d))
        ):
            output = layer(input_mat).detach().numpy()
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
            # reshaped_array = output.reshape(1, 10, 1, 128)
            output = output.reshape(1, output.shape[2], 1, output.shape[3])
            num_outputs = output.shape[1]
            # print(output.shape)
            feature_maps = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        else:
            print("input is not a tensor or layer is not non linear or a callable")
            raise ValueError
        return feature_maps

    @staticmethod
    def calculate_layer_output_linear(
        layer: nn.Linear, input_mat: torch.Tensor, normalize: bool = True
    ):
        if isinstance(layer, (nn.Linear)):
            # print(f'shape of input is {input_mat.shape}')
            output = layer(input_mat).detach().numpy()
            input_mat = input_mat.detach().numpy()
            # num_out_channels = output.shape[3]
            if len(output.shape) < 4:
                output = np.expand_dims(output, axis=0)
                output = np.expand_dims(output, axis=0)
                input_mat = np.expand_dims(input_mat, axis=0)
                input_mat = np.expand_dims(input_mat, axis=0)

            # num_outputs = output.shape[1]

            num_input_channels = input_mat.shape[3]

            num_out_channels = output.shape[3]
            # feature_maps = [np.array([output[0,i,:,:]]) for i in range(num_outputs)]
            input_vals = [input_mat[0, 0, 0, i] for i in range(num_input_channels)]
            output_vals = [output[0, 0, 0, i] for i in range(num_out_channels)]
        else:
            print("input is not a tensor or layer is not non linear or a callable")
            raise ValueError
        return output_vals, input_vals

    
    @staticmethod
    def calculate_layer_output_callable(
        layer: Callable, input_mat: torch.Tensor, normalize: bool = True,output:torch.Tensor=None
    ):
        if callable(layer):
            if output==None:
                output = layer(input_mat).detach().numpy()
            output_shape = output.shape
            if len(output_shape) == 2:  # layer is after flattening
                output_vals = [(output[0, i]) for i in range(output_shape[1])]
                output_vals = np.expand_dims(output_vals, axis=0)
            else:
                while len(output.shape) < 4:
                    output = np.expand_dims(output, axis=0)
                num_outputs = output.shape[1]
                # print(output.shape)
                output_vals = [
                    np.array([output[0, i, :, :]]) for i in range(num_outputs)
                ]
        else:
            print("input is not a tensor or layer is not callable")
            raise ValueError
        return output_vals
    
    @staticmethod
    def calculate_layer_output_non_callable(
        layer: Callable, input_mat: torch.Tensor, normalize: bool = True,output:torch.Tensor=None
    ):
        if callable(layer)==False:
            if output==None:
                pass
            output_shape = output.shape
            if len(output_shape) == 2:  # layer is after flattening
                output_vals = [(output[0, i]) for i in range(output_shape[1])]
                output_vals = np.expand_dims(output_vals, axis=0)
            else:
                while len(output.shape) < 4:
                    output = np.expand_dims(output, axis=0)
                num_outputs = output.shape[1]
                # print(output.shape)
                output_vals = [
                    np.array([output[0, i, :, :]]) for i in range(num_outputs)
                ]
        else:
            print("input is not a tensor or layer is not callable")
            raise ValueError
        return output_vals

    @staticmethod
    def extract_forward_steps(network: nn.Module):
        network = network.eval()
        layer_dict = {}
        traced_model = fx.symbolic_trace(network)
        for node in traced_model.graph.nodes:
            if node.op == "call_module":
                layer_name = node.target               
                layer_dict = LayerInfo.add_new_key(
                    layer_dict, layer_name, network.get_submodule(layer_name)
                )
            elif (
                node.op == "call_function"
            ):  
                func_name = str(node.target)                
                layer_dict = LayerInfo.add_new_key(layer_dict, func_name, node.target)

        return layer_dict
    
    @staticmethod
    def extract_args_from_node(args:torch.Tensor|list|tuple,layer_outputs:dict):
        if isinstance(args, (list, tuple)):            
            modified_structure = []
            for element in args:
                if isinstance(element, (list, tuple)):                    
                    modified_structure.append(LayerInfo.extract_args_from_node(element, layer_outputs))
                else:                    
                    modified_structure.append(layer_outputs[str(element)] if isinstance(element,fx.Node) else element)
            return modified_structure
        else:
            return layer_outputs[args]
        
    @staticmethod
    def extract_args_names_from_node(args:torch.Tensor|list|tuple):
        if isinstance(args, (list, tuple)):            
            modified_structure = []
            for element in args:
                if isinstance(element, (list, tuple)):
                    [modified_structure.append(x) for x in LayerInfo.extract_args_names_from_node(element)]                    
                    #modified_structure.append(LayerInfo.extract_args_names_from_node(element))
                else:                    
                    modified_structure.append(element)
            return modified_structure
        else:
            return [args]
    
    
    @staticmethod
    def extract_node_info(network: nn.Module, input_tensor: torch.Tensor = None,input_shape:tuple=(1,128,128)):
        network.eval()
        layer_dict = {}
        traced_model = fx.symbolic_trace(network)
        node_output_map = {}
        node_target_object = {}
        connections = {}

        if input_tensor is None:
            input_tensor = torch.rand(*input_shape)

        if not isinstance(input_tensor, torch.Tensor):
            input_tensor = torch.tensor(input_tensor, requires_grad=False)

        node_output_map[list(traced_model.graph.nodes)[0]] = input_tensor        
        intermediate_output = input_tensor        
        
        for node in traced_model.graph.nodes:
            #print(f'Debug748: node name {node.name} and target is {str(node.target)}')
            if node.op == 'placeholder':
                layer_dict[node.name] = intermediate_output.detach().clone()
                node_target_object[node] = layer_dict[node.name]

            elif node.op == 'call_module':
                submodule = dict(traced_model.named_modules())[node.target]
                args = LayerInfo.extract_args_from_node(args=node.args, layer_outputs=layer_dict)
                with torch.no_grad():
                    intermediate_output = submodule(*args, **node.kwargs)
                node_output_map[node] = intermediate_output
                layer_dict[node.name] = intermediate_output.detach().clone()
                node_target_object[node] = submodule

            elif node.op == 'get_attr':
                node_output_map[node] = getattr(network, node.target)
                layer_dict[node.name] = node_output_map[node].detach().clone()
                node_target_object[node] = layer_dict[node.name]

            elif node.op == 'call_function':
                args = LayerInfo.extract_args_from_node(args=node.args, layer_outputs=layer_dict)
                with torch.no_grad():
                    intermediate_output = node.target(*args, **node.kwargs)
                node_output_map[node] = intermediate_output
                layer_dict[node.name] = intermediate_output.detach().clone()
                node_target_object[node] = node.target
                args_names_as_value = LayerInfo.extract_args_names_from_node(args=node.args)
                #print(f'Debug769: {args_names_as_value} and layer name is: {node.name}')
                connections[node.name] = args_names_as_value

            elif node.op == 'call_method':
                args = LayerInfo.extract_args_from_node(args=node.args, layer_outputs=layer_dict)
                method_name = node.target
                with torch.no_grad():
                    intermediate_output = getattr(args[0], method_name)(*args[1:], **node.kwargs)
                layer_dict[node.name] = intermediate_output.detach().clone()
                node_target_object[node] = getattr(args[0], method_name)

            elif node.op == 'output':
                # The 'output' node contains the final output of the model
                args = LayerInfo.extract_args_from_node(args=node.args, layer_outputs=layer_dict)
                intermediate_output = args[0]  # The output is stored in args[0]
                layer_dict['output'] = intermediate_output.detach().clone()
                node_target_object[node] = layer_dict['output']
            else:
                print(f'Debug793: node name {node.name} and target is {str(node.target)}')
        #print('connections',connections)
        return layer_dict,node_target_object,connections

    @staticmethod
    def add_new_key(d, key, value):        
        if key in d:
            i = 1
            new_key = f"{key}_{i}"            
            while new_key in d:
                i += 1
                new_key = f"{key}_{i}"            
            d[new_key] = value
        else:            
            d[key] = value

        return d

