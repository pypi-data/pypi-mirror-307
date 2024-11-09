"""shared utils in base utils"""
import time
import subprocess as sp
from .info import Info

def get_gpu_memory(gpu_num=None):
    """
    Get GPU used memory and total memory (util is MB)
    fork from https://stackoverflow.com/questions/67707828/how-to-get-every-seconds-gpu-usage-in-python
    @Vivasvan Patel
    """
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    split_memory = lambda memory_info: [int(x.split()[0]) for i, x in enumerate(memory_info)]
    command_used = "nvidia-smi --query-gpu=memory.used --format=csv"
    command_total = "nvidia-smi --query-gpu=memory.total --format=csv"
    try:
        memory_used_info = output_to_list(sp.check_output(command_used.split(),stderr=sp.STDOUT))[1:]
        memory_total_info = output_to_list(sp.check_output(command_total.split(),stderr=sp.STDOUT))[1:]
        memory_used_mb = split_memory(memory_used_info)
        memory_total_mb = split_memory(memory_total_info)
    except sp.CalledProcessError:
        memory_used_mb = [0]*1024
        memory_total_mb = [0]*1024
        Info.warn(f"Failed to run command:\n\t{command_used}\n\t{command_total}\nPlease check it.")

    if gpu_num is None:
        return (memory_used_mb, memory_total_mb)
    elif isinstance(gpu_num, int):
        memory_used_mb_ = memory_used_mb[gpu_num]
        memory_total_mb_ = memory_total_mb[gpu_num]
        return (memory_used_mb_, memory_total_mb_)
    elif isinstance(gpu_num, list):
        memory_used_mb_ = [memory_used_mb[i] for i in gpu_num]
        memory_total_mb_ = [memory_used_mb[i] for i in gpu_num]
        return (memory_used_mb_, memory_total_mb_)
    else:
        raise TypeError(f"Assert type(gpu_num) in (None, int, list), but get {type(gpu_num)}.")

class TimeStatistic:
    """easy way to statistic time, like tic and toc in MATLAB"""
    def __init__(self) -> None:
        self.start_flag = False
        self.data = []
        self.num = []
        self.tmp_start_time = None
    
    def start(self):
        """start timer (like tic in MATLAB)"""
        assert not self.start_flag
        self.start_flag = True
        self.tmp_start_time = time.time()
    
    def stop(self):
        """stop timer (like toc in MATLAB)"""
        assert self.start_flag
        now_time = time.time()

        delta_time = now_time - self.tmp_start_time
        self.data.append(delta_time)

        self.start_flag = False
    
    def step(self, step_num=1):
        """step timer (like toc in MATLAB)"""
        self.num.append(step_num)
    
    def clear(self):
        """clear all timer"""
        self.start_flag = False
        self.data = []
        self.num = []
        self.tmp_start_time = None

    def statistic(self, statistic_type="avg"):
        """get statistic"""
        assert statistic_type in ["avg", "sum"]

        sum_time = sum(self.data)
        sum_num = sum(self.num)

        if statistic_type == "avg":
            return_data = sum_time / sum_num
        elif statistic_type == "sum":
            return_data = sum_time
        else:
            raise TypeError()
        
        return return_data
