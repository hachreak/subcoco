# -*- coding: utf-8 -*-
#
# This file is part of scraper.
# Copyright 2020 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.
#
# pysenslog is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pysenslog is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pysenslog.  If not, see <http://www.gnu.org/licenses/>.

"""Get a subset of COCO."""

import json
import argparse
import sys

from collections import defaultdict


def load_file(filename):
    with open(filename, 'r') as file_:
        data = json.load(file_)
    return data


def save_file(filename, data):
    with open(filename, 'w') as file_:
        json.dump(data, file_)


def filter_categories(categories, annotations):
    return [c for c in annotations['categories'] if c['id'] in categories]


def filter_annotations(categories, annotations):
    return [a for a in annotations['annotations']
            if a['category_id'] in categories]


def filter_images(image_ids, annotations):
    return [i for i in annotations['images'] if i['id'] in image_ids]


def get_image_ids(annotations):
    count_files = defaultdict(int)
    for a in annotations['annotations']:
        count_files[a['image_id']] = 1
    return count_files.keys()


def count_categories_occurrence(annotations):
    counter = defaultdict(int)
    for a in annotations['annotations']:
        counter[a['category_id']] += 1
    return counter


def load_classes(filename):
    file_ = open(filename)
    return {k: v for (k, v) in enumerate(file_.read().split('\n'), 1)}


def print_stats(ann):
    counter = count_categories_occurrence(ann)
    classes = {}
    if args.classes:
        classes = load_classes(args.classes)
    files = get_image_ids(ann)
    print('Files: {0}'.format(len(files)))
    for k, v in counter.items():
        text = "Category {0}: {1}".format(k, v)
        if classes.get(k):
            text = '{} -> {}'.format(text, classes.get(k))
        print(text)
    print('total: {0}'.format(sum(counter.values())))


parser = argparse.ArgumentParser(description='COCO Subset')
parser.add_argument(
    '--categories', '-c', nargs='+', type=int,
    help='Extract annotations containing these categories')
parser.add_argument('--classes', '-l', help='File containing class names')
parser.add_argument(
    '--stats', '-s', action='store_true', default=False,
    help='Show only stats')
parser.add_argument('--output-path', '-o', help='Output COCO annotation file')
parser.add_argument('input_path', help='Input COCO annotation file')

args = parser.parse_args(sys.argv[1:])

# load all categories
ann = load_file(args.input_path)

if args.categories:
    # filter by categories
    ann['categories'] = filter_categories(args.categories, ann)
    ann['annotations'] = filter_annotations(args.categories, ann)
    ann['images'] = filter_images(get_image_ids(ann), ann)

if args.stats:
    print_stats(ann)
    sys.exit()

save_file(args.output_path, ann)
