import pygame as pg


class Checker(pg.sprite.Sprite):
    def __init__(self, name, color):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.image = pg.Surface((n - 15, n - 15))  # хитбокс
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2.7)
        pg.draw.circle(self.image, self.color, self.rect.center, self.radius)  # визуальное отображение шашки

        self.image.set_colorkey((0, 0, 0))  # прячем хитбокс


class Cell(pg.sprite.Sprite):
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pg.Surface((n, n))
        self.image.fill((85, 45, 20))
        self.rect = self.image.get_rect()


def king_is_touching(previous_cell_cord, enemy_checkers_keys, our_checkers_keys,chosen):
    king_moves = [black_cells[previous_cell_cord]]
    i = 1
    while ((previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) not in enemy_checkers_keys) and (
            (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) not in our_checkers_keys) and (
            previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) in black_cells_keys:
        king_moves.append(black_cells[(previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n)])
        i += 1
    i = 1
    while ((previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) not in enemy_checkers_keys) and (
            (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) not in our_checkers_keys) and (
            previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) in black_cells_keys:
        king_moves.append(black_cells[(previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n)])
        i += 1
    i = 1
    while ((previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) not in enemy_checkers_keys) and (
            (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) not in our_checkers_keys) and (
            previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) in black_cells_keys:
        king_moves.append(black_cells[(previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n)])
        i += 1
    i = 1
    while ((previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) not in enemy_checkers_keys) and (
            (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) not in our_checkers_keys) and (
            previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) in black_cells_keys:
        king_moves.append(black_cells[(previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n)])
        i += 1
    king_touches = []
    for i in range(len(king_moves)):
        where = chosen.rect.colliderect(king_moves[i])
        king_touches.append(where)
    return king_moves, king_touches


