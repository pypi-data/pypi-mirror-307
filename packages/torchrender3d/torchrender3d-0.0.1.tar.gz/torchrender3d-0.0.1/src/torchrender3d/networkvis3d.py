import time
#import ray
import numpy as np
import torch
import torch.fx as fx
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import vtk
#from IPython.display import display

# import matplotlib.pyplot as plt
#from copy import copy, deepcopy
from tqdm import tqdm
from typing import Callable

from .drawing_tools import DrawTools 
from .extract_layer_methods import LayerInfo
from .parallel_methods import run_gen_parallel_method


class PlotBuilderNN:
    def __init__(
        self,
        neural_network: nn.Module,
        input_image_dim: tuple,
        plot_type: str = "param",
        network_param_path: str = "path_to_file",
        normalize: bool = True,
        test_data: np.memmap = None,
        layer_idx_to_render:list=None
    ):
        self.plot_type = plot_type
        self.normalize = normalize
        self.network_param_path = network_param_path
        self.image_dim = input_image_dim
        self.network_model = neural_network
        
        self.actors: list[vtk.vtkLODActor] = []
        self.actor_dict = {}
        self.test_data = test_data
        self.layer_idx_to_render=layer_idx_to_render

    def __call__(self):
        self.__execute_protocol()

    def __execute_protocol(self, interlayer_gap: int = 5):
        if self.plot_type == "param":
            # print('Debug: param mode')
            if not self.actors:
                self.build_param_actors_parallel()
                #self.build_param_actors(interlayer_gap=interlayer_gap)
            else:
                self.update_param_actors()
        elif self.plot_type == "output":
            if not self.actors:
                self.build_output_actors(interlayer_gap=interlayer_gap)
            else:
                self.update_output_actors()

        else:
            print(f"Wrong param type as {self.plot_type} not  param or output")
            raise ValueError
    
    @staticmethod
    def calculate_layer_pos(layers:list,interlayer_space:float=5):
        layer_pos = [0]*len(layers)
        current_layer_pos = 0
        for idx,layer in enumerate(layers):
            layer_pos[idx] = current_layer_pos
            current_depth = PlotBuilderNN.calculate_layer_depth(layer=layer)
            current_layer_pos = current_layer_pos + current_depth + interlayer_space
            
        return layer_pos

    @staticmethod
    def calculate_layer_depth(layer:nn.Module|Callable|torch.Tensor):
        if isinstance(layer, nn.Linear):
                # print('Debug: Plotting linear layer')
                depth = 10
                
        elif (
                isinstance(layer, (nn.Conv2d,nn.Conv1d,nn.ConvTranspose1d,nn.ConvTranspose2d))                
            ):
                depth = layer.in_channels
                if layer.bias != None:
                    depth = depth + 2
                
        elif isinstance(layer, (nn.BatchNorm1d,nn.BatchNorm2d)):
                depth = 5
                
        elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d,nn.AvgPool2d,nn.AvgPool1d,nn.AdaptiveAvgPool1d,nn.AdaptiveAvgPool2d)):
                depth = 5                
            
        elif isinstance(layer, (nn.ReLU,
                    nn.LeakyReLU,
                    nn.Sigmoid,
                    nn.Tanh,
                    nn.Softmax,
                    nn.ELU,
                    nn.SELU,
                    nn.GELU,)):
                depth = 5
                
        else:
                
                depth = 5
                
        return depth
       

    @staticmethod
    def make_param_actors_from_layer(idx:int,name:str, layer:nn.Module|Callable|torch.Tensor,output:torch.Tensor,normalize:bool,layer_pos:float):
        if isinstance(layer, nn.Linear):
                # print('Debug: Plotting linear layer')
                current_actors, depth, name_list = PlotBuilderNN.create_linear_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )
                
        elif (
                isinstance(layer, (nn.Conv2d,nn.Conv1d,nn.ConvTranspose1d,nn.ConvTranspose2d))                
            ):
                current_actors, depth, name_list = PlotBuilderNN.create_cnn_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )
                
        elif isinstance(layer, (nn.BatchNorm1d,nn.BatchNorm2d)):
                current_actors, depth, name_list = PlotBuilderNN.create_bn_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )
                
        elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d,nn.AvgPool2d,nn.AvgPool1d,nn.AdaptiveAvgPool1d,nn.AdaptiveAvgPool2d)):
                current_actors, depth, name_list = PlotBuilderNN.create_pool_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )                
            
        elif isinstance(layer, (nn.ReLU,
                    nn.LeakyReLU,
                    nn.Sigmoid,
                    nn.Tanh,
                    nn.Softmax,
                    nn.ELU,
                    nn.SELU,
                    nn.GELU,)):
                current_actors, depth, name_list = PlotBuilderNN.create_activation_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )
                
        else:
                current_actors, depth, name_list = PlotBuilderNN.create_non_tracked_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=normalize,
                )
                
                # print('Debug: Layer type not defined' )
        return current_actors,depth,name_list

    def build_param_actors_parallel(self, interlayer_gap: int = 5):        
        layer_pos = 0
        depth = 0
        names = []        
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        
        image_mat = (
            image.clone().unsqueeze(0).float()
        )
        #print(f'WARNING: METHOD UNDER DEVELOPMENT...')
        print(f'Debug183: Performing step calculations...')
        layer_info_dict,layer_type_dict,connections = LayerInfo.extract_node_info(network=self.network_model,input_tensor=image_mat)
        layer_outputs = layer_info_dict.values()
        layer_targets = layer_type_dict.values()
        layer_names = layer_info_dict.keys()
        layer_ids = np.arange(0,len(layer_names))

        print(f'Debug190: Performing layer position calculations...')
        layer_pos_list = PlotBuilderNN.calculate_layer_pos(layers=list(layer_targets),interlayer_space=interlayer_gap)

        print(f'Debug193: Performing actorcreations from layers...')
        #initialize_ray()
        
        normalize = self.normalize
        #parallel_output = ray.get([run_gen_parallel_method.options(scheduling_strategy="SPREAD").remote(func=PlotBuilderNN.make_param_actors_from_layer,idx=idx,name=name,layer=layer,output=output,normalize=normalize,layer_pos=layer_pos) 
        # for idx,name,layer,output,layer_pos in zip(layer_ids,layer_names,layer_targets,layer_outputs,layer_pos_list)])
        parallel_output = ([run_gen_parallel_method(func=PlotBuilderNN.make_param_actors_from_layer,idx=idx,name=name,layer=layer,output=output,normalize=normalize,layer_pos=layer_pos) 
         for idx,name,layer,output,layer_pos in zip(layer_ids,layer_names,layer_targets,layer_outputs,layer_pos_list)])
        #layer_ids_handle = put_as_handle_for_rayop(val=layer_ids)

        print(f'Debug207: Adding actors to the dict...')

        for current_output in parallel_output:
            #print(current_output)
            current_actors = current_output[0]
            name_list = current_output[2]
            [self.actors.append(x) for x in current_actors]
            [names.append(x) for x in name_list]
            [
                self.actor_dict.update({name: value})
                for name, value in zip(name_list, current_actors)
            ]
        


    def build_param_actors(self, interlayer_gap: int = 5):
        print("actors is empty")
        layer_pos = 0
        depth = 0
        names = []
        # for name, layer in tqdm(
        #     self.network_model.named_modules(), desc="Building Actors"
        # ):
        #layer_info = LayerInfo.extract_forward_steps(network=self.network_model)
        #layer_output_dict,layer_target_dict = LayerInfo.extract_node_info(network=self.network_model)
        #for name,layer in tqdm(layer_target_dict.items(), desc="Building"):
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        # image_mat = (
        #     torch.tensor(image, requires_grad=False).unsqueeze(0).unsqueeze(0).float()
        # )
        image_mat = (
            image.clone().unsqueeze(0).float()
        )
        
        layer_info_dict,layer_type_dict,connections = LayerInfo.extract_node_info(network=self.network_model,input_tensor=image_mat)
        layer_outputs = layer_info_dict.values()
        layer_targets = layer_type_dict.values()
        layer_names = layer_info_dict.keys()
        layer_ids = np.arange(0,len(layer_names))
        if isinstance(self.layer_idx_to_render,(list,np.ndarray)):
            layer_to_consider = self.layer_idx_to_render
        else:
            layer_to_consider = layer_ids
        #for name, layer in tqdm(layer_info.items(), desc="Building"):
        for idx,name, layer,output in tqdm(zip(layer_ids,layer_names,layer_targets,layer_outputs), desc="Building"):
        #for name, layer in tqdm(layer_info.items(), desc="Building"):
            #print(f'debug890: {name} and step number is {idx}')
            if isinstance(layer, nn.Linear):
                # print('Debug: Plotting linear layer')
                current_actors, depth, name_list = PlotBuilderNN.create_linear_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth
                image_mat = output
            elif (
                isinstance(layer, (nn.Conv2d,nn.Conv1d,nn.ConvTranspose1d,nn.ConvTranspose2d))                
            ):
                current_actors, depth, name_list = PlotBuilderNN.create_cnn_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
            elif isinstance(layer, (nn.BatchNorm1d,nn.BatchNorm2d)):
                current_actors, depth, name_list = PlotBuilderNN.create_bn_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
            elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d,nn.AvgPool2d,nn.AvgPool1d,nn.AdaptiveAvgPool1d,nn.AdaptiveAvgPool2d)):
                current_actors, depth, name_list = PlotBuilderNN.create_pool_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
            
            elif isinstance(layer, (nn.ReLU,
                    nn.LeakyReLU,
                    nn.Sigmoid,
                    nn.Tanh,
                    nn.Softmax,
                    nn.ELU,
                    nn.SELU,
                    nn.GELU,)):
                current_actors, depth, name_list = PlotBuilderNN.create_activation_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
            else:
                current_actors, depth, name_list = PlotBuilderNN.create_non_tracked_actors(
                    layer=layer,
                    layer_name=name,
                    layer_pos=layer_pos,
                    normalize=self.normalize,
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
                image_mat = output
                # print('Debug: Layer type not defined' )
                

    def update_param_actors(self):
        try:
            self.network_model.load_state_dict(
                torch.load(
                    self.network_param_path,
                    map_location=torch.device("cpu"),
                    weights_only=True,
                )
            )
        except:
            print('WARNING: Wrong file path {self.network_param_path} to stored model params ')

        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        # image_mat = (
        #     torch.tensor(image, requires_grad=False).unsqueeze(0).unsqueeze(0).float()
        # )
        image_mat = (
            torch.tensor(image, requires_grad=False).unsqueeze(0).float()
        )
        # print('actors is not empty')
        # for name, layer in tqdm(self.network_model.named_modules(), desc="Updating"):
        layer_info_dict,layer_type_dict,connections = LayerInfo.extract_node_info(network=self.network_model,input_tensor=image_mat)
        layer_outputs = layer_info_dict.values()
        layer_targets = layer_type_dict.values()
        layer_names = layer_info_dict.keys()
        #for name, layer in tqdm(layer_info.items(), desc="Building"):
        for name, layer,output in tqdm(zip(layer_names,layer_targets,layer_outputs), desc="updating"):
            if isinstance(layer, nn.Linear):
                # current_actors = PlotBuilderNN.get_linear_actor_names(layer_name=name)
                self.update_linear_actors(
                    layer=layer, layer_name=name, normalize=self.normalize
                )
            elif (
                isinstance(layer, nn.Conv2d)
                or isinstance(layer, nn.Conv1d)
                or isinstance(layer, nn.ConvTranspose1d)
                or isinstance(layer, nn.ConvTranspose2d)
            ):
                self.update_cnn_actors(
                    layer=layer, layer_name=name, normalize=self.normalize
                )
            elif isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
                self.update_bn_actors(
                    layer=layer, layer_name=name, normalize=self.normalize
                )
            else:
                # print('Debug: Layer type not defined' )
                pass

    def __build_output_actors(self, interlayer_gap: int = 5, depth: float = None):
        print("actors is empty")
        layer_pos = 0
        depth = 0
        names = []
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        image_mat = (
            torch.tensor(image, requires_grad=False).unsqueeze(0).unsqueeze(0).float()
        )
        # image_mat = torch.rand((1, 128, 128)).unsqueeze(0)
        # image_mat = torch.rand((1, 1, 128))
        # for name, layer in tqdm(self.network_model.named_modules(),desc='Building Actors'):
        layer_info = LayerInfo.extract_forward_steps(network=self.network_model)
        for name, layer in tqdm(layer_info.items(), desc="Building"):
            # print(f'Debug: Plotting step name {name}')
            if isinstance(layer, nn.Linear):
                # print(f'Debug: Plotting linear layer name {name}')
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_linear_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)
            elif (
                isinstance(layer, nn.Conv2d)
                or isinstance(layer, nn.Conv1d)
                or isinstance(layer, nn.ConvTranspose1d)
                or isinstance(layer, nn.ConvTranspose2d)
            ):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_cnn_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)
            elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d)):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_pool_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)
            elif isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_bn_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)

            elif isinstance(
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
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_activation_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)

            else:
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_callable_output_layer(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = layer(image_mat)
                # print('Debug: Layer type not defined' )
                # print(f'WARNING: {name} and input shape is {image_mat.shape} is not plotted')

            # print(f'DEBUG: {name} and input shape is {image_mat.shape}')
            # image_mat = layer(image_mat)
    
    def build_output_actors(self, interlayer_gap: int = 5, depth: float = None):
        print("actors is empty")
        layer_pos = 0
        depth = 0
        names = []
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        
        image_mat = image.clone().unsqueeze(0).detach().requires_grad_(False)        
        layer_info_dict,layer_type_dict,connections = LayerInfo.extract_node_info(network=self.network_model,input_tensor=image_mat)
        layer_outputs = layer_info_dict.values()
        layer_targets = layer_type_dict.values()
        layer_names = layer_info_dict.keys()
        
        for name, layer,output in tqdm(zip(layer_names,layer_targets,layer_outputs), desc="Building"):
            #print(f'Debug: Plotting step name {name}')
            if isinstance(layer, nn.Linear):
                # print(f'Debug: Plotting linear layer name {name}')
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_linear_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap                
                image_mat = output
            elif (
                isinstance(layer, nn.Conv2d)
                or isinstance(layer, nn.Conv1d)
                or isinstance(layer, nn.ConvTranspose1d)
                or isinstance(layer, nn.ConvTranspose2d)
            ):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_cnn_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap                
                image_mat = output
            elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d)):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_pool_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap                
                image_mat = output
            elif isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_bn_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap                
                image_mat = output
            elif isinstance(
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
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_activation_output_actors(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap                
                image_mat = output
            
            elif (isinstance(
                layer,
                (
                    Callable
                ))):
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_callable_output_layer(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                #image_mat = layer(image_mat)
                image_mat = output

            else:
                current_actors, depth, name_list = (
                    PlotBuilderNN.create_noncallable_output_layer(
                        input_mat=image_mat,
                        layer=layer,
                        layer_name=name,
                        layer_pos=layer_pos,
                        normalize=self.normalize,
                        output=output
                    )
                )
                [self.actors.append(x) for x in current_actors]
                [names.append(x) for x in name_list]
                [
                    self.actor_dict.update({name: value})
                    for name, value in zip(name_list, current_actors)
                ]
                layer_pos = layer_pos + depth + interlayer_gap
                image_mat = output
                #image_mat = output
        if connections:
            self.draw_connections(connections=connections)


    
    def update_output_actors(self):
        self.network_model.load_state_dict(
            torch.load(
                self.network_param_path,
                map_location=torch.device("cpu"),
                weights_only=True,
            )
        )
        # print('actors is not empty')
        # image_mat = torch.rand((1, 128, 128)).unsqueeze(0)
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        # image_mat = (
        #     torch.tensor(image, requires_grad=False).unsqueeze(0).unsqueeze(0).float()
        # )
        #image_mat = (
        #    torch.tensor(image, requires_grad=False).unsqueeze(0).float()
        #)
        image_mat = image.clone().unsqueeze(0).detach().requires_grad_(False)
        # image_mat = torch.rand((1, 1, 128)).unsqueeze(0)
        # image_mat = torch.rand((1, 1, 128))
        # for name, layer in tqdm(self.network_model.named_modules(),desc='Updating'):
        layer_info_dict,layer_type_dict,connections = LayerInfo.extract_node_info(network=self.network_model,input_tensor=image_mat)
        layer_outputs = layer_info_dict.values()
        layer_targets = layer_type_dict.values()
        layer_names = layer_info_dict.keys()
        #for name, layer in tqdm(layer_info.items(), desc="Building"):
        for name, layer,output in tqdm(zip(layer_names,layer_targets,layer_outputs), desc="Updating"):
            if isinstance(layer, nn.Linear):
                # current_actors = PlotBuilderNN.get_linear_actor_names(layer_name=name)
                self.update_linear_output_actors(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                image_mat = layer(image_mat)
                image_mat = output
            elif (
                isinstance(layer, nn.Conv2d)
                or isinstance(layer, nn.Conv1d)
                or isinstance(layer, nn.ConvTranspose1d)
                or isinstance(layer, nn.ConvTranspose2d)
            ):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                image_mat = output
            elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d)):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                #image_mat = layer(image_mat)
                image_mat=output
            elif isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                #image_mat = layer(image_mat)
                image_mat = output
            elif isinstance(
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
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                #image_mat = layer(image_mat)
                image_mat = output
            elif isinstance(layer,Callable):
                self.update_output_actors_callable(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                #image_mat = layer(image_mat)
                image_mat = output

            else:
                self.update_output_actors_non_callable(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                    output=output
                )
                #image_mat = layer(image_mat)
                image_mat = output
                #image_mat = output
    
    
    def __update_output_actors(self):
        self.network_model.load_state_dict(
            torch.load(
                self.network_param_path,
                map_location=torch.device("cpu"),
                weights_only=True,
            )
        )
        # print('actors is not empty')
        # image_mat = torch.rand((1, 128, 128)).unsqueeze(0)
        len_of_data = len(self.test_data)
        random_data_index = np.random.randint(0, len_of_data)
        image = self.test_data[random_data_index]
        image_mat = (
            torch.tensor(image, requires_grad=False).unsqueeze(0).unsqueeze(0).float()
        )
        # image_mat = torch.rand((1, 1, 128)).unsqueeze(0)
        # image_mat = torch.rand((1, 1, 128))
        # for name, layer in tqdm(self.network_model.named_modules(),desc='Updating'):
        layer_info = LayerInfo.extract_forward_steps(network=self.network_model)
        for name, layer in tqdm(layer_info.items(), desc="Updating"):
            if isinstance(layer, nn.Linear):
                # current_actors = PlotBuilderNN.get_linear_actor_names(layer_name=name)
                self.update_linear_output_actors(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)
            elif (
                isinstance(layer, nn.Conv2d)
                or isinstance(layer, nn.Conv1d)
                or isinstance(layer, nn.ConvTranspose1d)
                or isinstance(layer, nn.ConvTranspose2d)
            ):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)
            elif isinstance(layer, (nn.MaxPool2d, nn.MaxPool1d)):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)
            elif isinstance(layer, nn.BatchNorm1d) or isinstance(layer, nn.BatchNorm2d):
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)
            elif isinstance(
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
                self.update_output_actors_non_linear(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)
            else:
                self.update_output_actors_callable(
                    input_mat=image_mat,
                    layer=layer,
                    layer_name=name,
                    normalize=self.normalize,
                )
                image_mat = layer(image_mat)

    @staticmethod
    def create_linear_actors(
        layer: nn.Linear, layer_name: str, layer_pos: float, normalize: bool = True
    ):
        in_neurons, out_neurons, weight, bias = LayerInfo.extract_linear_params(
            layer=layer, normalize=normalize
        )
        depth = 10
        linear_actor, spheres_actor = DrawTools.draw_connections(
            connection_mat=weight,
            layer_pos=layer_pos,
            layer_spacing=depth,
            draw_nodes=True,
        )
        actors = [linear_actor, spheres_actor]
        name_list = [layer_name + ".weight", layer_name + ".nodes"]
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(0, 0, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        return actors, depth, name_list

    @staticmethod
    def create_linear_output_actors(
        input_mat: torch.Tensor,
        layer: nn.Linear,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor=None,
    ):
        depth = 10
        in_neurons, out_neurons, weight, bias = LayerInfo.extract_linear_params(
            layer=layer, normalize=normalize
        )
        #print(f"Debug: shape of weight is {weight.shape}")
        output_vals, input_vals = LayerInfo.calculate_layer_output_linear(
            layer=layer, input_mat=input_mat, normalize=normalize
        )
        # input_cubes = DrawTools.draw_colored_cubes_in_2d_grid(
        #     cube_colors=input_vals, layer_pos=layer_pos, inter_cube_gap=1
        # )
        if output!=None:
            output_vals = output.squeeze(0).detach().numpy()

        if normalize:
            output_vals = LayerInfo.normalize_mat(output_vals)
            input_vals = LayerInfo.normalize_mat(np.array(input_vals))
        input_cubes = DrawTools.draw_colored_cubes_in_2d_grid(
            cube_colors=input_vals, layer_pos=layer_pos, inter_cube_gap=1
        )    
        output_cubes = DrawTools.draw_colored_cubes_in_2d_grid(
            cube_colors=output_vals, layer_pos=layer_pos + depth, inter_cube_gap=1
        )

        linear_actor, _ = DrawTools.draw_connections(
            connection_mat=weight,
            layer_pos=layer_pos,
            layer_spacing=depth,
            draw_nodes=True,
            gap_length=1,
        )
        actors = [input_cubes, linear_actor, output_cubes]
        name_list = [
            layer_name + ".input",
            layer_name + ".weight",
            layer_name + ".output",
        ]
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(0, 0, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name+'.bounding_box')
        name_list.append(layer_name+'.label_actor')
        return actors, depth, name_list

    @staticmethod
    def get_linear_actor_names(layer_name: str):
        name_list = [
            layer_name + ".weight",
            layer_name + ".input",
            layer_name + ".output",
        ]
        return name_list

    def update_linear_actors(
        self, layer: nn.Linear, layer_name: str, normalize: bool = True
    ):
        name_list = PlotBuilderNN.get_linear_actor_names(layer_name=layer_name)
        print(f"namelist {name_list}")
        actors = [
            self.actor_dict[name]
            for name in name_list
            if name in list(self.actor_dict.keys())
        ]
        in_neurons, out_neurons, weight, bias = LayerInfo.extract_linear_params(
            layer=layer, normalize=normalize
        )
        linear_actor = actors[0]
        DrawTools.update_connections(
            linear_actor=linear_actor, updated_connection_mat=weight
        )

    def update_linear_output_actors(
        self,
        input_mat: torch.Tensor,
        layer: nn.Linear,
        layer_name: str,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        output_vals, input_vals = LayerInfo.calculate_layer_output_linear(
            layer=layer, input_mat=input_mat, normalize=normalize
        )
        if output!=None:
            output_vals = output.squeeze(0).detach().numpy()
        if normalize:
            output_vals = LayerInfo.normalize_mat(np.array(output_vals))
        name_list = PlotBuilderNN.get_linear_actor_names(layer_name=layer_name)
        actors = [self.actor_dict[name] for name in name_list]
        in_neurons, out_neurons, weight, bias = LayerInfo.extract_linear_params(
            layer=layer, normalize=normalize
        )

        linear_actor = actors[0]
        input_actor = actors[1]
        output_actor = actors[2]

        DrawTools.update_connections(
            linear_actor=linear_actor, updated_connection_mat=weight
        )
        DrawTools.update_colored_cubes(
            cube_actor=input_actor, updated_cube_colors=input_vals
        )
        DrawTools.update_colored_cubes(
            cube_actor=output_actor, updated_cube_colors=output_vals
        )

    

    @staticmethod
    def create_cnn_actors(
        layer: nn.Conv1d | nn.Conv2d | nn.ConvTranspose1d | nn.ConvTranspose2d,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
    ):
        num_kernels, depth, height, width, weight, bias = LayerInfo.extract_cnn_params(
            layer=layer, normalize=normalize
        )
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_kernels, gap_length=(width, height), layer_pos=layer_pos+depth/2
        )
        x_pos_list = uniform_points_3d[:, 0]
        y_pos_list = uniform_points_3d[:, 1]
        z_pos_list = uniform_points_3d[:, 2]

        cuboid_ids = np.arange(0, len(y_pos_list), 1)
        actors = [[]] * len(y_pos_list)
        name_list = [[]] * len(y_pos_list)

        for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
            weight_current = weight[id, :, :, :]
            actors[id] = DrawTools.draw_filled_grid_3d(
                volume_data=weight_current, coors_3d=(x, y, z)
            )
            name_current = layer_name + ".weight_k_no_" + str(id)
            name_list[id] = name_current

        if layer.bias != None:
            depth = depth + 2
            bias_actors = DrawTools.draw_colored_cubes_in_2d_grid(
                cube_colors=bias.flatten(),
                layer_pos=layer_pos + depth,
                inter_cube_gap=max(height, width),
            )
            actors.append(bias_actors)
            name_list.append(layer_name + ".bias")
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 0, 0)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        return actors, depth, name_list

    @staticmethod
    def create_cnn_output_actors(
        input_mat: torch.Tensor,
        layer: nn.Conv1d | nn.Conv2d | nn.ConvTranspose1d | nn.ConvTranspose2d,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor = None
    ):  
        if output==None:
            features_list = LayerInfo.calculate_cnn_layer_output(
                layer=layer, input_mat=input_mat, normalize=normalize
            )
        else:
            if isinstance(layer,(nn.Conv1d,nn.ConvTranspose1d)):
                if len(output.shape) < 4:
                    output = np.expand_dims(output, axis=0)
                # reshaped_array = output.reshape(1, 10, 1, 128)
                output = output.reshape(1, output.shape[2], 1, output.shape[3])
                num_outputs = output.shape[1]
                # print(output.shape)
                features_list = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
            elif isinstance(layer,(nn.Conv2d,nn.ConvTranspose2d)):
                #output = layer(input_mat).detach().numpy()
                if len(output.shape) < 4:
                    output = np.expand_dims(output, axis=0)
                num_outputs = output.shape[1]
                features_list = [np.array([output[0, i, :, :]]) for i in range(num_outputs)]
        if normalize:
            features_list = [LayerInfo.normalize_mat(x) for x in features_list]    
        num_features = len(features_list)
        feature_dimensions = features_list[0].shape

        # print(f'debug:841 {feature_dimensions}')
        height = feature_dimensions[1]
        width = feature_dimensions[2]
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
        )

        x_pos_list = uniform_points_3d[:, 0]
        y_pos_list = uniform_points_3d[:, 1]
        z_pos_list = uniform_points_3d[:, 2]

        cuboid_ids = np.arange(0, len(y_pos_list), 1)
        actors = [[]] * len(y_pos_list)
        name_list = [[]] * len(y_pos_list)

        depth = np.max(feature_dimensions)
        depth = layer.in_channels

        for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
            feature_current = features_list[id]
            actors[id] = DrawTools.draw_filled_grid_3d(
                volume_data=feature_current, coors_3d=(x, y, z)
            )
            name_current = layer_name + ".feature_k_no_" + str(id)
            name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 0, 0)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        name_list.append(layer_name+'.label_actor')
        return actors, depth, name_list

    @staticmethod
    def get_cnn_actor_names(layer_name: str, num_kernels: int, is_there_bias: bool):
        name_list = [
            layer_name + ".weight_k_no_" + str(id) for id in range(num_kernels)
        ]
        # name_list = [layer_name+'.weight',layer_name+'.nodes']
        if is_there_bias:
            name_list.append(layer_name + ".bias")
        return name_list

    def update_cnn_actors(
        self,
        layer: nn.Conv1d | nn.Conv2d | nn.ConvTranspose1d | nn.ConvTranspose2d,
        layer_name: str,
        normalize: bool = True,
    ):
        num_kernels, depth, height, width, weight, bias = LayerInfo.extract_cnn_params(
            layer=layer, normalize=normalize
        )
        name_list = PlotBuilderNN.get_cnn_actor_names(
            layer_name=layer_name,
            is_there_bias=layer.bias != None,
            num_kernels=num_kernels,
        )
        if layer.bias != None:
            actors = [self.actor_dict[name] for name in name_list]
            # volume_actors = [actor for actor in range(len(actors)-1)]
            volume_actors = [actor for actor in actors[0 : len(actors) - 1]]
            bias_actor = actors[len(actors) - 1]
            [
                DrawTools.update_filled_grid_3d(
                    volume_actor=actor, updated_volume_data=weight[id]
                )
                for id, actor in enumerate(volume_actors)
            ]
        else:
            volume_actors = [self.actor_dict[name] for name in name_list]
            # volume_actors = [actor for actor in actors[0:len(actors)-1]]
            [
                DrawTools.update_filled_grid_3d(
                    volume_actor=actor, updated_volume_data=weight[id]
                )
                for id, actor in enumerate(volume_actors)
            ]

    @staticmethod
    def create_bn_actors(
        layer: nn.BatchNorm1d | nn.BatchNorm2d,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
    ):
        actors = []
        depth = 5
        weight, bias = LayerInfo.extract_bn_params(layer=layer, normalize=normalize)
        weight_actor = DrawTools.draw_colored_cubes_in_2d_grid(
            cube_colors=weight.flatten(), layer_pos=layer_pos, inter_cube_gap=5
        )
        bias_actor = DrawTools.draw_colored_cubes_in_2d_grid(
            cube_colors=bias.flatten(), layer_pos=layer_pos + depth, inter_cube_gap=5
        )
        actors = [weight_actor, bias_actor]
        name_list = [layer_name + ".weight", layer_name + ".bias"]
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(0, 1, 0)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        return actors, depth, name_list

    @staticmethod
    def get_bn_actor_names(layer_name: str):
        name_list = [layer_name + ".weight", layer_name + ".bias"]
        return name_list

    def update_bn_actors(
        self,
        layer: nn.BatchNorm1d | nn.BatchNorm2d,
        layer_name: str,
        normalize: bool = True,
    ):
        name_list = PlotBuilderNN.get_bn_actor_names(layer_name=layer_name)
        weight, bias = LayerInfo.extract_bn_params(layer=layer, normalize=normalize)
        actors = [self.actor_dict[name] for name in name_list]
        DrawTools.update_colored_cubes(
            cube_actor=actors[0], updated_cube_colors=weight.flatten()
        )
        DrawTools.update_colored_cubes(
            cube_actor=actors[1], updated_cube_colors=bias.flatten()
        )

    @staticmethod
    def  create_pool_actors(
            layer: nn.MaxPool1d | nn.MaxUnpool2d,
            layer_name: str,
            layer_pos: float,
            normalize: bool = True,
        ):
        actors = []
        depth = 5
        if isinstance(layer,(nn.MaxPool1d,nn.AvgPool1d,nn.AdaptiveAvgPool1d)):
            dummy_tensor = torch.zeros(1,1,32)
            output_tensor = layer(dummy_tensor)
            if len(output_tensor .shape) < 4:
                output_tensor  = np.expand_dims(output_tensor , axis=0)
                dummy_tensor  = np.expand_dims(dummy_tensor , axis=0)

            # reshaped_array = output.reshape(1, 10, 1, 128)
            output_tensor  = output_tensor.reshape(1, output_tensor.shape[2], 1, output_tensor.shape[3])
            dummy_tensor   = dummy_tensor .reshape(1, dummy_tensor .shape[2], 1, dummy_tensor .shape[3])
            num_outputs = output_tensor.shape[1]
            # print(output.shape)
            features_list = [np.array([output_tensor[0, i, :, :]]) for i in range(num_outputs)]
        elif isinstance(layer,(nn.MaxPool2d,nn.AvgPool2d,nn.AdaptiveAvgPool2d)):
            dummy_tensor = torch.zeros(1,1,32,32)
            output_tensor = layer(dummy_tensor)
            if len(output_tensor .shape) < 4:
                output_tensor  = np.expand_dims(output_tensor , axis=0)
            num_outputs = output_tensor.shape[1]
            features_list = [np.array([output_tensor[0, i, :, :]]) for i in range(num_outputs)]


        uniform_points_3d_input = DrawTools.distribute_points_in_2d_grid(
            num_points=1, gap_length=(32, 32), layer_pos=layer_pos
        )
        uniform_points_3d_output = DrawTools.distribute_points_in_2d_grid(
            num_points=1, gap_length=(output_tensor.shape[-1], output_tensor.shape[-1]), layer_pos=layer_pos+depth
        )
        
        
        actor_input = DrawTools.draw_filled_grid_3d(
                volume_data=dummy_tensor[0], coors_3d=uniform_points_3d_input[0,:]
            )
        actor_output = DrawTools.draw_filled_grid_3d(
                volume_data=output_tensor[0], coors_3d=uniform_points_3d_output[0,:]
            )
        bounding_box_in, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=[actor_input], box_name=layer_name, color=(1, 1, 1))
        bounding_box_out, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=[actor_output], box_name=layer_name, color=(1, 1, 1))
        bounding_box_all, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=[bounding_box_in,bounding_box_out], box_name=layer_name, color=(1, 1, 1))
        

        num_features = len(features_list)
        feature_dimensions = features_list[0].shape

        # print(f'debug:841 {feature_dimensions}')
        height = feature_dimensions[1]
        width = feature_dimensions[2]
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
        )
        actors = [bounding_box_all,bounding_box_in,bounding_box_out,label_actor]
        name_list = [layer_name+'all',layer_name+'in',layer_name+'out']
        
        return actors, depth, name_list
    
    @staticmethod
    def  create_activation_actors(
            layer: nn.ReLU
            | nn.LeakyReLU
            | nn.Sigmoid
            | nn.Tanh
            | nn.Softmax
            | nn.ELU
            | nn.SELU
            | nn.GELU,
            layer_name: str,
            layer_pos: float,
            normalize: bool = True,
        ):
        actors = []
        depth = 5
        dummy_tensor = torch.zeros(1,1,32,32)

        uniform_points_3d_input = DrawTools.distribute_points_in_2d_grid(
            num_points=1, gap_length=(32, 32), layer_pos=layer_pos
        )

        actor_input = DrawTools.draw_filled_grid_3d(
                volume_data=dummy_tensor[0], coors_3d=uniform_points_3d_input[0,:]
            )

        bounding_box_in, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=[actor_input], box_name=layer_name, color=(1, 1, 1))

        
        actors = [bounding_box_in,label_actor]
        name_list = [layer_name]
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list
    
    @staticmethod
    def  create_non_tracked_actors(
            layer: Callable,
            layer_name: str,
            layer_pos: float,
            normalize: bool = True,
        ):
        actors = []
        depth = 5
        dummy_tensor = torch.zeros(1,1,32,32)

        uniform_points_3d_input = DrawTools.distribute_points_in_2d_grid(
            num_points=1, gap_length=(32, 32), layer_pos=layer_pos
        )

        actor_input = DrawTools.draw_filled_grid_3d(
                volume_data=dummy_tensor[0], coors_3d=uniform_points_3d_input[0,:]
            )

        bounding_box_in, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=[actor_input], box_name=layer_name, color=(.5, .5, .5))

        
        actors = [bounding_box_in,label_actor]
        name_list = [layer_name]
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list

    @staticmethod
    def create_activation_output_actors(
        input_mat: torch.Tensor,
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
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor=None
    ):
        features_list = LayerInfo.calculate_activation_layer_output(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        num_features = len(features_list)
        feature_dimensions = features_list[0].shape

        height = feature_dimensions[1]
        width = feature_dimensions[2]
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
        )

        x_pos_list = uniform_points_3d[:, 0]
        y_pos_list = uniform_points_3d[:, 1]
        z_pos_list = uniform_points_3d[:, 2]

        cuboid_ids = np.arange(0, len(y_pos_list), 1)
        actors = [[]] * len(y_pos_list)
        name_list = [[]] * len(y_pos_list)

        depth = np.max(feature_dimensions)

        for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
            feature_current = features_list[id]
            actors[id] = DrawTools.draw_filled_grid_3d(
                volume_data=feature_current, coors_3d=(x, y, z)
            )
            name_current = layer_name + ".feature_k_no_" + str(id)
            name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 1, 0)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list
    
    

    @staticmethod
    def create_pool_output_actors(
        input_mat: torch.Tensor,
        layer: nn.MaxPool1d | nn.MaxPool2d,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor=None
    ):
        features_list = LayerInfo.calculate_pool_layer_output(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        num_features = len(features_list)
        feature_dimensions = features_list[0].shape

        height = feature_dimensions[1]
        width = feature_dimensions[2]
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
        )

        x_pos_list = uniform_points_3d[:, 0]
        y_pos_list = uniform_points_3d[:, 1]
        z_pos_list = uniform_points_3d[:, 2]

        cuboid_ids = np.arange(0, len(y_pos_list), 1)
        actors = [[]] * len(y_pos_list)
        name_list = [[]] * len(y_pos_list)

        depth = np.max(feature_dimensions)

        for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
            feature_current = features_list[id]
            actors[id] = DrawTools.draw_filled_grid_3d(
                volume_data=feature_current, coors_3d=(x, y, z)
            )
            name_current = layer_name + ".feature_k_no_" + str(id)
            name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 0, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list

    @staticmethod
    def create_bn_output_actors(
        input_mat: torch.Tensor,
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
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        features_list = LayerInfo.calculate_bn_layer_output(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        num_features = len(features_list)
        feature_dimensions = features_list[0].shape

        height = feature_dimensions[1]
        width = feature_dimensions[2]
        uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
            num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
        )

        x_pos_list = uniform_points_3d[:, 0]
        y_pos_list = uniform_points_3d[:, 1]
        z_pos_list = uniform_points_3d[:, 2]

        cuboid_ids = np.arange(0, len(y_pos_list), 1)
        actors = [[]] * len(y_pos_list)
        name_list = [[]] * len(y_pos_list)

        depth = np.max(feature_dimensions)

        for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
            feature_current = features_list[id]
            actors[id] = DrawTools.draw_filled_grid_3d(
                volume_data=feature_current, coors_3d=(x, y, z)
            )
            name_current = layer_name + ".feature_k_no_" + str(id)
            name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(0, 1, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list

    @staticmethod
    def get_output_actor_names(layer_name: str, num_features: int):
        name_list = [
            layer_name + ".feature_k_no_" + str(id) for id in range(num_features)
        ]

        return name_list

    def update_output_actors_non_linear(
        self,
        input_mat: torch.Tensor,
        layer: (
            nn.Conv1d
            | nn.Conv2d
            | nn.ConvTranspose1d
            | nn.ConvTranspose2d
            | nn.ReLU
            | nn.LeakyReLU
            | nn.Sigmoid
            | nn.Tanh
            | nn.Softmax
            | nn.ELU
            | nn.SELU
            | nn.GELU
            | nn.MaxPool1d
            | nn.MaxPool2d
        ),
        layer_name: str,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        # num_kernels, depth, height, width, weight, bias = LayerInfo.extract_cnn_params(layer=layer,normalize=normalize)
        # num_kernels = layer.out_channels
        features_list = LayerInfo.calculate_layer_output_non_linear(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        if normalize:
            features_list = LayerInfo.normalize_mat(np.array(features_list))
        num_kernels = len(features_list)
        name_list = PlotBuilderNN.get_output_actor_names(
            layer_name=layer_name, num_features=num_kernels
        )
        volume_actors = [self.actor_dict[name] for name in name_list]
        # volume_actors = [actor for actor in actors[0:len(actors)-1]]
        # print(f'debug:1020 {len(volume_actors)} ')
        [
            DrawTools.update_filled_grid_3d(
                volume_actor=actor, updated_volume_data=features_list[id]
            )
            for id, actor in enumerate(volume_actors)
        ]

    def draw_connections(
        self,        
        connections:dict,
        
        ):
        for id,(key,values) in enumerate(connections.items()):
            target_actor_bbox = self.actor_dict[key+'.bounding_box']
            argument_actor_bbx_list = [self.actor_dict[value.name+'.bounding_box'] for value in values if isinstance(value,fx.Node)]
            argument_actor_bbx_list.append(target_actor_bbox)
            #print(f'debug2258: {argument_actor_bbx_list}')
            if argument_actor_bbx_list:
                connection_actor, connection_label_actor  = DrawTools.draw_bounding_box_around_actors(actors=argument_actor_bbx_list,box_name='connect_'+str(id))
                self.actors.append(connection_actor)
                self.actors.append(connection_label_actor)
                #[self.actors.append(x) for x in connection_actor]
                #[self.actors.append(x) for x in connection_label_actor]

        

    @staticmethod
    def create_callable_output_layer(
        input_mat: torch.Tensor,
        layer: Callable,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        input_mat_shape = input_mat.shape

        depth = 10
        output_vals = LayerInfo.calculate_layer_output_callable(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        if normalize:
            output_vals = LayerInfo.normalize_mat(np.array(output_vals))
        # print(f'DEBUG: at 1047 np.array(output_vals).shape  {np.array(output_vals).shape }')
        if len(np.array(output_vals).shape) == 2:
            # output_vals = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            output_cubes = DrawTools.draw_colored_cubes_in_2d_grid(
                cube_colors=output_vals.flatten(), layer_pos=layer_pos, inter_cube_gap=1
            )
            name_list = [layer_name + ".output"]
            actors = [output_cubes]
            depth = 5
        else:
            # output_vals = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            # features_list = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            num_features = len(output_vals)
            feature_dimensions = output_vals[0].shape
            # print(f'DEBUG: at 1059 dimension {feature_dimensions}')
            height = feature_dimensions[1]
            width = feature_dimensions[2]
            uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
                num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
            )

            x_pos_list = uniform_points_3d[:, 0]
            y_pos_list = uniform_points_3d[:, 1]
            z_pos_list = uniform_points_3d[:, 2]

            cuboid_ids = np.arange(0, len(y_pos_list), 1)
            actors = [[]] * len(y_pos_list)
            name_list = [[]] * len(y_pos_list)
            depth = np.max(feature_dimensions)

            for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
                feature_current = output_vals[id]
                actors[id] = DrawTools.draw_filled_grid_3d(
                    volume_data=feature_current, coors_3d=(x, y, z)
                )
                name_current = layer_name + ".feature_k_no_" + str(id)
                name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 1, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list
    
    @staticmethod
    def create_noncallable_output_layer(
        input_mat: torch.Tensor,
        layer,
        layer_name: str,
        layer_pos: float,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        input_mat_shape = input_mat.shape

        depth = 10
        output_vals = LayerInfo.calculate_layer_output_non_callable(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        if normalize:
            output_vals = LayerInfo.normalize_mat(np.array(output_vals))
        # print(f'DEBUG: at 1047 np.array(output_vals).shape  {np.array(output_vals).shape }')
        if len(np.array(output_vals).shape) == 2:
            # output_vals = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            output_cubes = DrawTools.draw_colored_cubes_in_2d_grid(
                cube_colors=output_vals.flatten(), layer_pos=layer_pos, inter_cube_gap=1
            )
            name_list = [layer_name + ".output"]
            actors = [output_cubes]
            depth = 5
        else:
            # output_vals = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            # features_list = LayerInfo.calculate_layer_output_callable(layer=layer,input_mat=input_mat,normalize=normalize)
            num_features = len(output_vals)
            feature_dimensions = output_vals[0].shape
            # print(f'DEBUG: at 1059 dimension {feature_dimensions}')
            height = feature_dimensions[1]
            width = feature_dimensions[2]
            uniform_points_3d = DrawTools.distribute_points_in_2d_grid(
                num_points=num_features, gap_length=(width, height), layer_pos=layer_pos
            )

            x_pos_list = uniform_points_3d[:, 0]
            y_pos_list = uniform_points_3d[:, 1]
            z_pos_list = uniform_points_3d[:, 2]

            cuboid_ids = np.arange(0, len(y_pos_list), 1)
            actors = [[]] * len(y_pos_list)
            name_list = [[]] * len(y_pos_list)
            depth = np.max(feature_dimensions)

            for id, x, y, z in zip(cuboid_ids, x_pos_list, y_pos_list, z_pos_list):
                feature_current = output_vals[id]
                actors[id] = DrawTools.draw_filled_grid_3d(
                    volume_data=feature_current, coors_3d=(x, y, z)
                )
                name_current = layer_name + ".feature_k_no_" + str(id)
                name_list[id] = name_current
        bounding_box, label_actor = DrawTools.draw_bounding_box_around_actors(
            actors=actors, box_name=layer_name, color=(1, 1, 1)
        )
        actors.append(bounding_box)
        actors.append(label_actor)
        name_list.append(layer_name + '.bounding_box')
        return actors, depth, name_list

    @staticmethod
    def get_callable_output_actor_names(
        layer_name: str, num_features: int, out_dim_len: int
    ):
        if out_dim_len == 2:
            name_list = [layer_name + ".output"]
        else:
            name_list = [
                layer_name + ".feature_k_no_" + str(id) for id in range(num_features)
            ]

        return name_list

    def update_output_actors_callable(
        self,
        input_mat: torch.Tensor,
        layer: Callable,
        layer_name: str,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        # num_kernels, depth, height, width, weight, bias = LayerInfo.extract_cnn_params(layer=layer,normalize=normalize)
        # num_kernels = layer.out_channels
        output_vals = LayerInfo.calculate_layer_output_callable(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        if normalize:
            output_vals = LayerInfo.normalize_mat(np.array(output_vals))
        num_kernels = len(output_vals)
        name_list = PlotBuilderNN.get_callable_output_actor_names(
            layer_name=layer_name,
            num_features=num_kernels,
            out_dim_len=len(np.array(output_vals).shape),
        )
        actors = [self.actor_dict[name] for name in name_list]
        # volume_actors = [actor for actor in actors[0:len(actors)-1]]

        if len(np.array(output_vals).shape) == 2:
            DrawTools.update_colored_cubes(
                cube_actor=actors[0], updated_cube_colors=output_vals.flatten()
            )
        else:
            [
                DrawTools.update_filled_grid_3d(
                    volume_actor=actor, updated_volume_data=output_vals[id]
                )
                for id, actor in enumerate(actors)
            ]

    def update_output_actors_non_callable(
        self,
        input_mat: torch.Tensor,
        layer: Callable,
        layer_name: str,
        normalize: bool = True,
        output:torch.Tensor = None
    ):
        # num_kernels, depth, height, width, weight, bias = LayerInfo.extract_cnn_params(layer=layer,normalize=normalize)
        # num_kernels = layer.out_channels
        output_vals = LayerInfo.calculate_layer_output_non_callable(
            layer=layer, input_mat=input_mat, normalize=normalize,output=output
        )
        if normalize:
            output_vals = LayerInfo.normalize_mat(np.array(output_vals))
        num_kernels = len(output_vals)
        name_list = PlotBuilderNN.get_callable_output_actor_names(
            layer_name=layer_name,
            num_features=num_kernels,
            out_dim_len=len(np.array(output_vals).shape),
        )
        actors = [self.actor_dict[name] for name in name_list]
        # volume_actors = [actor for actor in actors[0:len(actors)-1]]

        if len(np.array(output_vals).shape) == 2:
            DrawTools.update_colored_cubes(
                cube_actor=actors[0], updated_cube_colors=output_vals.flatten()
            )
        else:
            [
                DrawTools.update_filled_grid_3d(
                    volume_actor=actor, updated_volume_data=output_vals[id]
                )
                for id, actor in enumerate(actors)
            ]


class PlotNetwork3D:
    def __init__(
        self,
        neural_network: nn.Module,
        stored_network_params_path: str,
        normalize: bool = True,
        plot_type: str = "param",
        test_data: np.memmap = None,
        render_res: tuple = (1024, 1024),
        output_anim_folder:str= "./output_frames/",
        make_animation:bool = False,
        input_image_dim:tuple=(1, 126, 126),
    ):
        self.render_res = render_res
        self.setup_stage()
        self.network = neural_network

        self.stored_network_params_path = stored_network_params_path
        self.normalize = normalize
        self.plot_type = plot_type
        if isinstance( test_data,(np.ndarray,list,torch.Tensor)):
            if isinstance(test_data,(np.ndarray,list)):
                test_data = torch.tensor(test_data,requires_grad=False)
                #test_data = test_data.unsqueeze(0)
            self.test_data = test_data
        else:
            test_data = torch.rand(input_image_dim)

        self.plot_builder = PlotBuilderNN(
            neural_network=neural_network,
            input_image_dim=input_image_dim,
            network_param_path=self.stored_network_params_path,
            normalize=self.normalize,
            plot_type=self.plot_type,
            test_data=test_data,
        )
        self.plot_builder()
        self.add_actors_in_scene()

        self.frame_counter = 0
        self.tiff_writer = vtk.vtkTIFFWriter()
        self.window_to_image_filter = vtk.vtkWindowToImageFilter()

        self.output_tiff_folder = output_anim_folder
        self.tiff_writer.SetFileName(self.output_tiff_folder)
        self.make_animation = make_animation

    def setup_stage(self):
        self._renderer = vtk.vtkRenderer()
        self._renderer.UseDepthPeelingOn()
        #self._renderer.SetAutomaticCulling(vtk.vtkRenderer.FRUSTUM_CULLING_ON)

        self._render_window = vtk.vtkRenderWindow()
        res = self.render_res
        self._render_window.SetSize(*(res))

        self._render_window.SetWindowName("Network Parameter Visualizer")

        self._render_window.AddRenderer(self._renderer)
        self._interactor = vtk.vtkRenderWindowInteractor()
        self._interactor.SetRenderWindow(self._render_window)
        interactor_style = vtk.vtkInteractorStyleTerrain()
        self._interactor.SetInteractorStyle(interactor_style)

        light_0 = vtk.vtkLight()
        light_0.SetLightTypeToSceneLight()
        light_0.SetPosition(0, 50, 100)
        light_0.SetFocalPoint(0, 0, 0)
        light_0.SetColor(1, 1, 1)
        light_0.SetIntensity(1)

        self._renderer.AddLight(light_0)
        light_1 = vtk.vtkLight()
        light_1.SetLightTypeToSceneLight()
        light_1.SetPosition(0, -50, -100)
        light_1.SetFocalPoint(0, 0, 0)
        light_1.SetColor(1, 1, 1)
        light_1.SetIntensity(1)
        self._renderer.AddLight(light_0)
        self._renderer.AddLight(light_1)

    def add_actors_in_scene(self):
        for actor in tqdm(self.plot_builder.actors,desc='Adding actors to renderer'):
            self._renderer.AddActor(actor)
        #self._render_window.Render()
    def __call__(
        self,
        update_with_timer: bool = None,
        timer_interval: int = 5000,
        make_animation: bool = None,
        close_automatically_window:bool=None
    ):  
        if make_animation!=None:
            self.make_animation = make_animation
        #print(f'DEBUG: make anim {self.make_animation}')
        self.update_with_timer = update_with_timer
        self.timer_interval = timer_interval

        self._renderer.SetBackground(0, 0, 0.1)  # Set background color
        self._renderer.ResetCamera()
        self._render_window.Render()
        
        if update_with_timer==True:
            #print('Adding timer event')
            self._interactor.AddObserver("TimerEvent", self.timer_callback)
            self._interactor.CreateRepeatingTimer(self.timer_interval)
        elif update_with_timer==False:
            #print('Adding key press event')
            self._interactor.AddObserver("KeyPressEvent", self.key_press_callback)
        else:
            self.plot_builder()
            self._render_window.Render()             
        
        if close_automatically_window==True:
            self.close_render_window()
        else:
            self._interactor.Start()
        return True

    def update_plot(self,make_animation: bool = None):
        if make_animation!=None:
            self.make_animation = make_animation
        self.plot_builder()
        self._interactor.ProcessEvents()
        if self.make_animation:
            print("capturing frame")
            self.capture_frame()
        self._render_window.Render()       
    
    def key_press_callback(self,obj, event):
        key = obj.GetKeySym()
        print(f"COMMAND: {'Clossing' if key=='q' else 'Updating' if key=='u' else 'press u to update or q to close'}")
        if key == "q":
            self.close_render_window()
        elif key == "u":
            self.update_plot()
        else:
            print(f"No command Key pressed: {key}")

    def close_render_window(self):
        self._render_window.Finalize()
        self._interactor.TerminateApp()       
        self._render_window.SetWindowName("Closed Window")    

    def timer_callback(self, obj, event):
        self.plot_builder()
        if self.make_animation:
            print("capturing frame")
            self.capture_frame()
        self._render_window.Render()

    def capture_frame(self):
        self.window_to_image_filter.SetInput(self._render_window)
        self.window_to_image_filter.Modified()
        self.window_to_image_filter.ReadFrontBufferOff()
        self.window_to_image_filter.Update()
        frame_filename = (
            self.output_tiff_folder + f"frame_{self.frame_counter:03d}.tiff"
        )
        self.tiff_writer.SetFileName(frame_filename)
        self.tiff_writer.SetInputConnection(self.window_to_image_filter.GetOutputPort())
        self.tiff_writer.Write()
        print(f"Saved frame {self.frame_counter} as {frame_filename}")
        self.frame_counter += 1
