class Node:
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf
        
class BTree:
    def __init__(self, t):
        self.t = t
        self.root = Node(t, leaf=True)
    
    def search(self, key, node=None):
        """return (node, index) if key is found, else None."""
        
        if node is None:
            node = self.root
            
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
            
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        
        if node.leaf:
            return None
        
        return self.search(key, node.children[i])
    
    def insert (self, key):
        root = self.root
        
        #if root is full ,split it and grow the tree
        if len(root.keys) == 2*self.t - 1:
            new_root = Node(self.t, leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            
        self._insert_non_full(self.root, key)
        
    
    def _insert_non_full(self, node : Node, key):
        i = len(node.keys) - 1
        if node.leaf:
            #insert key in sorted position
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i+1] = key
            
        else :
            #find the correct child to recurse into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node , i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)
            
    def _split_child(self, parent, i):
        """Split the i-th child of parent"""
        t = self.t
        full_child = parent.children[i]
        new_child = Node(t, leaf=full_child.leaf)
        
        #median key moves up to the parent
        mid = t - 1
        parent.keys.insert(i , full_child.keys[mid])
        parent.children.insert(i+1, new_child)
        
        #right half of keys go to new child
        new_child.keys = full_child.keys[mid + 1:]
        full_child.keys = full_child.keys[:mid]
        
        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
            
            
    def delete(self, key, node:None):
        if node is None:
            node = self.root
        
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
            
        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i)
            elif len(node.children[i].keys) >= t:
                node.keys[i] = self._get_predecessor(node, i)   # Case 2a
                self.delete(node.keys[i], node.children[i])
            elif len(node.children[i + 1].keys) >= t:
                node.keys[i] = self._get_successor(node, i)     # Case 2b
                self.delete(node.keys[i], node.children[i + 1])
            else:
                self._merge(node, i)                             # Case 2c
                self.delete(key, node.children[i])
                
        else:
            if node.leaf:
                print(f"Key {key} not found.")
                return

            # Key is not in this node — go to appropriate child
            if len(node.children[i].keys) < t:
                self._fill(node, i)
                # Recompute i after possible restructuring
                i = 0
                while i < len(node.keys) and key > node.keys[i]:
                    i += 1

            self.delete(key, node.children[i])
        # Shrink root if it becomes empty
        if node is self.root and len(node.keys) == 0 and node.children:
            self.root = node.children[0]
    
    def _get_predecessor(self, node, i):
        """Largest key in the left subtree of node.keys[i]."""
        cur = node.children[i]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def _get_successor(self, node, i):
        """Smallest key in the right subtree of node.keys[i]."""
        cur = node.children[i + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]
    
    def _merge(self, parent, i):
        """Merge children[i] and children[i+1] through parent.keys[i]."""
        left = parent.children[i]
        right = parent.children[i + 1]

        left.keys.append(parent.keys.pop(i))
        left.keys.extend(right.keys)
        left.children.extend(right.children)
        parent.children.pop(i + 1)
        
    def _fill(self, parent, i):
        """Ensure children[i] has at least t keys before descending."""
        t = self.t
        if i > 0 and len(parent.children[i - 1].keys) >= t:
            self._borrow_from_prev(parent, i)
        elif i < len(parent.children) - 1 and len(parent.children[i + 1].keys) >= t:
            self._borrow_from_next(parent, i)
        else:
            if i < len(parent.children) - 1:
                self._merge(parent, i)
            else:
                self._merge(parent, i - 1)
    
    def _borrow_from_prev(self, parent, i):
        child = parent.children[i]
        sibling = parent.children[i - 1]
        child.keys.insert(0, parent.keys[i - 1])
        parent.keys[i - 1] = sibling.keys.pop()
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, parent, i):
        child = parent.children[i]
        sibling = parent.children[i + 1]
        child.keys.append(parent.keys[i])
        parent.keys[i] = sibling.keys.pop(0)
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))
            
    def traverse(self, node=None):
        """In-order traversal — returns sorted list of all keys."""
        if node is None:
            node = self.root
        result = []
        for i, key in enumerate(node.keys):
            if not node.leaf:
                result.extend(self.traverse(node.children[i]))
            result.append(key)
        if not node.leaf:
            result.extend(self.traverse(node.children[-1]))
        return result
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        print(" " * (level * 4) + prefix + str(node.keys))
        if not node.leaf:
            for i, child in enumerate(node.children):
                self.print_tree(child, level + 1, prefix=f"Child[{i}]: ")
            


bt = BTree(t=3)  # min degree 3 → each node holds 2–5 keys

for key in [10, 20, 5, 6, 12, 30, 7, 17, 3, 1, 8, 25]:
    bt.insert(key)

print("Tree structure:")
bt.print_tree()

print("\nIn-order traversal:", bt.traverse())

print("\nSearch 12:", bt.search(12))
print("Search 99:", bt.search(99))
   
bt.delete(6)
bt.delete(20)
print("\nAfter deleting 6 and 20:", bt.traverse())
    
        
         
    
        