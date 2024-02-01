# Inspired by the brain
We chose to utitilize the _INSERT_NN_TECHNIQUE_HERE_ technique for our purposes. Below you will find an explanation as to why.

## Active brain regions during risk assessment
_This is a very simplified overview of the active regions in the brain during risk assessment. For our purposes these regions will suffice._ 

In order from input to output:
1. [Prefrontal Cortex (PFC)](https://en.wikipedia.org/wiki/Prefrontal_cortex):
    + Function: Executive functions, decision-making, planning.
    + Keywords: Reasoning, decision, planning.
1. [Amygdala](https://en.wikipedia.org/wiki/Amygdala):
    + Function: Emotion processing, especially fear and reward.
    + Keywords: Emotion, fear, reward.
1. [Hippocampus](https://en.wikipedia.org/wiki/Hippocampus):
    + Function: Memory formation, spatial navigation.
    + Keywords: Memory, spatial, navigation.
1. [Basal Ganglia](https://en.wikipedia.org/wiki/Basal_ganglia):
    + Function: Procedural learning, habit formation, motor functions.
    + Keywords: Learning, habits, motor.
1. [Insular Cortex](https://en.wikipedia.org/wiki/Insular_cortex):
    + Function: Interoception, processing internal states.
    + Keywords: Internal, feedback, states.

## Clarification
1. **Input Layer (Prefrontal Cortex Analogy)**:
The initial game state and relevant information are processed first, mimicking the role of the prefrontal cortex in handling executive functions and initial decision-making processes.
1. **Memory Layer (Hippocampus Analogy)**:
The RNN includes a memory layer to capture and store information from past game states, allowing the network to learn from experience and adapt its strategies over time.
1. **Hidden Layers (Amygdala Analogy)**:
Hidden layers follow the memory layer to capture the emotional and intuitive aspects of risk assessment. This order reflects the idea that learned emotional responses and intuitive judgments are influenced by past experiences stored in memory.
1. **Decision-Making Layer (Basal Ganglia Analogy)**:
The decision-making layer processes information from the hidden layers and recurrent connections, allowing the RNN to form strategies and make decisions based on learned patterns and emotional cues.
1. **Feedback Layer (Insular Cortex Analogy)**:
A feedback layer follows the decision-making layer to integrate internal feedback signals, allowing the network to evaluate its own performance and adjust strategies based on its internal states and assessments.

## Alternative NNs
_These are more inline with the parallel nature of the brain_
- [Graph Neural Networks](https://en.wikipedia.org/wiki/Graph_neural_network) (GNNs):
    - Rationale:
GNNs operate on graph-structured data, allowing them to model relationships and dependencies more explicitly.
Nodes in the graph can represent different elements of the game, and edges can represent relationships or interactions between them.
GNNs can capture information from neighboring nodes, enabling more parallelized processing compared to the sequential nature of RNNs.
- [Recurrent Neural Networks](https://en.wikipedia.org/wiki/Recurrent_neural_network) (RNNs) with [Attention Mechanisms](https://en.wikipedia.org/wiki/Attention_(machine_learning)):
    - Rationale:
Attention mechanisms allow the model to focus on specific parts of the input, simulating the brain's ability to selectively attend to relevant information.
By incorporating attention mechanisms into an RNN or a variant like the Transformer, you can enhance the model's ability to capture dependencies in a more parallelized manner.
- [Neuromorphic Computing](https://en.wikipedia.org/wiki/Neuromorphic_engineering):
    - Rationale:
Neuromorphic computing architectures are designed to mimic the structure and function of the human brain more closely.
Spiking neural networks, a type of neuromorphic model, operate in an event-driven manner, potentially offering better parallelism.
- [Ensemble Learning](https://en.wikipedia.org/wiki/Ensemble_learning):
    - Rationale:
Ensembles combine multiple models to improve overall performance.
Each model in the ensemble can focus on different aspects of the problem, contributing to a more holistic and parallelized approach.

## Why we chose specific NNs
Each layer in the network has been commented to support our reasoning for choosing that NN. You can find these layers in [regions](src/brain/regions) and if you want to see them being used, check out [brain.py](src/brain/brain.py).

## Sources
- [Prefrontal Cortex](https://en.wikipedia.org/wiki/Prefrontal_cortex)
- [Amygdala](https://en.wikipedia.org/wiki/Amygdala)
- [Hippocampus](https://en.wikipedia.org/wiki/Hippocampus)
- [Basal Ganglia](https://en.wikipedia.org/wiki/Basal_ganglia)
- [Insular Cortex](https://en.wikipedia.org/wiki/Insular_cortex)
- [Graph Neural Networks](https://en.wikipedia.org/wiki/Graph_neural_network)
- [Recurrent Neural Networks](https://en.wikipedia.org/wiki/Recurrent_neural_network)
- [Attention Mechanisms](https://en.wikipedia.org/wiki/Attention_(machine_learning))
- [Neuromorphic Computing](https://en.wikipedia.org/wiki/Neuromorphic_engineering)
- [Ensemble Learning](https://en.wikipedia.org/wiki/Ensemble_learning)