import collections
import numpy as np
import itertools

class General:
    
    
    def __init__(self, g_id, loyalty, post=None):
        self.g_id = g_id
        self.loyalty = loyalty
        self.post = post
        self.allMessagesReceived = []
        self.previousRoundMessages = []
        self.messages = []
    
    def send_message(self, generalToSend, c_mes, round):
        mStr = str(self.g_id) + "," + c_mes
        
        if self.loyalty == "T":
            ord = mStr[-1]
            
            if round == 0:
                if ord == "A":
                    new_ord = "R"
                elif ord == "R":
                    new_ord = "A"
                mStr = mStr.replace(ord, new_ord)
        generalToSend.receive_message(mStr)
        #print("General {} (loyalty {}) sent message {} to General {}".format(self.g_id, self.loyalty, mStr, generalToSend.g_id))

    def cm_send_message(self, generalToSend, order):
        mStr = str(self.g_id) + "," + order
        generalToSend.receive_message(mStr)
    
    

    def receive_message(self, messageStr):
        self.messages.append(messageStr)
        self.allMessagesReceived.append(messageStr)


# Example Inputs


NUM_OF_LEIUTENANTS = 6
COMMANDER_LOYALTY = "L"
loyalties = "LTLLTL"


'''
NUM_OF_LEIUTENANTS = 3
COMMANDER_LOYALTY = "L"
loyalties = "LLT"
'''

'''
NUM_OF_LEIUTENANTS = 9
COMMANDER_LOYALTY = "T"
loyalties = "LLLLTTLLL"
'''

traitorCount = (COMMANDER_LOYALTY + loyalties).count("T")

if traitorCount > (NUM_OF_LEIUTENANTS + 1)*2/3:
    raise ValueError("Assumption Failure: Too many traitors!")
print(traitorCount)

# Initialize Commander
commander = General(0, COMMANDER_LOYALTY, "CM")

# Initialize Generals
generals = []
generals.append(commander)


for i in range(NUM_OF_LEIUTENANTS):
    generals.append(General(i+1, loyalties[i], "LT"))


print("Initializing Generals: Starting State ->")
for g in generals:
    print(g.__dict__)
    
print("Total Generals: ", NUM_OF_LEIUTENANTS+1, "  | ","Commander Loyalty: ", generals[0].loyalty, " |  Traitor Lieutenants: ", loyalties.count("T"))


#Oral Message Algorithm
print("Oral Message Algorithm Starting: Phase 1")

rounds = traitorCount 

#total rounds is equal to number of traitors + 1, use <= if using while with rounds var



#Phase 1: Commander's Turn
#print(generals[0].__dict__)


#send initial set of messages including actual order
for gens in generals[1:]:
    #print(gens.__dict__)
    if commander.loyalty == "L":
        #commander is loyal, send same message to all LTs
        order = "A"
        commander.cm_send_message(gens, order)
    elif commander.loyalty == "T":
        #commander is traitor, send different message to half
        n = len(generals[1:])//2
        halfgens1 = generals[1:n]
        halfgens2 = generals[n:]
        
        for g in halfgens1:
            commander.cm_send_message(g, "A")
        for g in halfgens2:
            commander.cm_send_message(g, "R")

    

for g in generals:
    g.previousRoundMessages += g.messages
    g.messages = []
    print(g.__dict__)

for r in range(rounds):
    
    print("\n Round: ",r+1 , "\n \n")

    for g in generals:
        for m in g.previousRoundMessages:
                #print("Message Sent: ", m)
                for other_g in generals:
                    if g.post == "CM" or other_g.post == "CM": continue
                    if g.g_id == other_g.g_id: continue
                    if str(other_g.g_id) in m: 
                        #print("Message: ", m, " | Id Found: ", other_g.g_id) 
                        continue
                    g.send_message(other_g, m, r)
        
    for g in generals:
        g.previousRoundMessages = g.messages
        g.messages = []
        print("General {}: ".format(g.g_id))
        print(g.__dict__, "\n")
        

# Format messages to match assignment
for g in generals[1:]:
    res = [x[-3::-1] + x[-2:] for x in g.allMessagesReceived if len(x) >= 3]
    g.allMessagesReceived = []
    g.allMessagesReceived += res



#Phase 2: Consensus
print('Phase 2: Consensus \n')


# Message Grouping

for g in generals[1:]:
    util_func = lambda x: x[0:5]
    temp = sorted(g.allMessagesReceived, key = util_func)
    res = [list(ele) for i, ele in itertools.groupby(temp, util_func)]
    #print(g.allMessagesReceived)
    #print(res)
    consensusList = [] # 'A', 'R'
    for r in res:
        print(r)
        rConsensusCommands = [s[-1] for s in r]
        print(rConsensusCommands)
        res_con = collections.Counter(rConsensusCommands)
        aCons, rCons = res_con['A'], res_con['R']
        #print("Consensus A: ", aCons, " Consensus R: ", rCons)
        if aCons > rCons:
            consensusList.append('A')
        else:
            consensusList.append('R')

    superConsensus = collections.Counter(consensusList)
    saCons, srCons = superConsensus['A'], superConsensus['R']

    if saCons > srCons:
        g.consensus = 'A'
    else:
        g.consensus = 'R'


    #print(consensusList)
    print("\n General {} Consensus: {}".format(g.g_id, g.consensus))

print("#########################")




'''
for g in generals[1:]:
    consensusCommands = [s[-1] for s in g.allMessagesReceived]
    #print("General {} (Loyalty {}) Consensus Str: {}".format(g.g_id, g.loyalty, consensusCommands))
    cons = collections.Counter(consensusCommands)
    aCons, rCons = cons['A'], cons['R']
    if aCons > rCons:
        g.consensus = "A"
        print("General {} (Loyalty {}) Consensus Reached. Command: {}".format(g.g_id, g.loyalty, "A"))
    else:
        g.consensus = "R"
        print("General {} (Loyalty {}) Consensus Reached. Command: {}".format(g.g_id, g.loyalty, "R"))

'''

print("Final Consensus ->")
for g in generals[1:]:
    print("General {} (Loyalty {}) Command: {}".format(g.g_id, g.loyalty, g.consensus))

