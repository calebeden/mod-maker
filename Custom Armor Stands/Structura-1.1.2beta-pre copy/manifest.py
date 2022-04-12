import json
import os
import uuid


def export(pack_name):
    manifest = {
        "format_version": 2,
        "header": {
            "name": pack_name,
            "description": "Structura block overlay pack, created by  \u00a7o\u00a75DrAv0011\u00a7r, \u00a7o\u00a79 FondUnicycle\u00a7r and\u00a7o\u00a75 RavinMaddHatter\u00a7r, FoxyNoTail armor stand version by \u00a7o\u00a72MrCraftable\u00a7r",
            "uuid": '34b86cb8-caec-45d6-903d-1e3172221432',
            "version": [
                2,
                0,
                2
            ],
            "min_engine_version": [
                1,
                16,
                0
            ]
        },
        "modules": [
            {
                "type": "resources",
                "uuid": '38eb0943-f6f8-4059-acbd-94fd8ea867ba',
                        "version": [
                    2, 0, 2]}],
	"dependencies": [
	  {
		"uuid": "fc4b58fb-132b-4d7d-81c9-af13b81ab0f5",
		"version": [2, 0, 2]
	  }
	]}


    path_to_ani = "{}/manifest.json".format(pack_name)
    os.makedirs(os.path.dirname(path_to_ani), exist_ok=True)

    with open(path_to_ani, "w+") as json_file:
        json.dump(manifest, json_file, indent=2)
