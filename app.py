class Room:
    def __init__(self, description, north, south, east, west):
        self.description = description
        self.north = north
        self.south = south
        self.east = east
        self.west = west


bed_room_2 = 0
bed_room_1 = 1
north_hall = 2
south_hall = 3
kitchen = 4
diving_room = 5


def main():
    room_list = []
    room = Room('Bed room 2', bed_room_1, None, south_hall, None)
    room_list.append(room)
    room = Room('Bed room 1, there is a passage to the south and north', None, bed_room_2, north_hall, None)
    room_list.append(room)
    room = Room('North hall', None, south_hall, kitchen, bed_room_1)
    room_list.append(room)
    room = Room("Kitchen", None, diving_room, None, north_hall)
    room_list.append(room)
    room = Room('Diving room', kitchen, None, None, south_hall)
    room_list.append(room)
    room = Room("South hall", north_hall, None, diving_room, bed_room_2)
    room_list.append(room)
    current_room = 0
    done = False
    for room in room_list:
        print(room.description)
    while not done:
        print()
        print(room_list[current_room].description)
        move = input("Where you want to go\n1. north - n\n2. south - s\n3. east - e\n4. west - w\n\n5. quit - q: ")
        if move == 'q':
            print('game ended')
            break
        if move == 'n':
            next_room = room_list[current_room].north
            if next_room is None:
                print('You can not go this way')
            else:
                current_room = next_room
        elif move == 's':
            next_room = room_list[current_room].south
            if next_room is None:
                print('You can not go this way')

            else:
                current_room = next_room

        elif move == 'e':
            next_room = room_list[current_room].east
            if next_room is None:
                print('You can not go this way')

            else:
                current_room = next_room

        elif move == 'w':
            next_room = room_list[current_room].west
            if next_room is None:
                print('You can not go this way')

            else:
                current_room = next_room

    pass
main()