# Stats

If you want collect multiple statistics from a COCO-like dataset
(output is a csv file):

```bash
$ python stats.py
usage: stats.py [-h] [-d DELTA] train_json val_json {instances_per_category,cats_per_img,instances_per_img,instance_size}
stats.py: error: the following arguments are required: train_json, val_json, action
python stats train.json val.json
```

Actions:
 - `instances_per_category`: instances per category - count how many instances
   per class (also with percentage).
 - `cats_per_img`: categories per image - number of annotated categories per
   image (% of images / number of categories).
 - `instances_per_img`: instances per image - number of annotated instances per
   image (% of images / number of instances).
 - `instance_size`: instance size - the distribution of instance sizes.
    Option: `-d 0.1` specify delta percentage value.

# View

Paint images with bbox and segmentation annotations:

```bash
$ python view.py annotation.json images_dir output_dir
```

# SubCoco

Get a subset of COCO.

Example: show categories stats on screen:

```
python subcoco.py $COCODATASET/annotations/instances_val2017.json \
        -l data/coco.names --stats
```

Example: you want only categories motorcycle, backpack, sheep and cow in your
subset of coco dataset.

```
python subcoco.py $COCODATASET/annotations/instances_train2017.json \
        -c 4 20 21 27 -o $COCODATASET/annotations/instances_subtrain2017.json
```

Help:

```
python subcoco.py -h
```
