from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import re
import json

data = pd.read_csv("./word_search.tsv", delimiter="\t", na_filter=False, header=None)
data.columns = ["word","frequency"]
data["length"] = data.word.str.len() 

def index(request):
    key = request.GET.get("word")
    return HttpResponse(json.dumps({"response": wordsort(key)}))

def wordsort(string):
    # first preference to the ones with full match
    # sort by frequency
    # sort by word length
    match1 = startsWith(string)
    if len(match1) > 25:
        return match1.sort_values(by=["length","frequency"], ascending=[True, False])[:25]["word"].tolist()
    else:
        match2 = contains(string, match1.word.tolist())
        length = len(match1)
        match1 = match1.sort_values(by=["length","frequency"], ascending=[True, False])
        match2 = match2.sort_values(by=["frequency", "length"], ascending=[False, True])
        return pd.concat([match1, match2[:(25-length)]])["word"].tolist()
        

def startsWith(keyword):
    return data[data.word.str.startswith(keyword, na=False)]

def contains(keyword, match):
    if match:
        match1 = data[~data.word.isin(match)]
        return match1[match1.word.str.contains(keyword, regex= True,na=False)]
    else:
        return data[data.word.str.contains(keyword, regex= True,na=False)]