def king_choose_attack(previous_cell_cord, enemy_checkers_keys, our_checkers_keys, cell_const, enemy_positions,
                       temp_enemy_pos,
                       go_left_up=True,
                       go_right_up=True,
                       go_left_down=True, go_right_down=True):
    # словарь, ключ которого - координаты изначальной позиции, а значение - массив с объектами клеток, на которые можно ходить
    king_attack_moves = {}
    cut_array = []
    if go_left_up:
        i = 1
        was_enemy_on_way_left_up = False
        # пока текущая клетка существует
        while (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) in black_cells_keys:
            if (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] - i * n,
                    previous_cell_cord[1] - i * n) not in temp_enemy_pos and was_enemy_on_way_left_up:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] - (i + 1) * n, previous_cell_cord[1] - (i + 1) * n) in black_cells_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] - (i + 1) * n) not in enemy_checkers_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] - (i + 1) * n) not in our_checkers_keys:

                    enemy_positions.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n))
                    # temp_enemy_pos += [(previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n)]
                    copied = temp_enemy_pos.copy()
                    p_enemy_positions, p_king_attack_moves = king_choose_attack(
                        (previous_cell_cord[0] - (i + 1) * n, previous_cell_cord[1] - (i + 1) * n),
                        enemy_checkers_keys, our_checkers_keys,
                        (previous_cell_cord[0] - (i - 1) * n, previous_cell_cord[1] - (i - 1) * n), copied,
                        temp_enemy_pos, go_right_down=False)
                    p_keys = list(p_king_attack_moves.keys())
                    for j in range(len(p_keys)):
                        if p_keys[j] in king_attack_moves.keys():
                            king_attack_moves[p_keys[j]].extend(p_king_attack_moves[p_keys[j]])
                        else:
                            king_attack_moves[p_keys[j]] = p_king_attack_moves[p_keys[j]]
                    king_attack_moves[cell_const] = [cut_array]
                    break

                else:
                    break
            # если текущая клетка содержит вражескую шашку
            elif (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) not in enemy_positions:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] - (i + 1) * n, previous_cell_cord[1] - (i + 1) * n) in black_cells_keys and (
                        previous_cell_cord[0] - (i + 1) * n,
                        previous_cell_cord[1] - (i + 1) * n) not in enemy_checkers_keys and (
                        previous_cell_cord[0] - (i + 1) * n,
                        previous_cell_cord[1] - (i + 1) * n) not in our_checkers_keys:
                    enemy_positions.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n))
                    temp_enemy_pos += [(previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n)]
                    was_enemy_on_way_left_up = True

                # если текущая клетка не существует или непустая
                else:
                    break

            elif (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) in our_checkers_keys:
                break

            # если уже съели 1 шашку и текущая свободна
            elif was_enemy_on_way_left_up and (
                    previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n) not in our_checkers_keys:
                cut_array.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n))
                copied = temp_enemy_pos.copy()
                # относительно новой ветви получаем всю нужную информацию
                p_enemy_positions, p_king_attack_moves = king_choose_attack(
                    (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n),
                    enemy_checkers_keys, our_checkers_keys,
                    (previous_cell_cord[0] - i * n, previous_cell_cord[1] - i * n), enemy_positions, copied,
                    go_right_down=False,
                    go_left_up=False)
                king_attack_moves.update(p_king_attack_moves)
                # если можно сходить
                king_attack_moves[cell_const] = [cut_array]
            i += 1

    if go_right_up:
        i = 1
        was_enemy_on_way_right_up = False
        # пока текущая клетка существует
        while (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) in black_cells_keys:
            if (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] + i * n,
                    previous_cell_cord[1] - i * n) not in temp_enemy_pos and was_enemy_on_way_right_up:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] - (i + 1) * n) in black_cells_keys and \
                        (previous_cell_cord[0] + (i + 1) * n,
                         previous_cell_cord[1] - (i + 1) * n) not in enemy_checkers_keys and \
                        (previous_cell_cord[0] + (i + 1) * n,
                         previous_cell_cord[1] - (i + 1) * n) not in our_checkers_keys:

                    enemy_positions.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n))
                    # temp_enemy_pos += [(previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n)]
                    copied = temp_enemy_pos.copy()
                    p_enemy_positions, p_king_attack_moves = king_choose_attack(
                        (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] - (i + 1) * n),
                        enemy_checkers_keys, our_checkers_keys,
                        (previous_cell_cord[0] + (i - 1) * n, previous_cell_cord[1] - (i - 1) * n), copied,
                        temp_enemy_pos, go_left_down=False)
                    p_keys = list(p_king_attack_moves.keys())
                    for j in range(len(p_keys)):
                        if p_keys[j] in king_attack_moves.keys():
                            king_attack_moves[p_keys[j]].extend(p_king_attack_moves[p_keys[j]])
                        else:
                            king_attack_moves[p_keys[j]] = p_king_attack_moves[p_keys[j]]
                    king_attack_moves[cell_const] = [cut_array]
                    break

                else:
                    break

            # если текущая клетка содержит вражескую шашку, которую мы еще не съели, а до этого мы не ели
            elif (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) not in temp_enemy_pos:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] - (i + 1) * n) in black_cells_keys and (
                        previous_cell_cord[0] + (i + 1) * n,
                        previous_cell_cord[1] - (i + 1) * n) not in enemy_checkers_keys and (
                        previous_cell_cord[0] + (i + 1) * n,
                        previous_cell_cord[1] - (i + 1) * n) not in our_checkers_keys:
                    enemy_positions.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n))
                    temp_enemy_pos += [(previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n)]
                    was_enemy_on_way_right_up = True

                # если текущая клетка не существует или непустая
                else:
                    break

            elif (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) in our_checkers_keys:
                break

            # если уже съели 1 шашку и текущая свободна
            elif was_enemy_on_way_right_up and (
                    previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n) not in our_checkers_keys:
                cut_array.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n))
                copied = temp_enemy_pos.copy()
                # относительно новой ветви получаем всю нужную информацию
                p_enemy_positions, p_king_attack_moves = king_choose_attack(
                    (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n),
                    enemy_checkers_keys, our_checkers_keys,
                    (previous_cell_cord[0] + i * n, previous_cell_cord[1] - i * n), enemy_positions, copied,
                    go_right_up=False,
                    go_left_down=False)
                king_attack_moves.update(p_king_attack_moves)
                # если можно сходить
                king_attack_moves[cell_const] = [cut_array]
            i += 1

    if go_right_down:
        i = 1
        was_enemy_on_way_right_down = False

        # пока текущая клетка существует
        while (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) in black_cells_keys:
            # если текущая клетка содержит вражескую шашку
            if (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] + i * n,
                    previous_cell_cord[1] + i * n) not in temp_enemy_pos and was_enemy_on_way_right_down:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] + (i + 1) * n) in black_cells_keys and \
                        (previous_cell_cord[0] + (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in enemy_checkers_keys and \
                        (previous_cell_cord[0] + (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in our_checkers_keys:

                    enemy_positions.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n))
                    # temp_enemy_pos += [(previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n)]
                    copied = temp_enemy_pos.copy()
                    p_enemy_positions, p_king_attack_moves = king_choose_attack(
                        (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] + (i + 1) * n),
                        enemy_checkers_keys, our_checkers_keys,
                        (previous_cell_cord[0] + (i - 1) * n, previous_cell_cord[1] + (i - 1) * n), copied,
                        temp_enemy_pos, go_left_up=False)
                    p_keys = list(p_king_attack_moves.keys())
                    for j in range(len(p_keys)):
                        if p_keys[j] in king_attack_moves.keys():
                            king_attack_moves[p_keys[j]].extend(p_king_attack_moves[p_keys[j]])
                        else:
                            king_attack_moves[p_keys[j]] = p_king_attack_moves[p_keys[j]]
                    king_attack_moves[cell_const] = [cut_array]
                    break

                else:
                    break
            elif (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) not in temp_enemy_pos:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] + (i + 1) * n, previous_cell_cord[1] + (i + 1) * n) in black_cells_keys and (
                        previous_cell_cord[0] + (i + 1) * n,
                        previous_cell_cord[1] + (i + 1) * n) not in enemy_checkers_keys and (
                        previous_cell_cord[0] + (i + 1) * n,
                        previous_cell_cord[1] + (i + 1) * n) not in our_checkers_keys:
                    enemy_positions.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n))
                    temp_enemy_pos += [(previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n)]
                    was_enemy_on_way_right_down = True


                # если текущая клетка не существует или непустая
                else:
                    break

            elif (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) in our_checkers_keys:
                break

            # если уже съели 1 шашку и текущая свободна
            elif was_enemy_on_way_right_down and (
                    previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n) not in our_checkers_keys:
                cut_array.append((previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n))
                copied = temp_enemy_pos.copy()
                # относительно новой ветви получаем всю нужную информацию
                p_enemy_positions, p_king_attack_moves = king_choose_attack(
                    (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n),
                    enemy_checkers_keys, our_checkers_keys,
                    (previous_cell_cord[0] + i * n, previous_cell_cord[1] + i * n), enemy_positions, copied,
                    go_right_down=False,
                    go_left_up=False)
                king_attack_moves.update(p_king_attack_moves)
                temp_enemy_pos = []
                # если можно сходить
                king_attack_moves[cell_const] = [cut_array]
            i += 1

    if go_left_down:
        i = 1
        was_enemy_on_way_left_down = False
        # пока текущая клетка существует
        while (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) in black_cells_keys:
            # если текущая клетка содержит вражескую шашку, которая является уже второй на диагонали
            if (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] - i * n,
                    previous_cell_cord[1] + i * n) not in temp_enemy_pos and was_enemy_on_way_left_down:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] - (i + 1) * n, previous_cell_cord[1] + (i + 1) * n) in black_cells_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in enemy_checkers_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in our_checkers_keys:

                    enemy_positions.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n))
                    # temp_enemy_pos += [(previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n)]
                    copied = temp_enemy_pos.copy()
                    p_enemy_positions, p_king_attack_moves = king_choose_attack(
                        (previous_cell_cord[0] - (i - 1) * n, previous_cell_cord[1] + (i - 1) * n),
                        enemy_checkers_keys, our_checkers_keys,
                        (previous_cell_cord[0] - (i - 1) * n, previous_cell_cord[1] + (i - 1) * n), copied,
                        temp_enemy_pos, go_right_up=False, go_left_up=False, go_right_down=False, go_left_down=True)
                    p_keys = list(p_king_attack_moves.keys())
                    for j in range(len(p_keys)):
                        if p_keys[j] in king_attack_moves.keys():
                            king_attack_moves[p_keys[j]].extend(p_king_attack_moves[p_keys[j]])
                        else:
                            king_attack_moves[p_keys[j]] = p_king_attack_moves[p_keys[j]]
                    king_attack_moves[cell_const] = [cut_array]
                    break

                else:
                    break
            # если текущая клетка содержит вражескую шашку
            elif (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) in enemy_checkers_keys and (
                    previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) not in temp_enemy_pos:
                # если следующая клетка пустая и существует. (Нужно, чтобы определить, есть ли противники на ветке)
                if (previous_cell_cord[0] - (i + 1) * n, previous_cell_cord[1] + (i + 1) * n) in black_cells_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in enemy_checkers_keys and \
                        (previous_cell_cord[0] - (i + 1) * n,
                         previous_cell_cord[1] + (i + 1) * n) not in our_checkers_keys:
                    enemy_positions.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n))
                    temp_enemy_pos += [(previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n)]
                    was_enemy_on_way_left_down = True

                # если следующая клетка не существует или непустая
                else:
                    break
            # если текущая клетка содержит нашу шашку
            elif (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) in our_checkers_keys:
                break

            # если уже съели 1 шашку и текущая свободна
            elif was_enemy_on_way_left_down and (
                    previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) not in our_checkers_keys and (
                    previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n) not in enemy_checkers_keys:
                cut_array.append((previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n))
                copied = temp_enemy_pos.copy()
                # относительно новой ветви получаем всю нужную информацию
                p_enemy_positions, p_king_attack_moves = king_choose_attack(
                    (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n),
                    enemy_checkers_keys, our_checkers_keys,
                    (previous_cell_cord[0] - i * n, previous_cell_cord[1] + i * n), enemy_positions, copied,
                    go_right_up=False,
                    go_left_down=False)
                king_attack_moves.update(p_king_attack_moves)
                # если можно сходить
                king_attack_moves[cell_const] = [cut_array]
            i += 1
        # king_attack_moves[cell_const] = cut_array

    if len(cut_array) == 0 and go_left_up + go_right_up + go_left_down + go_right_down == 3:
        cut_array.append(previous_cell_cord)
        king_attack_moves[cell_const] = cut_array
    return enemy_positions, king_attack_moves


