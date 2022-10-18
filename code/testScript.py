import imp
from time import time
from Tokenization_prototype import Tokenization_prototype
from Tokenization_BinarySearch import Tokenization_BinarySearch
from utils import outputScore, generateDict, generateSegment

def test_script():
    flag = input("测试哪个部分?(2 or 4)\n")
    time_path = 'file/output/time.txt'
    output = ''
    if flag == '2':
        model = Tokenization_prototype()
    if flag == '4':
        model = Tokenization_BinarySearch()
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

if __name__ == '__main__':
    # test_script()
    outputScore()