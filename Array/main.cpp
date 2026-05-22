//
// Created by HpElitebook on 3/29/2026.
//

#include <iostream>
#include <stdexcept>
#include <string>

class Array {
private:
    int* data;
    int size;
    int capacity;

    //double capacity when array is full
    void resize() {
        capacity *= 2;
        int *newData = new int[capacity];
        for (int i =0; i < size; i++) {
            newData[i] = data[i];
        }
        delete [] data;
        data = newData;
    }

    //shift elements right 'from' index to make room
    void shiftRight(int from) {
        if (size >= capacity) resize();
        for (int i = size; i > from; i--) {
            data[i] = data[i-1];
        }
        size ++ ;
    }

    void validateIndex(int index) const {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index" + std::to_string(index) +
                "out of range(size=" + std::to_string(size) + ")");
        }
    }

public:
    //constructor
    Array(int initialCapacity = 4)
        :size(0), capacity(initialCapacity) {
        data = new int[capacity];
    }

    //destructor
    ~Array() {
        delete[] data;
    }

    //insertion methods

    //insert beginning
    void insertAtBeginning(int value) {
        shiftRight(0);
        data[0] = value;
    }

    //insert at end
    void insertAtEnd(int value) {
        if (size >= capacity) resize();
        data[size++] = value;
    }

    //insert at given index
    void insertAtIndex(int index, int value) {
        //allow insert at the end
        if (index < 0 || index > size) {
            throw std::out_of_range("Index" + std::to_string(index) +
                "out of range(size=" + std::to_string(size) + ")");
        }
        shiftRight(index);
        data[index] = value;
    }
    void insertBefore(int index, int value) {
        validateIndex(index);
        shiftRight(index);
        data[index] = value;
    }

    void insertAfter(int index, int value) {
        validateIndex(index);
        shiftRight(index + 1);
        data[index + 1] = value;
    }

    //utility
    int getSize() const { return size; }

    int get(int index) const {
        validateIndex(index);
        return data[index];
    }

    void print() const {
        std::cout << "[";
        for (int i = 0; i < size; i++) {
            std::cout << data[i] << (i < size-1? "," : "");
        }
        std::cout << "]\n";
    }

};


int main () {
    Array object;

    // ── insertAtBeginning ─────────────────────────
    object.insertAtBeginning(10);
    std::cout << "insertAtBeginning(10):      "; object.print(); 

    object.insertAtBeginning(5);
    std::cout << "insertAtBeginning(5):       "; object.print(); 

    object.insertAtBeginning(1);
    std::cout << "insertAtBeginning(1):       "; object.print(); 


    // ── insertAtEnd ───────────────────────────────
    object.insertAtEnd(20);
    std::cout << "insertAtEnd(20):            "; object.print(); 

    object.insertAtEnd(30);
    std::cout << "insertAtEnd(30):            "; object.print(); 


    // ── insertAtIndex ─────────────────────────────
    object.insertAtIndex(2, 7);
    std::cout << "insertAtIndex(2, 7):        "; object.print();

    object.insertAtIndex(0, 0);
    std::cout << "insertAtIndex(0, 0):        "; object.print(); 

    object.insertAtIndex(object.getSize(), 99);
    std::cout << "insertAtIndex(size, 99):    "; object.print(); 


    // ── insertBefore ──────────────────────────────
    object.insertBefore(0, 100);
    std::cout << "insertBefore(0, 100):       "; object.print();

    object.insertBefore(4, 6);
    std::cout << "insertBefore(4, 6):         "; object.print(); 


    // ── insertAfter ───────────────────────────────
    object.insertAfter(0, 50);
    std::cout << "insertAfter(0, 50):         "; object.print(); 

    object.insertAfter(object.getSize()-1, 200);
    std::cout << "insertAfter(last, 200):     "; object.print(); 


    // ── out-of-range exceptions ───────────────────
    try { object.get(-1); }
    catch (const std::out_of_range& e) { std::cout << "get(-1) threw:              " << e.what() << "\n"; }

    try { object.get(object.getSize()); }
    catch (const std::out_of_range& e) { std::cout << "get(size) threw:            " << e.what() << "\n"; }

    try { object.insertAtIndex(-1, 99); }
    catch (const std::out_of_range& e) { std::cout << "insertAtIndex(-1) threw:    " << e.what() << "\n"; }

    try { object.insertBefore(object.getSize(), 99); }
    catch (const std::out_of_range& e) { std::cout << "insertBefore(size) threw:   " << e.what() << "\n"; }

    try { object.insertAfter(object.getSize(), 99); }
    catch (const std::out_of_range& e) { std::cout << "insertAfter(size) threw:    " << e.what() << "\n"; }

    return 0;
}