# [(150.0, 50.0), (350.0, 50.0), (750.0, 50.0), (50.0, 150.0), (650.0, 150.0), (550.0, 250.0), (550, 50), (50, 350), (650, 350), (150, 250)]
# [(750.0, 650.0), (50.0, 750.0), (250.0, 750.0), (650.0, 750.0), (350, 450), (450, 350), (250, 550), (250, 350), (450, 150), (550, 650)]
# {(350, 250): [[(550, 450), (650, 550)], [[(150, 450), (50, 550)]]], (650, 550): [[(450, 750)], [[(350, 250), (250, 150)]]], (150, 450): [[(350, 250)], [[(350, 650), (450, 750)]]], (450, 750): [[(150, 450)], [[(650, 550), (750, 450)]]], (550, 50): [[(350, 250)]]}

def remove_extra_cells(current, king_attack_keys, king_attack_moves):
    # массив, показывающий есть ли возможность идти дальше
    stop = []
    if current in king_attack_keys:
        # первый цикл
        for i in range(len(king_attack_moves[current])):
            for j in range(len(king_attack_moves[current][i])):
                if king_attack_moves[current][i][j] not in king_attack_keys:
                    stop.append(king_attack_moves[current][i][j])
            if len(stop) != len(king_attack_moves[current][i]):
                king_attack_moves[current][i] = [z for z in king_attack_moves[current][i] if z not in stop]
            stop.clear()

    return king_attack_moves


