""" Configuration for the pqthreads """

from dataclasses import dataclass


@dataclass
class Parameters:
    """ Configuration parameters for pqthreads """
    signal_slot_timeout: int = 1_000


params = Parameters()
