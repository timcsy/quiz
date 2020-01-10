import os
import sys
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
sns.set(style='darkgrid')

def count(test, static_dir, data, print_result = False):
    path = os.path.join(static_dir, test)
    url = '/' + os.path.relpath(path, os.path.join(os.getcwd(), 'static'))
    output = {
        'id': test,
        'url': url,
        'question': data
    }

    count_path = os.path.join(path, 'images', 'count')
    if not os.path.exists(count_path):
        os.makedirs(count_path)

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

    if print_result:
        if display:
            display(question)
        else:
            print(question)

    name = data['name']

    sns.countplot(question['answer'].sort_values(ascending=True))
    if data['type'] == 'discrete':
        plt.title('Question ' + str(name) + ':\n' + str(data['text']) + '\n\nAns: ' + str(data['answer']) + '\n\nDistribution of Question ' + str(name))
    else:
        plt.title('Question ' + str(name) + ':\n' + str(data['text']) + '\n\nDistribution of Question ' + str(name))
    plt.savefig(os.path.join(count_path, str(name) + '.png'))
    if print_result:
        plt.show()
    output['image'] = url + '/images/count/' + str(name) + '.png'
    
    return output

if __name__ == '__main__':
    test = sys.argv[1] if len(sys.argv) > 1 else ''
    path = os.path.relpath(sys.argv[2] if len(sys.argv) > 2 else '.')
    data = json.loads(sys.argv[3] if len(sys.argv) > 3 else '{ "name": "", "type": "boolean", "text": "", "answer": true, "responses": [] }')
    print(json.dumps(count(test, path, data, print_result=False)))