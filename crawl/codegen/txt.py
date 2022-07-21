import os
import re


def _title_transform(titles, contents):
    cnt = 1
    new_titles = []
    new_contents = {}
    for title in titles:
        if re.match(r'第.*话', title):
            new_title = re.sub(
                r'第.*话', '第{}章'.format(cnt), title)
            cnt += 1
            new_titles.append(new_title)
            new_contents[new_title] = contents[title]
        else:
            new_titles.append(title)
            new_contents[title] = contents[title]
    return new_titles, new_contents


def transform(titles, contents):
    titles, contents = _title_transform(titles, contents)
    return titles, contents

def generate(out, titles, contents):
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
    titles, contents = transform(titles, contents)
    with open(out, 'w') as f:
        for title in titles:
            f.write(title)
            f.write('\n\n\n')
            f.write(contents[title])
