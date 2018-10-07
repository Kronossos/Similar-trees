#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Leaf:
    def __init__(self, label):
        self.tag = label

    def __iter__(self):
        yield self

    def __str__(self, level=0, blank=False, sign="  "):
        if not blank:
            blank = []
        line = list(" " * level + sign + str(self.tag))
        for fill in blank:
            try:
                if line[fill] == " ":
                    line[fill] = "│"
            except:
                pass
        return "".join(line)

    def is_leaf(self):
        return True

    def label(self):
        return self.tag

    def height(self):
        return 0


class BinNode:
    def __init__(self, left, right):
        for node in [left, right]:
            if node.__class__.__name__ not in ["BinNode", "Leaf"]:
                exit("Given nodes are not possible part of BinNode.")
        self.left = left
        self.right = right

    def __iter__(self):
        yield from iter(self.left)
        yield self
        yield from iter(self.right)

    def __str__(self, level=0, blank=False, sign="  "):

        if not blank: blank = []
        switch = False
        line = list(" " * level + sign + "█")

        for fill in blank[:]:

            if switch or "".join(line[fill]) == "└":
                switch = True
                blank.pop(-1)
            elif line[fill] == " ":
                line[fill] = "│"

        tree = "".join(line)

        if not self.left.is_leaf(): blank.append(level + 2)

        tree += "\n" + self.left.__str__(level + 2, blank, "├-")
        tree += "\n" + self.right.__str__(level + 2, blank, "└-")
        return tree

    def is_leaf(self):
        return False

    def similar(self, root=None):
        if not root:
            root = self

        for one, two in [('R', 'R'), ('L', 'L'), ('L', 'R'), ('R', 'L')]:
            new = self.graft(one, two, True)
            if new != -1:
                yield root
                self.graft(one, two, True)
        if not self.left.is_leaf():
            for tree in self.left.similar(root):
                yield tree

        if not self.right.is_leaf():
            for tree in self.right.similar(root):
                yield tree

    def son(self, which):
        if which == "L":
            return self.left
        elif which == "R":
            return self.right
        else:
            print("Unknow son!")

    def antison(self, which):
        if which == "L":
            return self.right
        elif which == "R":
            return self.left
        else:
            print("Unknow son!")

    def graft(self, first, second, quiet=False):

        if self.antison(first).is_leaf():
            if quiet:
                return -1
            else:
                print("Chosen son is LEAF!")
        else:
            if first == "L":
                self.left, self.right = self.antison(first).son(second), self.antison(first).change(second,
                                                                                                    self.son(first))
            else:
                self.left, self.right = self.antison(first).change(second, self.son(first)), self.antison(first).son(
                    second)

    def change(self, which, new_node):
        if which == "L":
            return BinNode(new_node, self.right)
        elif which == "R":
            return BinNode(self.left, new_node)
        else:
            print("Unknow son!")

    def height(self):
        return max(self.left.height(), self.right.height()) + 1

    def min_height(self):
        height = self.height()
        for tree in self.similar():
            if tree.height() < height:
                self.left, self.right = tree.son('L'), tree.son('R')
                self.min_height()
                break

    def max_height(self):
        height = self.height()
        for tree in self.similar():
            if tree.height() > height:
                self.left, self.right = tree.son('L'), tree.son('R')
                self.max_height()
                break


class BinTree:
    def __init__(self, node):
        if node.__class__.__name__ in ["BinNode", "Leaf"]:
            self.node = node
        else:
            exit("Given root is not possible part of BinTree.")

    def __str__(self):
        if self.root: return self.node.__str__()

    def __iter__(self):
        return iter(self.node)

    def root(self):
        return self.node

    def similar(self):
        yield from self.node.similar()

    def height(self):
        return self.node.height()

    def max_height(self):
        self.node.max_height()

    def min_height(self):
        self.node.min_height()
