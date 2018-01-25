# grid_world_simulator
A grid world simulator, very useful to test my ideas about reinforcement learning and agent learning. Super light and super fast!

Following the complexity of 'CollectBall' experiment (simulator is available on github), and my increasing lack of computational power and time (imagine the frustration), I will build a more abstract/lighter simulator. The map is just a text file. Basic rules:
  - 4 directions: Up, Down, Left and Right
  - Sensory data: The robot can see the area around it (the 8 places surrounding him).

The target, again, is to provide a cheap environment to test my goal decomposition methods. The bottom line is: I really don't want to spend too much time on the details of the simulator. This approach proved to be successful during my masters internship (see my simulator on github). Some of the codes will be adapted directly from it.

The structure for this project will be:
- ./maps
  - Will contain all the maps
- map_generator.py (not done yet)
  - Will generate a random map for a particular task. It takes 3 parameters:
    - What is the task?
    - Nb of goals in this map
    - Size of the map
- map_parser.py
  - Will read the map, extract basic info:
    - The places of the wall.
    - The places of the goals.
- game_logic.py
  - This will have the controlling game logic
- game_state.py
- agents.py
- main.py
