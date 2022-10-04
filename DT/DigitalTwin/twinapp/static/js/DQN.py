environment_matrix = [[None, 0],
                  [-100, 0],
                  [0, 0],
                  [0, 0],
                  [0, 0],
                  [0, 100],
                  [0, 0],
                  [100, 0],
                  [0, 0],
                  [0, None]]

q_matrix = [[0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0]]

win_loss_states = [0,6]def getAllPossibleNextAction(cur_pos):
    step_matrix = [x != None for x in environment_matrix[cur_pos]]
    action = []
    if(step_matrix[0]):
        action.append(0)
    if(step_matrix[1]):
        action.append(1)
    return(action)def isGoalStateReached(cur_pos):
    return (cur_pos in [6])def getNextState(cur_pos, action):
    if (action == 0):
        return cur_pos - 1
    else:
        return cur_pos + 1def isGameOver(cur_pos):
    return cur_pos in win_loss_states


discount = 0.9
learning_rate = 0.1for _ in range(1000):
    # get starting place
    cur_pos = random.choice([0,1,2,3,4,5,6,7,8,9])
    # while goal state is not reached
    while(not isGameOver(cur_pos)):
        # get all possible next states from cur_step
        possible_actions = getAllPossibleNextAction(cur_pos)
        # select any one action randomly
        action = random.choice(possible_actions)
        # find the next state corresponding to the action selected
        next_state = getNextState(cur_pos, action)
        # update the q_matrix
        q_matrix[cur_pos][action] = q_matrix[cur_pos][action] + learning_rate * (environment_matrix[cur_pos][action] +
            discount * max(q_matrix[next_state]) - q_matrix[cur_pos][action])
        # go to next state
        cur_pos = next_state
    # print status
    print("Episode ", _ , " done")print(q_matrix)
print("Training done...")


[[0, 0], [-99.99999999730835, 65.60999997057485], [59.04899994359059, 72.8999999993016], [65.60999999858613, 80.99999999978154],
[72.89999999929572, 89.99999999991468], [80.99999999863587, 99.99999999997391], [0, 0], [99.9999999999985, 80.99999999994624],
[89.99999999999515, 72.89999999997386], [80.99999999999046, 0]]