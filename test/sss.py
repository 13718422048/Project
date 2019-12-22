#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/9/2
"""



import os


def cc():
	
	dd = {"ddd","sss"}
	ccdd = ["ddd","eeee","sss"]
	ddcc = ["ddd","sss","eeee"]
	print(ccdd == ddcc)
	dd = frozenset({1,3})
	print(len(dd))
	print(dd.issubset(ccdd))
	
	
def isequlist(firstlist, secondelist):
	ret = True
	
	if len(firstlist) == len(secondelist):
		for factor in firstlist:
			if factor not in secondelist:
				ret = False
				break
	
	else:
		ret = False
		
	return ret
	
def scandata(transmitions, items, support):
	
	ck = {}
	for item in items:
		
		for transmition in transmitions:
			if item.issubset(transmition):
				if item not in ck.keys():
					ck[item] = 1
					continue
				ck[item] += 1
				
	itemsupport = {}
	lk = []
	
	for key in ck.keys():
		keysupo = ck[key] / float(len(data))
		if keysupo > support:
			lk.append(key)
		itemsupport[key] = keysupo
	
	return lk, itemssupport


def prioricandiset(transmitions, lenght):
	ck = []
	
	for i,transmition in enumerate(transmitions):
		itemsset = set(transmition)
		for j in range(len(transmitions)):
			union = transmition | transmitions[j]
			if len(union) == lenght:
				ck.append(transmition)
				
	return ck
			
	
	
## Definition for singly-linked list.
#class ListNode(object):
	#def __init__(self, x):
		#self.val = x
		#self.next = None

#class Solution(object):
	#def addTwoNumbers(self, l1, l2):
		#"""
		#:type l1: ListNode
		#:type l2: ListNode
		#:rtype: ListNode
		#"""
		#fitem = 0
		#pos = 0
		#while l1 != None:
			#fitem += l1.val * (10 ** pos)
			#l1 = l1.next
			#pos += 1
			
		#sitem = 0
		#pos = 0
		#while l2 != None:
			#sitem += l2.val * (10 ** pos)
			#l2 = l2.next
			#pos += 1
		
		#val = str(fitem + sitem)
		#pos = 0
		#l3 = ListNode(val[-1])
		#for i in range(0, len(val) - 1):
			#newnode = ListNode(val[i])
			#newnode.next = l3.next
			#l3.next = newnode
		
		#return l3

#def generatelist(ls):
	#l = ListNode(ls[0])
	#startpos = len(ls) - 1
	#if ls[-1] == 0:
		#startpos -= 1

	#for i in range(startpos, 0, -1):
		#newnode = ListNode(ls[i])
		#newnode.next = l.next
		#l.next = newnode

	#return l



