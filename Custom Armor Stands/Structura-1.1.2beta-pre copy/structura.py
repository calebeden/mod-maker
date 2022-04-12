import armor_stand_class
import structure_reader
import animation_class
from tkinter import StringVar, Button, Label, Entry, Tk
from tkinter import filedialog
import manifest
from shutil import copyfile
import os
from zipfile import ZipFile
import glob
import shutil
from tkinter import filedialog
from tkinter import messagebox

def generate_pack(struct_name, pack_name):
    # check that the pack name is not already used
    while os.path.isfile("{}.mcpack".format(pack_name)) or pack_name == "":
        pack_name = filedialog.asksaveasfilename(initialdir = os.getcwd(),
                                                 title = "Select a New Name",
                                                 filetypes = (("pack files",
                                                               "*.mcpack"),
                                                              ("all files",
                                                               "*.*")))
    ##manifest is mostly hard coded in this function.
    manifest.export(pack_name)
    #reads structure
    struct2make = structure_reader.process_structure(struct_name)
    #creates a base armorstand class for us to insert blocks
    armorstand = armor_stand_class.armorstand()
    #creats a base animation controller for us to put pose changes into
    animation = animation_class.animations()
    #gets the shape for looping
    [xlen, ylen, zlen] = struct2make.get_size()
    for y in range(ylen):
        #creates the layer for controlling. Note there is implied formating here
        #for layer names
        armorstand.make_layer(y)
        #adds links the layer name to an animation
        animation.insert_layer(y)
        for x in range(xlen):
            for z in range(zlen):
                #gets block
                block = struct2make.get_block(x, y, z)
                rot = None
                top = False
                open_bit = False
                ## everything below is handling the garbage mapping and naming in NBT
                #probably should be cleaned up into a helper function/library. for now it works-ish
                variant="Default"
                if "wall_block_type" in block["states"].keys():
                    variant = ["wall_block_type",block["states"]["wall_block_type"]]
                if "wood_type" in block["states"].keys():
                    variant = ["wood_type",block["states"]["wood_type"]]
                    if block["name"] == "minecraft:wood":
                        keys = block["states"]["wood_type"]
                        if bool(block["states"]["stripped_bit"]):
                            keys+="_stripped"
                        variant = ["wood",keys]
                if "old_log_type" in block["states"].keys():
                    variant = ["old_log_type",block["states"]["old_log_type"]]
                if "new_log_type" in block["states"].keys():
                    variant = ["new_log_type",block["states"]["new_log_type"]]
                if "stone_type" in block["states"].keys():
                    variant = ["stone_type",block["states"]["stone_type"]]
                if "prismarine_block_type" in block["states"].keys():
                    variant = ["prismarine_block_type",block["states"]["prismarine_block_type"]]
                if "stone_brick_type" in block["states"].keys():
                    variant = ["stone_brick_type",block["states"]["stone_brick_type"]]
                if "color" in block["states"].keys():
                    variant = ["color",block["states"]["color"]]
                if "sand_stone_type" in block["states"].keys():
                    variant = ["sand_stone_type",block["states"]["sand_stone_type"]]
                if "stone_slab_type" in block["states"].keys():
                    variant = ["stone_slab_type",block["states"]["stone_slab_type"]]
                if "stone_slab_type_2" in block["states"].keys():
                    variant = ["stone_slab_type_2",block["states"]["stone_slab_type_2"]]
                if "stone_slab_type_3" in block["states"].keys():
                    variant = ["stone_slab_type_3",block["states"]["stone_slab_type_3"]]
                if "stone_slab_type_4" in block["states"].keys():
                    variant = ["stone_slab_type_4",block["states"]["stone_slab_type_4"]]
                if "facing_direction" in block["states"].keys():
                    rot = block["states"]["facing_direction"]
                if "direction" in block["states"].keys():
                    rot = block["states"]["direction"]
                if "top_slot_bit" in block["states"].keys():
                    top = bool(block["states"]["top_slot_bit"])
                if "weirdo_direction" in block["states"].keys():
                    rot = int(block["states"]["weirdo_direction"])
                if "upside_down_bit" in block["states"].keys():
                    top = bool(block["states"]["upside_down_bit"])
                if "open_bit" in block["states"].keys():
                    open_bit = bool(block["states"]["open_bit"])
                ##  If java worlds are brought into bedrock the tools some times
                ##   output unsupported blocks, will log.
                try:
                    armorstand.make_block(x, y, z, block["name"].replace(
                        "minecraft:", ""), rot = rot, top = top,variant = variant, trap_open=open_bit)
                except:
                    armorstand.make_block(x, y, z, block["name"].replace(
                        "minecraft:", ""), rot = rot, top = top,variant = variant, trap_open=open_bit)
                    print("There is an unsuported block in this world and it was skipped")
                    print("x:{} Y:{} Z:{}, Block:{}, Variant: {}".format(x,y,z,block["name"],variant))

    ## this is a quick hack to get block lists, doesnt consider vairants.... so be careful
    allBlocks = struct2make.get_block_list()
    fileName="{} block list.txt".format(pack_name)
    with open(fileName,"w+") as text_file:
        text_file.write("This is a list of blocks, there is a known issue with variants, all variants are counted together\n\
Also the stack counts are currently based on a hardcoded 64 stack size! If you have smaller stack size involved in this, be sure to multiply accordingly\n")
        #This process combines lit/unlit, powered/unpowered, etc blockstates into one entry
        reformatted_blocks = {}
        for pair in allBlocks.items():
            name = pair[0]
            commonName = name.replace("minecraft:","").replace("unpowered_",'').replace('unlit_','').replace('powered_','').replace('lit_','')
            if commonName in reformatted_blocks.keys():
                reformatted_blocks[commonName] += pair[1]
            else:
                reformatted_blocks[commonName] = pair[1]

        #This part sorts the key-value pairs from highest-->lowest item count, calculates the item count according to Minecraft stacks, and outputs to text file
        for pair in sorted(reformatted_blocks.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
            name = pair[0]
            commonName = name.replace("minecraft:","").replace("unpowered_",'').replace('unlit_','').replace('powered_','').replace('lit_','')

            count = pair[1]
            #############   This assumes a 64 count item stack for everything!!!!!!!   #############
            stack_count = count // 64
            remainder = count % 64
            if stack_count >= 27:
                shulker_count = round(stack_count / 27, 2)
            if commonName != 'air' and commonName !='pistonArmCollision':
                if stack_count == 1:
                    text_file.write("{}: {}, or 1 stack and {}\n".format(commonName, count, remainder))
                elif stack_count > 1 and stack_count < 27:
                    text_file.write("{}: {}, or {} stacks and {}\n".format(commonName, count, stack_count, remainder))
                elif stack_count >= 27:
                    text_file.write("{}: {}, or {} stacks and {}, approx {} shulker boxes\n".format(commonName, count, stack_count, remainder, shulker_count))
                else:
                    text_file.write("{}: {}\n".format(commonName, count))

    ## copies the structure into the pack. This is to support the ablity to "update"
    ## old packs when we eventually fix some block bugs (cough cough buttons)
    copyfile(struct_name, "{}/template.mcstructure".format(pack_name))
    # call export fuctions
    armorstand.export(pack_name)
    animation.export(pack_name)
    # Copy my icons in
    copyfile("lookups/pack_icon.png", "{}/pack_icon.png".format(pack_name))
    os.makedirs(os.path.dirname(
        "{}/entity/armor_stand.entity.json".format(pack_name)), exist_ok=True)
    # the entities are hard coded and just copied, they dont change so this is fine
    copyfile("lookups/entity/armor_stand.entity.json",
             "{}/entity/armor_stand.entity.json".format(pack_name))

    # Adds to zip file a modified armor stand geometry to enlarge the render area of the entity
    larger_render = "lookups/models/entity/armor_stand.geo.json"
    larger_render_path = "{}/models/entity/{}".format(pack_name, "armor_stand.geo.json")
    copyfile(larger_render, larger_render_path)
    # the base render controller is hard coded and just copied in
    rc = "lookups/render_controllers/armor_stand.ghost_blocks.render_controllers.json"
    rcpath = "{}/render_controllers/{}".format(pack_name, "armor_stand.ghost_blocks.render_controllers.json")
    try:
        os.makedirs(os.path.dirname(rcpath))
    except:
        pass
    copyfile(rc, rcpath)

    ##This section was added to work with the foxynotail armor stand pack
    animation_controllers = ['rotateX.json', 'rotateZ.json', 'sit.json']
    for animation_controller in animation_controllers:
        original = os.path.join("lookups/animation_controllers/", animation_controller)
        new_path = "{}/animation_controllers/{}".format(pack_name, animation_controller)
        try:
            os.makedirs(os.path.dirname(new_path))
        except:
            pass
        copyfile(original, new_path)
    animations = ['rotateX.json', 'rotateZ.json', 'sit.json']
    for animation in animations:
        original = os.path.join("lookups/animations/", animation)
        new_path = "{}/animations/{}".format(pack_name, animation)
        copyfile(original, new_path)
    original_null = "lookups/models/entity/null.geo.json"
    new_null_path = "{}/models/entity/{}".format(pack_name, "null.geo.json")
    copyfile(original_null, new_null_path)
    rc_original = "lookups/render_controllers/armor_stand.render_controllers.json"
    rcpath = "{}/render_controllers/{}".format(pack_name, "armor_stand.render_controllers.json")
    copyfile(rc_original, rcpath)
    textures = ['armor_stand.png', 'armor_stand_locked.png']
    for texture in textures:
        original = os.path.join("lookups/textures/entity/", texture)
        new_path = "{}/textures/entity/{}".format(pack_name, texture)
        copyfile(original, new_path)


    ## get all files
    file_paths = []
    for directory,_,_ in os.walk(pack_name):
        file_paths.extend(glob.glob(os.path.join(directory, "*.*")))

    ## add all files to the mcpack file
    with ZipFile("{}.mcpack".format(pack_name), 'x') as zip:
        # writing each file one by one

        for file in file_paths:
            print(file)
            zip.write(file)
    ## delete all the extra files.
    shutil.rmtree(pack_name)


def runFromGui():
    ##wrapper for a gui.
    stop = False
    if len(FileGUI.get()) == 0:
        stop = True
        messagebox.showinfo("Error", "You need to browse for a structure file!")
    if len(packName.get()) == 0:
        stop = True
        messagebox.showinfo("Error", "You need a Name")
    if not stop:
        generate_pack(FileGUI.get(), packName.get())


def browseStruct():
    #brows for a structure file.
    FileGUI.set(filedialog.askopenfilename(filetypes=(
        ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))


root = Tk()
root.title("Structura")


FileGUI = StringVar()
packName = StringVar()
file_entry = Entry(root, textvariable=FileGUI)
packName_entry = Entry(root, textvariable=packName)
file_lb = Label(root, text="Structure file")
packName_lb = Label(root, text="Pack Name")
packButton = Button(root, text="Browse", command=browseStruct)

saveButton = Button(root, text="Make Pack", command=runFromGui)
r = 0
file_lb.grid(row=r, column=0)
file_entry.grid(row=r, column=1)
packButton.grid(row=r, column=2)
r += 1
packName_lb.grid(row=r, column=0)
packName_entry.grid(row=r, column=1)
r += 1
saveButton.grid(row=r, column=2)


root.mainloop()