def king_is_touching_attack_cells(king_attacks, previous_cell_cord, chosen, king_attack_moves):
    king_att_touches = []
    for i in range(len(king_attacks[previous_cell_cord])):
        for j in range(len(king_attack_moves[previous_cell_cord][i])):
            where = chosen.rect.colliderect(black_cells[king_attack_moves[previous_cell_cord][i][j]])
            if where:
                king_att_touches.append(king_attack_moves[previous_cell_cord][i][j])
    return king_att_touches


def where_is_enemy(previous_cell_cord, current_cell_cord, enemy_positions):
    delta_x = current_cell_cord[0] - previous_cell_cord[0]
    delta_y = current_cell_cord[1] - previous_cell_cord[1]
    direction = (delta_x // abs(delta_x), delta_y // abs(delta_y))
    i = 1
    while (
            previous_cell_cord[0] + i * n * direction[0],
            previous_cell_cord[1] + i * n * direction[1]) not in enemy_positions:
        i += 1
    enemy_position = (previous_cell_cord[0] + i * n * direction[0], previous_cell_cord[1] + i * n * direction[1])
    return enemy_position


def find_cells_to_move(previous_cell_cord):
    right_up_cell = (previous_cell_cord[0] + n,
                     previous_cell_cord[1] - n)  # 2 клетки, помимо начальной, на которые можно сходить
    left_up_cell = (previous_cell_cord[0] - n, previous_cell_cord[1] - n)
    left_down_cell = (previous_cell_cord[0] - n, previous_cell_cord[1] + n)
    right_down_cell = (previous_cell_cord[0] + n, previous_cell_cord[1] + n)
    return right_up_cell, left_up_cell, left_down_cell, right_down_cell


def find_cells_to_attack(previous_cell_cord):
    eat_left_up = (previous_cell_cord[0] - 2 * n, previous_cell_cord[1] - 2 * n)
    eat_right_up = (previous_cell_cord[0] + 2 * n, previous_cell_cord[1] - 2 * n)
    eat_left_down = (previous_cell_cord[0] - 2 * n, previous_cell_cord[1] + 2 * n)
    eat_right_down = (previous_cell_cord[0] + 2 * n, previous_cell_cord[1] + 2 * n)
    return eat_left_up, eat_right_up, eat_left_down, eat_right_down


def make_choose_attack(eat_left_up, is_enemy_on_left_up, eat_right_up, is_enemy_on_right_up, eat_left_down,
                       is_enemy_on_left_down, eat_right_down, is_enemy_on_right_down):
    choose_attack = [0, 0, 0, 0]
    if (eat_left_up in black_cells_keys) and (eat_left_up not in white_checkers_keys) and \
            (eat_left_up not in black_checkers_keys) and is_enemy_on_left_up:  # атака налево-вверх
        choose_attack[0] = black_cells[eat_left_up]

    if (eat_right_up in black_cells_keys) and (eat_right_up not in white_checkers_keys) and \
            (eat_right_up not in black_checkers_keys) and is_enemy_on_right_up:  # атака направо-вверх
        choose_attack[1] = black_cells[eat_right_up]

    if (eat_left_down in black_cells_keys) and (eat_left_down not in white_checkers_keys) and \
            (eat_left_down not in black_checkers_keys) and is_enemy_on_left_down:  # атака налево-вниз
        choose_attack[2] = black_cells[eat_left_down]

    if (eat_right_down in black_cells_keys) and (eat_right_down not in white_checkers_keys) and (
            eat_right_down not in black_checkers_keys) and is_enemy_on_right_down:  # атака направо-вниз
        choose_attack[3] = black_cells[eat_right_down]
    return choose_attack


def is_touching_to_attack(choose_attack, chosen):
    touches_attack = []
    for i in range(len(choose_attack)):
        if choose_attack[i] != 0:
            where = chosen.rect.colliderect(choose_attack[i])
            touches_attack.append(where)
        else:
            touches_attack.append(choose_attack[i])
    return touches_attack


# для каждой шашки мы просчитываем, должна ли она есть. Возвращаем массив с теми, что должны
def have_to_eat_checker(checker_color, checker_keys_color, enemy_checker_keys_color, king_color):
    have_to_eat = []
    for i in range(len(checker_color)):
        if checker_color[checker_keys_color[i]].color != king_color:
            right_up_cell, left_up_cell, left_down_cell, right_down_cell = find_cells_to_move(
                checker_color[checker_keys_color[i]].rect.center)
            eat_left_up, eat_right_up, eat_left_down, eat_right_down = find_cells_to_attack(
                checker_color[checker_keys_color[i]].rect.center)
            is_enemy_on_left_up = left_up_cell in enemy_checker_keys_color
            is_enemy_on_right_up = right_up_cell in enemy_checker_keys_color
            is_enemy_on_left_down = left_down_cell in enemy_checker_keys_color
            is_enemy_on_right_down = right_down_cell in enemy_checker_keys_color
            elem = make_choose_attack(eat_left_up, is_enemy_on_left_up, eat_right_up, is_enemy_on_right_up,
                                      eat_left_down,
                                      is_enemy_on_left_down, eat_right_down, is_enemy_on_right_down)
            if elem != [0, 0, 0, 0]:
                have_to_eat.append(checker_color[checker_keys_color[i]].rect.center)
        if checker_color[checker_keys_color[i]].color == king_color:
            f, attack_moves = king_choose_attack(checker_keys_color[i], enemy_checker_keys_color, checker_keys_color,
                                                 checker_keys_color[i], [], [])
            if len(attack_moves) > 0:
                have_to_eat.append(checker_keys_color[i])
            attack_moves.clear()
    return have_to_eat


# def king_have_to_eat(enemy_checkers_keys,our_checker_keys_color,our_checker_color):
#     king_HTE = []
#     for i in range(len(our_checker_keys_color)):
#         if our_checker_color[our_checker_keys_color[i]].color == king_black_color:
#             attack_moves = king_choose_attack(our_checker_keys_color[i],enemy_checkers_keys,our_checker_keys_color,our_checker_keys_color[i],[],[])
#             if len(attack_moves) > 0:
#                 king_HTE.append(our_checker_keys_color[i])
#     return king_HTE


def is_attacking(touches_attack, enemy_checkers, our_checkers, our_checkers_keys, choose_attack, left_up_cell,
                 right_up_cell, left_down_cell, right_down_cell, previous_cell_cord, chosen):
    if touches_attack[0]:
        chosen.rect.center = choose_attack[0].rect.center
        all_sprites.remove(enemy_checkers[left_up_cell])
        del enemy_checkers[left_up_cell]
        enemy_checkers_keys = list(enemy_checkers.keys())

    elif touches_attack[1]:
        chosen.rect.center = choose_attack[1].rect.center
        all_sprites.remove(enemy_checkers[right_up_cell])
        del enemy_checkers[right_up_cell]
        enemy_checkers_keys = list(enemy_checkers.keys())

    elif touches_attack[2]:
        chosen.rect.center = choose_attack[2].rect.center
        all_sprites.remove(enemy_checkers[left_down_cell])
        del enemy_checkers[left_down_cell]
        enemy_checkers_keys = list(enemy_checkers.keys())

    elif touches_attack[3]:
        chosen.rect.center = choose_attack[3].rect.center
        all_sprites.remove(enemy_checkers[right_down_cell])
        del enemy_checkers[right_down_cell]
        enemy_checkers_keys = list(enemy_checkers.keys())

    del our_checkers[previous_cell_cord]
    our_checkers[chosen.rect.center] = chosen
    our_checkers_keys.remove(previous_cell_cord)
    our_checkers_keys.append(chosen.rect.center)

    # print(white_checkers_keys)
    # print(white_checkers_values)
    previous_cell_cord = chosen.rect.center

    right_up_cell, left_up_cell, left_down_cell, right_down_cell = find_cells_to_move(
        previous_cell_cord)
    eat_left_up, eat_right_up, eat_left_down, eat_right_down = find_cells_to_attack(previous_cell_cord)

    # есть ли промежуточная вражеская клетка
    is_enemy_on_left_up = left_up_cell in enemy_checkers_keys
    is_enemy_on_right_up = right_up_cell in enemy_checkers_keys
    is_enemy_on_left_down = left_down_cell in enemy_checkers_keys
    is_enemy_on_right_down = right_down_cell in enemy_checkers_keys

    choose_attack = make_choose_attack(eat_left_up, is_enemy_on_left_up, eat_right_up,
                                       is_enemy_on_right_up,
                                       eat_left_down,
                                       is_enemy_on_left_down, eat_right_down, is_enemy_on_right_down)

    if our_checkers_keys == white_checkers_keys:
        if choose_attack != [0, 0, 0, 0]:
            white_move = True
            in_war = True
            loop = True
        else:
            white_move = False
            in_war = False
            loop = False

    else:
        if choose_attack != [0, 0, 0, 0]:
            white_move = False
            in_war = True
            loop = True

        else:
            white_move = True
            in_war = False
            loop = False

    return enemy_checkers, enemy_checkers_keys, our_checkers, our_checkers_keys, white_move, in_war, previous_cell_cord, loop


# [(150, 650), (350, 650), (550, 650), (750, 650)]

n = 100
WIDTH = 8 * n
FPS = 30
counter = 0
king_black_color = (142, 142, 142)
king_white_color = (169, 135, 111)
running = True
white_move = True
already = False
in_war = False
flag = False
loop = False
matrix = [[0, 11, 0, 11, 0, 11, 0, 11],
          [11, 0, 11, 0, 11, 0, 11, 0],
          [0, 11, 0, 11, 0, 11, 0, 11],
          [1, 0, 1, 0, 1, 0, 1, 0],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [2, 0, 2, 0, 2, 0, 2, 0],
          [0, 2, 0, 2, 0, 2, 0, 2],
          [2, 0, 2, 0, 2, 0, 2, 0]]
black_cells = {}
white_checkers = {}
black_checkers = {}

pg.init()  # старт pygame
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, WIDTH))  # создание окна
pg.display.set_caption("Checkers")  # установка названия окна
clock = pg.time.Clock()  # ставим таймер, чтобы прорисовка шла не хаотично, а цивильно
all_sprites = pg.sprite.LayeredUpdates()  # создаем массив для прорисовки

