class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_the_begin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")

    def insert_at_index(self, index, data):
        if index == 0:
            self.insert_at_the_begin(data)

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        current_node = self.head
        while current_node.next:
            current_node = current_node.next

        current_node.next = Node(data, None)

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def length_of_list(self):
        length = 0
        current_node = self.head
        while current_node:
            length += 1
            current_node = current_node.next
        return length

    def remove_at(self, index):
        if index < 0 or index >= self.length_of_list():
            raise ValueError('Invalid index')

        if index == 0:
            self.head = self.head.next
        else:
            i = 0
            current_node = self.head
            while current_node:
                if i == index - 1:
                    current_node.next = current_node.next.next
                    break
                current_node = current_node.next
                i += 1

    def insert_at(self, index, data):
        if index < 0 or index > self.length_of_list():  # Дозволяємо вставку в кінець списку
            raise ValueError('Invalid index')

        if index == 0:
            self.insert_at_the_begin(data)
            return

        current_node = self.head
        i = 0
        while current_node:
            if i == index - 1:
                node = Node(data, current_node.next)
                current_node.next = node
                break
            current_node = current_node.next
            i += 1

# Тестування
ll = LinkedList()
ll.insert_values(['nigers', 'snickers', 'tweeks', 'mikmok'])
ll.print_list()  # Перевірте, чи правильно виводиться список

ll.remove_at(3)
ll.print_list()  # Перевірте, чи правильно видаляється елемент

ll.insert_at(1, 'new_value')
ll.print_list()  # Перевірте, чи правильно вставляється новий елемент
