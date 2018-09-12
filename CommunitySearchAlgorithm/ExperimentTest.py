# -*- coding: utf-8 -*-
from AlgorithmOur.ExperimentData import DataInformation
from AlgorithmOur.ExperimentSearch import OurSearch
from AlgorithmOur.ExperimentSearch2 import OurSearch2
from AlgorithmACC.ACC import ACCSearch
from AlgorithmATC.locATC import locATCSearch
from AlgorithmATC2.locATC2 import locATC2Search
from AlgorithmATC3.locATC3 import locATC3Search
from AlgorithmLCTC.LCTC import LCTCSearch
from AlgorithmLCTC2.LCTC2 import LCTC2Search
from AlgorithmLCTC3.LCTC3 import LCTC3Search

gplus_list = ["100129275726588145876","100329698645326486178","100466178325794757407","100500197140377336562","100518419853963396365",
			"100521671383026672718","100535338638690515335","100637660947564674695","100668989009254813743","100715738096376666180",
			"100720409235366385249","100962871525684315897","101130571432010257170","101133961721621664586","101185748996927059931",
			"101263615503715477581","101373961279443806744","101499880233887429402","101541879642294398860","101560853443212199687",
			"101626577406833098387","101848191156408080085","101997124338642780860","102170431816592344972","102340116189726655233",
			"102615863344410467759","102778563580121606331","103236949470535942612","103241736833663734962","103251633033550231172",
			"103338524411980406972","103503116383846951534","103537112468125883734","103752943025677384806","103892332449873403244",
			"104076158580173410325","104105354262797387583","104226133029319075907","104290609881668164623","104607825525972194062",
			"104672614700283598130","104905626100400792399","104917160754181459072","104987932455782713675","105565257978663183206",
			"105646458226420473639","106186407539128840569","106228758905254036967","106328207304735502636","106382433884876652170",
			"106417861423111072106","106724181552911298818","106837574755355833243","107013688749125521109","107040353898400532534",
			"107203023379915799071","107223200089245371832","107296660002634487593","107362628080904735459","107459220492917008623",
			"107489144252174167638","107965826228461029730","108156134340151350951","108404515213153345305","108541235642523883716",
			"108883879052307976051","109130886479781915270","109213135085178239952","109327480479767108490","109342148209917802565",
			"109596373340495798827","109602109099036550366","110232479818136355682","110241952466097562819","110538600381916983600",
			"110581012109008817546","110614416163543421878","110701307803962595019","110739220927723360152","110809308822849680310",
			"110971010308065250763","111048918866742956374","111058843129764709244","111091089527727420853","111213696402662884531",
			"111278293763545982455","112317819390625199896","112463391491520264813","112573107772208475213","112724573277710080670",
			"112737356589974073749","112787435697866537461","113112256846010263985","113122049849685469495","113171096418029011322",
			"113356364521839061717","113455290791279442483","113597493946570654755","113718775944980638561","113799277735885972934",
			"113881433443048137993","114054672576929802335","114104634069486127920","114122960748905067938","114124942936679476879",
			"114147483140782280818","114336431216099933033","115121555137256496805","115273860520983542999","115360471097759949621",
			"115455024457484679647","115516333681138986628","115573545440464933254","115576988435396060952","115625564993990145546",
			"116059998563577101552","116247667398036716276","116315897040732668413","116450966137824114154","116807883656585676940",
			"116825083494890429556","116899029375914044550","116931379084245069738","117412175333096244275","117503822947457399073",
			"117668392750579292609","117734260411963901771","117798157258572080176","117866881767579360121","118107045405823607895",
			"118255645714452180374","118379821279745746467"]
