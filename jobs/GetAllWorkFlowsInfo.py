
import optparse
#from operator import itemgetter
#import sys
#import json
#import os
import pprint
from time import time

from WorkFlowInfoCollectionModules import *

#from es_utils import es_query, es_workflow_stats, format


def get_opt():
    usage = 'usage: GetAllWorkFlowsInfo.py --show -s '

    parser = optparse.OptionParser(usage)

    parser.add_option('-r', '--release',
                      help='CMSSW release, e.g. 10_4_X.',
                      dest='release',
                      default='CMSSW_10_4_X_*'
                      )

    parser.add_option('-a', '--architecture',
                      help='CMSSW architecture, e.g. slc6_amd64_gcc700.',
                      dest='architecture',
                      default='slc6_amd64_gcc700'
                      )

    opt, args = parser.parse_args()

    return opt, args


if __name__ == '__main__':
    file_name = "workflows.json"
    opt, args = get_opt()
    wfs = {}
    wfs = get_wf_info_from_es()
    raw_wfs = GetWorkFlowsByReleaseArch(wfs)
    #workflowinfo = GroupWorkFlowInfoByReleaseArch(raw_wfs)
    if dump_json_data(file_name, wfs):
        print "json file %s has been dumped." % file_name
    else:
        print "json file %s dump has failed." % file_name
    get_statistics(wfs)
