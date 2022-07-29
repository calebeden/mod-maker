###########################################
# Author: calebeden
# File: heads.py
# Created on Wed Jun 15 2022
###########################################

from shutil import copy
from PIL import Image, ImageOps
import json
from os import path

name_exceptions = {'tnt': 'TNT',
                   'jack_olantern': "Jack o'Lantern", 'jeb_sheep': 'jeb_ Sheep'}


class PlayerHead:
    def __init__(self, filename, directory, language_template):
        self._filename = filename
        self._item_name = filename[:-4].lower()
        self.__language_template = language_template
        self._directory = directory

    @property
    def filename(self):
        return self._filename

    @property
    def name(self):
        return self._item_name

    @property
    def human_readable(self):
        # Microblocks
        # TNT is an exception because it is all caps
        if self._item_name in name_exceptions.keys():
            return name_exceptions[self._item_name]

        return self._item_name.replace('_', ' ').title().replace(' Of ', ' of ').replace(' And ', ' and ')

    def generate_attachable(self):
        with open('template/resource_pack/attachables/template.json', 'r') as infile:
            attachable_json = json.load(infile)
        attachable_json['minecraft:attachable']['description']['identifier'] = "mrc:" + \
            self._item_name + "_head"
        if (self._item_name.endswith('stained_glass') or self._item_name == 'tinted_glass' or self._item_name == 'ice'):
            # Stained/tinted glass and regular ice are exceptions: has translucency and only uses the base layer, we will use a different rendering material
            attachable_json['minecraft:attachable']['description']['materials']['default'] = "beacon_beam_transparent"
        attachable_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/mrc_heads/' + self._item_name
        with open(path.join(self._directory, 'resource_pack/attachables/mrc_' + self._item_name + '_head.json'), 'w') as outfile:
            json.dump(attachable_json, outfile)

    def generate_item_textures(self, item_texture_json):
        skin = Image.open(path.join(
            self._directory, 'resource_pack/textures/models/mrc_heads', self._filename))
        base_layer = skin.crop((8, 8, 16, 16))
        outer_layer = skin.crop((40, 8, 48, 16))
        composite = Image.alpha_composite(base_layer, outer_layer)
        item_texture = ImageOps.expand(composite, 4)
        if self._item_name.endswith('glass'):
            glass_background = Image.open(
                'template/skins/glass_background.png')
            item_texture = Image.alpha_composite(
                glass_background, item_texture)
        item_texture.save(path.join(
            self._directory, 'resource_pack/textures/items/mrc_heads', self._filename))

        item_texture_json['texture_data'][f'mrc:{self._item_name}_head'] = {
            'textures': f'textures/items/mrc_heads/{self._filename}'}

        with Image.open('template/resource_pack/textures/items/head_bundle.png') as bundle:
            bundle_pixels = bundle.load()
            head_pixels = item_texture.load()
            for row in range(4, 12):
                for col in range(4, 12):
                    bundle_pixels[row+1, col-3] = head_pixels[row, col]
            bundle.save(path.join(self._directory, 'resource_pack/textures/items/mrc_head_bundles',
                        f'{self._item_name}_head_bundle.png'))
        item_texture_json['texture_data'][f'mrc:{self._item_name}_head_bundle'] = {
            'textures': f'textures/items/mrc_head_bundles/{self._item_name}_head_bundle.png'}

    def generate_behavior(self):
        with open('template/behavior_pack/items/template_head.json', 'r') as infile:
            item_behavior = json.load(infile)
        item_behavior['minecraft:item']['description']['identifier'] = 'mrc:' + \
            self._item_name + '_head'
        item_behavior['minecraft:item']['components']['minecraft:icon']['texture'] = 'mrc:' + \
            self._item_name + '_head'
        with open(path.join(self._directory, 'behavior_pack/items/mrc_' + self._item_name + '_head.json'), 'w') as outfile:
            json.dump(item_behavior, outfile)

        with open('template/behavior_pack/items/template_bundle.json', 'r') as infile:
            bundle_item_behavior = json.load(infile)
        bundle_item_behavior['minecraft:item']['description']['identifier'] = 'mrc:' + \
            self._item_name + '_head_bundle'
        bundle_item_behavior['minecraft:item']['components']['minecraft:icon']['texture'] = 'mrc:' + \
            self._item_name + '_head_bundle'
        with open(path.join(self._directory, 'behavior_pack/items/mrc_' + self._item_name + '_head_bundle.json'), 'w') as outfile:
            json.dump(bundle_item_behavior, outfile)

    def generate_bundle_recipes(self):
        with open('template/behavior_pack/recipes/template_bundle_pack.json', 'r') as infile:
            bundle_pack = json.load(infile)
        bundle_pack['minecraft:recipe_shapeless']['description'][
            'identifier'] = f'mrc:{self._item_name}_head_bundle_pack'
        for i in range(8):
            bundle_pack['minecraft:recipe_shapeless']['ingredients'][
                i]['item'] = f'mrc:{self._item_name}_head'
        bundle_pack['minecraft:recipe_shapeless']['result'][
            'item'] = f'mrc:{self._item_name}_head_bundle'
        with open(path.join(self._directory, f'behavior_pack/recipes/{self._item_name}_head_bundle_pack.json'), 'w') as outfile:
            json.dump(bundle_pack, outfile)

        with open('template/behavior_pack/recipes/template_bundle_unpack.json', 'r') as infile:
            bundle_unpack = json.load(infile)
        bundle_unpack['minecraft:recipe_shaped']['description'][
            'identifier'] = f'mrc:{self._item_name}_head_bundle_unpack'
        bundle_unpack['minecraft:recipe_shaped']['key']['#'][
            'item'] = f'mrc:{self._item_name}_head_bundle'
        for i in range(8):
            bundle_unpack['minecraft:recipe_shaped']['result'][
                i]['item'] = f'mrc:{self._item_name}_head'
        with open(path.join(self._directory, f'behavior_pack/recipes/{self._item_name}_head_bundle_unpack.json'), 'w') as outfile:
            json.dump(bundle_unpack, outfile)

    def generate_text(self):
        head_text = self.__language_template.replace(
            'lower', self._item_name).replace('template', self.human_readable)
        with open(path.join(self._directory, 'resource_pack/texts/en_US.lang'), 'a') as outfile:
            outfile.write(head_text)

        head_bundle_text = self.__language_template.replace(
            'lower', self._item_name).replace('_head', '_head_bundle').replace('template', self.human_readable).replace('=', '=Bundle of ')
        with open(path.join(self._directory, 'resource_pack/texts/en_US.lang'), 'a') as outfile:
            outfile.write(head_bundle_text)

    def add_to_pack(self, item_texture_json):
        self.generate_attachable()
        self.generate_text()
        self.copy_texture()
        self.generate_item_textures(item_texture_json)
        self.generate_behavior()
        self.generate_bundle_recipes()
        print(self.human_readable)