for i in range(8):
    for j in range(8):
        if matrix[i][j] != 0:
            a = (n * (j + 0.5), n * (i + 0.5))
            black_cells[a] = Cell(f'cell_{i}_{j}')
            black_cells[a].rect.center = a
            all_sprites.add(black_cells[a])
            all_sprites.move_to_back(black_cells[a])
            counter += 1

        if matrix[i][j] == 11:
            a = (n * (j + 0.5), n * (i + 0.5))
            black_checkers[a] = Checker(f'black_checker_{i}_{j}', (1, 1, 1))
            black_checkers[a].rect.center = a
            all_sprites.add(black_checkers[a])
        if matrix[i][j] == 2:
            a = (n * (j + 0.5), n * (i + 0.5))
            white_checkers[a] = Checker(f'black_checker_{i}_{j}', (255, 255, 255))
            white_checkers[a].rect.center = a
            all_sprites.add(white_checkers[a])

black_cells_keys = list(black_cells.keys())
white_checkers_keys = list(white_checkers.keys())
black_checkers_keys = list(black_checkers.keys())

# Конструктор
while running:
    clock.tick(FPS)  # ставим периодичность
    for event in pg.event.get():  # если в окне происходит вообще что угодно
        if event.type == pg.QUIT:  # если нажали на выход - выход
            running = False
        m_pos = pg.mouse.get_pos()
        if white_move:
            if pg.mouse.get_pressed()[0]:
                HTE_lst = have_to_eat_checker(white_checkers, white_checkers_keys, black_checkers_keys,
                                              king_white_color)
                for i in range(len(white_checkers_keys)):

                    # если еще не выбрана шашка, которую мы держим и на шашку направлен курсор
                    if white_checkers[white_checkers_keys[i]].rect.collidepoint(m_pos) and already is not True:
                        # если не надо есть
                        if HTE_lst == []:
                            chosen = white_checkers[
                                white_checkers_keys[i]]  # находим шашку, на которую направлен курсор
                            previous_cell_cord = chosen.rect.center  # координаты начальной клетки
                            in_war = False
                            already = True
                        # если надо есть
                        if HTE_lst != []:
                            if loop is False:
                                if white_checkers_keys[i] in HTE_lst:
                                    chosen = white_checkers[white_checkers_keys[i]]
                                    previous_cell_cord = white_checkers_keys[i]
                                    already = True
                                    in_war = True
                            if loop:
                                chosen = white_checkers[previous_cell_cord]
                                already = True
                                in_war = True

                    if already is True:  # когда уже выбрана
                        chosen.rect.center = m_pos  # приклеиваем ее центр к курсору
                        break

            elif already is True and pg.mouse.get_pressed()[0] is not True:
                already = False
                previous_cell = black_cells[previous_cell_cord]
                if chosen.color != king_white_color:
                    # вычисление координат клеток, что расположены диагонально на 1 клетку
                    right_up_cell, left_up_cell, left_down_cell, right_down_cell = find_cells_to_move(
                        previous_cell_cord)

                    # вычисление координат клеток, на которые перейдем, когда съедим
                    eat_left_up, eat_right_up, eat_left_down, eat_right_down = find_cells_to_attack(previous_cell_cord)

                    # 3 клетки, на которых может оказаться шашка, если она никого не будет есть
                    choose_3 = [previous_cell]

                    # есть ли промежуточная вражеская клетка
                    is_enemy_on_left_up = left_up_cell in black_checkers_keys
                    is_enemy_on_right_up = right_up_cell in black_checkers_keys
                    is_enemy_on_left_down = left_down_cell in black_checkers_keys
                    is_enemy_on_right_down = right_down_cell in black_checkers_keys

                    # проверка, есть ли шашке, куда ходить
                    if left_up_cell in black_cells_keys and left_up_cell not in white_checkers_keys and left_up_cell not in black_checkers_keys:
                        choose_3.append(black_cells[left_up_cell])
                    if right_up_cell in black_cells_keys and right_up_cell not in white_checkers_keys and right_up_cell not in black_checkers_keys:
                        choose_3.append(black_cells[right_up_cell])

                    # механика атаки
                    choose_attack = make_choose_attack(eat_left_up, is_enemy_on_left_up, eat_right_up,
                                                       is_enemy_on_right_up,
                                                       eat_left_down,
                                                       is_enemy_on_left_down, eat_right_down, is_enemy_on_right_down)
                    touches_attack = is_touching_to_attack(choose_attack, chosen)

                    # обработка коллизии шашки и клеток для передвижения
                    touches = []
                    for i in range(len(choose_3)):
                        where = chosen.rect.colliderect(choose_3[i])
                        touches.append(where)

                    if sum(touches_attack) > 0:
                        black_checkers, black_checkers_keys, white_checkers, white_checkers_keys, white_move, in_war, previous_cell_cord, loop = is_attacking(
                            touches_attack,
                            black_checkers, white_checkers, white_checkers_keys, choose_attack,
                            left_up_cell,
                            right_up_cell, left_down_cell, right_down_cell, previous_cell_cord, chosen)

                    # если просто ходим
                    # print(touches)

                    if in_war is False:
                        if (sum(touches) > 1) or (sum(touches) == 0) or (touches[0] and (sum(touches)) == 1):
                            chosen.rect.center = previous_cell_cord

                        elif touches[1]:
                            chosen.rect.center = choose_3[1].rect.center  # передвигаем шашку на левую-верхнюю клетку
                            del white_checkers[previous_cell_cord]
                            white_checkers[chosen.rect.center] = chosen
                            white_checkers_keys.remove(previous_cell_cord)
                            white_checkers_keys.append(chosen.rect.center)
                            # print(white_checkers_keys)
                            # print(white_checkers_values)
                            white_move = False


                        elif touches[2]:
                            chosen.rect.center = choose_3[2].rect.center  # передвигаем шашку на правую-верхнюю клетку
                            del white_checkers[previous_cell_cord]
                            white_checkers[chosen.rect.center] = chosen
                            white_checkers_keys.remove(previous_cell_cord)
                            white_checkers_keys.append(chosen.rect.center)
                            # print(white_checkers_keys)
                            # print(white_checkers_values)
                            white_move = False



                    else:
                        chosen.rect.center = previous_cell_cord

                    if chosen.rect.centery == (0.5 * n):
                        all_sprites.remove(chosen)
                        temp_position = chosen.rect.center
                        del white_checkers[chosen.rect.center]
                        chosen = Checker(previous_cell_cord, king_white_color)
                        chosen.rect.center = temp_position
                        white_checkers[chosen.rect.center] = chosen
                        all_sprites.add(chosen)

                else:
                    king_moves, king_touches = king_is_touching(previous_cell_cord, black_checkers_keys,
                                                                white_checkers_keys,chosen)

                    # black_checkers_keys.remove(previous_cell_cord)
                    black_positions, king_attack_moves = king_choose_attack(
                        previous_cell_cord,
                        black_checkers_keys,
                        white_checkers_keys, previous_cell_cord, [], [])
                    print(black_positions)
                    king_attack_keys = list(king_attack_moves.keys())
                    king_attack_moves = remove_extra_cells(previous_cell_cord, king_attack_keys,
                                                           king_attack_moves)  # 333
                    print(in_war, king_attack_moves)
                    if previous_cell_cord in king_attack_keys:
                        king_att_touches = king_is_touching_attack_cells(king_attack_moves, previous_cell_cord, chosen,
                                                                         king_attack_moves)
                        if len(king_att_touches) == 1:
                            chosen.rect.center = king_att_touches[0]
                            white_checkers_keys.remove(previous_cell_cord)
                            white_checkers_keys.append(king_att_touches[0])
                            del white_checkers[previous_cell_cord]
                            white_checkers[chosen.rect.center] = chosen
                            black_position = where_is_enemy(previous_cell_cord, king_att_touches[0], black_positions)
                            all_sprites.remove(black_checkers[black_position])
                            del black_checkers[black_position]
                            black_checkers_keys = list(black_checkers.keys())
                            if king_att_touches[0] not in king_attack_keys:
                                white_move = False
                                in_war = False
                                loop = False
                            else:
                                in_war = True
                                loop = True
                                previous_cell_cord = king_att_touches[0]
                        else:
                            chosen.rect.center = previous_cell_cord
                    else:
                        in_war = False

                    if in_war is False and white_move is True:
                        if (sum(king_touches) > 1) or (sum(king_touches) == 0) or (
                                king_touches[0] and (sum(king_touches)) == 1):
                            chosen.rect.center = previous_cell_cord
                        else:
                            for i in range(len(king_touches)):
                                if king_touches[i]:
                                    chosen.rect.center = king_moves[i].rect.center
                                    del white_checkers[previous_cell_cord]
                                    white_checkers[chosen.rect.center] = chosen
                                    white_checkers_keys.remove(previous_cell_cord)
                                    white_checkers_keys.append(chosen.rect.center)
                                    # print(white_checkers_keys)
                                    # print(white_checkers_values)
                                    white_move = False

                # print('black', black_checkers)
                # print('      ')
                # print("white", white_checkers)
                # print(' ')
                # print(' ')









        # если ход черных
        else:
            if pg.mouse.get_pressed()[0]:
                HTE_lst = have_to_eat_checker(black_checkers, black_checkers_keys, white_checkers_keys,
                                              king_black_color)
                for i in range(len(black_checkers_keys)):

                    # если еще не выбрана шашка, которую мы держим и на шашку направлен курсор
                    if black_checkers[black_checkers_keys[i]].rect.collidepoint(m_pos) and already is not True:
                        # если не надо есть
                        if HTE_lst == []:
                            chosen = black_checkers[
                                black_checkers_keys[i]]  # находим шашку, на которую направлен курсор
                            previous_cell_cord = chosen.rect.center  # координаты начальной клетки
                            in_war = False
                            already = True
                        # если надо есть
                        if HTE_lst != []:
                            if loop is False:
                                if black_checkers_keys[i] in HTE_lst:
                                    chosen = black_checkers[black_checkers_keys[i]]
                                    previous_cell_cord = black_checkers_keys[i]
                                    already = True
                                    in_war = True
                            if loop:
                                chosen = black_checkers[previous_cell_cord]
                                already = True
                                in_war = True

                    if already is True:  # когда уже выбрана
                        chosen.rect.center = m_pos  # приклеиваем ее центр к курсору
                        break
