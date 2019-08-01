#!/usr/bin/env python
# encoding: utf-8
import json


import sys,os,json,time,re
from collections import Counter
import pandas as pd



base_path = os.path.dirname(os.path.abspath(__file__) ) 
file_path = os.path.join(base_path,'te_content_all.json')
top_8_keys = ['unemployment rate', 'retail sales mom',
        'pce price index', 'non farm payrolls',
        'inflation rate mom', 'gdp growth rate',
        'balance of trade', 'wage growth','interest rate']

def read_df(path = file_path):
    result = []
    with open(file_path) as f:
        for line in f:
            content = json.loads(line)
            cate = content['category'].lower()
            title = content['title'].lower()
            description = content['description'].lower()
            country = content['country'].lower()
            result.append([cate,title,description,country])
    df = pd.DataFrame(result, columns=['category', 'title','description','country'])
    return df


def extract_economic_news(title, text):
    content = title +' '+ text 
    label = 'no match'
    p = re.compile('market expectati.*? |market consensus')

    match = ['match','in line with','unchange']   
    above = ['better','above','beating','higher','increas*','the same as']
    below = ['low*','below','worse','missing']
    
    match = '|'.join(match)
    p_match = re.compile(match)
    
    above = '|'.join(above)
    p_above = re.compile(above)
    
    below = '|'.join(below)
    p_below = re.compile(below)
    m = p.search(content)
    if m:
        start = m.start()
        end = m.end()
        i = max(start - 60,0)
        j = end + 40
        line = content[i:j]
        if p_match.search(line):
            label = 'equal'
        elif p_above.search(line):
            label = 'above'
        elif p_below.search(line):
            label = 'below'
    return label

def query(df,cat,country=None,label=None):
    if cat and country and label:
        return df[(df['category'] == cat) & (df['country'] == country) & (df['label'] == label)]
    elif cat and not country and not label:
        return df[df['category'] == cat]
    elif cat and country and not label:
        return df[df['category'] == cat]
    else:
        print('XXXXX')
        

if __name__ == "__main__":
    df = read_df()
    df['label'] = (df['title'] + df['description']).apply(extract_economic_news)
    query(df,'retail sales mom')
    