class Solution(object):
	def lengthOfLongestSubstring1(self, s):
		"""
		:type s: str
		:rtype: int
		"""
		winds = []
		
		for char in s:
			if char not in winds:
				compsubstr = "".join(x for x in winds) + char
				if compsubstr in s:
					winds.append(char)
					continue
				
				parsubstr = "".join(x for x in winds[1:]) + char	
				if parsubstr in s:
					winds.pop(0)
					winds.append(char)
					continue

		return len(winds), winds

	def lengthOfLongestSubstring(self, s):
		"""
		:type s: str
		:rtype: int
		"""
		maxsub = []
		if s is not None and s != "":
			if len(s) == 1:
				maxsub.append(s)
				
			if len(s) >= 2:
		
				winds = []
				
				for char in s:
		
					if char in winds:
						if len(maxsub) <= len(winds):
							maxsub = winds
						
						tmp = winds[winds.index(char) + 1:]
						winds = tmp
					
					winds.append(char)
						
				if len(winds) > len(maxsub):
					maxsub = winds
					
		return len(maxsub), maxsub

	def convert(self, s, numRows):
		"""
        :type s: str
        :type numRows: int
        :rtype: str
        """	
		retlen = (2 *numRows - 2)
		try:
			
			if numRows > 1:
				
				substrls = []		
				substr = ""
				
				for i, char in enumerate(s):
					
					if i % retlen == 0 and i != 0:
						substrls.append(substr)
						substr = ""
						
					substr = substr + char
						
				if substr != "":
					substrls.append(substr)
				
				ret = ["" for x in range(numRows)]
				
				for i, factor in enumerate(substrls):
					pos = 0
					for j, char in enumerate(factor):
						pos = j % numRows
						if j >= numRows:
							pos = pos * -1 - 2
						ret[pos] = ret[pos] + char
					
				return "".join(x for x in ret)
			else:
				return s
			
		except Exception as e:
			print(e)
			return ""


	def convert1(self, s, numRows):
		ret = ["" for x in range(min([numRows, len(s)]))]
		
		pos = 0
		isdown = -1
		for char in s:
			ret[pos] = ret[pos] + char
			if pos == 0 or pos == numRows - 1:
				isdown = isdown * -1
			
			pos = pos + 1 if isdown == 1 else pos - 1
			
		print(str(ret))
	
	
	def reverse(self, x):
		"""
		:type x: int
		:rtype: int
		"""
		
		xstr = str(x)
		
		symbol = ""
		if xstr[0] == "-":
			symbol = xstr[0]
			xstr = xstr[1:]
			
		retstr = xstr[::-1]
		boundary = 2 ** 31
			
		if symbol == "-" and len(retstr) < str(boundary - 1):
			return -1 * int(retstr)
			
		if len(retstr) < len(str(boundary)) or (len(str(retstr)) < len(str(boundary)) and retstr < str(boundary)):
			return int(retstr)
		
		return 0
		
	# 回文
	def isPalindrome(self, x):
		flag = 1
		if isinstance(x, int):
			num = str(x)
			length = len(num)
			middle = int(length / 2) + length % 2
			
			for i in range(middle):
				if num[i] != num[length - i - 1]:
					flag = 0
					break
		
		return flag
	
	def isValid(self, s):
		"""
		:type s: str
		:rtype: bool
		"""
		stack = []
		rightsymbol = {")" : "(", "}" : "{", "]" : "["}
		
		
		if len(s) % 2 != 0:
			return False
		
		for char in s:
			
			if char in rightsymbol.keys():
				topsymbol = stack.pop()
				if topsymbol != rightsymbol[char]:
					break
				continue
			
			stack.append(char)
			
		return len(stack) == 0
		
	
def bin(n, k):
	
	matrix = [[1]]
	
	for i in range(1, n + 1):
		matrix.append([])
			
		for j in range(min([i, k]) + 1):
			if j == 0 or i == j:
				matrix[i].append(1)
				
			else:
				matrix[i].append(matrix[i - 1][j - 1] + matrix[i - 1][j])
	
	print(str(matrix[n][k]))
	



	
if __name__ == "__main__":
	#cc = Solution()
	#l2 = generatelist([9,9,9])
	#l1 = generatelist([7])
	#l3 = cc.addTwoNumbers(l1, l2)

	#pnode = l3
	#while pnode != None:
		#print(pnode.val)
		#pnode = pnode.next


	#cc = Solution()
	#s = "asdfgh"
	#length, substr = cc.lengthOfLongestSubstring(s)
	#print(length, str(substr))
	
	#n = 10
	#k = 4
	#bin(n, k)
	
	#cc = Solution()
	#s = "LEETCODEISHIRING"
	#numRows = 4
	#dd = cc.convert1(s, numRows)
	
	cc = Solution()
	number = 556464
	#print(cc.reverse(number))
	
	#for i in range(number, 0, -1):
		#print(i)

	#number = 12321
	#print(cc.isPalindrome(number))
	
	ss = "()[]{}"
	print(cc.isValid(ss))
	
	
	
	
	
	
	
	
	
	
	