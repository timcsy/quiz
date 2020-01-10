import json
import pandas as pd
import os
import sys
import math
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Spearman-Brown 折半信度計算 function
def sb(df, first, second):
    sum_first = df[first].sum(axis=1) # 第一部分的分數總和
    sum_second = df[second].sum(axis=1) # 第二部分的分數總和
    r_half = sum_first.corr(sum_second) # 第一部分和第二部分的相關係數
    r_SB = 2 * r_half / (1 + r_half) # 使用 Spearman-Brown formula 對相關係數做修正
    r_total = sum_first.cov(sum_second) * 4 / df.sum(axis=1).var() # 第一部分和第二部分的共變數除上全體的標準差
    return r_SB # 回傳修正結果

# Guttman 折半信度計算 function
def guttman(df, first, second):
    Var_first = df[first].sum(axis=1).var() # 第一部分分數的變異數
    Var_second = df[second].sum(axis=1).var() # 第二部分分數的變異數
    Var_all = df[first + second].sum(axis=1).var() # 分數總和的變異數
    return 2 * (1 - (Var_first + Var_second) / Var_all) # 回傳體結果

def split(test, static_dir, first, second, print_result = False):
    path = os.path.join(static_dir, test)
    url = '/' + os.path.relpath(path, os.path.join(os.getcwd(), 'static'))
    output = {
        'id': test,
        'url': url,
        'files': {}
    }

    if print_result:
        print(path)
        print()
    split_path = os.path.join(path, 'split')
    if not os.path.exists(split_path):
        os.makedirs(split_path)

    responses = pd.read_csv(os.path.join(path, 'responses.csv'), index_col = 0)
    right = pd.read_csv(os.path.join(path, 'right.csv'), index_col = 0)

    split_sb = sb(right, first, second)
    split_guttman = guttman(right, first, second)
    split = 'Spearman-Brown 折半信度 = {:.3f}\r\n'.format(split_sb)
    split += '測量標準誤 (SEM) = {:.2f}\r\n\r\n'.format(responses['Score'].std() * math.sqrt(1 - split_sb))
    split += 'Guttman 折半信度 = {:.3f}\r\n'.format(split_guttman)
    split += '測量標準誤 (SEM) = {:.2f}'.format(responses['Score'].std() * math.sqrt(1 - split_guttman))

    question_text = '第一部分： ' + ', '.join(first) + '\r\n第二部分： ' + ', '.join(second) + '\r\n'
    now = datetime.now()
    filename = 'split_' + now.strftime("%Y%m%d_%H%M%S_%f") + '.txt'
    with open(os.path.join(split_path, filename), 'w+') as f:
        f.write(question_text + '\r\n' + split)
    if print_result:
        print(question_text + '\r\n' + split)
    output['splitResult'] = split
    output['files']['splitResult'] = url + '/split/' + filename

    return output

if __name__ == '__main__':
    test = sys.argv[1] if len(sys.argv) > 1 else ''
    path = os.path.relpath(sys.argv[2] if len(sys.argv) > 2 else '.')
    first = json.loads(sys.argv[3] if len(sys.argv) > 3 else '[]')
    second = json.loads(sys.argv[4] if len(sys.argv) > 4 else '[]')
    print(json.dumps(split(test, path, first, second, print_result=False)))