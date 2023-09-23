# -*- coding: utf-8 -*-
"""hw01_d_tree_part3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c-c8ZS-HF_DvkG_aA-TW-0iwYqi2R0ZE
"""

#Parker Beckett u0283152
#HW01 decision trees

import pandas as pd
import numpy as np
import scipy as sp
import sys #for arguments from bash
#import warnings
#warnings.filterwarnings('ignore')
#import time #for benchmarking

#I/O file to add header line and load into dataframe
def load_csv(filename):

  attributecount = 0
  examplecount = 0

  with open(filename) as f:
    for line in f:
      examplecount += 1
      terms = line.strip().split(',')
      attributecount = len(terms)

  attributecount -= 1
  names = []

  for i in range(0,attributecount):
    name = "A"+str(i)
    names.append(name)

  names.append("label")
  df = pd.read_csv(filename, names = names)

  return df

#cleaner for unknown values
def cleanunknown(data):

  newdata = data.copy()

  for col in data.columns:
    coll = data[col]
    frame = data[data[col].str.contains("unknown")]

    if (frame.shape[0] > 0):
      newval = data[col].mode()
      check = str(newval).split(" ")
      index = len(check) - 1 - 3
      totrim = check[index]
      actual = str(totrim.split("\nName")[0])

      if(actual == "unknown"):
        modelist = data[col].value_counts().index.tolist()[:2]
        actual = modelist[1]

      for i in range(len(coll)):
        coll[i] =  actual

      newdata[col] = coll

  return newdata

#cleaner for numerical values
def numtobin(data):

  newdata = data.copy()

  for col in data.columns:
    if col == "label":
      break

    coll = data[col]

    if(coll.dtype == np.int64):
      median = coll.median()

      for i in range(len(coll)):
        num = coll[i]
        result = ""

        if num >= median:
          result = "greater"

        else:
          result = "lesser"

        coll[i] = result

      newdata[col] = coll

  return newdata

#determines attribute with most gain
def get_best(gainID, data):

  backupattr = ""
  maxentropy = 0.0
  maxattribute = "ERROR"
  rows = data.shape[0]-1
  labels = data["label"]
  uniquelabels = data[data.columns[data.shape[1] - 1]].unique()
  labelcount = np.zeros(len(uniquelabels))

  for l in labels:
    for i in range(len(uniquelabels)):
      ul = uniquelabels[i]
      if l == ul:
        labelcount[i] += 1

  pk = labelcount / data.shape[0]
  startentropy = get_entropy(gainID, pk)
  labels = data["label"]

  for col in data.columns:
    backupattr = col
    if col == "label":
      break

    attrentropy = 0.0
    coll = data[col]
    attrvalues = coll.unique()
    attrcount = np.zeros(len(attrvalues))
    labelsbyattr = {}

    for a in range(len(coll)):
      for i in range(len(attrvalues)):
        ua = attrvalues[i]
        if coll[a] == ua:
          attrcount[i] += 1
          if(ua not in labelsbyattr):
            labelsbyattr[ua] = []
            labelsbyattr[ua].append(labels[a])

          else:
            labelsbyattr[ua].append(labels[a])

    probs = attrcount / data.shape[0]
    countsbyattr = {}

    for i in range(len(attrvalues)):
      alabels = labelsbyattr[attrvalues[i]]
      numlabels = len(alabels)
      counter = np.zeros(len(uniquelabels))
      for l in alabels:
        for u in range(len(uniquelabels)):
          ul = uniquelabels[u]
          if l == ul:
            counter[u] += 1

      countsbyattr[attrvalues[i]] = counter/numlabels

    for i in range(len(attrvalues)):
      pk = countsbyattr[attrvalues[i]]
      valentropy = get_entropy(gainID, pk)
      attrentropy += probs[i] * valentropy

    trueentropy = startentropy - attrentropy

    if trueentropy > maxentropy:
      maxentropy = trueentropy
      maxattribute = col

    attrentropy = 0.0

  if maxattribute == "ERROR":
    maxattribute = backupattr

  return maxattribute

