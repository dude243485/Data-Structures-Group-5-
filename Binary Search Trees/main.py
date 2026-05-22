class Node():
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


class Tree():
    def __init__(self):
        self.root = None

    def _insert(self, value, node: Node):
        if value <= node.data:
            if node.left: self._insert(value, node.left)
            else: node.left = Node(value)
        else:
            if node.right: self._insert(value, node.right)
            else: node.right = Node(value)

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def search(self, value, node: Node):
        if not node: return
        if value == node.data:
            return "Found the target"
        if value < node.data:
            return self.search(value, node.left)
        return self.search(value, node.right)

    # --- Delete ---

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node: Node | None, value) -> Node | None:
        if node is None:        # value not in tree — nothing to do
            return None

        if value < node.data:
            node.left = self._delete(node.left, value)
        elif value > node.data:
            node.right = self._delete(node.right, value)
        else:
            # Found the node to delete — three cases:

            # Case 1: leaf node
            if node.left is None and node.right is None:
                return None

            # Case 2: one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: two children
            # Replace with inorder successor (smallest value in right subtree),
            # then delete that successor from the right subtree.
            successor = self._min_node(node.right)
            node.data = successor.data
            node.right = self._delete(node.right, successor.data)

        return node

    def _min_node(self, node: Node) -> Node:
        current = node
        while current.left:
            current = current.left
        return current

    # --- Traversals ---

    def inOrder(self, node: Node):
        if not node: return
        self.inOrder(node.left)
        print(node.data, end=", ")
        self.inOrder(node.right)

    def preOrder(self, node: Node):
        if not node: return
        print(node.data, end=", ")
        self.preOrder(node.left)
        self.preOrder(node.right)

    def postOrder(self, node: Node):
        if not node: return
        self.postOrder(node.left)
        self.postOrder(node.right)
        print(node.data, end=", ")

    def print(self, flag: str):
        if flag == "in":
            print("Inorder:", end=" ")
            self.inOrder(self.root); print("")
        elif flag == "pre":
            print("Preorder:", end=" ")
            self.preOrder(self.root); print("")
        elif flag == "post":
            print("Postorder:", end=" ")
            self.postOrder(self.root); print("")
        else:
            print("Invalid flag")

    # Helper for tests: collect inorder into a list
    def _inorder_list(self, node, result):
        if not node: return
        self._inorder_list(node.left, result)
        result.append(node.data)
        self._inorder_list(node.right, result)

    def to_list(self):
        result = []
        self._inorder_list(self.root, result)
        return result


# ─────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────
def build_tree():
    """Fresh tree used by most tests: [10, 20, 5, 6, 12, 30, 7, 17]"""
    t = Tree()
    for v in [10, 20, 5, 6, 12, 30, 7, 17]:
        t.insert(v)
    return t


def run_tests():
    passed = 0
    failed = 0

    def check(label, condition):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {label}")
            passed += 1
        else:
            print(f"  [FAIL] {label}")
            failed += 1

    # ── Insert & Search ──────────────────────
    print("\n=== Insert & Search ===")
    t = build_tree()
    check("search finds 7",              t.search(7,  t.root) == "Found the target")
    check("search finds 10 (root)",      t.search(10, t.root) == "Found the target")
    check("search finds 30 (rightmost)", t.search(30, t.root) == "Found the target")
    check("search misses 99",            t.search(99, t.root) is None)
    check("search misses 0",             t.search(0,  t.root) is None)

    # ── Delete leaf node ─────────────────────
    print("\n=== Delete Leaf Node ===")
    t = build_tree()
    t.delete(7)                              # 7 is a leaf
    check("leaf 7 no longer found",      t.search(7, t.root) is None)
    check("other keys still present",    t.search(6, t.root) == "Found the target")
    check("inorder still sorted",        t.to_list() == sorted(t.to_list()))
    check("inorder excludes 7",          7 not in t.to_list())

    # ── Delete node with one child ───────────
    print("\n=== Delete Node With One Child ===")
    t = build_tree()
    # 6 has one right child (7)
    t.delete(6)
    check("node 6 no longer found",      t.search(6, t.root) is None)
    check("child 7 still present",       t.search(7, t.root) == "Found the target")
    check("inorder still sorted",        t.to_list() == sorted(t.to_list()))
    check("inorder excludes 6",          6 not in t.to_list())

    # ── Delete node with two children ────────
    print("\n=== Delete Node With Two Children ===")
    t = build_tree()
    # 20 has two children: 12 (left) and 30 (right)
    t.delete(20)
    check("node 20 no longer found",     t.search(20, t.root) is None)
    check("child 12 still present",      t.search(12, t.root) == "Found the target")
    check("child 30 still present",      t.search(30, t.root) == "Found the target")
    check("inorder still sorted",        t.to_list() == sorted(t.to_list()))
    check("inorder excludes 20",         20 not in t.to_list())

    # ── Delete root ──────────────────────────
    print("\n=== Delete Root ===")
    t = build_tree()
    original_list = t.to_list()
    t.delete(10)
    check("root 10 no longer found",     t.search(10, t.root) is None)
    check("root is now a different node", t.root is not None and t.root.data != 10)
    check("all other keys present",      t.to_list() == [v for v in original_list if v != 10])
    check("inorder still sorted",        t.to_list() == sorted(t.to_list()))

    # ── Delete non-existent key ──────────────
    print("\n=== Delete Non-Existent Key ===")
    t = build_tree()
    before = t.to_list()
    t.delete(999)
    check("tree unchanged after deleting missing key", t.to_list() == before)

    # ── Delete all nodes one by one ──────────
    print("\n=== Delete All Nodes ===")
    t = build_tree()
    for v in [10, 20, 5, 6, 12, 30, 7, 17]:
        t.delete(v)
    check("tree is empty after deleting all nodes", t.root is None)
    check("to_list returns [] on empty tree",        t.to_list() == [])
    check("search on empty tree returns None",       t.search(10, t.root) is None)

    # ── Single-node tree ─────────────────────
    print("\n=== Single-Node Tree ===")
    t = Tree()
    t.insert(42)
    t.delete(42)
    check("root is None after deleting only node", t.root is None)
    check("search returns None on now-empty tree", t.search(42, t.root) is None)

    # ── Duplicates ───────────────────────────
    print("\n=== Duplicate Values ===")
    t = Tree()
    for v in [5, 5, 5]:
        t.insert(v)
    t.delete(5)
    check("one 5 removed, others still present", len(t.to_list()) == 2)
    check("remaining values are still 5s",       all(v == 5 for v in t.to_list()))

    # ── BST property preserved after deletes ─
    print("\n=== BST Property After Multiple Deletes ===")
    t = build_tree()
    for v in [5, 20, 7]:
        t.delete(v)
    lst = t.to_list()
    check("inorder is sorted after 3 deletes",   lst == sorted(lst))
    check("deleted keys are gone",               not any(v in lst for v in [5, 20, 7]))
    check("remaining keys still found",          all(
        t.search(v, t.root) == "Found the target" for v in [6, 10, 12, 17, 30]
    ))

    # ── Summary ──────────────────────────────
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print('='*40)


if __name__ == "__main__":
    print("=== Original Demo ===")
    mt = build_tree()
    print("search(7):", mt.search(7, mt.root))
    mt.print("in")
    mt.print("pre")
    mt.print("post")

    run_tests()