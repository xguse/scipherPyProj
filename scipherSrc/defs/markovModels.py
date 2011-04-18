import random
import bisect

from scipherSrc.defs.basicDefs import slidingWindow

class WeightedRandomGenerator(object):
    def __init__(self, weights):
        self.totals = []
        running_total = 0
        for w in weights:
            running_total += w
            self.totals.append(running_total)
    def next(self):
        rnd = random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)
    def __call__(self):
        return self.next()

def nOrdMkvBkg(order,seqList):
    """Returns a dict representing the 'order'^th order background
    model of 'order' length substrings in 'seqList'.
    bkg[i-order:-1][i] = (count,freqTot,freqGroup)
    """   
    bkg = {}
    totWin = 0
    for seq in seqList:
        windows = slidingWindow(sequence=seq,winSize=order+1,step=1)
        for win in windows:
            try:
                bkg[tuple(win[:-1])]
                try:
                    bkg[tuple(win[:-1])][win[-1]] += 1
                    totWin += 1
                except KeyError:
                    bkg[tuple(win[:-1])][win[-1]] = 1
                    totWin += 1
            except KeyError:
                bkg[tuple(win[:-1])] = {}
                bkg[tuple(win[:-1])][win[-1]] = 1
                totWin += 1
    for k in bkg:
        totGroup = 0
        for j in bkg[k]:
            totGroup += bkg[k][j]
        for j in bkg[k]:
            count = bkg[k][j]
            bkg[k][j] = (count,float(count)/totWin,float(count)/totGroup)
    return bkg

def buildMarkovTxt(mkBkg,seed,length=100):
    """Given a <seed> of correct length, use the <mkBkg> to produce a markov chain of length <length>"""
    win = len(seed)
    chain = seed[:]
    for i in range(length):
        print tuple(chain[-win:])
        nextOptions = mkBkg[tuple(chain[-win:])].items()
        rand = WeightedRandomGenerator([x[1][2] for x in nextOptions])
        chain.append(nextOptions[rand()][0])
    return ' '.join(chain)

