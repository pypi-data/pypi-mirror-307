if __name__=="__main__":
    import gym
    from l3c.anymdp import AnyMDPEnv, AnyMDPSolverOpt, AnyMDPSolverQ, AnyMDPSolverMBRL, AnyMDPTaskSampler, Resampler

    env = gym.make("anymdp-v0", max_steps=32000)
    task = AnyMDPTaskSampler(128, 5)
    prt_freq = 1000
    env.set_task(Resampler(task))
    print(task)

    # Test Random Policy
    state, info = env.reset()
    acc_reward = 0
    epoch_reward = 0
    done = False

    while not done:
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        acc_reward += reward
        epoch_reward += reward
        if(info["steps"] % prt_freq == 0 and info["steps"] > 0):
            print("Step:{}\tEpoch Reward: {}".format(info["steps"], epoch_reward))
            epoch_reward = 0
    print("Random Policy Summary: {}".format(acc_reward))

    # Test AnyMDPSolverOpt
    solver = AnyMDPSolverOpt(env)
    state, info = env.reset()
    done = False
    acc_reward = 0
    epoch_reward = 0

    while not done:
        action = solver.policy(state)
        state, reward, done, info = env.step(action)
        acc_reward += reward
        epoch_reward += reward
        if(info["steps"] % prt_freq == 0 and info["steps"] > 0):
            print("Step:{}\tEpoch Reward: {}".format(info["steps"], epoch_reward))
            epoch_reward = 0
    print("Optimal Solver Summary:  {}".format(acc_reward))

    # Test AnyMDPSolverQ
    solver = AnyMDPSolverQ(env)
    state, info = env.reset()
    done = False
    acc_reward = 0
    epoch_reward = 0

    while not done:
        action = solver.policy(state)
        next_state, reward, done, info = env.step(action)
        solver.learner(state, action, next_state, reward, done)
        acc_reward += reward
        epoch_reward += reward
        state = next_state
        if(info["steps"] % prt_freq == 0 and info["steps"] > 0):
            print("Step:{}\tEpoch Reward: {}".format(info["steps"], epoch_reward))
            epoch_reward = 0
    print("Q Solver Summary: {}".format(acc_reward))

    # Test AnyMDPSolverMBRL
    solver = AnyMDPSolverMBRL(env)
    state, info = env.reset()
    done = False
    acc_reward = 0
    epoch_reward = 0

    while not done:
        action = solver.policy(state)
        next_state, reward, done, info = env.step(action)
        solver.learner(state, action, next_state, reward, done)
        acc_reward += reward
        epoch_reward += reward
        state = next_state
        if(info["steps"] % prt_freq == 0 and info["steps"] > 0):
            print("Step:{}\tEpoch Reward: {}".format(info["steps"], epoch_reward))
            epoch_reward = 0
    print("MBRL Solver Summary: {}".format(acc_reward))

    print("Test Passed")