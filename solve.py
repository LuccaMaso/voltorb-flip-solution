import copy

INT_MAX = 2147483648

def permutations(number, voltorb, row, answer, turn_string=False):
    counter_number = sum(row)
    counter_voltorb = row.count(0)
    if len(row) == 5:
        if counter_number == number and counter_voltorb == voltorb:
            if turn_string:
                answer.append("".join(list((map(str, row)))))
            else: 
                answer.append(row.copy())
            return
    if counter_voltorb > voltorb or counter_number > number:
        return 
    for i in range(0, 4):
        row.append(i)
        permutations(number, voltorb, row, answer, turn_string)
        row.pop()


def get_column(answer):
    column = len(answer)
    row = len(answer[0])
    all_prefix = []
    for i in range(row):
        word = []
        for k in range(column):
            word.append(str(answer[k][i]))
        all_prefix.append("".join(word))
    return all_prefix


def check_prefix(columns_permutations, answer):
    columns = get_column(answer)
    for i, prefix in enumerate(columns):
        for combination in columns_permutations[i]:
            if combination.startswith(prefix):
                break
        else:
            return False
    return True


def backtrack_solution(row_permutations, column_permutations, index, sequence, answer):
    if len(sequence) == 5:
        answer.append(sequence.copy())
        return
    for row in row_permutations[index]:
        sequence.append(row)
        if check_prefix(column_permutations, sequence):
            backtrack_solution(row_permutations, column_permutations, index+1, sequence, answer)
        sequence.pop()


def show_answer(answer):
    for solution in answer:
        print(solution)


def heuristic(answer):
    length = len(answer)
    aprox = [length//3, length//3, length//3]
    counter = {}
    for i in range(5):
        for k in range(5):
            counter[(i, k)] = [0, 0, 0]
    for solution in answer:
        for x in range(5):
            for y in range(5):
                number = solution[x][y]
                if number == 0:
                    counter[(x, y)][0] = INT_MAX
                    continue
                counter[(x, y)][number-1] += 1
    best_play = (-1, -1)
    best_point = INT_MAX
    for key, value in counter.items():
        if value[0] == length or value[1] == length or value[2] == length:
            continue
        points = abs(value[0] - aprox[0]) + abs(value[1] - aprox[1]) + abs(value[2] - aprox[2])
        if points < best_point:
            best_point = points
            best_play = key
    return (best_play[0]+1, best_play[1]+1)


def zero_heurisct(answer):
    length = len(answer)
    counter = {}
    for i in range(5):
        for k in range(5):
            counter[(i, k)] = 0
    for solution in answer:
        for x in range(5):
            for y in range(5):
                number = solution[x][y]
                if number != 0:
                    counter[(x, y)] += 1
    best_play = (-1, -1)
    best_point = 0
    for key, value in counter.items():
        if value == length:
            continue
        points = value / length
        if points > best_point:
            best_point = points
            best_play = key
    best_play = (best_play[0]+1, best_play[1]+1)
    return (best_play, best_point)


def choose_play(answer):
    show_answer(answer)
    best_play = heuristic(answer)
    if best_play == (0, 0):
        best_play, chance = zero_heurisct(answer)
        print(f"There's a {chance:.2f} that {best_play} is not a voltorb")
    else:
        print(f"You should try playing: ", best_play)


def is_finished(answer, played):
    first_solution = answer[0]
    plays = set()
    for x in range(5):
        for y in range(5):
            number = first_solution[x][y]
            if number == 2 or number == 3:
                plays.add((x+1, y+1))
                for solutions in answer:
                    if solutions[x][y] == 0 or solutions[x][y] == 1:
                        return False
    print("You won! Now just mark these squares:")
    final_answer = plays - played
    for play in final_answer:
        print(play)
    return True


if __name__ == "__main__":
    row_permutations = [[] for _ in range(5)]
    column_permutations = [[] for _ in range(5)]
    for i in range(5):
        number, voltorb = map(int, input().split())
        permutations(number, voltorb, [], column_permutations[i], True)
    for i in range(5):
        number, voltorb = map(int, input().split())
        permutations(number, voltorb, [], row_permutations[i], False)
    answer = []
    backtrack_solution(row_permutations, column_permutations, 0, [], answer) 
    show_answer(answer)
    choose_play(answer)
    played = set()
    while len(answer) != 1:
        x, y, number = map(int, input().split())
        played.add((x, y))
        x -= 1
        y -= 1
        for solution in copy.deepcopy(answer):
            if solution[x][y] != number:
                answer.remove(solution)
        show_answer(answer)
        if is_finished(answer, played):
            break
        choose_play(answer)
