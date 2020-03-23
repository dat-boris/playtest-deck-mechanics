from typing import List, Dict

from playtest.components import Component


class ScoringRiver(Component):
    river: List[Dict]

    def to_data(self):
        pass

    def reset(self):
        pass

    def __len__(self):
        return len(self.river)

    def __getitem__(self, i: int):
        assert isinstance(i, int), "Deck only takes integer subscription"
        return self.river[i]


class TraderRiver(Component):
    river: List[Dict]

    def to_data(self):
        pass

    def reset(self):
        pass

    def __len__(self):
        return len(self.river)

    def __getitem__(self, i: int):
        assert isinstance(i, int), "Deck only takes integer subscription"
        return self.river[i]
