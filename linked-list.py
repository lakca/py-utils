

class Node(object):
    def __init__(self, value):
        self._value = value
        self._next = None
        self._prev = None


class LinkedList(object):
    '''双向链表'''

    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0

    @property
    def length(self):
        return self._length

    @property
    def tail(self):
        return self._tail

    @property
    def head(self):
        return self._tail

    def empty(self):
        self._head = None
        self._tail = None
        self._length = 0
        return self

    def push(self, value):
        node = Node(value)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            tail = self._head
            while tail._next is not None:
                tail = tail._next
            tail._next = node
            node._prev = tail
            self._tail = node
            self._length += 1
        return self

    def pop(self):
        if self._tail is None:
            return
        node = self._tail
        if self._tail._prev is None:
            self._head = None
            self._tail = None
        else:
            self._tail = self._tail._prev
            self._tail._next = None
        self._length -= 1
        del node._prev
        del node._next
        return node

    def unshift(self, value):
        node = Node(value)
        node._next = self._head
        if self._head is not None:
            self._head._prev = node
        self._head = node
        self._length += 1
        return self

    def shift(self):
        if self._head is None:
            return
        node = self._head
        if self._head._next is None:
            self._tail = None
            self._head = None
        else:
            self._head = self._head._next
            self._head._prev = None
        self._length -= 1
        del node._next
        del node._prev
        return node

    def index(self, n):
        if n not in range(0, self.length):
            return
        i = 0
        cur = self._head
        if n < self.length / 2:
            while i < n:
                cur = cur._next
                i += 1
        else:
            cur = self._tail
            i = self.length - 1
            while i > n:
                cur = cur._prev
                i -= 1
        return cur

    def truncate(self, left_len: int, head=False):
        '''
        截短链表，返回新的链表（不在原链表上操作）。
        - head: `False` 从尾开始截去， `True` 从头开始截去
        '''
        if left_len == 0:
            self.empty()

        else:
            if head:  # 从头开始截去
                cur = self._tail
                count = 1
                while (count < left_len) and (cur._prev is not None):
                    cur = cur._prev
                self._head = cur
                self._head._prev = None
                self.length -= count
            else:  # 从尾开始截去
                cur = self._head
                count = 1
                while (count < left_len) and (cur._next is not None):
                    cur = cur._next
                self._tail = cur
                self._tail._next = None
                self.length -= count

        return self

    def iter(self):
        '''从头开始遍历值'''
        cur = self._head
        while cur is not None:
            yield cur._value
            cur = cur._next

    def iter_reverse(self):
        '''从尾开始遍历值'''
        cur = self._tail
        while cur is not None:
            yield cur._value
            cur = cur._prev

    def items(self):
        '''返回值列表 `list`'''
        return [e for e in self.iter()]
