# Byzantine Generals Problem

This is an exmaple implementation of the Byzantine Generals problem (also known as Byzantine fault). It is an important conceptual problem in distrubuted computing to identify faulty or "traitor" nodes/servers/generals. Practical implementations of Byzantine Fault Tolerance is one of the most important concepts in modern computer science with its most notable use in cryptocurrencies like Bitcoin.

Understanding the problem
-------------------------
Many allied generals have surrounded an enemy castle. They must decide what the do next with the only catch being that they must all come to the same conclusion (reach **consensus**). They must decide as a group to either **attack** or **retreat**. And they can communicate with each other by sending messages to others. But there's a twist: within the allied generals exist few which are _traitors_. These traitors may or may not at any time choose to vote for a suboptimal command in an attempt to ruin the coordination between all generals. All allied generals by default vote to retreat.

Thus, the Byzantine Generals problem states that all non-traitorous allied generals must decide together as a whole to either **attack** or **retreat**. A failure to come a single conclusive decision for all such generals results in an uncoordinated attack where some generals attacks and some retreat.

A system which _always_ achieves consensus in considered a Byzantine fault tolerant system. 

Generals
--------
There are two types of generals within this simulation:
- Commander (only 1 commander)
- Lieutenents (many lieutenents)

Both Commanders and Lieutenents can be traitorous and act maliciously at any time. This means they don't have to choose the suboptimal action every time. 

Assumptions
-----------
This scenario has a few assumption which are needed to ensure that the system in fault tolerant. These are:
- Messages sent between generals are secure
- Generals are not aware of the **loyalty** (loyal or traitor) of any other general
- There are only _m_ traitors in _3m_ generals

The last assumption was proven in the original paper as a requirement for the system to work correctly. Note that in the code, you can remove any check for the number of traitors, and see the system working incorrectly as well.

Solution (Oral Message Algorithm)
---------------------------------
One of the solutions to this problem is the Oral Message Algorithm. This algorithm works by exchanging messages between the generals. When sending a message, each general adds their own ID on to the message. There are 2 main phases in this algorithm:

Phase 1: Pass messages within the generals 
    - This phase runs for _m + 1_ rounds with _m_ traitors
    - Round 0 is the Commander general sending a command to all Lieutenent generals. A loyal Commander will send the same message to all lieutenents but a traitorous Commander may send conflicting messages.
    - Round 1 - _m+1_: Each general propogates the messages they receive in the previous round appending their own ID to the message. This message is sent to all generals which don't already exist within the chain of the message received

Phase 2: Each general decides an action
    - To find consensus, each general finds the consensus from the messages received (each message contains a command) is the last round
    - Each such consensus is used to roll-up for the messages received for the round
    - At the end, the final consensus will be reached and this command will be the chosen action from the general.

Cost
----
This algorithm is very costly. For _n_ generals and _m_ traitors, the total number of messages is _O(n^m+1)_

