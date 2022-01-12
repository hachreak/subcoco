from pycocotools.coco import COCO
import numpy as np
import cv2
import sys

import os

ann_file = sys.argv[1]
images_path = sys.argv[2]
dest_path = sys.argv[3]

coco = COCO(ann_file)

for img_id in coco.getImgIds():
    ann_ids = coco.getAnnIds(img_id)
    anns = coco.loadAnns(ann_ids)
    # load image
    image_info = coco.loadImgs(img_id)
    image_path = image_info[0]["file_name"]
    image_path = os.path.join(images_path, image_path)
    image = cv2.imread(image_path)

    for ann in anns:
        segs = ann["segmentation"]
        bbox = np.array(ann["bbox"])
        bbox[2:4] = bbox[0:2] + bbox[2:4]

        segs = [np.array(seg, np.int32).reshape((1, -1, 2))
                for seg in segs]

        for seg in segs:
            cv2.drawContours(image, seg, -1, (0, 255, 0), 2)
        # third aug -1 means draw all contours in 3-D array, Or
        # for seg in segs: cv2.fillPoly(image, segm, (0,255,0))
        cv2.rectangle(image, (int(bbox[0]), int(bbox[1])),
                      (int(bbox[2]), int(bbox[3])), (0, 0, 255), 2)

    fname = image_info[0]["file_name"]

    outdir = os.path.join(dest_path, str(ann['category_id']))
    os.makedirs(outdir, exist_ok=True)

    filename = os.path.join(outdir, fname)
    print(filename)

    cv2.imwrite(filename, image)
    #  break

print('done')
