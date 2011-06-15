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






## Wikipedia Viterbi Example ##

# Helps visualize the steps of Viterbi.
def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7s" % ("%d" % i),
    print
 
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print
 
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
 
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])




if __name__ == "__main__":
    states = ('Rainy', 'Sunny')
 
    observations = ('walk', 'shop', 'clean')
     
    start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
     
    transition_probability = {
       'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
       'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
       }
     
    emission_probability = {
       'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
       'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
       }
    def example():
        return viterbi(observations,
                       states,
                       start_probability,
                       transition_probability,
                       emission_probability)
    print example()