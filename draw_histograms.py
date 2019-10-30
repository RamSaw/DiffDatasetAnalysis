#!/usr/bin/env python3

import difflib
import json
import os
import random
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

N_SAMPLES = 10
SEED = 94763
np.random.seed(SEED)


def get_range_from_filename(filename):
    split = [piece for piece in re.split(r"[._, \-!?:]+", filename) if piece.isdigit()]
    if len(split) != 2:
        raise Exception(f'Could not find range in filename {filename}')
    return int(split[0]), int(split[1])


def draw_histogram(code_sizes, diff_size_range, ax):
    diff_sizes_in_range = code_sizes[code_sizes >= diff_size_range[0] * 2]
    diff_sizes_in_range = diff_sizes_in_range[diff_sizes_in_range <= diff_size_range[1] * 2]
    ax.hist(code_sizes)
    statistics_about_histogram = f'Number of diffs: {len(code_sizes)}\n' \
                                 f'Mean size: {np.mean(code_sizes)}\n' \
                                 f'Median size: {np.median(code_sizes)}\n' \
                                 f'Std of size: {np.std(code_sizes)}\n' \
                                 f'Min size: {float("nan") if len(code_sizes) == 0 else np.min(code_sizes)}\n' \
                                 f'Max size: {float("nan") if len(code_sizes) == 0 else np.max(code_sizes)}\n' \
                                 f'Number of diffs with size in [{diff_size_range[0]}, {diff_size_range[1]}]: {len(diff_sizes_in_range)}'
    ax.text(0.425, 0.7, statistics_about_histogram, transform=ax.transAxes)
    ax.set_xlabel('number of lines in diff (prev + updated)')
    ax.set_ylabel('count')


def print_diffs_that_have_size_out_of_range(data_points, diff_sizes, diff_size_range):
    incorrect_diffs_indices = []
    for i, diff_size in enumerate(diff_sizes):
        if not (diff_size_range[0] <= diff_size[i] <= diff_size_range[1]):
            incorrect_diffs_indices.append(i)
    for i in incorrect_diffs_indices:
        print(data_points[i]['PrevCodeChunk'])
        print('--------------------')
    print('\n\n\n')
    print('=======================')
    print('\n\n\n')
    for i in incorrect_diffs_indices:
        print(data_points[i]['UpdatedCodeChunk'])
        print('--------------------')


def save_min_changes(data_points, diff_sizes, filename):
    save_diffs(data_points, [] if len(diff_sizes) == 0 else [np.argmin(diff_sizes)], filename)


def save_max_changes(data_points, diff_sizes, filename):
    save_diffs(data_points, [] if len(diff_sizes) == 0 else [np.argmax(diff_sizes)], filename)


def save_random_changes(data_points, n, filename):
    shuffled_indices = list(range(len(data_points)))
    random.Random(SEED).shuffle(shuffled_indices)
    save_diffs(data_points, shuffled_indices[:n], filename)


def save_diffs(data_points, indices, filename):
    with open(filename, 'w') as output_file:
        for id in indices:
            output_file.write('<<<<<<<<id>>>>>>>>\n')
            output_file.write(f'{data_points[id]["Id"]}\n')
            output_file.write('>>>>>>>>id<<<<<<<<\n')
            output_file.write(f'{data_points[id]["PrevCodeChunk"]}\n')
            output_file.write('---------------\n')
        output_file.write('===========END_OF_PREV===========\n')
        for id in indices:
            output_file.write('<<<<<<<<id>>>>>>>>\n')
            output_file.write(f'{data_points[id]["Id"]}\n')
            output_file.write('>>>>>>>>id<<<<<<<<\n')
            output_file.write(f'{data_points[id]["UpdatedCodeChunk"]}\n')
            output_file.write('---------------\n')


def process_one_experiment(root, filename):
    print(filename)
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    fig_changes_only, ax_changes_only = plt.subplots(1, 1, tight_layout=True)
    with open(os.path.join(root, filename), encoding='utf-8-sig') as data_file:
        data_points = [json.loads(line) for line in data_file.readlines()]
        min_diff_size, max_diff_size = get_range_from_filename(filename)
        diff_sizes = np.array(
            [len(diff['PrevCodeChunk'].splitlines()) + len(diff['UpdatedCodeChunk'].splitlines()) for diff in
             data_points])

        save_min_changes(data_points, diff_sizes, os.path.join(root, "data", os.path.splitext(filename)[0]) + ".min_samples")
        save_max_changes(data_points, diff_sizes, os.path.join(root, "data", os.path.splitext(filename)[0]) + ".max_samples")
        save_random_changes(data_points, N_SAMPLES, os.path.join(root, "data", os.path.splitext(filename)[0]) + ".random_samples")

        ax.set_title('Diff sizes histogram')
        draw_histogram(diff_sizes, (min_diff_size, max_diff_size), ax)
        ax_changes_only.set_title("Diff sizes histogram for changes only")
        changes = []
        for diff in data_points:
            changes_in_diff = []
            for text in difflib.unified_diff(diff['PrevCodeChunk'].splitlines(), diff['UpdatedCodeChunk'].splitlines()):
                if text[:3] not in ('+++', '---', '@@ ') and (text.startswith('-') or text.startswith('+')):
                    changes_in_diff.append(text)
            changes.append(changes_in_diff)
        changes_sizes = np.array([len(change) for change in changes])
        draw_histogram(changes_sizes, (min_diff_size, max_diff_size), ax_changes_only)

    fig.savefig(os.path.join(root, "histograms", os.path.splitext(filename)[0]) + ".png")
    fig_changes_only.savefig(os.path.join(root, "histograms", os.path.splitext(filename)[0]) + "_changes_only.png")


if __name__ == "__main__":
    root_folder = sys.argv[1]
    experiments = np.sort([f for f in os.listdir(root_folder) if os.path.isfile(os.path.join(root_folder, f))])
    for i, experiment_filename in enumerate(experiments):
        process_one_experiment(root_folder, experiment_filename)
