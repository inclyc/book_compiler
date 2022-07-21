import os
import re


def generate(out, titles, contents):
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
    cnt = 1
    with open(out, 'w') as f:
        for title in titles:
            wtitle = title
            if re.match(r'第.*话', title):
                wtitle = re.sub(r'第.*话', '第{}章'.format(cnt), title)
                cnt += 1

            f.write(wtitle)
            f.write('\n\n\n')
            f.write(contents[title])
