### Useful resources

1. Decription of terms: https://www.nrel.gov/docs/fy19osti/74426.pdf



## Simulation Process

The each time step in the simulation has two parts that happen sequentially in the following order:

1. The current state of the world is updated by running the increment / update methods for each object. This takes the existing state of those objects and computes their new values. For example, a battery's state is set to `DISCHARGING` with a given discharge rate in the previous step. In this step, the first thing to occur is computing the amount of power the battery will have discharged in the previous step. In other words, catch up the battery state based on decisions taken in the previous step
2. The new state of the world is read and decisions are taken on what to do next. These decision result in object states and parameters being updated.

This is repeated for each simulation step.

The simulation can therefore be understood to initially lookback and update itself
 - Is this the right way to do it? Should the last thing to happen in each step be the computation of new values? Does it matter?
- Only matters in the first and last steps. First step won't have any instructions and updates to run (not a terrible thing). The last step will miss updating the final state the simulation objects

## Sites

A site is a collection of batteries located in the same place.

Sites can implement a variety of charging strategies, which dictate which battery should be charged/discharged once a charging/discharging request is made.

## Batteries

A battery is the smallest unit used in the simulation. It can be thought of as a combination of state and current charge (kWh), with constraints applied to the amount that can be discharged in a given time unit and the amount of total energy that can be stored.