import os
import torch
import torch.nn as nn
#import ray;num_cpus = os.cpu_count()
from typing import Callable


# def initialize_ray():
#     if ray.is_initialized():
#         ray.shutdown()
#         ray.init(num_cpus=num_cpus)
    
# def put_as_handle_for_rayop(val):
#     val_handle = ray.put(val)
#     return val_handle


#@ray.remote(num_cpus=1)
def run_gen_parallel_method(func, **kwargs):
    return func(**kwargs)



def make_output_actors_from_layer(idx:int,name:str, layer:nn.Module|Callable,output:torch.Tensor):

    pass