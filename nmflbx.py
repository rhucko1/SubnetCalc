#!/usr/bin/python
import numpy as np
import sys

'''
IP Subnet Calc Tool
Can be used as a module imported or ran directly
written by Richard Hucko (2018)
'''

#####################################################
# Function Definitions:
#####################################################
def octManip(str1,str2,operator="+"):
	list1,list2,list3=str1.split('.'),str2.split('.'),[]
	upOne=False

	for i in range(len(list1)-1,-1,-1):
		list1[i]=int(list1[i])
		list2[i]=int(list2[i])
		if operator == '+':
			solution=int(list1[i]).__add__(int(list2[i]))
		elif operator == '-':
			solution=int(list1[i]).__sub__(int(list2[i]))
		elif operator == '*':
			solution=int(list1[i]).__mul__(int(list2[i]))
		elif operator == '/':
			solution=int(list1[i]).__div__(int(list2[i]))
		if upOne:
			solution=int(solution).__add__(1)
			upOne=True
		if solution>=256:
			solution=0
			upOne=True
		list3.append(solution)
	list3.reverse()
	dotDec='.'.join(map(str,list3))
	return dotDec
#####################################################
def NetID(ip,subnetmask):
	mask=subnetmask.split('.')
	ip=ip.split('.')
	netid=''
	for oct in range(len(ip)):
		netid+=str(np.bitwise_and(int(ip[oct]),int(mask[oct])))+'.'
	netid=netid.strip('.')
	return netid
#####################################################
def cidr2mask(cidr):
	'''
	convert CIDR into Subnet Mask
	accepts one argument (CIDR), returns Subnet Mask
	'''
	powersrev=[2**x for x in range(8)]
	powersrev.reverse()
	blockSize=[sum(powersrev[:x]) for x in range(1,len(powersrev)+1)]
	octetOfInterest=0
	cidr=int(cidr)
	mask=''
	count=0
	
	for i in range(cidr//8):
		mask+='255.'
		count+=1
	for x in range(cidr%8):
		octetOfInterest=blockSize[x]
	count+=1
	mask+=str(octetOfInterest)
	
	while count<4:
		mask+='.0'
		count+=1
	return mask
#####################################################
# Main Body of Program:            - if run directly
#####################################################
if __name__=='__main__':
	try:
		ANS=sys.argv[1]
	except:
		print("Enter IP and CIDR [ex. xxx.xxx.xxx.xxx/xx]: ")
		ANS=sys.stdin.readline()

	if '/' not in ANS:
		ANS+='/32'

	IP,CIDR=ANS.split('/')

	subnetmask=cidr2mask(CIDR)
	netid=NetID(IP,subnetmask)
	wildmask=octManip('255.255.255.255',subnetmask,'-')
	broadcast=octManip(netid,wildmask)
	first=octManip(netid,'0.0.0.1')
	last=octManip(broadcast,'0.0.0.1','-')
	nextnet=octManip(broadcast,'0.0.0.1')
        
	print("NetID: {0}\nCIDR: {1}".format(netid,CIDR))
	print("Subnet Mask: {0}\nWildcard Mask: {1}\nBroadcast: {2}\nFirst: {3}\nLast: {4}\nNext Network: {5}".format(subnetmask,wildmask,broadcast,first,last,nextnet))
