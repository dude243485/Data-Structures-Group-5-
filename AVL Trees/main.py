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
        
    def _height(self, node : Node | None)  :
        if node :
            return node.height
        else:
            return 0
        
    def _balance_factor(self, node : Node | None):
        if not node :
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _update_height(self, node : Node):
        node.height = 1 + max (self._height(node.left), self._height(node.right))
        
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
        
        if bf > 1 and self._balance_factor(node.left) < 0 :
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if bf < -1 and self._balance_factor(node.right) <= 0 :
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
        else :
            return node
        return self._rebalance(node)
    
    def search(self, key) :
        return self._search(self.root, key)
    
    def _search(self, node : Node, key):
        if node is None: return None
        if key == node.key: return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    

mt = AVLTree()
mt.insert(10)
mt.insert(20)
mt.insert(30)
mt.insert(40)
mt.insert(50)
mt.insert(25)

print(mt.search(30))