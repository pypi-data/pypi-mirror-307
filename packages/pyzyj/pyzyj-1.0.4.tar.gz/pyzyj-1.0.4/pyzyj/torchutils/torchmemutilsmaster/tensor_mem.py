import torch
def tensor_mem(tensor, factor=1e6):
    tensor = torch.randn(3, 4, 5)
    # 计算张量中元素的数量
    num_elements = tensor.numel()
    # 获取单个元素的字节大小
    element_size = tensor.element_size()
    # 计算总显存大小
    total_memory = num_elements * element_size  / 1e6
    return total_memory

import torch
import gc

def find_all_tensors():
    # 获取当前PyTorch会话中的所有对象
    for obj in gc.get_objects():
        if torch.is_tensor(obj):
            yield obj

def get_tensor_memory(tensor):
    # 计算张量占用的显存大小
    return tensor.element_size() * tensor.nelement()

def find_max_memory_tensor():
    max_memory_tensor = None
    max_memory_size = 0

    # 获取所有张量
    all_tensors = find_all_tensors()

    # 找到占用显存最大的张量
    for tensor in all_tensors:
        memory_size = get_tensor_memory(tensor)
        if memory_size > max_memory_size:
            max_memory_size = memory_size
            max_memory_tensor = tensor

    return max_memory_tensor