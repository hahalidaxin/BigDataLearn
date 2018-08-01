# -*- coding: utf-8 -*-
from AlgorithmOur.ExperimentData import DataInformation
from GenGraphStatics import gengraphstatics
from AlgorithmOur.ExperimentSearch import OurSearch
from AlgorithmACC.ACC import ACCSearch
from AlgorithmATC.locATC import locATCSearch
from AlgorithmLCTC.LCTC import LCTCSearch

data_list = {
    'Ego': [[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "0", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "107", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "1684", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "1912", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "3437", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "348", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "3980", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "414", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "686", 'Ego'],
            [".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "698", 'Ego']],
    'EgoAll': [[".\\ExperimentDatasets\\Ego\\ego-Facebook\\facebook\\", "[0,107,1684,1912,3437,348,3980,414,686,698]",
                'EgoAll']],
    'Attribute': [[".\\ExperimentDatasets\\Attribute\\Cora\\", ["Cora.cites", "Cora.content"], 'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\Citeseer\\", ["Citeseer.cites", "Citeseer.content"], 'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\TerrorAttack\\", ["terrorist_attack_loc.edges", "terrorist_attack.nodes"], 'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\WebKB\\", ["Cornell.cites", "Cornell.content"], 'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\WebKB\\", ["Texas.cites", "Texas.content"], 'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\WebKB\\", ["Washington.cites", "Washington.content"],'Attribute'],
                  [".\\ExperimentDatasets\\Attribute\\WebKB\\", ["Wisconsin.cites", "Wisconsin.content"], 'Attribute']],
    'SNAP': [[".\\ExperimentDatasets\\SNAP\\", "amazon", 'SNAP'],
             [".\\ExperimentDatasets\\SNAP\\", "youtube", 'SNAP'],
             [".\\ExperimentDatasets\\SNAP\\", "dblp", 'SNAP'],
             [".\\ExperimentDatasets\\SNAP\\", "lj", 'SNAP'],
             [".\\ExperimentDatasets\\SNAP\\", "orkut", 'SNAP']],
    'SMALL': [[".\\ExperimentDatasets\\SMALL\\", "dolphins", 'SMALL'],
              [".\\ExperimentDatasets\\SMALL\\", "football", 'SMALL'],
              [".\\ExperimentDatasets\\SMALL\\", "karate", 'SMALL'],
              [".\\ExperimentDatasets\\SMALL\\", "polbooks", 'SMALL']],
    'Others': [[".\\ExperimentDatasets\\Others\\Yeast\\", "Yeast", 'Others'],
               [".\\ExperimentDatasets\\Others\\Ning\\", "Ning", 'Others']],
    'Special': [[".\\ExperimentDatasets\\Attribute\\TerroristRel\\",["TerroristRel", ["contact", "family", "colleague", "congregate"]], 'Special']]
}
with open("ResultforExperiment.txt",'a') as f:
    dataname = 'SNAP'
    datanum = len(data_list[dataname])
    for datarank in range(1):
        data = data_list[dataname][datarank]
        file_dir = data[0]
        data_name = data[1]
        data_type = data[2]
        QVn = -1
        QAn = -1
        pa = 0
        pb = 3
        pc = 0.7
        pd = 50

        f.writelines("--------------------------------DATA-{} || RANK-{} -------------------------------".format(dataname, datarank))
        f.write('\n')
        f.writelines("data:    {}".format(data))
        f.write('\n')
        print(data)

        # 获取实验数据
        obj1 = DataInformation(file_dir, data_name, data_type)
        Information = obj1.main()
        graph_information = Information[0]
        tempt_nodes_information = Information[1]
        # 获取输入集
        ExperimentalDataList = obj1.SampleList(QVn, QAn)
        # gengraphstatics(tempt_nodes_information)

        # print(graph_information)
        # print(tempt_nodes_information)
        # print(ExperimentalDataList)
        ##############################四个算法性能对比################################
        # 社区查找评估
        '''
        obj2 = OurSearch(graph_information, tempt_nodes_information, ExperimentalDataList)
        result = obj2.main(pa, pb, pc, pd)
        resultS = result[0]
        resultP = result[1]
        resultR = result[2]
        duration = result[3]
        TimeEvaluation = result[4]
        f.writelines("Finall results of Our is as follows ...... ")
        f.write('\n')
        f.writelines(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        f.write('\n')
        f.writelines(" \t Time : " + str(duration))
        f.write('\n')
        f.writelines(" \t TimeEvaluation : " + str(TimeEvaluation))
        f.write('\n')
        print("Our is done")
        print("Finall results of Our is as follows ...... ")
        print(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        print(" \t Time : " + str(duration))
        print(" \t TimeEvaluation : " + str(TimeEvaluation))
        print("Our is done")
        # f.writelines(graph_information)
        # f.writelines(tempt_nodes_information)
        # f.writelines(ExperimentalDataList)
        
        # 社区查找评估
        
        obj2 = ACCSearch(graph_information, tempt_nodes_information, ExperimentalDataList)
        result = obj2.main()
        resultS = result[0]
        resultP = result[1]
        resultR = result[2]
        duration = result[3]
        TimeEvaluation = result[4]
    
        f.writelines("Finall results of ACC is as follows ...... ")
        f.write('\n')
        f.writelines(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        f.write('\n')
        f.writelines(" \t Time : " + str(duration))
        f.write('\n')
        f.writelines(" \t TimeEvaluation : " + str(TimeEvaluation))
        f.write('\n')
        print("ACC is done")

        print("Finall results of ACC is as follows ...... ")
        print(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        print(" \t Time : " + str(duration))
        print(" \t TimeEvaluation : " + str(TimeEvaluation))
        print("ACC is done")
        '''
        # 社区查找评估
        obj2 = LCTCSearch(graph_information, tempt_nodes_information, ExperimentalDataList)
        result = obj2.main()
        resultS = result[0]
        resultP = result[1]
        resultR = result[2]
        duration = result[3]
        TimeEvaluation = result[4]
        '''
        f.writelines("Finall results of LCTC is as follows ...... ")
        f.write('\n')
        f.writelines(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        f.write('\n')
        f.writelines(" \t Time : " + str(duration))
        f.write('\n')
        f.writelines(" \t TimeEvaluation : " + str(TimeEvaluation))
        f.write('\n')
        print("LCTC is done")
        '''
        print("Finall results of LCTC is as follows ...... ")
        print(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        print(" \t Time : " + str(duration))
        print(" \t TimeEvaluation : " + str(TimeEvaluation))
        print("LCTC is done")

        '''
        # 社区查找评估
        obj2 = locATCSearch(graph_information, tempt_nodes_information, ExperimentalDataList)
        result = obj2.main()
        resultS = result[0]
        resultP = result[1]
        resultR = result[2]
        duration = result[3]
        TimeEvaluation = result[4]
        f.writelines("Finall results of ATC is as follows ...... ")
        f.write('\n')
        f.writelines(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        f.write('\n')
        f.writelines(" \t Time : " + str(duration))
        f.write('\n')
        f.writelines(" \t TimeEvaluation : " + str(TimeEvaluation))
        print("ATC is done")
        f.write('\n\n\n\n')

        print("Finall results of ATC is as follows ...... ")
        print(" \t F1score : " + str(resultS) + ", Precision : " + str(resultP) + ", Recall : " + str(resultR))
        print(" \t Time : " + str(duration))
        print(" \t TimeEvaluation : " + str(TimeEvaluation))
        print("ATC is done")
        '''
        ##############################四个算法性能对比#################################
