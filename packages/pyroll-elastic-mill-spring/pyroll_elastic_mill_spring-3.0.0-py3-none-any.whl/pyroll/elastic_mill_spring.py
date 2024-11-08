from pyroll.core import SymmetricRollPass, Hook, root_hooks

VERSION = "3.0.0"

SymmetricRollPass.stand_stiffness = Hook[float]()
"""Stiffness of the roll stand of the current roll pass."""

SymmetricRollPass.elastic_gap_offset = Hook[float]()
"""Elastic roll gap offset of the roll stand of the current roll pass."""

@SymmetricRollPass.stand_stiffness
def default_stand_stiffness(self: SymmetricRollPass):
    return 1

@SymmetricRollPass.elastic_gap_offset
def default_elastic_gap_offset(self: SymmetricRollPass, cycle):
    if cycle:
        return None

    return self.roll_force / self.stand_stiffness


@SymmetricRollPass.gap
def widened_gap(self: SymmetricRollPass, cycle):
    if cycle:
        return None

    if not hasattr(self, "nominal_gap"):
        self.nominal_gap = self.gap

    elastic_gap = self.nominal_gap + self.elastic_gap_offset
    return elastic_gap


root_hooks.add(SymmetricRollPass.gap)
root_hooks.add(SymmetricRollPass.elastic_gap_offset)