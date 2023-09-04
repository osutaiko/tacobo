from constants import *
import requests
import zipfile
from io import BytesIO
import os


def download_mapset(mapset_id):
    api_url = 'https://api.chimu.moe/v1/download/' + str(mapset_id)
    mapset_zip = zipfile.ZipFile(BytesIO(requests.get(api_url).content))
    mapset_zip.extractall('./mapset-temp')


def find_diff_name(map_id):
    for file_name in os.listdir('./mapset-temp'):
        if file_name.endswith('.osu'):
            f = open('./mapset-temp/' + file_name, 'r', encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                if line[:9] == 'BeatmapID' and line[10:].strip() == str(map_id):
                    f.close()
                    return file_name
            f.close()


class MapData:
    def __init__(self, title, artist, creator, diff, hp, od, timing_points, hit_objects): #timing_points: list of (time, beat_length, meter), hit_objects: list of (time, type)
        self.title = title
        self.artist = artist
        self.creator = creator
        self.diff = diff
        self.hp = hp
        self.od = od
        self.timing_points = timing_points
        self.hit_objects = hit_objects


def parse_map(map_id):
    map_data = MapData(None, None, None, None, None, None, [], [])

    f = open('./mapset-temp/' + find_diff_name(map_id), 'r', encoding='utf-8')

    while True:
        line = f.readline().strip()
        if line[:min(6, len(line))] == 'Title:':
            map_data.title = line[6:]
        elif line[:min(7, len(line))] == 'Artist:':
            map_data.artist = line[7:]
        elif line[:min(8, len(line))] == 'Creator:':
            map_data.creator = line[8:]
        elif line[:min(8, len(line))] == 'Version:':
            map_data.diff = line[8:]
        elif line[:min(12, len(line))] == 'HPDrainRate:':
            map_data.hp = float(line[12:])
        elif line[:min(18, len(line))] == 'OverallDifficulty:':
            map_data.od = float(line[18:])
        elif line == '[TimingPoints]':
            break

    while True: #time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects
        line = f.readline().strip()
        if line == '[HitObjects]':
            break
        if line == '':
            continue
        elif line[0].isdigit() == False:
            continue

        val_list = list(map(float, line.split(',')))
        if val_list[6] == 1:
            map_data.timing_points.append((int(val_list[0]), val_list[1], int(val_list[2])))

    while True: #x,y,time,type,hitsound,objectParams,hitSample
        line = f.readline().strip()
        if line == '':
            break

        val_list = list(map(int, line.split(',')[:5]))
        time = val_list[2]
        obj_type = None

        if val_list[3]&(1<<0): #hitcircles
            if val_list[4]&(1<<1) or val_list[4]&(1<<3):
                if val_list[4]&(1<<2):
                    obj_type = BIG_KAT
                else:
                    obj_type = HIT_KAT
            else:
                if val_list[4]&(1<<2):
                    obj_type = BIG_DON
                else:
                    obj_type = HIT_DON
            map_data.hit_objects.append((time, obj_type))

        elif val_list[3]&(1<<3): #spinners
            time_start = val_list[2]
            time_end = int(line.split(',')[5])
            map_data.hit_objects.append((time_start, SPINNER_START))
            #map_data.hit_objects.append((time_end, SPINNER_END))
        elif val_list[3]&(1<<1): #sliders
            time = val_list[2]
            #length = val_list[7]
            if val_list[4]&(1<<2):
                map_data.hit_objects.append((time, BLIDER_START))
                #map_data.hit_objects.append((time + length, BLIDER_END))
            else:
                map_data.hit_objects.append((time, SLIDER_START))
                #map_data.hit_objects.append((time + length, SLIDER_END))

    f.close()
    return map_data