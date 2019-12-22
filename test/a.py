#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/14
"""

def ddd():
	cc = getattr(__import__("sss"), "cc")
	cc()
	print(cc)
	

import itertools

def loadDataSet():
	return [[1,2,5],[2,4],[2,3],[1,2,4],[1,3],[2,3],[1,3],[1,2,3,5],[1,2,3]]
#1.构建候选1项集C1
def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])

	C1.sort()
	return list(map(frozenset, C1))

#将候选集Ck转换为频繁项集Lk
#D：原始数据集
#Cn: 候选集项Ck
#minSupport:支持度的最小值
def scanD(D, Ck, minSupport):
	#候选集计数
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if can not in ssCnt.keys(): ssCnt[can] = 1
				else: ssCnt[can] += 1

	numItems = float(len(D))
	Lk= []     # 候选集项Cn生成的频繁项集Lk
	supportData = {}    #候选集项Cn的支持度字典
	#计算候选项集的支持度, supportData key:候选项， value:支持度
	for key in ssCnt:
		support = ssCnt[key] / numItems
		if support >= minSupport:
			Lk.append(key)
		supportData[key] = support
	return Lk, supportData

#连接操作，将频繁Lk-1项集通过拼接转换为候选k项集
def aprioriGen(Lk_1, k):
	Ck = []
	lenLk = len(Lk_1)
	for i in range(lenLk):
		L1 = list(Lk_1[i])[:k - 2]
		L1.sort()
		for j in range(i + 1, lenLk):
			#前k-2个项相同时，将两个集合合并
			L2 = list(Lk_1[j])[:k - 2]
			L2.sort()
			if L1 == L2:
				Ck.append(Lk_1[i] | Lk_1[j])

	return Ck

def apriori(dataSet, minSupport = 0.5):
	C1 = createC1(dataSet)
	L1, supportData = scanD(dataSet, C1, minSupport)
	L = [L1]
	k = 2
	while (len(L[k-2]) > 0):
		Lk_1 = L[k-2]
		Ck = aprioriGen(Lk_1, k)
		print("ck:",Ck)
		Lk, supK = scanD(dataSet, Ck, minSupport)
		supportData.update(supK)
		print("lk:", Lk)
		L.append(Lk)
		k += 1

	return L, supportData




if __name__ == "__main__":
	#ddd()
	
	#dataset = loadDataSet()
	#L, supportData = apriori(dataset, minSupport=0.2)
	
	
