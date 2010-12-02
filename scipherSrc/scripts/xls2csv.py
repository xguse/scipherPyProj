import sys,optparse
from scipherSrc.defs.files_io import xls2csv
def main():
    usage = """python %prog [options] xlsPath outPath"""
    parser = optparse.OptionParser(usage)
    parser.add_option('--delim',type="str", default=",", 
                      help="""The text deleminator you wish to use. (default=%default)""")
    
    (opts, args) = parser.parse_args()
        
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        exit(0)
    if not len(args) == 2:
        raise Exception("**ERROR: you must supply both an xlsPath and outPath.**")
    
    xls2csv(args[0],args[1],sep=opts.delim)
    
if __name__ == "__main__":
    main()