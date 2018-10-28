import json
import os
import pprint
import sys
from operator import itemgetter
from time import time
sys.path.append('/afs/cern.ch/user/m/magradze/dfs/cms-bot-hermag/cms-bot')
from es_utils import es_query, es_workflow_stats, format


def get_wf_info_from_es(release, architecture):
    query_info = {'workflows': '*',
                  'architecture': architecture,
                  'release_cycle': release}
    '''
    wf_hits = es_query(index='relvals_stats_*',
                       query='*',
                       start_time=int(time() * 1000) - int(86400 * 1000 * 7),
                       end_time=int(time() * 1000))
    '''
    wf_hits = es_query(index='relvals_stats_*',
                       query=format(
                           'release:%(release_cycle)s AND architecture:%(architecture)s AND (%(workflows)s)', **query_info),
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


def GroupWorkFlowInfoByReleaseArch(jsonData):
    wfs = {}
    for wf_info in jsonData['hits']['hits']:
        release = str(get_release(wf_info))
        workflowid = str(get_workflow_id(wf_info))
        stepid = str(get_step_id(wf_info))
        cpu_avg = float(get_cpu_avg(wf_info))
        mem_avg = float(get_mem_avg(wf_info))
        if release not in wfs.keys():
            wfs[release] = {}
        if workflowid not in wfs[release].keys():
            wfs[release][workflowid] = {}
        if stepid not in wfs[release][workflowid].keys():
            wfs[release][workflowid][stepid] = {}
            wfs[release][workflowid][stepid]["cpu_avg"] = []
            wfs[release][workflowid][stepid]["mem_avg"] = []
        wfs[release][workflowid][stepid]["cpu_avg"].append(float(cpu_avg))
        wfs[release][workflowid][stepid]["mem_avg"].append(float(mem_avg))
    return wfs


def AverageGroupWorkFlowInfoByReleaseArch(grouped_wfs):
    av_grpd_wf_by_rel_arch = {}
    for cmssw_release in grouped_wfs.keys():
        av_grpd_wf_by_rel_arch[cmssw_release] = {}
        for workflowid in grouped_wfs[cmssw_release].keys():
            av_grpd_wf_by_rel_arch[cmssw_release][workflowid] = {}
            for stepid in grouped_wfs[cmssw_release][workflowid].keys():
                av_grpd_wf_by_rel_arch[cmssw_release][workflowid][stepid] = {}
                av_grpd_wf_by_rel_arch[cmssw_release][workflowid][stepid]['cpu_avg'] = sum(
                    grouped_wfs[cmssw_release][workflowid][stepid]['cpu_avg']) / float(len(grouped_wfs[cmssw_release][workflowid][stepid]['cpu_avg']))
                av_grpd_wf_by_rel_arch[cmssw_release][workflowid][stepid]['mem_avg'] = sum(
                    grouped_wfs[cmssw_release][workflowid][stepid]['mem_avg']) / float(len(grouped_wfs[cmssw_release][workflowid][stepid]['mem_avg']))
    return av_grpd_wf_by_rel_arch


def workflow_output_check(jsonData):
    try:
        if 'hits' in jsonData.keys():
            if jsonData['hits']['hits'] and jsonData['hits']['hits'][0]:
                return True
        else:
            return False
    except:
        return False


def dump_wf_data(json_data):
    for workflow in json_data.keys():
        json_file_name = "%s.json" % str(workflow)
        with open(json_file_name, 'w') as outfile:
            json.dump(json_data[workflow], outfile, sort_keys=True, indent=4)


def dump_json_data(file_name, jsonData):
    raw_wfs = {}
    if workflow_output_check(jsonData):
        with open(file_name, 'w') as outfile:
            json.dump(jsonData['hits']['hits'], outfile, sort_keys=True, indent=4)
        return True
    return False
