#!/usr/bin/env python
import sys
import pprint
import optparse
from time import time

from WorkFlowInfoCollectionModules import *


def get_opt():
    usage = 'usage: GetAllWorkFlowsInfo.py --show -s '

    parser = optparse.OptionParser(usage)

    parser.add_option('-r', '--release',
                      help='CMSSW release, e.g. "CMSSW_10_4_X_*"',
                      dest='release',
                      default='*'
                      )

    parser.add_option('-a', '--architecture',
                      help='CMSSW architecture, e.g. "slc6_amd64_gcc700"',
                      dest='architecture',
                      default='*'
                      )
    opt, args = parser.parse_args()
    return opt, args


if __name__ == '__main__':
    file_name = "workflows.json"
    opt, args = get_opt()
    wfs = {}
    raw_wfs = get_wf_info_from_es(str(opt.release), str(opt.architecture))
    grouped_wfs = GroupWorkFlowInfoByReleaseArch(raw_wfs)
    averaged_wfs = AverageGroupWorkFlowInfoByReleaseArch(grouped_wfs)
    if dump_wf_data(averaged_wfs):
        sys.exit(0)
    else:
        sys.exit(2)