#recursive ID3 algorithm
def ID3_run(gainID, maxdepth, data, previousAttr, previousValue, currdepth):

  mytree = dtree()
  attr = [data.shape[1] - 1]
  labels = data[data.columns[data.shape[1] - 1]].unique()

  if(labels.size == 1):
    mytree.label = labels[0]
    mytree.attribute = previousAttr
    mytree.value = previousValue
    return mytree

  bestattr = get_best(gainID, data)
  bestvals = data[bestattr].unique()
  childs = []

  for i in range(len(bestvals)):
    newtree = dtree()
    childs.append(newtree)

  mytree.children = childs

  for i in range(len(bestvals)):
    currdepth -= 1
    splitdata = data.copy()
    col = splitdata[bestattr]
    todrop = []

    for j in range(len(col)):
      if col[j] != bestvals[i]:
        todrop.append(j)

    splitdata = splitdata.drop(todrop)
    splitdata.drop(bestattr, 1)
    splitdata.reset_index(drop=True, inplace=True)

    if(len(splitdata[bestattr])) == 0:
      uniquelabels = data[data.columns[data.shape[1] - 1]].unique()
      labelcount = np.zeros(len(uniquelabels))

      for l in labels:
        for i in range(len(uniquelabels)):
          ul = uniquelabels[i]
          if l == ul:
            labelcount[i] += 1

      common = labelcount.index(labelcount.max())
      newtree = mytree()
      newtree.data = common
      mytree.children[i] = newtree

    else:
      bestval = bestvals[i]
      mytree.attribute = previousAttr
      mytree.value = previousValue
      mytree.children[i] = ID3_run(gainID, maxdepth, splitdata, bestattr, bestval, currdepth)

  return mytree

#checks whether guesses are correct
def predict(tree, example):#, count):

    for child in tree.children:
      attribute = child.attribute
      value = child.value
      label = child.label
      if(attribute == ""):
        return 0
      if(example[attribute] == value):
        if label == "":
          code = predict(child, example)
          if(code == 1):
            return 1
        else:
          if(label == example["label"]):
            return 1
          else:
            return 0
    return 0

#verifies accuracy
def verifytree(tree, data, max_depth):

  count = 0
  testing = dtree()
  testing = tree
  traverse(tree, 0, 0, max_depth)

  for i in range(data.shape[0]):
    example = data.iloc[i]
    count += predict(testing, example)

  acc = count / data.shape[0]

  return acc

#traverse and prune tree, uncomment to print the tree to the console
def traverse(tree, depth, branch, max_depth):

  if tree is None:
    return
  else:
    if depth > max_depth: #prune tree
      tree.children = []
      return

    depth += 1

    #allows tree to be drawn
    '''
    space = ""
    for d in range(depth):
      space = space + "  "

    print(space + tree.attribute + ">" + tree.value + ": " + tree.label)#shouldnt be this
    '''
    for child in tree.children:
      ##print(space + "{")
      branch += 1 #allows for debugging with depth by branch
      traverse(child, depth, branch, max_depth)
      ##print(space + "}")

#dtree class
class dtree():
  def __init__(self):
    self.attribute = ""
    self.value = ""
    self.label = ""
    self.children = [] #array of children

#calculate entropy based on heuristic
def get_entropy(gainID, pk):
  entropy = 0.0
  if (gainID == 0): #normal gain
    for p in pk:
      term = 0
      if p != 0:
        term = p * np.log2(p)
      entropy -= term
    return entropy
  if(gainID == 1): #majority error
    majerr = 1 - pk.max()
    for p in pk:
      entropy += p * majerr
    return entropy
  if(gainID == 2): #gini
    for p in pk:
      entropy += p * p
    return 1 - entropy

def main():

  if(len(sys.argv)< 5):
    print("the arguments should be <gain>, <depth>, <training> <testing>")

  gainarg = int(sys.argv[1])
  deptharg = int(sys.argv[2])
  trainarg =  str(sys.argv[3])
  testarg = str(sys.argv[4])

  traindata = numtobin(load_csv(trainarg))
  testdata = numtobin(load_csv(testarg))

  traindata = cleanunknown(traindata)
  testdata = cleanunknown(testdata)

  tree = ID3_run(gainarg, deptharg, traindata, "root", "none", 0)
  acc = verifytree(tree, testdata, deptharg)

  print("tree with depth " + str(deptharg) + "and gain code " + str(gainarg) + " trained on " + trainarg + " and tested on " + testarg + " has accuracy : " + str(acc))

if __name__=="__main__":
  main()