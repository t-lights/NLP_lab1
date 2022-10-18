from tqdm import tqdm
import utils

class Tokenization_BinarySearch():
    max_length = 0
    word_list = []
    def __init__(self, dict_path='file/segment/dict.txt') -> None:
        with open(dict_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            self.word_list.append(line[:-1]) # 去\n
            if len(line) - 1 > self.max_length:
                self.max_length = len(line) - 1

    def search(self, word=''):
        left = 0
        right = len(self.word_list) -1
        while left < right - 1:
            mid = int((left + right) / 2)
            if word > self.word_list[mid]:
                left = mid
            elif word < self.word_list[mid]:
                right = mid
            elif word == self.word_list[mid]:
                return True
        return False
            

    def fmm(self, test_path='file/segment/test.txt', result_path='file/output/seg_FMM.txt'):
        with open(test_path, 'r', encoding='utf-8') as f:
            test_lines = f.readlines()
        with open(result_path, 'w', encoding='utf-8') as result:
            for line in tqdm(test_lines):
                result_line = ''
                line = line.strip()
                while len(line) > 0:
                    word_try = line[0:len(line) if len(line) < self.max_length else self.max_length]
                    while self.search(word_try) == False and (len(word_try) > 1):
                        word_try = word_try[:-1]
                    line = line[len(word_try):]
                    result_line += word_try + '/ '
                result.write(utils.outputLine(line=result_line) + '\n')

    def bmm(self, test_path='file/segment/test.txt', result_path='file/output/seg_BMM.txt'):
        with open(test_path, 'r', encoding='utf-8') as f:
            test_lines = f.readlines()
        with open(result_path, 'w', encoding='utf-8') as result:
            for line in tqdm(test_lines):
                line = line.strip()
                result_list = []
                while len(line) > 0:
                    if len(line) < self.max_length:
                        word_try = line
                    else:
                        word_try = line[-self.max_length:]
                    while self.search(word_try) == False and len(word_try) > 1:
                        word_try = word_try[1:]
                    result_list.append(word_try + '/ ')
                    line = line[:-len(word_try)]
                result_list.reverse()
                result.write(utils.outputLine(''.join(result_list)) + '\n')
