import subprocess
from termcolor import colored
from tqdm import tqdm
import torch
import argparse


def run_commands_in_parallel(commands):
    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()

def split_list(input_list, K):
    return [input_list[i:i+K] for i in range(0, len(input_list), K)]



if __name__ == '__main__':
    # with graph pool
    torch.cuda.empty_cache()

    num_cmds = 1
    cmd_biao = '/root/miniconda3/envs/td3/bin/python /root/td3-ddpg/main.py'
    cmds =[]
    seeds = [857,7465,673,5431,3081]
    envs= [" Walker2d-v3"," Ant-v3"," Humanoid-v3"," Hopper-v3"]
    for seed in seeds:
        for env in envs:
            cmd = cmd_biao+" --seed {} --env{} ".format(seed,env)
            cmds.append(cmd)
          
    commands_batches = split_list(cmds,num_cmds)

    cnt = 0
    for commands in tqdm(commands_batches):
        cnt +=1
        print (colored(f"--------current progress: {cnt} out of {len(commands_batches)}---------", 'blue','on_white'))
        run_commands_in_parallel(commands)