# Byzantine Generals Problem

This is an exmaple implementation of the Byzantine Generals problem (also known as Byzantine fault). It is an important conceptual problem in distrubuted computing to identify faulty or "traitor" nodes/servers/generals. 

Understanding the problem
-------------------------

Many allied generals have surrounded an enemy castle. They must decide what the do next with the only catch being that they must all come to the same conclusion (reach **consensus**). They must decide as a group to either **attack** or **retreat**. But there's a twist: within the allied generals exist few which are __traitors__. These traitors may or may not at any time choose to vote for a suboptimal command in an attempt to ruin the coordination between all generals. 

Thus, the Byzantine Generals problem states that all non-traitorous allied generals must decide together as a whole to either **attack** or **retreat**. A failure to come a single conclusive decision for all such generals results in an uncoordinated attack where some generals attacks and some retreat. 