#!/usr/bin/env python

import argparse
import os
import logging
from talp_pages.io.run_folders import get_run_folders

from talp_pages.common import TALP_IMPLICIT_REGION_NAME
from talp_pages.reports.ci_report import CIReport, CIReportArgs
from pathlib import Path
def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-i", "--input-path", dest="path", help="Root path to search the *.json files in",required=True
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output",
        help="relative path for the output",
        required=True,
    )
    parser.add_argument('--regions', nargs='+', help='Names of regions of that will be highlited seperated by spaces',dest="regions")
    parser.add_argument('--region-for-badge', help=f"Name of region that will be used to generate the performance badges (Default: {TALP_IMPLICIT_REGION_NAME})",dest="region_for_badge",default=TALP_IMPLICIT_REGION_NAME)
    parser.add_argument('--badge', action=argparse.BooleanOptionalAction,default=True, help="Generate Parallel effiency badge .svg (Requires internet)")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],dest="log_level",help="Logger Level" ,default="ERROR")
    

def _verify_input(args):
    path = None

    # Check if the JSON file exists
    if os.path.exists(args.path):
        found_a_json = False
        for _, _, filenames in os.walk(args.path):
            for _ in [f for f in filenames if f.endswith(".json")]:
                found_a_json = True

        if not found_a_json:
            logging.error(
                f"The specified path '{args.path}' doesnt contain any .json files "
            )
            raise Exception("Path empty of .json files")
    else:
        logging.error(f"The specified path '{args.path}' does not exist.")
        raise Exception("Not existing path")

    # Check if output is empty
    if os.path.exists(args.output):
        if len(os.listdir(args.output)) != 0:
            logging.error(f"The specified output folder '{args.output}' is not empty")
            raise Exception("Non Empty output path")

    path = args.path
    output = args.output
    regions = [TALP_IMPLICIT_REGION_NAME]
    if args.regions:
        regions.extend(args.regions)

    region_for_badge = args.region_for_badge

    return path, output,regions,region_for_badge


def main(parsed_args):
    input_path, output_path, selected_regions,region_for_badge = _verify_input(parsed_args)

    log_level = getattr(logging, parsed_args.log_level.upper(), None)
    logging.basicConfig(level=log_level)
    
    run_folders = get_run_folders(input_path)
    report = CIReport(CIReportArgs(run_folders,selected_regions,region_for_badge,parsed_args.badge))
    report.write_to_folder(Path(output_path))

            
        


    

    

