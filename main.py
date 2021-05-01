# -*- coding: utf-8 -*-
import content_based

def read_user_id():
    with open('input.txt', 'r') as f:
        return [l.strip() for l in  f.readlines()]


def write_output(prediction):
    with open('output.txt', 'w') as f:
        for p in prediction:
            for r in p:
                f.write(r + "\n")

def do(ids):
    # test implementation
    final_prediction = []
    for i in ids:
        final_prediction += content_based.recommendations(int(i))
        
    final_prediction = [['{},{},{}'.format(line[0], line[2], round(line[1], 4))] for line in final_prediction]
    return final_prediction


if __name__ == "__main__":
    user_ids = read_user_id()
    result = do(user_ids)
    write_output(result)