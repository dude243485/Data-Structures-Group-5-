# Data Structures Collection - Group 5

Welcome to the **Data Structures Collection** repository by **Group 5**. This repository contains premium, robust, and clean implementations of fundamental and advanced data structures in **Python** and **C++**. Each implementation includes a comprehensive suite of built-in unit tests and demo operations to verify correctness.

---

## 📂 Project Structure

Below is an overview of the directory structure and the files included in this project:

| Directory | Core File(s) | Language | Description |
| :--- | :--- | :--- | :--- |
| **`[Array] /Data Structures/Array`** | [`main.cpp`]<br>[`main.exe`] | C++ | A custom dynamic array (`Array` class) featuring dynamic resizing (doubling capacity), insertions (`insertAtBeginning`, `insertAtEnd`, `insertAtIndex`, `insertBefore`, `insertAfter`), bounds checking, and custom error handling with `std::out_of_range`. |
| **`[Binary Search Trees] /Data Structures/Binary Search Trees`** | [`main.py`] | Python | A complete Binary Search Tree (BST) supporting sorted insertion, node searching, recursive leaf/single-child/two-child deletions, Inorder, Preorder, and Postorder traversals, and automated test validations. |
| **`[AVL Trees] /Data Structures/AVL Trees`** | [`main.py`] | Python | A self-balancing AVL Tree that maintains a strict balance factor of $\pm 1$ using left/right rotations. Implements recursive insert, search, standard traversals, level-order traversal, and structural balance verification tests. |
| **`[B-Trees] /Data Structures/B-Trees`** | [`main.py`] | Python | A standard, disk-optimized B-Tree of order $t$ ($t=3$). Includes multi-way node splitting, search, sorted key traversal, tree structure visualization, and advanced deletion handling (borrowing, merging, and root-shrinking). |
| **`[B-Plus Trees] /Data Structures/B-Plus Trees`** | [`main.py`] | Python | An advanced B+ Tree implementation where all actual data is stored in the leaf nodes, connected as a singly-linked list for rapid sequential access. Implements leaf-level splitting, key router updates during deletion, and level-by-level structure printing. |
| **`[Graph] /Data Structures/Graph`** | [`main.py`] | Python | A graph traversal demo implementing **Depth-First Search (DFS)** (using an iterative stack approach) and **Breadth-First Search (BFS)** (using a queue) on a custom graph defined as an adjacency list. |

---

## 💻 Environment & Requirements

All implementations are designed with **zero external third-party library dependencies** to maximize portability and ease of execution.

### C++ Environment
- **Compiler**: GCC / G++ (supporting C++11 or newer)
- **Standard Library Components**: `<iostream>`, `<stdexcept>`, `<string>`

### Python Environment
- **Python Version**: **Python 3.10 or higher**
  > [!IMPORTANT]
  > The Python code uses modern union type hinting (e.g., `Node | None`). Using Python versions older than 3.10 will result in a syntax error unless you modify the type annotations. Please ensure your Python interpreter is up-to-date.

---

## 🚀 How to Run and Test Each Implementation

### 1. Custom Dynamic Array (C++)

The `Array` directory contains both the C++ source file and a **pre-compiled Windows executable (`main.exe`)** ready for the instructor or grader to run instantly without compilation.

#### Option A: Running the Pre-compiled Executable (Windows)
Open your terminal (PowerShell, Command Prompt, or Git Bash), navigate to the `Array` folder, and execute:
```powershell
# Navigate into the Array directory
cd "Array"

# Run the pre-built executable
.\main.exe
```

#### Option B: Compiling from Source (Terminal with GCC/G++)
If you are on a non-Windows environment (Mac/Linux) or wish to recompile the source code:
```bash
# Navigate into the Array directory
cd "Array"

# Compile with g++ using the C++11 standard
g++ -std=c++11 main.cpp -o main.exe

# Run the newly compiled executable
# On Windows:
.\main.exe
# On macOS / Linux:
./main.exe
```

*The program will output a step-by-step trace of insertions, print array states, and verify out-of-range exception handling.*

---

### 2. Binary Search Tree (Python)

Run the script to see a live demonstration followed by a comprehensive, automated test suite covering BST insertions, node search, single/double child deletions, root deletions, and duplicates.

```bash
# Navigate and run
cd "Binary Search Trees"
python main.py
```

---

### 3. AVL Tree (Python)

Run the AVL Tree script to see the balance rotations in action, sorted traversals (Inorder, Preorder, Postorder, Level-order), and a battery of automated tests checking the AVL balance properties after sequential updates.

```bash
# Navigate and run
cd "AVL Trees"
python main.py
```

---

### 4. B-Tree (Python)

Run the B-Tree script to observe how the tree handles splitting and merging keys of order $t=3$. The terminal will print a clear tree visualization showing root and child relationships.

```bash
# Navigate and run
cd "B-Trees"
python main.py
```

---

### 5. B-Plus Tree (Python)

Run the B+ Tree script to see how internal router keys are updated during key deletions and trace the leaf-level singly-linked list traversal.

```bash
# Navigate and run
cd "B-Plus Trees"
python main.py
```

---

### 6. Graph Traversals (Python)

Runs Depth-First Search (DFS) and Breadth-First Search (BFS) starting from node `1` on a custom-built, 10-node graph adjacency list.

```bash
# Navigate and run
cd "Graph"
python main.py
```

---

> [!TIP]
> Each script is self-contained. You can easily modify the values in the `__main__` section of any `main.py` or the `main()` function in `main.cpp` to test custom inputs and verify outputs.
