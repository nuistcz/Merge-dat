#!/usr/bin/env python
import os, sys, getopt
import numpy as np

def makeuplist():
	templist = []
	file_path = str(os.getcwd())+ '/atom_selection.txt'
	file_content = open(file_path, 'r') 
	sourcelines = file_content.readlines()
	if sourcelines[0] == 'list\n':
		for index in range(len(sourcelines)-1):
			templist.append(sourcelines[index+1].strip('\n').zfill(4))
	else :
		pass
	return templist


def addlines(linelist, lineindex, needlineindex):
	output = ''
	count = 1
	for i in needlineindex:
		startline = lineindex[int(i)-1]
		endline = lineindex[int(i)]-1
		flag = startline

		templine = linelist[flag].split()
		templinecontent = templine[0] + ' '+ templine[1] + '   ' + str(count) + '  ' +templine[3] + '\n'
		count += 1
		output += templinecontent

		for j in range(endline-startline):
			output += linelist[flag+1]
			flag += 1
	return output

def mergy(filename, outname = 'CHGCAR_OUTPUT'):
	headercontent = ''
	footercontent = ''
	p = len(filename)
	CHGCAR_path = str(os.getcwd())+ '/CHGCAR'
	#Add the first 6 lines in head
	for i in range(6):
		headercontent += open(CHGCAR_path).readlines()[i]
	line_7 = open(CHGCAR_path).readlines()[6]
	rows = 0
	for s in line_7.split():
		rows += int(s)
	factor = int(rows/p)
	#Add line #7
	headercontent += '     ' + str(int(int(line_7.split()[0])/factor)) + '     '+ str(int(int(line_7.split()[1])/factor)) + '\n'
	# open(CHGCAR_path).readlines()[0:5]
	# Add line #8
	headercontent += open(CHGCAR_path).readlines()[7]

	for i in range(p):
		nextrow = int(filename[i]) + 7
		headercontent += open(CHGCAR_path).readlines()[nextrow]
	# Add final line
	headercontent += open(CHGCAR_path).readlines()[8+rows]
	finalrow = open(CHGCAR_path).readlines()[9+rows].splitlines()
	headercontent += finalrow[0]
	# Caculate the main martix
	flag = 0


	for i in range(len(filename)):
		path = str(os.getcwd())+"/BvAt"+filename[i]+".dat"
		try:
			x = open(path).readline()
			print("Processing Atom #"+str(filename[i]))
			a = np.loadtxt(path , skiprows = rows + 10)
			if flag == 0:
				res = a
				flag = 1
			else:
				res += a
		except:
			print("Error: Problem File "+"/BvAt"+filename[i]+".dat")

	# Add footer
	print ('Shape is '+str(res.shape[0]))
	footerlist = open(CHGCAR_path).readlines()[res.shape[0]+10+rows : len(open(CHGCAR_path).readlines())]
	footerindex = []
	for i, val in enumerate(footerlist):
		if val.find('augmentation') == 0:
				footerindex.append(i)
	footerindex.append(len(footerlist))

	footercontent = addlines(footerlist,footerindex,filename)
	# print (footercontent)

	#DELETE FINAL LINE
	pass

	np.savetxt(outname,res,fmt=' %.11E %.11E %.11E %.11E %.11E',header=headercontent, footer=footercontent[:-1], comments='')
	print ("Finish Successfully")

def check(filename):
	for i in range(len(filename)):
		path = str(os.getcwd())+"/BvAt"+filename[i]+".dat"
		content = open(path).readlines()

		lastrowlist = content[-1].split()
		# print (lastrowlist)

		#Stupid Method haha
		if len(lastrowlist)==5:
			print ("Atom #" + str(filename[i]) + " Martix Check Pass")
		else:
			if len(lastrowlist)==4:
				lastrowlist.append(lastrowlist[-1])
			elif len(lastrowlist)==3:
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
			elif len(lastrowlist)==2:
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
			elif len(lastrowlist)==1:
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
				lastrowlist.append(lastrowlist[-1])
			# print (lastrowlist)
			tempxx = " ".join(lastrowlist)
			strlastrow = " " + tempxx + '\n'
			# print (strlastrow)
			finalcontent = content[:-1]
			finalcontent.append (strlastrow)
			fout = open(path,'w')
			fout.writelines(finalcontent)
			fout.close()
			print ("Atom #" + str(filename[i]) + " Martix Makeup")

def main(argv):
	Atom_selection = []
	outputfile_name = ''

	try:
		opts, args = getopt.getopt(argv, "ci:o:",["inputfile=","outputfile="])

	except getopt.GetoptError:
		print ("Error parameter: BaderMerge.py -i <AtomSelection_1> -i <AtomSelection_2> -o <Outputfile_name>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-c':
			print ('Copyright CaoZheng @ 2018')
			sys.exit()

		elif opt in ("-i","--inputfile"): #Atom-selection number
			# Atom_selection.append(arg)
			pass

		elif opt in ("-o","--outputfile"):
			outputfile_name = arg

	# Atom_selection_file_path = str(os.getcwd())+ '/atom_selection.txt'
	# Atom_selection_file = open(Atom_selection_file_path, 'r') 
	# sourcelines = Atom_selection_file.readlines()
	# for lines in sourcelines:
	# 	Atom_selection.append(lines.strip('\n'))
	Atom_selection = makeuplist()
	#Atom_selection should be list ['0001','0002',etc.]
	if Atom_selection == []:
		print ("Please add -i atom-selection!")
	else:
		print ("Atom selection:" + str(Atom_selection))
		if outputfile_name != '':
			check(Atom_selection)
			mergy(Atom_selection,outputfile_name)
		else:
			check(Atom_selection)
			mergy(Atom_selection)


if __name__ == "__main__":
	main(sys.argv[1:])