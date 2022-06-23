
class TokenNode:

    def __init__(self, token, processed, pos=''):
        self.token = token
        self.processed = processed
        self.pos = pos
        self.next = None
        self.previous = None
        self.visited = False

    def __str__(self):
        return f"{self.token} - {self.processed}"

    def set_next(self, node):
        self.next = node

    def set_previous(self, node):
        self.previous = node


class LinkedTokens:

    def __init__(self):
        self.head = None
        self.tail = None

    def __str__(self):
        return ' -> '.join([str(node) for node in self])

    def __len__(self):
        count = 0
        node = self.head
        while node:
            count += 1
            node = node.next
        return count

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def add_node(self, node: TokenNode):
        if self.head is None:
            self.tail = self.head = node
        else:
            self.tail.next = node
            node.previous = self.tail
            self.tail = self.tail.next

    def init_from_prenorm_tuples(self, tuples: list):
        for tup in tuples:
            if len(tup) != 2:
                ValueError('Tuples have to have len 2, len is ' + str(len(tup)))
            else:
                node = TokenNode(tup[0], tup[1])
                self.add_node(node)

    def init_from_norm_tuples(self, tuples: list):
        for tup in tuples:
            if len(tup) != 3:
                ValueError('Tuples have to have len 3, len is ' + str(len(tup)))
            else:
                node = TokenNode(tup[0], tup[1], pos=tup[2])
                self.add_node(node)
