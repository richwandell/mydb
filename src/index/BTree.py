from src.index import BTreeNode


class BTree:

    node_size: int
    root: BTreeNode

    def __init__(self, node_size: int):
        self.node_size = node_size
        self.root = BTreeNode()

    def split_children(self, node):
        left_vals = node.children[0:len(node.children) // 2]
        mid_val = node.children[len(left_vals)]
        right_vals = node.children[len(left_vals) + 1:]

        left_node = BTreeNode(left_vals[0].value)
        left_node.children = left_vals
        left_node.parent = node.parent
        left_node.update_parent()

        mid_node = BTreeNode(mid_val.value)
        mid_node.data = mid_val.data
        mid_node.parent = node.parent
        mid_node.update_parent()

        right_node = BTreeNode(right_vals[0].value)
        right_node.children = right_vals
        right_node.parent = node.parent
        right_node.update_parent()

        left_node.update_keys()
        right_node.update_keys()

        if node.parent is not None:
            parents_children = []
            for n in node.parent.children:
                if n.value != node.value:
                    parents_children.append(n)
            node.parent.children = parents_children
            node.parent.children.append(left_node)
            node.parent.children.append(mid_node)
            node.parent.children.append(right_node)
            node.parent.children.sort(key=lambda x: x.value)
            node.parent.update_keys()
            node.parent.data = []
            return node.parent
        else:
            root_node = BTreeNode()
            root_node.children = [left_node] + [mid_node] + [right_node]
            root_node.update_keys()
            left_node.parent = root_node
            right_node.parent = root_node
            mid_node.parent = root_node
            self.root = root_node
            return root_node

    def add_to_node(self, node, key, data):
        new_node = BTreeNode(key, [data])
        new_node.parent = node
        node.children.append(new_node)
        node.children.sort(key=lambda x: x.value)
        node.update_keys()

    def find_insertion(self, node: BTreeNode, key):
        if len(node.keys) == 0:
            return node
        if len(node.keys) == 1:
            val = node.children[node.keys[0]].value
            if key < val and len(node.children) > 1:
                return self.find_insertion(node.children[node.keys[0] - 1], key)
            elif key > val and len(node.children)-1 > node.keys[0]:
                return self.find_insertion(node.children[node.keys[0] + 1], key)
        for k in node.keys:
            val = node.children[k].value
            if key < val and len(node.children) > 1:
                return self.find_insertion(node.children[k - 1], key)
            elif key == val:
                return node.children[k]
        if len(node.children) > 0:
            if not node.children[-1].is_leaf:
                return node.children[-1]
        return node

    def insert(self, key, data):
        node = self.root
        node = self.find_insertion(node, key)
        if node.value != key:
            self.add_to_node(node, key, data)
        else:
            node.data.append(data)
        while len(node.keys) >= self.node_size:
            node = self.split_children(node)


if __name__ == "__main__":
    import binascii
    b = BTree(node_size=50)

    # for i in range(1, 15):
    #     b.insert(i, i)
    #
    # b.insert(3, "its 3")
    # b.insert(3, "its 3")
    # b.insert(3, "its 3")

    import csv
    with open("../../junk/nestest_log_comma.csv", newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            key = int(binascii.hexlify(row[0].encode("utf8")), 16)
            b.insert(key, row)

    key = int(binascii.hexlify("FAEF".encode("utf8")), 16)
    row = b.find_insertion(b.root, key)

    print(b)