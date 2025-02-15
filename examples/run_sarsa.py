''' An example of solve New Hold'em with SARSA
'''
import os
import argparse

import rlcard
from rlcard.agents import (
    QLAgent, SARSAAgent,
    RandomAgent, ThresholdAgent, ThresholdAgent2
)
from rlcard.utils import (
    set_seed,
    tournament,
    Logger,
    plot_curve,
)


def train(args):
    # Make environments
    env = rlcard.make(
        'new-limit-holdem',
        config={
            'seed': 0,
            'allow_step_back': True,
        }
    )
    eval_env = rlcard.make(
        'new-limit-holdem',
        config={
            'seed': 0,
        }
    )

    # Seed numpy, torch, random
    set_seed(args.seed)

    # Initilize training Agent
    agent = SARSAAgent(
        env,
        os.path.join(
            args.log_dir,
            'sarsa_model',

        ),
    )
    agent.load()  # If we have saved model, we first load the model

    # Evaluate SARSA
    eval_env.set_agents([
        agent,
        RandomAgent(num_actions=env.num_actions),
    ])

    env.set_agents([
        agent,
        RandomAgent(num_actions=env.num_actions),
    ])

    # sarsa vs ql
    # agent2 = QLAgent(
    #     env,
    #     os.path.join(
    #         args.log_dir,
    #         'ql_model',
    #
    #     ),
    # )
    # agent2.load
    #
    # eval_env.set_agents([
    #     agent,
    #     agent2,
    # ])
    #
    # env.set_agents([
    #     agent,
    #     agent2,
    # ])

    # Start training
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):
            print('\rIteration {}'.format(episode), end='')
            # Evaluate the performance. Play with Random agents.
            if episode % args.evaluate_every == 0:
                agent.save()  # Save model
                logger.log_performance(
                    episode,
                    tournament(
                        eval_env,
                        args.num_eval_games
                    )[0]
                )
                # print(agent.epsilon)
            agent.train()


        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path
    # Plot the learning curve
    plot_curve(csv_path, fig_path, 'SARSA')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("SARSA Agent example in RLCard")
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=2000,
    )
    parser.add_argument(
        '--num_eval_games',
        type=int,
        default=2000,
    )
    parser.add_argument(
        '--evaluate_every',
        type=int,
        default=100,
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='experiments/new_limit_holdem_sarsa_result/',
    )

    args = parser.parse_args()

    train(args)