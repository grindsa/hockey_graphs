import json

if __name__ == '__main__':

    filename = 'c:\\temp\\2590.json'

    team_hash = {8: 'WOB', 44: 'FRA'}

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    with open(filename, 'r', encoding='utf8') as json_file:

        shot_dic = json.load(json_file)

        for shot in shot_dic['match']['shots']:
            # print('{0};{1};{2};{3};{4}'.format(shot['time'], shot['team_id'], shot['coordinate_x'], shot['coordinate_y'], shot['match_shot_resutl_id']))
            if shot['coordinate_x'] <= x_min:
                x_min = shot['coordinate_x']
            if shot['coordinate_x'] >= x_max:
                x_max = shot['coordinate_x']
            if shot['coordinate_y'] <= y_min:
                y_min = shot['coordinate_y']
            if shot['coordinate_y'] >= y_max:
                y_max = shot['coordinate_y']

    print('x_min:', x_min)
    print('x_max:', x_max)
    print('y_min:', y_min)
    print('y_max:', y_max)