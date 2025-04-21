
"""
Credit: https://github.com/mgtezak/Advent_of_Code/blob/master/2024/21/p2.py

my keypad.py solution does not take into account the distance away from the 
button 'A'. I missed this part of the solution. line 29 here for mgtezak figures
out elegantly where a negative number multiplied by a string doesn't produce a string. 

Even my memoization approach is taken from this solution, but my keypad.py script doesn't produce
the correct answer due to the issue described above. 
"""


from functools import lru_cache as cache

def part2(puzzle_input):
    numpad  = {
        '7': (0, 0), '8': (0, 1), '9': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '1': (2, 0), '2': (2, 1), '3': (2, 2),
                     '0': (3, 1), 'A': (3, 2),
    }
    dirpad = {
                     '^': (0, 1), 'A': (0, 2),
        '<': (1, 0), 'v': (1, 1), '>': (1, 2),
    }

    def create_graph(keypad, invalid_coords):
        graph = {}
        for a, (x1, y1) in keypad.items():
            for b, (x2, y2) in keypad.items():
                path = '<' * (y1 - y2) +  'v' * (x2 - x1) + '^' * (x1 - x2) + '>' * (y2 - y1)
                if invalid_coords == (x1, y2) or invalid_coords == (x2, y1):
                    path = path[::-1]
                graph[(a, b)] = path + 'A'
        return graph

    numpad_graph = create_graph(numpad, (3, 0))
    dirpad_graph = create_graph(dirpad, (0, 0))
    
#     for k,v in dirpad_graph.items():
#     	print(f"{k} -> {v}")
    #sys.exit()

    @cache(maxsize=None)
    def get_length(sequence, iterations, first_iter=False) -> int:
        
        print(sequence, iterations)
        
        if iterations == 0: 
            return len(sequence)
        prev = 'A'
        total_length = 0
        graph = numpad_graph if first_iter else dirpad_graph
        for char in sequence:
            print(prev, char, iterations)
            total_length += get_length(graph[(prev, char)], iterations - 1) 
            prev = char
        return total_length

    total_complexity = 0
    sub = 0
    for button_presses in puzzle_input.split('\n'):
        sub = int(button_presses[:-1]) * get_length(button_presses, 26, True)
        print(f'sub {sub}')
        total_complexity += sub

    return total_complexity

codes = ['593A','283A','670A','459A','279A']
codes = '\n'.join(codes)

print(part2(codes))
