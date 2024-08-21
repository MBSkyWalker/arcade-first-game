class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self, val=0):
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
    def reverse_list(self, head):
        current_node = self.head

        while current_node:
            if not current_node.next:
                self.head = current_node
            print(current_node.data, end=' -> ')
            current_node = current_node.next


        print('None')
# Тестування
ll = LinkedList()
ll.insert_at_the_begin(6)
ll.insert_at_the_begin(2)
ll.insert_at_the_begin(3)
 # Перевірте, чи правильно вставляється новий елемент
ll.reverse_list(2)