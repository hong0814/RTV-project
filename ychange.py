import glob
import re
import os
import pandas as pd
import random
from konlpy.tag import Mecab
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--shuffle_ratio', type=float, default=0.0, help='Shuffle ratio')
parser.add_argument('--josa', type=bool, default=False, help='random without josa')
parser.add_argument('--punctuation', type=bool, default=False, help='random without punctuation')

args = parser.parse_args()

mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")

before_mapping_dict = {'1': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETECT.csv'],
  'summary': './RTV_data/비정형모의전장자료/1. 수시상황보고서',
  'key': [],
  'threshold': {}},
 '2': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_FIRE_SAM.csv',
   './RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETONATION_SAM.csv'],
  'summary': './RTV_data/비정형모의전장자료/3. 지대공 미사일 사격 보고서',
  'key': [['SIMULATIONID', 'TARGET_MSN_NO']],
  'threshold': {}},
 '3': {'csv_file': ['./RTV_data/정형모의전장자료/new_CSV/T_AIRFORCE_DETECT.csv'],
  'summary': './RTV_data/비정형모의전장자료/2. 적기 공격 임박 보고서',
  'key': [],
  'threshold': {'C_AIRFORCE_DETECT_TARGET_RANGE': 30}}}

# 조사 제거 
def delete_josa(text):       
    token=mecab.pos(text)    
    token=[t[0] for t in token if t[1][0]=='J']
    for i in range(len(token)):
        text=text.replace(token[i], '', 1).strip()
        # text=re.sub(token[i],'',text).strip()
    return text

# !, 제거
def delete_punctuation(text):
    text = re.sub('[!,]', '', text)
    return text

# 순서 변경
class generate_01:
    def __init__(self, gold, iter_ratio): # Input : 보고서, 섞는 횟수, 몇개 생성할지
        
        self.sents = gold
        self.ratio = max(1, int(iter_ratio * len(gold)))
        
    
    def split_sent(self, doc): 
        reObj = re.compile(r'[,!]') # ,와 !로 문장 split 
        temp_sents = reObj.split(doc)
        temp_sents[2:4] = ["".join(temp_sents[2:4])] # 문장이 섞이면 안되는 부분 붙혀줌
        temp_sents[0] = temp_sents[0] + "!" # 첫 번째 문장 ! 붙혀줌
        return temp_sents
 
    def random_swap(self, words, n): # 섞는 부분
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)

        return new_words

    def swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random_idx_1
        counter = 0

        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words)-1)
            counter += 1
            if counter > 3:
                return new_words

        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words        

    def shuf_gold(self): # 동작 코드
        self.tot_shuf = []
        split_gold = self.split_sent(self.sents)
        
        shuf = self.random_swap(split_gold[1:-1], self.ratio)
        shuf.insert(0, split_gold[0]) # 맨 앞 OOO보고! 부분 앞에 붙히기
        shuf.append(split_gold[-1]) # OOO로 식별합니다 마지막에 붙힘.
        self.tot_shuf.append(shuf)
        
        return list(map(list,list(set(map(tuple,self.tot_shuf))))) # 마지막 중복해서 생성된 보고서 제거해서 return

class generate_02:
    def __init__(self, gold, iter_ratio): # Input : 보고서, 섞는 횟수, 몇개 생성할지
        
        self.sents = gold
        self.ratio = max(1, int(iter_ratio * len(gold)))
    
    def split_sent(self, doc):
        reObj = re.compile(r'[,!]') # ,와 !로 문장 split 
        temp_sents = reObj.split(doc)[:-1]
        #temp_sents[2:4] = ["".join(temp_sents[2:4])]
        temp_sents[0] = temp_sents[0] + "!" # 첫 번째 문장 ! 붙혀줌
        return temp_sents
 
    def random_swap(self, words, n): # 섞는 부분
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)

        return new_words

    def swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random_idx_1
        counter = 0

        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words)-1)
            counter += 1
            if counter > 3:
                return new_words

        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words        

    def shuf_gold(self): # 동작 코드
        self.tot_shuf = []
        split_gold = self.split_sent(self.sents)

        shuf = self.random_swap(split_gold[1:], self.ratio)
        shuf.insert(0, split_gold[0]) # 맨 앞 OOO보고! 부분 앞에 붙히기
        self.tot_shuf.append(shuf)

        return list(map(list,list(set(map(tuple,self.tot_shuf)))))

