# Template file for CSCI 5481 Fall 2015 Exercise 1
# Usage:
# template.py -h
import sys, os
import argparse
from subprocess import Popen, PIPE

def make_arg_parser():
    parser = argparse.ArgumentParser(prog='antismash_wrapper.py',
                          version="%prog 1.0",
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-q","--query",
                      default=argparse.SUPPRESS,
                      required=True,
                      help="Path to query .fna files [required]") 
    parser.add_argument("-o","--output",
                      default=argparse.SUPPRESS,
                      required=True,
                      help="Path to output directory [required]")
    parser.add_argument("-c","--command",
                      default='python run_antismash.py',
                      help="Path to run_antiSMASH.py") 
#     parser.add_argument("-V","--verbose",
#                       action="store_true",
#                       help="Verbose output")
    return parser

# Runs embalmer in --inline mode to obtain an alignment ID of two sequences
def run_embalmer(query, ref, embalmer_cmd='embalm')
    """thread worker function"""
    args = [embalmer_cmd]
    args.append('--inline')
    args.append(ref)
    args.append(query)

    cmd = ' '.join(args)
    return run_command(cmd, verbose=verbose)

# runs the given command and returns return value and output
def run_command(cmd, verbose=False):
    if verbose:
        print cmd
    proc = Popen(cmd,shell=True,universal_newlines=True,stdout=PIPE,stderr=PIPE)
    stdout, stderr = proc.communicate()
    return_value = proc.returncode
    return return_value, stdout, stderr

    
if __name__ == '__main__':
    parser = make_arg_parser()
    args = parser.parse_args()

    
    query_file = open(args.query,'U')
    header = query_file.readline()
    query = query_file.readline().strip()
    query_file.close()

    ref_file = open(args.ref,'U')
    header = ref_file.readline()
    ref = ref_file.readline().strip()
    ref_file.close()

    retval, stdout, stderr = run_embalmer(query, ref, args.command, args.verbose)
    print 'Return value', retval
    print 'Standard out:'
    print stdout
    print 'Standard err:'
    print stderr
    print 'Semiglobal alignment was:', stdout.split('\n')[3].strip().split(':')[1].strip()


