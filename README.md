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