data_list = {
	'Ego':[[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","0",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","107",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","1684",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","1912",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","3437",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","348",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","3980",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","414",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","686",'Ego',""],
		[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","698",'Ego',""]],
	'EgoAll':[[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\","[0,107,1684,1912,3437,348,3980,414,686,698]",'EgoAll',"facebook"],
		[".\\ExperimentDatasets\\Ego\\ego-Gplus\\gplus\\",str(gplus_list),'EgoAll',"gplus"]],
	'Attribute':[[".\\ExperimentDatasets\\Attribute\\Cora\\",["Cora.cites","Cora.content"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\Citeseer\\",["Citeseer.cites","Citeseer.content"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\TerrorAttack\\",["terrorist_attack_loc.edges","terrorist_attack.nodes"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\WebKB\\",["Cornell.cites","Cornell.content"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\WebKB\\",["Texas.cites","Texas.content"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\WebKB\\",["Washington.cites","Washington.content"],'Attribute',""],
		[".\\ExperimentDatasets\\Attribute\\WebKB\\",["Wisconsin.cites","Wisconsin.content"],'Attribute',""]],
	'SNAP':[[".\\ExperimentDatasets\\SNAP\\","amazon",'SNAP',""],
		[".\\ExperimentDatasets\\SNAP\\","youtube",'SNAP',""],
		[".\\ExperimentDatasets\\SNAP\\","dblp",'SNAP',""],
		[".\\ExperimentDatasets\\SNAP\\","lj",'SNAP',""],
		[".\\ExperimentDatasets\\SNAP\\","orkut",'SNAP',""]],
	'SMALL':[[".\\ExperimentDatasets\\SMALL\\","dolphins",'SMALL',""],
		[".\\ExperimentDatasets\\SMALL\\","football",'SMALL',""],
		[".\\ExperimentDatasets\\SMALL\\","karate",'SMALL',""],
		[".\\ExperimentDatasets\\SMALL\\","polbooks",'SMALL',""]],
	'Others':[[".\\ExperimentDatasets\\Others\\Yeast\\","Yeast",'Others',"0"],
		[".\\ExperimentDatasets\\Others\\Ning\\","Ning",'Others',"1"],
		[".\\ExperimentDatasets\\Others\\MarketLesser\\","MarketLesser",'Others',"1"],
		[".\\ExperimentDatasets\\Others\\BlogCatalog\\","BlogCatalog",'Others',"-1"],
		[".\\ExperimentDatasets\\Others\\Flicker\\","Flicker",'Others',"-1"],
		[".\\ExperimentDatasets\\Others\\Email\\","Email",'Others',"-1"]],
	'Special':[[".\\ExperimentDatasets\\Attribute\\TerroristRel\\",["TerroristRel",["contact","family","colleague","congregate"]],'Special',""]]
	}


data = data_list['SMALL'][0]
file_dir = data[0]
data_name = data[1]
data_type = data[2]
added = data[3]
QVn = -1
QAn = -1
pa = 0
pb = 3
pc = 0.7
pd = 50
# 获取实验数据
obj1 = DataInformation(file_dir,data_name,data_type,added)
Information = obj1.main()
graph_information = Information[0]
tempt_nodes_information = Information[1]
# 获取输入集
ExperimentalDataList = obj1.SampleList(QVn,QAn)


# ##############################四个算法性能对比#################################
# 社区查找评估
obj2 = OurSearch(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main(pa,pb,pc,pd)
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of Our is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of Our is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = OurSearch2(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main(pa,pb,pc,pd)
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of Our2 is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of Our2 is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = ACCSearch(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of ACC is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of ACC is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = locATCSearch(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of locATC is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of locATC is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = locATC2Search(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of locATC2 is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of locATC2 is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = locATC3Search(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of locATC3 is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of locATC3 is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()

# 社区查找评估
obj2 = LCTCSearch(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of LCTC is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of LCTC is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()
#
# 社区查找评估
obj2 = LCTC3Search(graph_information,tempt_nodes_information,ExperimentalDataList)
result = obj2.main()
resultS = result[0]
resultP = result[1]
resultR = result[2]
duration = result[3]
build_duration = result[4]
query_duration = result[5]
TimeEvaluation = result[6]
print("Finall results of LCTC3 is as follows ...... ")
print(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR))
print(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration))
print(" \t TimeEvaluation : "+str(TimeEvaluation))
f = open("Result_"+str(data_name)+".txt","a+")
f.write("Finall results of LCTC3 is as follows ...... \n")
f.write(" \t F1score : "+str(resultS)+", Precision : "+str(resultP)+", Recall : "+str(resultR)+"\n")
f.write(" \t Time : "+str(duration)+", build_duration : "+str(build_duration)+", query_duration : "+str(query_duration)+"\n")
f.write(" \t TimeEvaluation : "+str(TimeEvaluation)+"\n")
f.close()
##############################四个算法性能对比#################################