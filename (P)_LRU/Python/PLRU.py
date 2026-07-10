from functools import reduce

#=======================================================================================
#  PseudoRU
#=======================================================================================
class TreeNode:
    def __init__(self):
        self.bit = 0
        self.left = None
        self.right = None
        self.parent = None
        self.index = None  # Only for leaf nodes, represents cache line index

class PLRUCache:
    def __init__(self, size=4):
        self.size = size
        # self.cache = [None] * size
        self.root = self._build_tree(size)

    def _build_tree(self, size):
        nodes = [TreeNode() for _ in range(size)]
        while len(nodes) > 1:
            parents = []
            for i in range(0, len(nodes), 2):
                parent = TreeNode()
                parent.left = nodes[i]
                parent.right = nodes[i + 1] if i + 1 < len(nodes) else None
                nodes[i].parent = parent
                if parent.right:
                    parent.right.parent = parent
                parents.append(parent)
            nodes = parents
        return nodes[0]

    def _assign_indices(self, node, index=0):
        if node:
            if not node.left and not node.right:  # Leaf node
                node.index = index[0]
                index[0] += 1
            self._assign_indices(node.left, index)
            self._assign_indices(node.right, index)

    def access(self, touch_way):
        self.get_next_state(touch_way)
    
    #=======================================================================================
    # get_next_state
    #======================================================================================= 

    def get_next_state(self, index):
        leaf = self._get_leaf(self.root, index)
        while leaf.parent:
            parent = leaf.parent
            if parent.left == leaf:
                parent.bit = 1
            else:
                parent.bit = 0
            leaf = parent
    #=======================================================================================
    #get_replace_way
    #=======================================================================================
    
    def get_replace_way(self):
        node = self.root
        while node.left or node.right:  # While not a leaf node
            if node.bit == 0 and node.left:
                node = node.left
            else:
                node = node.right
        return node.index

    def _get_leaf(self, node, index):
        if not node:
            return None
        if hasattr(node, 'index') and node.index == index:
            return node
        left_search = self._get_leaf(node.left, index)
        if left_search:
            return left_search
        return self._get_leaf(node.right, index)

    # def __str__(self):
    #     return str(self.cache)
    
    def way(self):
        return self.get_replace_way()
            
