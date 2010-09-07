import collections
import csv

def tableFile2namedTuple(tablePath,sep='\t'):
    """Returns namedTuple from table file using first row fields as col headers."""

    reader  = csv.reader(open(tablePath), delimiter=sep)
    headers = reader.next()
    Table   = collections.namedtuple('Table', ', '.join(headers))
    data    = map(Table._make, reader)
    return data

class ParseSolexaSorted(object):
    """Class to parse and return a single read entry from solexa x_sorted.txt file type."""
    def __init__(self,filePath):
        """Returns a line-by-line solexa x_sorted.txt parser analogous to file.readline().
        Exmpl: parser.getNext() """
        self._file = open(filePath, 'rU')
    
    def _parseCoords(self,line):
        """Takes solexa file line, returns t(contig,start,stop)"""
        contig = line[11]
        start  = int(line[12])
        stop   = int(line[12])+int(line[14])-1 # start+len-1
        return tuple([contig,start,stop])
        
    def getNext(self):
        """Reads in next line, parses fields, returns fieldTuple or None (eof)."""
        line = self._file.readline()
        if line:
            return tuple(line.strip('\n').split('\t'))
        else: 
            return None
    
    def getNextReadSeq(self):
        """Calls self.getNext and returns only the readSeq."""
        line = self.getNext()
        if line:
            return line[8]
        
    def getNextReadCoords(self):
        """Calls self.getNext and returns only the readCoords t(str(contig),int(start),int(stop))."""
        line = self.getNext()
        if line:
            return self._parseCoords(line)
            

class ParseBowtieMap(object):
    """Class to parse and return a single read entry from bowtie.map file type."""
    def __init__(self,filePath):
        """Returns a line-by-line bowtie.map parser analogous to file.readline().
        Exmpl: parser.getNext() """
        self._file = open(filePath, 'rU')
        
    def _parseCoords(self,line):
        """Returns coords info t(contig,start,stop) for a bowtie.map line tuple"""
        contig = line[2]
        start  = int(line[3])
        stop   = int(line[3])+len(line[4])-1 # start+len-1
        return tuple([contig,start,stop])
    
    def _parseReadSeq(self,line):
        """Returns seq string bowtie.map line tuple"""
        return line[4]
    
    def getNext(self):
        """Reads in next line, splits fields, returns fieldTuple or None (eof)."""
        line = self._file.readline()
        if line:
            return tuple(line.strip('\n').split('\t'))
        else: 
            return None
    
    def getNextReadSeq(self):
        """Calls self.getNext and returns only the readSeq."""
        line = self.getNext()
        if line:
            return self._parseReadSeq(line)


class ParseFastQ(object):
    """Returns a read-by-read fastQ parser analogous to file.readline()"""
    def __init__(self,filePath,headerSymbols=['@','+']):
        """Returns a read-by-read fastQ parser analogous to file.readline().
        Exmpl: parser.next()
        -OR-
        Its an iterator so you can do:
        for rec in parser:
            ... do something with rec ...

        rec is tuple: (seqHeader,seqStr,qualHeader,qualStr)
        """
        self._file = open(filePath, 'rU')
        self._currentLineNumber = 0
        self._hdSyms = headerSymbols
        
    def __iter__(self):
        return self
    
    def next(self):
        """Reads in next element, parses, and does minimal verification.
        Returns: tuple: (seqHeader,seqStr,qualHeader,qualStr)"""
        # ++++ Get Next Four Lines ++++
        elemList = []
        for i in range(4):
            line = self._file.readline()
            self._currentLineNumber += 1 ## increment file position
            if line:
                elemList.append(line.strip('\n'))
            else: 
                elemList.append(None)
        
        # ++++ Check Lines For Expected Form ++++
        trues = [bool(x) for x in elemList].count(True)
        nones = elemList.count(None)
        # -- Check for acceptable end of file --
        if nones == 4:
            raise StopIteration
        # -- Make sure we got 4 full lines of data --
        assert trues == 4,\
               "** ERROR: It looks like I encountered a premature EOF or empty line.\n\
               Please check FastQ file near line #%s (plus or minus ~4 lines) and try again**" % (self._currentLineNumber)
        # -- Make sure we are in the correct "register" --
        assert elemList[0].startswith(self._hdSyms[0]),\
               "** ERROR: The 1st line in fastq element does not start with '%s'.\n\
               Please check FastQ file and try again **" % (self._hdSyms[0])
        assert elemList[2].startswith(self._hdSyms[1]),\
               "** ERROR: The 3rd line in fastq element does not start with '%s'.\n\
               Please check FastQ file and try again **" % (self._hdSyms[1])
        
        # ++++ Return fatsQ data as tuple ++++
        return tuple(elemList)
    
    def getNextReadSeq(self):
        """Convenience method: calls self.getNext and returns only the readSeq."""
        try:
            record = self.next()
            return record[1]
        except StopIteration:
            return None

            


class ParseFastA(object):
    """Returns a record-by-record fastA parser analogous to file.readline()."""
    def __init__(self,filePath,joinWith='',key=None):
        """Returns a record-by-record fastA parser analogous to file.readline().
        Exmpl: parser.next()
        Its ALSO an iterator so "for rec in parser" works too!
        
        <joinWith> is string to use to join rec lines with.
        joinWith='' results in a single line with no breaks (usually what you want!)
        
        <key> is func used to parse the recName from HeaderInfo.
        """
        
        self._file = open(filePath, 'rU')
        if key:
            self._key = key
        else:
            self._key = lambda x:x[1:].split()[0]
        self.bufferLine = None   # stores next headerLine between records.
        self.joinWith = joinWith
        
    
    def __iter__(self):
        return self
        
    def next(self):
        """Reads in next element, parses, and does minimal verification.
        Returns: tuple: (seqName,seqStr)"""
        # ++++ Get A Record ++++
        recHead = ''
        recData = []
        # ++++ Check to see if we already have a headerLine ++++
        if self.bufferLine:
            recHead = self.bufferLine
        else:
        # ++++ If not, seek one ++++
            while 1:
                line = self._file.readline()
                if line.startswith('>'):
                    recHead = line
                    break
                elif not line:
                    raise Exception, "CheckFastaFile: Encountered EOF before any data."
                elif line.strip() == '':
                    continue
                else:
                    raise Exception, 'CheckFastaFile: The first line containing text does not start with ">".'
        # ++++ Collect recData ++++
        while 1:
            line = self._file.readline()
            if not line:
                raise StopIteration
            elif line.startswith('>'):
                self.bufferLine = line.strip('\n')
                break
            elif not line.startswith('>'):
                recData.append(line.strip('\n'))

        # ++++ Minor Seq Validation ++++
        ## AddHere
        # ++++ Format Rec For Return ++++
        if not recData:
            return None
        else:
            recHead = self._key(recHead)
            return (recHead,self.joinWith.join(recData))   
    
    def toDict(self):
        """Returns a single Dict populated with the fastaRecs
        contained in self._file."""
        fasDict = {}
        while 1:
            try:
                fasRec = self.next()
            except StopIteration:
                break
            if fasRec:
                if not fasRec[0] in fasDict:
                    fasDict[fasRec[0]] = fasRec[1]
                else:
                    raise Exception, "DuplicateFastaRec: %s occurs in your file more than once."
            else:
                break
        return fasDict