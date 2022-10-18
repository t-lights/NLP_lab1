import imp
from time import time
from Tokenization_prototype import Tokenization_prototype
from Tokenization_BinarySearch import Tokenization_BinarySearch
from utils import outputScore, generateDict, generateSegment

def test_k(k_max, model, time_path):
    precision = float(0)
    recall = float(0)
    f1 = float(0)
    for i in range(k_max):
        generateSegment(k_max=k_max, k_num=i)
        generateDict()
        output = ''
        print("运行FMM\n")
        start_time = time()
        model.fmm()
        fmm_time = time()
        print("FMM耗时: "+str(fmm_time - start_time)+'s\n')
        output += "FMM耗时: "+str(fmm_time - start_time)+'s\n'

        print("运行BMM\n")
        start_time = time()
        model.bmm()
        bmm_time = time()
        print("BMM耗时: "+str(bmm_time - fmm_time)+'s\n')
        output += "BMM耗时: "+str(bmm_time - fmm_time)+'s\n'
        output += "--------------------------------------------------------------------------"
        with open(time_path, 'a', encoding='utf-8') as f:
            f.write(output)
        _p, _r, _f = outputScore()
        precision+=_p
        recall+=_r
        f1+=_f
    precision /= float(k_max)
    recall /= float(k_max)
    f1 /= float(k_max)
    output = '本次'+str(k_max)+'折测试结果\nPrecision_mean: '+str(precision)+'\tRecall_mean: '+str(recall)+'\tF1: '+str(f1)
    print(output)
    with open('file/output/score.txt', 'a', encoding='utf-8') as f:
        f.write(output)

def test_script():
    model_flag = input("测试哪个分词模型?\n1 Tokenization_prototype\n2 Tokenization_BinarySearch\n")
    k_flag = input("是否进行k折测试?\n0 仅取7的倍数行作为测试集\n大于0的整数k 进行k折测试\n")
    time_path = 'file/output/time.txt'
    output = ''
    if model_flag == '1':
        model = Tokenization_prototype()
    elif model_flag == '2':
        model = Tokenization_BinarySearch()
    else:
        raise ValueError("模型编号不存在")
    if k_flag != '0':
        test_k(int(k_flag), model, time_path)
        return
    generateSegment()
    generateDict()
    print("运行FMM\n")
    start_time = time()
    model.fmm()
    fmm_time = time()
    print("FMM耗时: "+str(fmm_time - start_time)+'s\n')
    output += "FMM耗时: "+str(fmm_time - start_time)+'s\n'
    print("运行BMM\n")
    model.bmm()
    bmm_time = time()
    print("BMM耗时: "+str(bmm_time - fmm_time)+'s\n')
    output += "BMM耗时: "+str(bmm_time - fmm_time)+'s\n'
    output += "--------------------------------------------------------------------------"
    with open(time_path, 'a', encoding='utf-8') as f:
        f.write(output)       
    outputScore()

if __name__ == '__main__':
    test_script()