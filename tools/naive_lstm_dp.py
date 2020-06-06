import csv
import copy
import os


def train_dp_withspeed():
    all_trajs = []
    traj = []
    TTI = []
    road_id = 0
    date = ""
    batch_size = 256
    for line in open("./train/train_TTI.csv"):
        line = line.split(",")
        if line[0] == 'id_road':
            continue
        else:
            if (road_id != line[0]) or (date != line[3].split(" ")[0]):
                road_id = line[0]
                date = line[3].split(" ")[0]
                traj = []
                TTI = []
            else:
                if (len(TTI) == 6):
                    TTI.append(line[1])
                    temp_traj = copy.deepcopy(traj[:12])
                    temp_traj.append(TTI[-1])
                    all_trajs.append(copy.deepcopy(temp_traj))
                    traj.append(line[1])
                    traj.append(line[2])
                    traj = traj[2:]
                    TTI.pop(0)
                else:
                    traj.append(line[1])
                    traj.append(line[2])
                    assert (float(traj[0]) < 20)
                    TTI.append(line[1])
        if len(all_trajs) == batch_size:
            with open("./train/processed/kr.csv", "a+", newline='') as objfile:
                obj_writer = csv.writer(objfile)
                for item in all_trajs:
                    obj_writer.writerow(item)
            all_trajs = []


def train_dp():
    all_trajs = []
    TTI = []
    road_id = 0
    date = ""
    batch_size = 256
    for line in open("./train/train_TTI.csv"):
        line = line.split(",")
        if line[0] == 'id_road':
            continue
        else:
            if (road_id != line[0]) or (date != line[3].split(" ")[0]):
                road_id = line[0]
                date = line[3].split(" ")[0]
                TTI = []
            else:
                if (len(TTI) == 6):
                    TTI.append(line[1])
                    all_trajs.append(copy.deepcopy(TTI))
                    TTI.pop(0)
                else:
                    TTI.append(line[1])
        if len(all_trajs) == batch_size:
            with open("./train/processed/kr.csv", "a+", newline='') as objfile:
                obj_writer = csv.writer(objfile)
                for item in all_trajs:
                    obj_writer.writerow(item)
            all_trajs = []


def test_dp():
    all_trajs = []
    traj = []
    count = -1
    for line in open("./train/toPredict_train_TTI.csv"):
        line = line.split(",")
        if (line[0] == "id_road"):
            continue
        count += 1
        if (len(traj) == 6):
            assert (count % 6 == 0)
            traj.append(0)
            all_trajs.append(copy.deepcopy(traj))
            traj = []
            traj.append(line[1])
        else:
            traj.append(line[1])
    if (len(traj) == 6):
        traj.append(0)
        all_trajs.append(traj)
    with open("./train/processed/ToPredict.csv", "a+", newline='') as objfile:
        obj_writer = csv.writer(objfile)
        for item in all_trajs:
            obj_writer.writerow(item)


def test_dp_withspeed():
    all_trajs = []
    traj = []
    count = -1
    for line in open("./train/toPredict_train_TTI.csv"):
        line = line.split(",")
        if (line[0] == "id_road"):
            continue
        count += 1
        if (len(traj) == 12):
            assert (count % 6 == 0)
            traj.append(0)
            all_trajs.append(copy.deepcopy(traj))
            traj = []
            traj.append(line[1])
            traj.append(line[2])
        else:
            traj.append(line[1])
            traj.append(line[2])
    if (len(traj) == 12):
        all_trajs.append(traj)
    with open("./train/processed/ToPredict.csv", "a+", newline='') as objfile:
        obj_writer = csv.writer(objfile)
        for item in all_trajs:
            obj_writer.writerow(item)


def clear():
    # if(os.path.exists("D:\projects\python\sodic\train\processed\kr.csv")):
    os.remove(r"D:\projects\python\sodic\train\processed\kr.csv")
    # if(os.path.exists("D:\projects\python\sodic\train\processed\ToPredict.csv")):
    os.remove(r"D:\projects\python\sodic\train\processed\ToPredict.csv")
    # if(os.path.exists("D:\projects\python\sodic\train\submit.csv")):
    # os.remove(r"D:\projects\python\sodic\train\submit.csv")


if __name__ == '__main__':
    clear()
    train_dp()
    test_dp()