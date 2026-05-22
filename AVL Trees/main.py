class Node:
    def __init__(self, key):
        self.key = key
        self.left : "Node | None" = None
        self.right : "Node | None" = None
        self.height : int = 1
        
    def __repr__(self):
        return f"Node({self.key}, h = {self.height})"
    

class AVLTree:
    def __init__(self):
        self.root : Node | None = None
        
    def _height(self, node : Node | None):
        if node:
            return node.height
        else:
            return 0
        
    def _balance_factor(self, node : Node | None):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _update_height(self, node : Node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        
    def _rotate_right(self, y : Node):
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _rotate_left(self, x : Node):
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self._update_height(x)
        self._update_height(y)
        return y
    
    def _rebalance(self, node : Node):
        self._update_height(node)
        bf = self._balance_factor(node)
        
        if bf > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        if bf > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if bf < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        if bf < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def insert(self, key):
        self.root = self._insert(self.root, key)
        
    def _insert(self, node : Node | None, key):
        if node is None:
            return Node(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        return self._rebalance(node)
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node : Node, key):
        if node is None: return None
        if key == node.key: return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # --- Traversals ---

    def inorder(self) -> list:
        """Left → Root → Right. Produces sorted output for a BST."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Node | None, result: list):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def preorder(self) -> list:
        """Root → Left → Right."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Node | None, result: list):
        if node is None:
            return
        result.append(node.key)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def postorder(self) -> list:
        """Left → Right → Root."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Node | None, result: list):
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.key)

    def level_order(self) -> list:
        """Breadth-first, level by level."""
        if self.root is None:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result


# ─────────────────────────────────────────────
# Helper to check AVL balance property on the whole tree
# ─────────────────────────────────────────────
def is_balanced(tree: AVLTree) -> bool:
    def check(node):
        if node is None:
            return True
        bf = tree._balance_factor(node)
        if abs(bf) > 1:
            return False
        return check(node.left) and check(node.right)
    return check(tree.root)


# ─────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────
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
    t = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        t.insert(v)

    check("search existing key 30", t.search(30) is not None)
    check("search existing key 10", t.search(10) is not None)
    check("search existing key 50", t.search(50) is not None)
    check("search missing key 99 returns None", t.search(99) is None)
    check("search missing key 0 returns None",  t.search(0)  is None)

    # ── Duplicate insert (no duplicates in BST) ──
    print("\n=== Duplicate Insert ===")
    t2 = AVLTree()
    t2.insert(5)
    t2.insert(5)
    check("inorder after duplicate insert has no duplicate", t2.inorder() == [5])

    # ── Balance property ────────────────────
    print("\n=== Balance Property ===")
    check("tree is balanced after [10,20,30,40,50,25]", is_balanced(t))

    t3 = AVLTree()
    for v in range(1, 16):           # 15-node sequential insert; triggers many rotations
        t3.insert(v)
    check("tree is balanced after sequential insert 1-15", is_balanced(t3))

    # ── Inorder (must be sorted) ─────────────
    print("\n=== Inorder Traversal ===")
    result = t.inorder()
    check("inorder of [10,20,30,40,50,25] is sorted",    result == sorted(result))
    check("inorder contains all 6 keys",                  sorted(result) == [10, 20, 25, 30, 40, 50])

    result3 = t3.inorder()
    check("inorder of 1-15 is [1..15]", result3 == list(range(1, 16)))

    # ── Preorder ────────────────────────────
    print("\n=== Preorder Traversal ===")
    pre = t.preorder()
    check("preorder contains all 6 keys", sorted(pre) == [10, 20, 25, 30, 40, 50])
    check("preorder root is first element", pre[0] == t.root.key)

    # ── Postorder ───────────────────────────
    print("\n=== Postorder Traversal ===")
    post = t.postorder()
    check("postorder contains all 6 keys", sorted(post) == [10, 20, 25, 30, 40, 50])
    check("postorder root is last element", post[-1] == t.root.key)

    # ── Level-order ──────────────────────────
    print("\n=== Level-Order Traversal ===")
    lvl = t.level_order()
    check("level-order contains all 6 keys", sorted(lvl) == [10, 20, 25, 30, 40, 50])
    check("level-order root is first element", lvl[0] == t.root.key)

    # ── Empty tree edge cases ────────────────
    print("\n=== Empty Tree ===")
    empty = AVLTree()
    check("search on empty tree returns None",     empty.search(1) is None)
    check("inorder on empty tree returns []",      empty.inorder()     == [])
    check("preorder on empty tree returns []",     empty.preorder()    == [])
    check("postorder on empty tree returns []",    empty.postorder()   == [])
    check("level-order on empty tree returns []",  empty.level_order() == [])

    # ── Single-node tree ─────────────────────
    print("\n=== Single-Node Tree ===")
    single = AVLTree()
    single.insert(42)
    check("search finds the only node",           single.search(42) is not None)
    check("search misses non-existent key",       single.search(1)  is None)
    check("inorder of single node is [42]",       single.inorder()     == [42])
    check("preorder of single node is [42]",      single.preorder()    == [42])
    check("postorder of single node is [42]",     single.postorder()   == [42])
    check("level-order of single node is [42]",   single.level_order() == [42])

    # ── Summary ──────────────────────────────
    print(f"\n{'='*35}")
    print(f"Results: {passed} passed, {failed} failed out of {passed+failed} tests")
    print('='*35)


if __name__ == "__main__":
    # Original demo
    print("=== Original Demo ===")
    mt = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        mt.insert(v)
    print("search(30)    :", mt.search(30))
    print("inorder       :", mt.inorder())
    print("preorder      :", mt.preorder())
    print("postorder     :", mt.postorder())
    print("level-order   :", mt.level_order())

    run_tests()