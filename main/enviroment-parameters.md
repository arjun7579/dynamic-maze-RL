### About Enviroment Parameters
---
1. Alpha (Learning Rate): α
  - Definition: Alpha determines to what extent newly acquired information overrides the old information.
  - Range: Between 0 and 1.
  - Effect: A higher value makes the agent learn faster from new experiences, while a lower value makes it rely more on existing knowledge.
---
2. Gamma (Discount Factor): γ
  - Definition: Gamma determines the importance of future rewards in the agent's learning process.
  - Range: Between 0 and 1.
  - Effect: A higher value makes the agent prioritize long-term rewards, whereas a lower value focuses more on immediate rewards.
---
3. Epsilon (Epsilon-greedy): ε
  - Definition: Epsilon controls the exploration-exploitation trade-off in the agent's decision-making.
  - Range: Between 0 and 1.
  - Effect: A higher value increases exploration (random actions), allowing the agent to discover new strategies. A lower value increases exploitation (choosing actions based on current knowledge), focusing on known good strategies.
---
4. Episodes:
  - Definition: Episodes refer to the number of times the agent interacts with the environment during training.
  - Purpose: Determines how much experience the agent gathers over its training period. More episodes generally lead to better learning and performance.
  - Range: Take values atleast more than or equal to 100.
---
5. Entropy (Dynamic Obstacles): 
  - Definition: Entropy influences the randomness in the behavior of dynamic obstacles in the environment.
  - Range: Between 0 and 1.
  - Effect: A higher value increases the randomness of dynamic obstacle movements, making the environment more unpredictable and challenging. This can lead to more varied learning experiences for the agent.
---
