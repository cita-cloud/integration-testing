#!/usr/bin/env python
#
# Copyright Rivtower Technologies LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess, sys, json, time

if __name__ == "__main__":
    # emergency-brake default is off
    # check it with send tx
    cmd = "cldi -c default create 6080604052348015600f57600080fd5b50603580601d6000396000f3006080604052600080fd00a165627a7a7230582046766cd5070278ffbc2c4e4c4440283d2f56a8ffb73b0f93eb52fc092a6fa15a0029"
    tx_hash = subprocess.getoutput(cmd)
    print("send tx ret: ", tx_hash)
    if not len(tx_hash) == 66 or not tx_hash.__contains__("0x"):
        print("send tx failed!")
        exit(10)

    for i in range(3):
        time.sleep(6 * (i + 1))

        cmd = "cldi -c default get receipt {}"
        cmd_result = subprocess.getoutput(cmd.format(tx_hash))
        if not cmd_result.__contains__("Error"):
            break
        if i == 2:
            print("get receipt failed!", cmd_result)
            exit(20)

    tx_receipt = json.loads(cmd_result)
    if len(tx_receipt['error_msg']) != 0:
        print("receipt has error!", tx_receipt)
        exit(30)        

    # turn on emergency-brake
    cmd = "cldi -c default -u admin admin emergency-brake on"
    tx_hash = subprocess.getoutput(cmd)
    print("turn on emergency-brake ret:", tx_hash)

    if not len(tx_hash) == 66 or not tx_hash.__contains__("0x"):
        print("turn on emergency-brake failed!")
        exit(40)

    for i in range(3):
        time.sleep(6 * (i + 1))

        cmd = "cldi -c default get tx {}"
        cmd_result = subprocess.getoutput(cmd.format(tx_hash))
        if not cmd_result.__contains__("Error"):
            break
        if i == 2:
            print("get turn on emergency-brake tx failed!", cmd_result)
            exit(50)

    # check emergency_brake in system-config
    cmd = "cldi -c default get system-config"
    cmd_result = subprocess.getoutput(cmd)
    system_config = json.loads(cmd_result)
    
    if system_config['emergency_brake'] == False:
        print("emergency-brake is also off!", system_config)
        exit(60)
    
    if system_config['emergency_brake_pre_hash'] != tx_hash:
        print("emergency_brake tx hash mismatch!", system_config)
        exit(70)

    # check emergency_brake with send tx
    cmd = "cldi -c default create 6080604052348015600f57600080fd5b50603580601d6000396000f3006080604052600080fd00a165627a7a7230582046766cd5070278ffbc2c4e4c4440283d2f56a8ffb73b0f93eb52fc092a6fa15a0029"
    result = subprocess.getoutput(cmd)
    if not result.__contains__("Error"):
        print("emergency-brake is also off!", result)
        exit(80)

    # turn off emergency-brake
    cmd = "cldi -c default -u admin admin emergency-brake off"
    tx_hash = subprocess.getoutput(cmd)
    print("turn off emergency-brake ret:", tx_hash)

    if not len(tx_hash) == 66 or not tx_hash.__contains__("0x"):
        print("turn off emergency-brake failed!")
        exit(90)

    for i in range(3):
        time.sleep(6 * (i + 1))

        cmd = "cldi -c default get tx {}"
        cmd_result = subprocess.getoutput(cmd.format(tx_hash))
        if not cmd_result.__contains__("Error"):
            break
        if i == 2:
            print("get turn off emergency-brake tx failed!", cmd_result)
            exit(100)

    # check emergency_brake in system-config
    cmd = "cldi -c default get system-config"
    cmd_result = subprocess.getoutput(cmd)
    system_config = json.loads(cmd_result)
    
    if system_config['emergency_brake'] == True:
        print("emergency-brake is also on!", system_config)
        exit(110)
    
    if system_config['emergency_brake_pre_hash'] != tx_hash:
        print("emergency_brake tx hash mismatch!", system_config)
        exit(120)


    # check with send tx
    cmd = "cldi -c default create 6080604052348015600f57600080fd5b50603580601d6000396000f3006080604052600080fd00a165627a7a7230582046766cd5070278ffbc2c4e4c4440283d2f56a8ffb73b0f93eb52fc092a6fa15a0029"
    tx_hash = subprocess.getoutput(cmd)
    print("send tx ret: ", tx_hash)
    if not len(tx_hash) == 66 or not tx_hash.__contains__("0x"):
        print("send tx failed!")
        exit(130)

    for i in range(3):
        time.sleep(6 * (i + 1))

        cmd = "cldi -c default get receipt {}"
        cmd_result = subprocess.getoutput(cmd.format(tx_hash))
        if not cmd_result.__contains__("Error"):
            break
        if i == 2:
            print("get receipt failed!", cmd_result)
            exit(20)

    tx_receipt = json.loads(cmd_result)
    if len(tx_receipt['error_msg']) != 0:
        print("receipt has error!", tx_receipt)
        exit(150)  

    exit(0)
