import json
import pandas as pd
import math
import os
import sys
import string
import random
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
sns.set(style='darkgrid')

# Alpha
# Cronbach's alpha 信度的 function
def alpha(df):
    Var = df.sum(axis=1).var() # 每人總分的變異數
    Var_all = df.var(axis=0).sum() # 每題的變異數的總和
    n = len(df.columns) # 總題數
    a = (n / (n - 1)) * (1 - (Var_all / Var)) # Cronbach's alpha 信度的公式
    return a # 回傳結果

def result(test, static_dir, data, corr_img = False, print_result = False):
    path = os.path.join(static_dir, test)
    url = '/' + os.path.relpath(path, os.path.join(os.getcwd(), 'static'))
    output = {
        'id': test,
        'url': url,
        'test': data,
        'images': {
            'analysis': {}
        },
        'files': {}
    }
    
    if print_result:
        print(path)
        print()
    image_path = os.path.join(path, 'images')
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    analysis_path = os.path.join(image_path, 'analysis')
    if not os.path.exists(analysis_path):
        os.makedirs(analysis_path)

    question = pd.DataFrame.from_dict(data['questions'], orient='index')
    if not 'name' in question:
        question['name'] = ''
    if not 'type' in question:
        question['type'] = 'continuous'
    if not 'score' in question:
        question['score'] = 0
    if not 'text' in question:
        question['text'] = None
    if not 'answer' in question:
        question['answer'] = None
    question = question.set_index('name')
    questions = question.index
    answer = question['answer']
    boolean = question[question['type'] == 'boolean'].index
    discrete = question[question['type'] == 'discrete'].index
    continuous = question[question['type'] == 'continuous'].index

    responses = pd.DataFrame.from_dict(data['responses'], orient='index')

    if print_result:
        if display:
            print('Questions:')
            display(question)
            print()
            print('Answers:')
            display(answer)
            print()
            print('Responses:')
            display(responses)
            print()
        else:
            print('Questions:')
            print(question)
            print()
            print('Answers:')
            print(answer)
            print()
            print('Responses:')
            print(responses)
            print()

    right = responses.copy()
    right.loc[:, boolean] = (responses.loc[:, boolean] == answer).astype(int)
    right.loc[:, discrete] = (responses.loc[:, discrete] == answer).astype(int)
    right.loc[:, continuous] = responses.loc[:, continuous] / question.T.loc['score', continuous]

    score = (right[questions] * question['score']).sum(axis=1)
    responses['Score'] = score
    right['Score'] = score
    responses = responses.sort_values(by='Score', ascending=False)
    right = right.sort_values(by='Score', ascending=False)

    question.reset_index().to_csv(os.path.join(path, 'questions.csv'))
    output['files']['questions'] = url + '/questions.csv'
    responses.to_csv(os.path.join(path, 'responses.csv'))
    output['files']['responses'] = url + '/responses.csv'
    right.to_csv(os.path.join(path, 'right.csv'))
    output['files']['right'] = url + '/right.csv'

    H = responses.head(int(math.ceil(len(responses.index) * 0.27)))
    L = responses.tail(int(math.ceil(len(responses.index) * 0.27)))
    H_right = right.head(int(math.ceil(len(right.index) * 0.27)))
    L_right = right.tail(int(math.ceil(len(right.index) * 0.27)))

    PH = H_right[questions].mean()
    PL = L_right[questions].mean()
    p = right[questions].mean()
    P = (PH + PL) / 2
    P_text = P.apply(lambda v: 'Very Difficult' if v <= 0.1 else 'Difficult' if v <= 0.25 else 'Optimum Difficulty' if v <= 0.75 else 'Easy' if v <= 0.9 else 'Very Easy')
    D = PH - PL
    r = right.corr().loc[questions, 'Score']
    r_text = r.apply(lambda v: 'Bad' if v < 0.2 else 'Not Bad' if v < 0.3 else 'Good' if v < 0.4 else 'Very Good')

    analysis = pd.concat([PH, PL, P, p, r, D, P_text, r_text], axis=1, keys=['高分組平均(PH)', '低分組平均(PL)', '高低分組平均(P)', '全部平均(p)', '點二系列相關(r)', '鑑別度(D)', '難易度(P)', '鑑別度(r)'])
    output['analysis'] = json.loads(analysis.to_json(orient='index'))
    analysis.to_csv(os.path.join(path, 'analysis.csv'))
    output['files']['analysis'] = url + '/analysis.csv'

    df_H = H.copy()
    df_H['Score'] = 'High'
    df_L = L.copy()
    df_L['Score'] = 'Low'
    df_All = responses.copy()
    df_All['Score'] = 'All'
    All = pd.concat([df_H, df_L, df_All], axis=0, ignore_index=True)

    for key in questions:
        plt.figure()
        sns.countplot(x=key, hue='Score', hue_order=['High', 'Low', 'All'], data=All.sort_values(by=key))
        if key in discrete:
            plt.title('Question ' + str(key) + ':\n' + str(question.loc[key, 'text']) + '\n\nAns: ' + str(answer[key]) + '\n\nDifficulty = ' + str(format(P[key],'.3f')) + ', ' + P_text[key] + '\nDiscrimination = ' + str(format(r[key],'.3f')) + ', ' + r_text[key] + '\n\nDistribution of Question ' + key)
        else:
            plt.title('Question ' + str(key) + ':\n' + str(question.loc[key, 'text']) + '\n\nDifficulty = ' + str(format(P[key],'.3f')) + ', ' + P_text[key] + '\nDiscrimination = ' + str(format(r[key],'.3f')) + ', ' + r_text[key] + '\n\nDistribution of Question ' + str(key))
        plt.savefig(os.path.join(analysis_path, str(key) + '.png'), bbox_inches='tight')
        if print_result:
            plt.show()
        output['images']['analysis'][key] = url + '/images/analysis/' + str(key) + '.png'

    score = '全體：\r\n'
    score += '平均 = {:.2f}\r\n'.format(responses['Score'].mean())
    score += '標準差 = {:.2f}\r\n'.format(responses['Score'].std())
    score += '-------------\r\n'
    score += '高分組：\r\n'
    score += '平均 = {:.2f}\r\n'.format(H['Score'].mean())
    score += '標準差 = {:.2f}\r\n'.format(H['Score'].std())
    score += '-------------\r\n'
    score += '低分組\r\n'
    score += '平均 = {:.2f}\r\n'.format(L['Score'].mean())
    score += '標準差 = {:.2f}'.format(L['Score'].std())
    with open(os.path.join(path, 'score.txt'), 'w+') as f:
        f.write(score)
    if print_result:
        print(score)
    output['score'] = score
    output['files']['score'] = url + '/score.txt'

    plt.figure()
    if len(H.index) < 2:
        sns.distplot(H['Score'], label='High', kde=False)
    else:
        sns.distplot(H['Score'], label='High')
    if len(L.index) < 2:
        sns.distplot(L['Score'], label='Low', kde=False)
    else:
        sns.distplot(L['Score'], label='Low')
    if len(responses.index) < 2:
        sns.distplot(responses['Score'], label='All', kde=False)
    else:
        sns.distplot(responses['Score'], label='All')

    plt.title('The Total Score')
    plt.legend()
    plt.savefig(os.path.join(image_path, 'score.png'), bbox_inches='tight')
    output['images']['score'] = url + '/images/score.png'
    if print_result:
        plt.show()

    a = alpha(right[questions])
    consistency = 'Cronbach\'s alpha 信度 = {:.3f}\r\n'.format(a)
    consistency += '測量標準誤 (SEM) = {:.2f}'.format(responses['Score'].std() * math.sqrt(1 - a))
    with open(os.path.join(path, 'consistency.txt'), 'w+') as f:
        f.write(consistency)
    if print_result:
        print(consistency)
    output['consistency'] = consistency
    output['files']['consistency'] = url + '/consistency.txt'

    corr = right.loc[:,questions].corr()

    corr.to_csv(os.path.join(path, 'corr.csv'))
    if print_result:
        if display:
            display(corr)
        else:
            print(corr)
    output['corr'] = json.loads(corr.to_json(orient='index'))
    output['files']['corr'] = url + '/corr.csv'

    if corr_img:
        sns.pairplot(right.loc[:,questions], diag_kind='kde', kind="reg")
        plt.savefig(os.path.join(image_path, 'corr.png'), bbox_inches='tight')
        if print_result:
            plt.show()
    return output

if __name__ == '__main__':
    test = sys.argv[1] if len(sys.argv) > 1 else ''
    path = os.path.relpath(sys.argv[2] if len(sys.argv) > 2 else '.')
    data = json.loads(sys.argv[3] if len(sys.argv) > 3 else '{ "questions": {}, "responses": {} }')
    print(json.dumps(result(test, path, data, corr_img=False, print_result=False)))