if __name__ == "__main__":

    processed_dir = './txt_processed2/'
    if not os.path.exists(processed_dir):
        os.mkdir(processed_dir)

    # 수시상황보고서
    print("Start Generating 수시상황보고서")
    processed_dir_1 = processed_dir + '1. 수시상황보고서/'
    if not os.path.exists(processed_dir_1):
        os.mkdir(processed_dir_1)
    
    pth = list(before_mapping_dict.values())[0]
    total = glob.glob(pth['summary']+"/*")
    for txt_file in total :
        with open(txt_file, 'r', encoding = 'UTF-8') as f:
            tmp = f.read()
            tmp = tmp[3:]
            tmp = re.sub('\n','',tmp).strip()  # \n 제거
            tmp = re.sub('Z','',tmp).strip()  # Z 제거
            tmp = tmp.replace('도', ' 도')  # 도 앞에 띄어쓰기
            tmp = tmp.replace('기가', ' 기가')  # 기가 앞에 띄어쓰기
            tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
            tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
            tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
            tmp = tmp.replace('속 도로', '속도로')  # 속 도 띄어쓰기 제거
            tmp = tmp.replace('(으)로', ' 로')  # (으)로 앞에 띄어쓰기
            tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
            if args.shuffle_ratio > 0:
                tmp = generate_01(re.sub('\n','',tmp).strip(),args.shuffle_ratio).shuf_gold()
                tmp = '\t'.join(str(s) for s in tmp[0]) + '\n'
            if args.josa:
                if random.random() > 0.5:
                    tmp = delete_josa(tmp)
            if args.punctuation:
                if random.random() > 0.5:
                    tmp = delete_punctuation(tmp)
            

        ff = open('{}/{}'.format(processed_dir_1, txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
        ff.write(tmp)
        ff.close()
    print("Finish Generating 수시상황보고서")

    # 지대공 미사일 사격 보고서 
    print("Start Generating 지대공 미사일 사격 보고서")
    processed_dir_3 = processed_dir + '3. 지대공 미사일 사격 보고서/'
    if not os.path.exists(processed_dir_3):
        os.mkdir(processed_dir_3)
   
    pth = list(before_mapping_dict.values())[1]
    total = glob.glob(pth['summary']+"/*")
    for txt_file in total :
        with open(txt_file, 'r', encoding = 'UTF-8') as f:
            tmp = f.read()
            tmp = tmp[3:]
            tmp = re.sub('\n','',tmp).strip()  # \n 제거
            tmp = tmp.replace('발', ' 발')  # 발 앞에 띄어쓰기
            tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
            tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
            tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
            tmp = tmp.replace('로', ' 로')  # 로 앞에 띄어쓰기
            tmp = tmp.replace('에', ' 에')  # 에 앞에 띄어쓰기
            tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
            if args.josa:
                if random.random() > 0.5:
                    tmp = delete_josa(tmp)
            if args.punctuation:
                if random.random() > 0.5:
                    tmp = delete_punctuation(tmp)

        ff = open('{}/{}'.format(processed_dir_3, txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
        ff.write(tmp)
        ff.close()
    print("Finish Generating 지대공 미사일 사격 보고서")

    # 적기 공격 임박 보고서
    print("Start Generating 적기 공격 임박 보고서")
    processed_dir_2 = processed_dir + '2. 적기 공격 임박 보고서/'
    if not os.path.exists(processed_dir_2):
        os.mkdir(processed_dir_2)
    
    pth = list(before_mapping_dict.values())[2]
    total = glob.glob(pth['summary']+"/*")
    for txt_file in total :
        with open(txt_file, 'r', encoding = 'UTF-8') as f:
            tmp = f.read()
            tmp = tmp[3:]
            tmp = re.sub('\n','',tmp).strip()  # \n 제거
            tmp = tmp.replace('대', ' 대')  # 발 앞에 띄어쓰기
            tmp = tmp.replace(' 오전 ', '오전')  # 오전 앞뒤 띄어쓰기 제거
            tmp = tmp.replace(' 오후 ', '오후')  # 오후 앞뒤 띄어쓰기 제거
            tmp = tmp.replace('오후4', '오후04')  # 04시로 변경
            tmp = tmp.replace('로', ' 로')  # 로 앞에 띄어쓰기
            tmp = tmp.replace(',', ' ,')  # , 앞에 띄어쓰기
            if args.shuffle_ratio > 0:
                tmp = generate_02(re.sub('\n','',tmp).strip(),args.shuffle_ratio).shuf_gold()
                tmp = '\t'.join(str(s) for s in tmp[0]) + '\n'
            if args.punctuation:
                if random.random() > 0.5:
                    tmp = delete_punctuation(tmp)
            

        ff = open('{}/{}'.format(processed_dir_2, txt_file.split('\\')[1]), 'wt', encoding = 'UTF-8')
        ff.write(tmp)
        ff.close()
    print("Finish Generating 적기 공격 임박 보고서")