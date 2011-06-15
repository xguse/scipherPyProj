import sys,optparse
from scipherSrc.defs.files_io import xls2csv
def main():
    usage = """python %prog [options] xlsPath [outPath]"""
    parser = optparse.OptionParser(usage)
    parser.add_option('-d','--delim',type="str", default=",", 
                      help="""The text deleminator you wish to use. (default=%default)""")
    
    (opts, args) = parser.parse_args()
        
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        exit(0)
    if not len(args) >= 1:
        raise Exception("**ERROR: you must supply at least an xlsPath.**")
    if len(args) == 1:
        args.append(None)
        
    xls2csv(args[0],args[1],sep=opts.delim)
    
if __name__ == "__main__":
    main()