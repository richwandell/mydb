from __future__ import annotations
from typing import List, Any


class BTreeNode:

    children: List[BTreeNode]
    value: int
    parent: BTreeNode | None
    data: List[Any]
    keys: List[int]

    def __init__(self, value=None, data=[]):
        self.value = value
        self.children = []
        self.parent = None
        self.keys = []
        self.data = data

    def update_keys(self):
        self.keys = []
        for i, n in enumerate(self.children):
            if n.is_leaf:
                self.keys.append(i)

    def update_parent(self):
        for n in self.children:
            n.parent = self

    @property
    def is_leaf(self):
        return len(self.keys) == 0

    # def __str__(self):
    #     return "Node: " + str(self.value) + " " + str(list(str(c) for c in self.children))