class Microblock(PlayerHead):
    def __init__(self, filename, directory):
        super().__init__(filename, directory, "item.mrc:lower_head=Micro-template\n")

    def copy_texture(self):
        copy(path.join('template/skins/microblocks', self._filename), path.join(
            self._directory, 'resource_pack/textures/models/mrc_heads', self._filename))


class Person(PlayerHead):
    # CASE SENSITIVE FILENAMES
    def __init__(self, filename, directory):
        self.__name = filename[:-4]
        super().__init__(filename, directory, "item.mrc:lower_head=template's Head\n")

    # Have to override parent class because case sensitive
    @property
    def human_readable(self):
        return self.__name

    def copy_texture(self):
        copy(path.join('template/skins/people', self._filename), path.join(self._directory,
             'resource_pack/textures/models/mrc_heads', self._filename))

    # Have to override parent class because case sensitive
    def generate_attachable(self):
        with open('template/resource_pack/attachables/template.json', 'r') as infile:
            item_json = json.load(infile)
        item_json['minecraft:attachable']['description']['identifier'] = "mrc:" + \
            self._item_name + "_head"
        item_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/mrc_heads/' + self.__name
        with open(path.join(self._directory, 'resource_pack/attachables/mrc_' + self._item_name + '_head.json'), 'w') as outfile:
            json.dump(item_json, outfile)


class Custom(PlayerHead):
    def __init__(self, filename, directory):
        super().__init__(filename, directory, "item.mrc:lower_head=template\n")

    def copy_texture(self):
        copy(path.join('template/skins/custom', self._filename), path.join(self._directory,
             'resource_pack/textures/models/mrc_heads', self._filename))


class Mob(PlayerHead):
    def __init__(self, filename, directory):
        super().__init__(filename, directory, "item.mrc:lower_head=template Head\n")

    def copy_texture(self):
        copy(path.join('template/skins/mobs/', self._filename), path.join(self._directory,
             'resource_pack/textures/models/mrc_heads/', self._filename))
