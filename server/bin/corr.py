import json
import pandas as pd
import os
import sys
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
sns.set(style='darkgrid')

def corr(test, static_dir, columns, print_result = False):
    path = os.path.join(static_dir, test)
    url = '/' + os.path.relpath(path, os.path.join(os.getcwd(), 'static'))
    output = {
        'id': test,
        'url': url,
        'images': {}
    }

    if print_result:
        print(path)
        print()
    corr_path = os.path.join(path, 'images', 'corr')
    if not os.path.exists(corr_path):
        os.makedirs(corr_path)

    right = pd.read_csv(os.path.join(path, 'right.csv'), index_col = 0)

    now = datetime.now()
    filename = 'corr_' + now.strftime("%Y%m%d_%H%M%S_%f") + '.png'
    sns.pairplot(right.loc[:, columns], diag_kind='kde', kind="reg")
    plt.savefig(os.path.join(corr_path, filename), bbox_inches='tight')
    output['images']['corr'] = url + '/images/corr/' + filename
    if print_result:
        plt.show()
    return output

if __name__ == '__main__':
    test = sys.argv[1] if len(sys.argv) > 1 else ''
    path = os.path.relpath(sys.argv[2] if len(sys.argv) > 2 else '.')
    columns = json.loads(sys.argv[3] if len(sys.argv) > 3 else '[]')
    print(json.dumps(corr(test, path, columns, print_result=False)))