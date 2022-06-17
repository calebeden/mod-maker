###########################################
# Author: calebeden
# File: heads.py
# Created on Wed Jun 15 2022
###########################################

from shutil import copy
from PIL import Image, ImageOps
import json
from os import path


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

        # with open('../template/resource_pack/attachables/render/template.player.json', 'r') as infile:
        #     armor_json = json.load(infile)
        # armor_json['minecraft:attachable']['description']['identifier'] = "mrc:" + \
        #     self._item_name + "_head.player"
        # armor_json['minecraft:attachable']['description']['item'] = {
        #     "mrc:" + self._item_name: "query.owner_identifier == 'minecraft:player'"}
        # armor_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/mrc_heads/' + self._item_name
        # with open('in_progress/resource_pack/attachables/render/mrc_' + self._item_name + '_head.player.json', 'w') as outfile:
        #     json.dump(armor_json, outfile)

    def generate_item_texture(self, item_texture_json):
        image = Image.open(path.join(
            self._directory, 'resource_pack/textures/models/mrc_heads', self._filename))
        base_layer = image.crop((8, 8, 16, 16))
        outer_layer = image.crop((40, 8, 48, 16))
        composite = Image.alpha_composite(base_layer, outer_layer)
        item_texture = ImageOps.expand(composite, 4)
        item_texture.save(path.join(
            self._directory, 'resource_pack/textures/items/mrc_heads', self._filename))

        item_texture_json['texture_data']['mrc:' + self._item_name +
                                          '_head'] = {'textures': 'textures/items/mrc_heads/' + self._filename}

    def generate_behavior(self):
        with open('template/behavior_pack/items/template.json', 'r') as infile:
            item_behavior = json.load(infile)
        item_behavior['minecraft:item']['description']['identifier'] = 'mrc:' + \
            self._item_name + '_head'
        item_behavior['minecraft:item']['components']['minecraft:icon']['texture'] = 'mrc:' + \
            self._item_name + '_head'
        with open(path.join(self._directory, 'behavior_pack/items/mrc_' + self._item_name + '_head.json'), 'w') as outfile:
            json.dump(item_behavior, outfile)

    def generate_text(self):
        head_text = self.__language_template.replace(
            'lower', self._item_name).replace('template', self.human_readable)
        with open(path.join(self._directory, 'resource_pack/texts/en_US.lang'), 'a') as outfile:
            outfile.write(head_text)

    def add_to_pack(self, item_texture_json):
        self.generate_attachable()
        self.generate_text()
        self.copy_texture()
        self.generate_item_texture(item_texture_json)
        self.generate_behavior()
        print(self.human_readable)


class Microblock(PlayerHead):
    def __init__(self, filename, directory):
        super().__init__(filename, directory, "item.mrc:lower_head=Micro-template\n")

    @property
    def human_readable(self):
        # TNT is an exception because it is all caps
        if self._item_name == 'tnt':
            return 'TNT'
        # Jack o'Lantern is an exception because it has a lowercase at the start of the word
        if self._item_name == 'jack_olantern':
            return "Jack o'Lantern"
        return self._item_name.replace('_', ' ').title().replace(' Of ', ' of ').replace(' And ', ' and ')

    def copy_texture(self):
        copy(path.join('template/skins/microblocks', self._filename), path.join(
            self._directory, 'resource_pack/textures/models/mrc_heads', self._filename))


class Person(PlayerHead):
    # CASE SENSITIVE FILENAMES
    def __init__(self, filename, directory):
        self.__name = filename[:-4]
        super().__init__(filename, directory, "item.mrc:lower_head=template's Head\n")

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

    @property
    def human_readable(self):
        return self._item_name.replace('_', ' ').title().replace(' Of ', ' of ').replace(' And ', ' and ')

    def copy_texture(self):
        copy(path.join('template/skins/custom', self._filename), path.join(self._directory,
             'resource_pack/textures/models/mrc_heads', self._filename))


class Mob(PlayerHead):
    def __init__(self, filename, directory):
        super().__init__(filename, directory, "item.mrc:lower_head=template Head\n")

    @property
    def human_readable(self):
        # jeb_ sheep is an exception because it has an underscore and starts lowercase
        if self._item_name == 'jeb_sheep':
            return "jeb_ Sheep"
        return self._item_name.replace('_', ' ').title()

    def copy_texture(self):
        copy(path.join('template/skins/mobs/', self._filename), path.join(self._directory,
             'resource_pack/textures/models/mrc_heads/', self._filename))
