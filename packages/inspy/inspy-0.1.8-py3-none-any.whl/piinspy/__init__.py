# -*- encoding: utf-8 -*-
"""
    @File: __init__.py.py \n
    @Contact : yafei.wang@pisemi.com \n
    @License: (C)Copyright {} \n
    @Modify Time: 2023/11/20 10:01 \n
    @Author : Pisemi Yafei Wang \n
    @Version: 1.0 \n
    @Description : None \n
    @Create Time: 2023/11/20 10:01 \n
"""
from piinspy.ins_class import PiIns
from piinspy.insconst import *


def ins_scan(pInsrm):
    """
    scan the instrument automatically
    :param pInsrm: pyvsia object
    :return: instrument class, name and port dict
    """
    ins_visa_dict = {}
    for i in pInsrm.list_resources():
        ''' ::0:: unconnected ins ASRL3,ASEL4 Bluetooth COM ports '''

        if "::0::" in i or "ASRL3::INSTR" in i or "ASRL4::INSTR" in i:
            pass
        else:
            # print("scan", i)
            ins = pInsrm.open_resource(i)
            ins.read_termination = "\n"
            ins.timeout = 5000
            try:
                try:
                    ins_info = ins.query("*IDN?")
                except Exception as e:
                    print("query", e)
                for k in insconst.ins_all_dict:
                    for j in insconst.ins_all_dict[str(k)]:
                        if j in str(ins_info):
                            print(k, j, i, ins_info)
                            ins_visa_dict.update({i: {k: j}})

                ins.close()
            except Exception as result:
                print(result)
    print(ins_visa_dict)
    id_list = list(ins_visa_dict.keys())
    print(id_list)
    ins_list = []
    for ins in id_list:
        ins_list.append(PiIns(pInsrm, list(ins_visa_dict[ins].keys())[0],
                              ins_visa_dict[ins][list(ins_visa_dict[ins].keys())[0]], ins))

    for index, ins in enumerate(ins_list):
        temp_type = ins.pInsType
        if index >= 1:
            if temp_type == ins_list[index - 1].pInsType:
                ins.index += 1

    power_list = []
    dmm_list = []
    smu_list = []
    load_list = []

    for ins in ins_list:
        if ins.pInsType == "POWER":
            power_list.append(ins)
        elif ins.pInsType == "DMM":
            dmm_list.append(ins)
        elif ins.pInsType == "SMU":
            smu_list.append(ins)
        elif ins.pInsType == "LOAD":
            load_list.append(ins)

    return power_list, dmm_list, smu_list, load_list
