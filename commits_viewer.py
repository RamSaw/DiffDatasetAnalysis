import json
import sys
import random

with open(sys.argv[1], encoding='utf-8-sig') as data_file, \
     open("prev_file", encoding='utf-8', mode="w") as prev_file, \
     open("updated_file", encoding='utf-8', mode="w") as updated_file:
    # lines = [next(data_file) for x in range(1000)]
    lines = data_file.readlines()
    cnt = 0
    for line in lines:
        try:
            data = json.loads(line)
            if ".Add(new OnCallAssignment" in data['prev_file'] and ".StartTime <= DateTime.UtcNow && DateTime.UtcNow <= " in data['prev_file'] and " ?? false;" in data['updated_file']:
                print('-----------------------')
                print(data['prev_file'])
                print("=======================")
                print(data['updated_file'])
                print('-----------------------')
                prev_file.write(data['prev_file'])
                updated_file.write(data['updated_file'])
                cnt += 1
                if cnt == 5:
                    break
        except Exception as e:
            print(line)
            print("ERROR")
            print(e)
            break
    diff = 0
    print(f'Found: {cnt}')
    #for line in lines:
    #    prev_lines = set(data['PrevCodeChunk'].splitlines())
    #    updated_lines = set(data['UpdatedCodeChunk'].splitlines())
    #    diff += len(prev_lines.symmetric_difference(updated_lines)) / 2
    #print(f"Number of datapoints: {len(lines)}")
    #print(f"Total lines changed: {diff}")
    #print(f"Average lines changed: {diff / len(lines)}")
