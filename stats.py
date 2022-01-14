import json
import sys
import argparse
import pandas as pd

from collections import defaultdict


def to_pandas(fun):
    def f(train, val, **kwargs):
        to_train = fun(train, **kwargs)
        to_val = fun(val, **kwargs)
        merged = merge_dict(to_train, to_val)
        data = pd.DataFrame.from_dict(
            merged, orient='index', columns=['train', 'val'])
        for k in data.keys():
            data['{}_perc'.format(k)] = data[k] / data[k].sum()
        return data.sort_index()
    return f


def cat_id2name(content):
    cats = defaultdict(int)
    for cat in content['categories']:
        cats[cat['id']] = cat['name']
    return cats


def merge_dict(d1, d2):
    d3 = dict()
    keys = set(d1.keys()) | set(d2.keys())
    for k in keys:
        d3[k] = [d1.get(k, 0), d2.get(k, 0)]
    return d3


def filter_ann_by_image_id(content, img_id):
    return [ann for ann in content['annotations'] if ann['image_id'] == img_id]


@to_pandas
def instances_per_cat(content):
    inst = defaultdict(int)
    cats = cat_id2name(content)
    for ann in content['annotations']:
        cat = cats[ann['category_id']]
        inst[cat] += 1
    return inst


@to_pandas
def count_instances_per_img(content):
    count = defaultdict(int)
    for ann in content['images']:
        anns = filter_ann_by_image_id(content, ann['id'])
        count[len(anns)] += 1
    return count


@to_pandas
def count_cats_per_img(content):
    count = defaultdict(int)
    for ann in content['images']:
        anns = filter_ann_by_image_id(content, ann['id'])
        cats = set([ann['category_id'] for ann in anns])
        count[len(cats)] += 1
    return count


@to_pandas
def instance_size(content, delta=0.1):
    count = defaultdict(int)
    for img in content['images']:
        anns = filter_ann_by_image_id(content, img['id'])
        for ann in anns:
            perc_size = (ann['bbox'][2] * ann['bbox'][3]) / \
                (img['width'] * img['height'])
            idx = min(1., (perc_size // delta) * delta + delta)
            idx = "{:.3f}".format(idx)
            count[idx] += 1
    return count

parser = argparse.ArgumentParser(description='COCO Subset')
parser.add_argument('train_json', help='Input COCO train annotation file')
parser.add_argument('val_json', help='Input COCO validation annotation file')
parser.add_argument('action', help='Action to perform', choices=[
    'instances_per_category', 'cats_per_img', 'instances_per_img',
    'instance_size'])
parser.add_argument('-d', dest='delta', default=0.05, type=float,
                    help='delta percentage')

args = parser.parse_args(sys.argv[1:])

with open(args.train_json, 'r') as f:
    train = json.load(f)

with open(args.val_json, 'r') as f:
    val = json.load(f)

if args.action == 'instances_per_category':
    print(instances_per_cat(train, val).to_csv())
elif args.action == 'cats_per_img':
    print(count_cats_per_img(train, val).to_csv())
elif args.action == 'instances_per_img':
    print(count_instances_per_img(train, val).to_csv())
elif args.action == 'instance_size':
    print(instance_size(train, val, delta=args.delta).to_csv())
