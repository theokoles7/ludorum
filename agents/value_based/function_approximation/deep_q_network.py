"""Implementation of Deep Q Network as proposed in the 2013 paper "Playing Atari with Deep 
Reinforcement Learning", by Mnih et al."""

__all__ = ["DeepQNetwork"]

from typing                                     import override

from agents.value_based.tabular_based.__base__  import TabularBasedAgent

class DeepQNetwork():
    """Deep Q Network class based on the 2013 paper, by Mnih et al.
    
    Link to paper: https://people.engr.tamu.edu/guni/csce642/files/dqn.pdf
    """

    def __init__(self):

        raise NotImplementedError(f"Deep Q Network has not been implemented.")