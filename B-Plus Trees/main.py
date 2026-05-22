class Node:
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None  # leaf-level linked list pointer

class BPlusTree:
    def __init__(self, t):
        self.t = t
        self.root = Node(t, leaf=True)

    # ─────────────────────────────────────────
    # Search
    # ─────────────────────────────────────────

    def search(self, key, node=None):
        """Return (node, index) if key found in a leaf, else None."""
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                return (node, i)
            return None

        # Internal node: all keys are routers, always descend
        return self.search(key, node.children[i])

    # ─────────────────────────────────────────
    # Insert
    # ─────────────────────────────────────────

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = Node(self.t, leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, i):
        t = self.t
        full = parent.children[i]
        new_node = Node(t, leaf=full.leaf)
        mid = t - 1

        if full.leaf:
            # B+ tree: copy the middle key up (it stays in the leaf too)
            new_node.keys = full.keys[mid:]
            full.keys = full.keys[:mid]
            # maintain linked list
            new_node.next = full.next
            full.next = new_node
            parent.keys.insert(i, new_node.keys[0])
        else:
            # Internal node: same as B-tree — middle key moves up, not copied
            parent.keys.insert(i, full.keys[mid])
            new_node.keys = full.keys[mid + 1:]
            full.keys = full.keys[:mid]
            new_node.children = full.children[t:]
            full.children = full.children[:t]

        parent.children.insert(i + 1, new_node)

    # ─────────────────────────────────────────
    # Delete
    # ─────────────────────────────────────────

    def delete(self, key, node=None):
        if node is None:
            node = self.root

        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                node.keys.pop(i)
            else:
                print(f"Key {key} not found.")
            return

        # Descend into the right child
        # i is the child index to descend into
        child_i = i
        # If key equals a router key, we still descend right to find it in a leaf
        self._ensure_min(node, child_i)

        # Recompute i after possible restructuring
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        child_i = i

        self.delete(key, node.children[child_i])

        # After deletion, update router keys if needed
        # (router keys in internal nodes are just guides — update if stale)
        if child_i < len(node.children) and node.children[child_i].leaf:
            if node.children[child_i].keys:
                if child_i < len(node.keys):
                    node.keys[child_i] = node.children[child_i].keys[0]

        # Shrink root
        if node is self.root and len(node.keys) == 0 and node.children:
            self.root = node.children[0]

    def _ensure_min(self, parent, i):
        """Ensure children[i] has at least t keys before descending."""
        t = self.t
        child = parent.children[i]
        if len(child.keys) >= t:
            return
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
        if child.leaf:
            child.keys.insert(0, sibling.keys.pop())
            parent.keys[i - 1] = child.keys[0]
        else:
            child.keys.insert(0, parent.keys[i - 1])
            parent.keys[i - 1] = sibling.keys.pop()
            if sibling.children:
                child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, parent, i):
        child = parent.children[i]
        sibling = parent.children[i + 1]
        if child.leaf:
            child.keys.append(sibling.keys.pop(0))
            parent.keys[i] = sibling.keys[0]
        else:
            child.keys.append(parent.keys[i])
            parent.keys[i] = sibling.keys.pop(0)
            if sibling.children:
                child.children.append(sibling.children.pop(0))

    def _merge(self, parent, i):
        left = parent.children[i]
        right = parent.children[i + 1]
        if left.leaf:
            left.keys.extend(right.keys)
            left.next = right.next
        else:
            left.keys.append(parent.keys[i])
            left.keys.extend(right.keys)
            left.children.extend(right.children)
        parent.keys.pop(i)
        parent.children.pop(i + 1)

    # ─────────────────────────────────────────
    # Traversal
    # ─────────────────────────────────────────

    def traverse(self):
        """Tree traversal: walk down to the leftmost leaf,
        then follow the linked list across all leaves."""
        result = []
        node = self.root
        while not node.leaf:
            node = node.children[0]
        while node:
            result.extend(node.keys)
            node = node.next
        return result

    def traverse_tree(self, node=None):
        """In-order tree traversal (visits internal router keys too)."""
        if node is None:
            node = self.root
        result = []
        for i, key in enumerate(node.keys):
            if not node.leaf:
                result.extend(self.traverse_tree(node.children[i]))
            result.append(key)
        if not node.leaf:
            result.extend(self.traverse_tree(node.children[-1]))
        return result

    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        tag = " [leaf]" if node.leaf else ""
        print(" " * (level * 4) + prefix + str(node.keys) + tag)
        if not node.leaf:
            for i, child in enumerate(node.children):
                self.print_tree(child, level + 1, prefix=f"Child[{i}]: ")


# ─────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────

bt = BPlusTree(t=3)

# ── insert ────────────────────────────────────
bt.insert(10)
print("insert(10):                  ", bt.traverse())

bt.insert(20)
print("insert(20):                  ", bt.traverse())

bt.insert(5)
print("insert(5):                   ", bt.traverse())

bt.insert(6)
print("insert(6):                   ", bt.traverse())

bt.insert(12)
print("insert(12):                  ", bt.traverse())

bt.insert(30)
print("insert(30):                  ", bt.traverse())

bt.insert(7)
print("insert(7):                   ", bt.traverse())

bt.insert(17)
print("insert(17):                  ", bt.traverse())

bt.insert(3)
print("insert(3):                   ", bt.traverse())

bt.insert(1)
print("insert(1):                   ", bt.traverse())

bt.insert(8)
print("insert(8):                   ", bt.traverse())

bt.insert(25)
print("insert(25):                  ", bt.traverse())


# ── search ────────────────────────────────────
print("\nsearch(1):                   ", bt.search(1))    # found (leftmost leaf)
print("search(12):                  ", bt.search(12))    # found (middle leaf)
print("search(30):                  ", bt.search(30))    # found (rightmost leaf)
print("search(99):                  ", bt.search(99))    # None
print("search(0):                   ", bt.search(0))     # None


# ── delete leaf key ───────────────────────────
bt.delete(1)
print("\ndelete(1)  [leaf]:           ", bt.traverse())

bt.delete(3)
print("delete(3)  [leaf]:           ", bt.traverse())


# ── delete key that updates router ───────────
bt.delete(5)
print("\ndelete(5)  [router update]:  ", bt.traverse())

bt.delete(10)
print("delete(10) [router update]:  ", bt.traverse())


# ── delete key that triggers borrow/merge ────
bt.delete(6)
print("\ndelete(6)  [rebalance]:      ", bt.traverse())

bt.delete(25)
print("delete(25) [rebalance]:      ", bt.traverse())


# ── delete non-existent key ───────────────────
print("\ndelete(99) [missing]:        ", end="")
bt.delete(99)


# ── linked-list traversal (B+ tree specific) ─
print("\nleaf linked-list traversal:  ", bt.traverse())


# ── tree-level traversal ──────────────────────
print("in-order tree traversal:     ", bt.traverse_tree())


# ── print structure ───────────────────────────
print("\nTree structure:")
bt.print_tree()