import json
import sys
import random

with open(sys.argv[1], encoding='utf-8-sig') as data_file:
    # lines = [next(myfile) for x in range(100)]
    datapoints = data_file.readlines()
    random.Random().shuffle(datapoints)
    n = 10
    print(f'{n} random datapoints')
    for line in datapoints[:n]:
        try:
            data = json.loads(line)
            print('-----------------------')
            print(data['PrevCodeChunk'])
            print('=======================')
            print(data['UpdatedCodeChunk'])
            print('-----------------------')
            # break
        except Exception as e:
            print(line)
            print('ERROR')
            print(e)
            break
    diff = 0
    number_of_prev_lines_total = 0
    number_of_updated_lines_total = 0
    number_of_datapoints_more_than_7_lines = 0
    max_datapoint_len = 0
    max_datapoint = None
    for line in datapoints:
        data = json.loads(line)
        prev_lines = data['PrevCodeChunk'].splitlines()
        updated_lines = data['UpdatedCodeChunk'].splitlines()
        number_of_prev_lines_total += len(prev_lines)
        number_of_updated_lines_total += len(updated_lines)
        number_of_datapoints_more_than_7_lines += 1 if len(data['PrevCodeChunk'].splitlines()) + len(data['UpdatedCodeChunk'].splitlines()) >= 2 * 7 else 0
        diff += len(set(prev_lines).symmetric_difference(set(updated_lines))) / 2
        if len(prev_lines) + len(updated_lines) > max_datapoint_len:
            max_datapoint_len = len(prev_lines) + len(updated_lines)
            max_datapoint = data
    print(f'Max Datapoint: ')
    print(f'--------------')
    print(max_datapoint['PrevCodeChunk'])
    print(f'==============')
    print(max_datapoint['UpdatedCodeChunk'])
    print(f'--------------')
    print(f'Max Datapoint Size: {max_datapoint_len / 2}')
    print(f'Number of datapoints: {len(datapoints)}')
    print(f'Number of lines in prev change parts: {number_of_prev_lines_total}')
    print(f'Number of lines in updated change parts: {number_of_updated_lines_total}')
    print(f'Number of lines in prev and updated change parts: {number_of_prev_lines_total + number_of_updated_lines_total}')
    print(
        f'Average number of lines in prev and updated change parts: {(number_of_prev_lines_total + number_of_updated_lines_total) / (len(datapoints) * 2)}')
    print(f'Number of datapoints with more than 7 lines: {number_of_datapoints_more_than_7_lines}')
    print(f'Total lines changed (approximate value): {diff}')
    print(f'Average lines changed (approximate value): {diff / len(datapoints)}')
