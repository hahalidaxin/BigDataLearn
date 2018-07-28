# -*- coding: utf-8 -*-
import time

### STEP2 社区查找 ###
### STEP3 结果评估 ###
class OurSearch:
	def __init__(self,graph_information,tempt_nodes_information,ExperimentalDataList):
		self.graph_information = graph_information
		self.tempt_nodes_information = tempt_nodes_information
		self.ExperimentalDataList = ExperimentalDataList
		return

	def ACommunitySearch(self,QVlist,QAlist):
		SearchedInformation = {
				'SearchedMembers':[],
				'AdjacencyLists':{},
				'Inner':0,
				'InnerSquar':0,
				'Degree':0,
				'Node':0,
				'RelatedAttribute':0,
				'InnerList':{},
				'EvaluationSocre':0
				}
		# 数据初始化
		SearchedInformation['SearchedMembers'] = list(QVlist)
		SearchedInformation['Node'] = len(QVlist)
		for node in QVlist:
			Adjacency = self.tempt_nodes_information[node][0]
			Attribute = self.tempt_nodes_information[node][1]
			InnerN = 0
			for i in Adjacency:
				if i in SearchedInformation['SearchedMembers']:
					InnerN = InnerN + 1
				else:
					if i not in SearchedInformation['AdjacencyLists'].keys():
						SearchedInformation['AdjacencyLists'][i] = []
			SearchedInformation['Inner'] = SearchedInformation['Inner'] + InnerN
			SearchedInformation['InnerSquar'] = SearchedInformation['InnerSquar'] + InnerN**2
			SearchedInformation['Degree'] = SearchedInformation['Degree'] + len(Adjacency)
			SearchedInformation['InnerList'][node] = InnerN
			for i in Attribute:
				if i in QAlist:
					SearchedInformation['RelatedAttribute'] = SearchedInformation['RelatedAttribute'] + 1
		EvaluationSocre = self.Evaluation(SearchedInformation)
		SearchedInformation['EvaluationSocre'] = EvaluationSocre
		for node in SearchedInformation['AdjacencyLists'].keys():
			Adjacency = self.tempt_nodes_information[node][0]
			Attribute = self.tempt_nodes_information[node][1]
			tempt = [[],0,0,0,0,0,0,[],{}]
			for i in Adjacency:
				if i in SearchedInformation['SearchedMembers']:
					tempt[1] = tempt[1] + 1
					tempt[2] = tempt[2] + 2.0*SearchedInformation['InnerList'][i]
					tempt[7].append(i)
				else:
					tempt[0].append(i)
			tempt[2] = tempt[2] + tempt[1]**2 + tempt[1]
			tempt[3] = tempt[3] + len(Adjacency)
			tempt[4] = 1
			for i in Attribute:
				if i in QAlist:
					tempt[5] = tempt[5] + 1
			tempt[6] = len(Attribute)
			SearchedInformation['AdjacencyLists'][node] = list(tempt)
		# 循环加点
		BestAdjacency = {
			'node':'',
			'tempt':[],
			'PreEvaluationSocre':SearchedInformation['EvaluationSocre'],
			'notfind':0,
			'EvaluationSocre':0
		}
		deleted = []
		while 1:
			if SearchedInformation['AdjacencyLists'] == {}:
				break
			for node in SearchedInformation['AdjacencyLists'].keys():
				tempt = list(SearchedInformation['AdjacencyLists'][node])
				EvaluationSocre = self.Evaluation_Add(SearchedInformation,tempt)
				if EvaluationSocre > BestAdjacency['EvaluationSocre']:
					BestAdjacency['node'] = node
					BestAdjacency['tempt'] = list(tempt)
					BestAdjacency['EvaluationSocre'] = EvaluationSocre
			if BestAdjacency['EvaluationSocre'] < self.pc*BestAdjacency['PreEvaluationSocre'] or BestAdjacency['notfind'] > self.pd:
				break
			SearchedInformation['SearchedMembers'].append(BestAdjacency['node'])
			del SearchedInformation['AdjacencyLists'][BestAdjacency['node']]
			SearchedInformation['Inner'] = SearchedInformation['Inner'] + 2.0*BestAdjacency['tempt'][1]
			SearchedInformation['InnerSquar'] = SearchedInformation['InnerSquar'] + BestAdjacency['tempt'][2]
			SearchedInformation['Degree'] = SearchedInformation['Degree'] + BestAdjacency['tempt'][3]
			SearchedInformation['Node'] = SearchedInformation['Node'] + BestAdjacency['tempt'][4]
			SearchedInformation['RelatedAttribute'] = SearchedInformation['RelatedAttribute'] + BestAdjacency['tempt'][5]
			SearchedInformation['EvaluationSocre'] = BestAdjacency['EvaluationSocre']
			SearchedInformation['InnerList'][BestAdjacency['node']] = BestAdjacency['tempt'][1]
			for i in BestAdjacency['tempt'][7]:
				SearchedInformation['InnerList'][i] = SearchedInformation['InnerList'][i] + 1
			for i in BestAdjacency['tempt'][0]:
				if i in SearchedInformation['AdjacencyLists'].keys():
					SearchedInformation['AdjacencyLists'][i][2] = SearchedInformation['AdjacencyLists'][i][2] + 2.0*SearchedInformation['AdjacencyLists'][i][1] + 2 + 2.0*BestAdjacency['tempt'][1]
					SearchedInformation['AdjacencyLists'][i][1] = SearchedInformation['AdjacencyLists'][i][1] + 1
					SearchedInformation['AdjacencyLists'][i][7].append(BestAdjacency['node'])
					SearchedInformation['AdjacencyLists'][i][0].remove(BestAdjacency['node'])			
				else:
					Adjacency = self.tempt_nodes_information[i][0]
					Attribute = self.tempt_nodes_information[i][1]
					tempt = [[],0,0,0,0,0,0,[],{}]
					for j in Adjacency:
						if j in SearchedInformation['SearchedMembers']:
							tempt[1] = tempt[1] + 1
							tempt[2] = tempt[2] + 2.0*SearchedInformation['InnerList'][j]
							tempt[7].append(j)
						else:
							tempt[0].append(j)
					tempt[2] = tempt[2] + tempt[1]**2 + tempt[1]
					tempt[3] = tempt[3] + len(Adjacency)
					tempt[4] = 1
					for j in Attribute:
						if j in QAlist:
							tempt[5] = tempt[5] + 1
					tempt[6] = len(Attribute)
					SearchedInformation['AdjacencyLists'][i] = list(tempt)
			if BestAdjacency['EvaluationSocre'] < BestAdjacency['PreEvaluationSocre']:
				deleted.append(BestAdjacency['node'])
				BestAdjacency['node'] = ''
				BestAdjacency['tempt'] = []
				BestAdjacency['notfind'] = BestAdjacency['notfind'] + 1
				BestAdjacency['EvaluationSocre'] = 0
			else:
				BestAdjacency['node'] = ''
				BestAdjacency['tempt'] = []
				BestAdjacency['PreEvaluationSocre'] = BestAdjacency['EvaluationSocre']
				BestAdjacency['EvaluationSocre'] = 0
				deleted = []
		# 返回最终结果
		SearchedMembers = SearchedInformation['SearchedMembers']
		for i in deleted:
			if i in SearchedMembers:
				SearchedMembers.remove(i)
		return SearchedMembers

	### STEP3 结果评估 ###
	def Evaluation(self,SearchedMembers):
		if SearchedMembers['Node'] == 1:
			Quality = 0
		else:
			Quality = (SearchedMembers['Inner']+SearchedMembers['InnerSquar']*1.0/(SearchedMembers['Node']-1))*SearchedMembers['Inner']/(SearchedMembers['Degree']*SearchedMembers['Node'])*(SearchedMembers['Inner']/SearchedMembers['Degree'])**self.pa
		Relation = SearchedMembers['RelatedAttribute']*1.0/SearchedMembers['Node']
		SearchedMembers['EvaluationSocre'] = Quality*(Relation+0.00001)**self.pb
		EvaluationSocre = SearchedMembers['EvaluationSocre']
		return EvaluationSocre

	### STEP3 结果评估 ###
	def Evaluation_Add(self,SearchedMembers,tempt):
		Inner = SearchedMembers['Inner'] + tempt[1]
		InnerSquar = SearchedMembers['InnerSquar'] + tempt[2]
		Degree = SearchedMembers['Degree'] + tempt[3]
		Node = SearchedMembers['Node'] + tempt[4]
		RelatedAttribute = SearchedMembers['RelatedAttribute'] + tempt[5]
		#
		Quality = (Inner+InnerSquar*1.0/(Node-1))*Inner/(Degree*Node)*(Inner/Degree)**self.pa
		Relation = RelatedAttribute*1.0/Node
		EvaluationSocre = Quality*(Relation+0.00001)**self.pb
		return EvaluationSocre

	### STEP3 结果评估 ###
	def F1Score(self,GMembers,SearchedMembers):
		samen = 0
		for i in GMembers:
			if i in SearchedMembers:
				samen = samen + 1
		precision = samen*1.0/len(SearchedMembers)
		recall = samen*1.0/len(GMembers)
		Fscore = 2*precision*recall/(precision+recall)
		return [precision,recall,Fscore]

	def main(self,pa,pb,pc,pd):
		self.pa = pa
		self.pb = pb
		self.pc = pc
		self.pd = pd
		starttime = time.time()
		results = {
				'allscore':0,
				'allprecision':0,
				'allrecall':0,
				'allmemberlen':0
			}
		for i in range(0,len(self.ExperimentalDataList)):
			TestData = self.ExperimentalDataList[i]
			group_name = TestData[0]
			QVlist = TestData[1]
			QAlist = TestData[2]
			GMembers = self.graph_information['Groups'][group_name][0]
			SearchedMembers = self.ACommunitySearch(QVlist,QAlist)
			[precision,recall,score] = self.F1Score(GMembers,SearchedMembers)
			results['allscore'] = results['allscore'] + score
			results['allprecision'] = results['allprecision'] + precision
			results['allrecall'] = results['allrecall'] + recall
			results['allmemberlen'] = results['allmemberlen'] + len(GMembers)
		endtime = time.time()
		duration = endtime-starttime
		if len(self.ExperimentalDataList) == 0:
			resultS = -1
			resultP = -1
			resultR = -1
			averagelen = -1
			TimeEvaluation = -1
		else:
			resultS = results['allscore']*1.0/len(self.ExperimentalDataList)
			resultP = results['allprecision']*1.0/len(self.ExperimentalDataList)
			resultR = results['allrecall']*1.0/len(self.ExperimentalDataList)
			averagelen = results['allmemberlen']*1.0/len(self.ExperimentalDataList)
			TimeEvaluation = duration*1.0/len(self.ExperimentalDataList)/averagelen
		return [resultS,resultP,resultR,duration,TimeEvaluation]

