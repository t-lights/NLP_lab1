from tqdm import tqdm

def generateSegment(ori_paths=['file/origin/199801_seg&pos.txt',
                               'file/origin/199802.txt',
                               'file/origin/199803.txt'],
                    train_path='file/segment/train.txt',
                    truth_path='file/segment/truth.txt', 
                    test_path='file/segment/test.txt',
                    k_max=7,
                    k_num=0):
    '''
    同时生成训练集与测试集以及测试集的groundTruth,各文件%10=0的行取为测试集
    '''
    truth_file = open(truth_path, 'w', encoding='utf-8')
    train_file = open(train_path, 'w', encoding='utf-8')
    test_file = open(test_path, 'w', encoding='utf-8')
    for ori_path in ori_paths:
        with open(ori_path, 'r', encoding='gbk') as f:
            ori_lines = f.readlines()
        for i, line in enumerate(ori_lines):
            if i % k_max != k_num:
                train_file.write(line)
            else:
                words = line.split()
                test_line = ''
                truth_line = ''
                for word in words:
                    word = word[1 if word[0] == '[' else 0:word.index('/')]
                    test_line += word
                    truth_line += word + '/ '
                test_line += '\n'
                truth_line += '\n'
                test_file.write(test_line)
                truth_file.write(truth_line)
    truth_file.close()
    train_file.close()
    test_file.close()


def generateDict(train_path='file/segment/train.txt', dict_path='file/segment/dict.txt'):
    '''
    由训练集生成词典,时间戳虽然作为数词/m在词表里出现,但是此处考虑不加入词典
    '''
    max_length = 0  #最大词长
    word_set = set()
    with open(train_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        words = line.split()
        words = words[1:]   # 考虑略去时间戳数词
        for word in words:
            word = word[1 if word[0] == '[' else 0:word.index('/')]  # 去掉两个空格之间的非词字符
            word_set.add(word)  # 将词加入词典集合, 去重
            max_length = len(word) if len(word) > max_length else max_length
    word_list = list(word_set)
    word_list.sort()    # 按字典序排序
    with open(dict_path, 'w', encoding='utf-8') as dict_file:
        dict_file.write('\n'.join(word_list))
    return word_list, max_length

def outputLine(line=''):
    punc = '/.-'
    buffer = ''
    result = ''
    words = line.split('/ ')
    for i, word in enumerate(words):
        if word == '':
            continue
        if word.isascii() or (word in punc):
            buffer += word
            if i + 1 == len(words):
                result += buffer + '/ '
        else:
            if buffer:
                result += buffer + '/ '
                buffer = ''
            result += word + '/ '
    return result

def preprocessScoreLine(seg_path):
    with open(seg_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    seg_list = []
    for line in lines:
        if line == '\n':
            continue
        new_line = ''
        for word in line.split():
            new_line += word[1 if word[0] == '[' else 0:word.index('/')] + '/ '
        seg_list.append(new_line)
    return seg_list

def score(truth_path='', result_path=''):
    truth_num = 0
    result_num = 0
    right_num = 0
    truth_lines = preprocessScoreLine(truth_path)
    result_lines = preprocessScoreLine(result_path)
    for i, line in enumerate(truth_lines):
        truth_words = line.split('/ ')
        result_words = result_lines[i].split('/ ')
        truth_size = len(truth_words) - 1
        truth_num += truth_size
        result_size = len(result_words) - 1
        result_num += result_size
        j = 0
        k = 0
        num1, num2 = len(truth_words[0]), len(result_words[0])
        while j < truth_size and k < result_size:
            if num1 == num2:
                right_num += 1
                if j == truth_size - 1:
                    break
                j += 1
                k += 1
                num1 += len(truth_words[j])
                num2 += len(result_words[k])
            else:
                while True and j < truth_size and k < result_size:
                    if num1 < num2:
                        j += 1
                        num1 += len(truth_words[j])
                    elif num1 > num2:
                        k += 1
                        num2 += len(result_words[k])
                    else:
                        if j < truth_size - 1:
                            num1 += len(truth_words[j + 1])
                            num2 += len(result_words[k + 1])
                        j += 1
                        k += 1
                        break
    precision = right_num / float(truth_num)
    recall = right_num / float(result_num)
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def outputScore(score_path='file/output/score.txt',
          truth_path='file/segment/truth.txt',
          fmm_path='file/output/seg_FMM.txt',
          bmm_path='file/output/seg_BMM.txt'):
    output = '本轮运行结果\n'
    precision, recall, f1 = score(truth_path, fmm_path)
    output += 'FMM\n Precision: '+str(precision*100)\
              +'%\tRecall:'+str(recall*100)\
              +'%\tF1:'+str(f1*100)+'\n\n'
    precision, recall, f1 = score(truth_path, bmm_path)
    output += 'BMM\n Precision: '+str(precision*100)\
              +'%\tRecall:'+str(recall*100)\
              +'%\tF1:'+str(f1*100)+'\n\n-----------------------------------------------------------------------------------------------------------\n'
    print(output)
    with open(score_path, 'a', encoding='utf-8') as f:
        f.write(output)
    return precision, recall, f1

if __name__ == '__main__':
    generateSegment(test_path='test.txt', train_path='train.txt', truth_path='truth.txt',k_max=40, k_num=0)
    # generateDict()