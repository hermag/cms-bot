import json
import os
import pprint
import sys
from operator import itemgetter
from time import time
sys.path.append('/afs/cern.ch/user/m/magradze/dfs/cms-bot-hermag/cms-bot')
from es_utils import es_query, es_workflow_stats, format

def get_wf_info_from_es():
    query_info = {'workflows': '*', 'architecture': 'slc6_amd64_gcc700', 'release_cycle': 'CMSSW_10_4_X_*'}
    wf_hits = es_query(index='relvals_stats_*',
                       query='*',
                       start_time=int(time() * 1000) - int(86400 * 1000 * 7),
                       end_time=int(time() * 1000))
    return wf_hits


def get_release(item):
    cmssw_release = str(item['_source']["release"]).replace("-", "_")
    cmssw_release_list = cmssw_release.split("_")
    cmssw_release = "CMSSW_%s_%s_X" % (str(cmssw_release_list[1]), str(cmssw_release_list[2]))
    return cmssw_release


def get_workflow_id(item):
    return item['_source']["workflow"]


def get_step_id(item):
    return item['_source']["step"]


def get_cpu_avg(item):
    return item['_source']["cpu_avg"]


def get_mem_avg(item):
    return item['_source']["vms_avg"]


def GroupWorkFlowsByReleaseArch(jsonData):
    wfs = {}
    for wf_info in jsonData:
        print get_release(wf_info)
        print get_workflow_id(wf_info)
        print get_step_id(wf_info)
        print get_cpu_avg(wf_info)
        print get_mem_avg(wf_info)
    return 0


def workflow_output_check(jsonData):
    try:
        if 'hits' in jsonData.keys():
            if jsonData['hits']['hits'] and jsonData['hits']['hits'][0]:
                return True
        else:
            return False
    except:
        return False


def dump_json_data(file_name, jsonData):
    if workflow_output_check(jsonData):
        GroupWorkFlowsByReleaseArch(jsonData['hits']['hits'])
        with open(file_name, 'w') as outfile:
            json.dump(jsonData['hits']['hits'], outfile, sort_keys=True, indent=4)
        return True
    return False


def get_statistics(workflows):
    print workflows.keys()
    print "hits ---> ", workflows['hits'].keys()
    print "hits --> hits ---> "
    # pprint.pprint(workflows['hits']['hits'])
    print "hits --> total ---> "
    # pprint.pprint(workflows['hits']['total'])
    print "hits --> max_score ---> "
    # pprint.pprint(workflows['hits']['max_score'])
    # print "took ---> ", workflows['hits'].keys()
    # pprint.pprint(workflows['hits']['took'])
    print "timed_out ---> "
    pprint.pprint(workflows['timed_out'])
    return 0
