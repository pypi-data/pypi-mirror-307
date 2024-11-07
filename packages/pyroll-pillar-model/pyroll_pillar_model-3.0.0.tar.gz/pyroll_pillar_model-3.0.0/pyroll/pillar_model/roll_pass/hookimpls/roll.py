import numpy as np

from pyroll.core import RollPass


@RollPass.Roll.contact_area
def roll_contact_area(self: RollPass.Roll):
    return self.roll_pass.contact_area / 2


@RollPass.Roll.total_pillar_contact_lengths
def total_pillar_contact_lengths(self: RollPass.Roll):
    rp = self.roll_pass
    for de in rp.disk_elements:
        for i in range(len(de.in_profile.pillars)):
            if not de.pillars_in_contact[i]:
                continue
            de_pillar_contact_lengths = [de.length for de in self.roll_pass.disk_elements]
            return np.sum(de_pillar_contact_lengths, axis=0)