#
            elif already is True and pg.mouse.get_pressed()[0] is not True:
                already = False
                previous_cell = black_cells[previous_cell_cord]
                if chosen.color != king_black_color:
                    # вычисление координат клеток, что расположены диагонально на 1 клетку
                    right_up_cell, left_up_cell, left_down_cell, right_down_cell = find_cells_to_move(
                        previous_cell_cord)

                    # вычисление координат клеток, на которые перейдем, когда съедим
                    eat_left_up, eat_right_up, eat_left_down, eat_right_down = find_cells_to_attack(previous_cell_cord)

                    # 3 клетки, на которых может оказаться шашка, если она никого не будет есть
                    choose_3 = [previous_cell]

                    # есть ли промежуточная вражеская клетка
                    is_enemy_on_left_up = left_up_cell in white_checkers_keys
                    is_enemy_on_right_up = right_up_cell in white_checkers_keys
                    is_enemy_on_left_down = left_down_cell in white_checkers_keys
                    is_enemy_on_right_down = right_down_cell in white_checkers_keys

                    # проверка, есть ли шашке, куда ходить
                    if left_down_cell in black_cells_keys and left_down_cell not in white_checkers_keys and left_down_cell not in black_checkers_keys:
                        choose_3.append(black_cells[left_down_cell])
                    if right_down_cell in black_cells_keys and right_down_cell not in white_checkers_keys and right_down_cell not in black_checkers_keys:
                        choose_3.append(black_cells[right_down_cell])

                    # механика атаки
                    choose_attack = make_choose_attack(eat_left_up, is_enemy_on_left_up, eat_right_up,
                                                       is_enemy_on_right_up,
                                                       eat_left_down,
                                                       is_enemy_on_left_down, eat_right_down, is_enemy_on_right_down)
                    touches_attack = is_touching_to_attack(choose_attack, chosen)

                    # обработка коллизии шашки и клеток для передвижения
                    touches = []
                    for i in range(len(choose_3)):
                        where = chosen.rect.colliderect(choose_3[i])
                        touches.append(where)

                    if sum(touches_attack) > 0:
                        white_checkers, white_checkers_keys, black_checkers, black_checkers_keys, white_move, in_war, previous_cell_cord, loop = is_attacking(
                            touches_attack,
                            white_checkers, black_checkers, black_checkers_keys, choose_attack,
                            left_up_cell,
                            right_up_cell, left_down_cell, right_down_cell, previous_cell_cord, chosen)

                    # если просто ходим
                    # print(touches)

                    if in_war is False:
                        if (sum(touches) > 1) or (sum(touches) == 0) or (touches[0] and (sum(touches)) == 1):
                            chosen.rect.center = previous_cell_cord

                        elif touches[1]:
                            chosen.rect.center = choose_3[1].rect.center  # передвигаем шашку на левую-верхнюю клетку
                            del black_checkers[previous_cell_cord]
                            black_checkers[chosen.rect.center] = chosen
                            black_checkers_keys.remove(previous_cell_cord)
                            black_checkers_keys.append(chosen.rect.center)
                            # print(white_checkers_keys)
                            # print(white_checkers_values)
                            white_move = True


                        elif touches[2]:
                            chosen.rect.center = choose_3[2].rect.center  # передвигаем шашку на правую-верхнюю клетку
                            del black_checkers[previous_cell_cord]
                            black_checkers[chosen.rect.center] = chosen
                            black_checkers_keys.remove(previous_cell_cord)
                            black_checkers_keys.append(chosen.rect.center)
                            # print(white_checkers_keys)
                            # print(white_checkers_values)
                            white_move = True



                    else:
                        chosen.rect.center = previous_cell_cord

                    if chosen.rect.centery == (7.5 * n):
                        all_sprites.remove(chosen)
                        temp_position = chosen.rect.center
                        del black_checkers[chosen.rect.center]
                        chosen = Checker(previous_cell_cord, king_black_color)
                        chosen.rect.center = temp_position
                        black_checkers[chosen.rect.center] = chosen
                        all_sprites.add(chosen)

                else:
                    king_moves, king_touches = king_is_touching(previous_cell_cord, white_checkers_keys,
                                                                black_checkers_keys,chosen)

                    # black_checkers_keys.remove(previous_cell_cord)
                    white_positions, king_attack_moves = king_choose_attack(
                        previous_cell_cord,
                        white_checkers_keys,
                        black_checkers_keys, previous_cell_cord, [], [])
                    king_attack_keys = list(king_attack_moves.keys())
                    king_attack_moves = remove_extra_cells(previous_cell_cord, king_attack_keys,
                                                           king_attack_moves)
                    print(king_attack_moves)

                    if previous_cell_cord in king_attack_keys:
                        king_att_touches = king_is_touching_attack_cells(king_attack_moves, previous_cell_cord, chosen,
                                                                         king_attack_moves)
                        if len(king_att_touches) == 1:
                            chosen.rect.center = king_att_touches[0]
                            black_checkers_keys.remove(previous_cell_cord)
                            black_checkers_keys.append(chosen.rect.center)
                            del black_checkers[previous_cell_cord]
                            black_checkers[chosen.rect.center] = chosen
                            white_position = where_is_enemy(previous_cell_cord, king_att_touches[0], white_positions)
                            all_sprites.remove(white_checkers[white_position])
                            del white_checkers[white_position]
                            white_checkers_keys = list(white_checkers.keys())
                            if king_att_touches[0] not in king_attack_keys:
                                white_move = True
                                in_war = False
                                loop = False
                            else:
                                loop = True
                                in_war = True
                                previous_cell_cord = king_att_touches[0]
                        else:
                            chosen.rect.center = previous_cell_cord
                    else:
                        in_war = False

                    if in_war is False and white_move is False:
                        if (sum(king_touches) > 1) or (sum(king_touches) == 0) or (
                                king_touches[0] and (sum(king_touches)) == 1):
                            chosen.rect.center = previous_cell_cord
                        else:
                            for i in range(len(king_touches)):
                                if king_touches[i]:
                                    chosen.rect.center = king_moves[i].rect.center
                                    del black_checkers[previous_cell_cord]
                                    black_checkers[chosen.rect.center] = chosen
                                    black_checkers_keys.remove(previous_cell_cord)
                                    black_checkers_keys.append(chosen.rect.center)
                                    # print(white_checkers_keys)
                                    # print(white_checkers_values)
                                    white_move = True

    # прорисовка
    all_sprites.update()
    screen.fill((255, 255, 220))
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()