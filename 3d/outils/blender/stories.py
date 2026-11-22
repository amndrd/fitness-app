# Instagram stories (22/11/2026): the validated models, grouped, on white, no text. 1080 x 1920 (9:16).
# The user's direction: no floor in the picture. The objects are isolated, lit like the models' catalogue renders
# (3d/modeles/2-haltere/flottant.jpg), with only a light soft shadow under them; and the bars standing in an arc,
# their coloured end caps on top (3d/modeles/3-barre/couleurs-rack.jpg).
#   S1  the bars in an arc at the bottom, the plates floating above;
#   S2a the dumbbells floating in a grid, S2b in a cascade;
#   S3a the 25 mm plates in a row and the clips below, S3b the plates in a column, the clips on both sides.
# Instagram covers the top and the bottom of a story (profile, reply bar): the models stay in the middle.
# Two transparent renders per story: the objects alone (story-X.png), then only their shadow (story-X-ombre.png);
# outils/stories.py lays the shadow, lighter, then the objects on white.
# usage: Blender -b --factory-startup -P stories.py -- scenes=S1,S2a res=1440 samples=128 out=<dir>
import os, random
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_HALTERES = True
exec(open(os.path.join(HERE, 'halteres.py')).read())

SCENES = ARGS.get('scenes', 'S1').split(',')
COLS = list(PALETTE)                    # noir, graphite, blanc, rose, bleu, vert, rouge, sable
LIFT = 0.10                             # floating: 10 cm above the (invisible) floor


# ------------------------------------------------------------------ pieces
def plate(c, w=20, name='d'):
    return disque(w, plate_mats(c, 'moule'), name=name)             # axis Y


def bar(c, fin='A', name='b'):
    return barre_olympique(bar_mats(fin, c), name=name)             # axis X, centred


def round_db(c, w=15, name='h'):
    return haltere(w, dumbbell_mats(c, 'fin'), name)                # axis X, centred; resting on the floor z = DB2[w][0]


def clip(c, name='p'):
    return pince3(collar_mats(c), c, name)                           # coil axis Z, lying flat at z = GROUND


def vplate(c, w=2.5, name='v'):
    return vinyl_plate(w, plate_mats_v(c), name)                     # axis X


def loaded(c, name='hd'):
    return dumbbell(colour=c, name=name)                             # axis X; resting on the floor z = e['R']


def pose(o, loc, rot=(0, 0, 0)):
    o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    return o


def jitter(k, a):
    return [random.uniform(-a, a) for _ in range(k)]


# ------------------------------------------------------------------ light: isolated objects, a light shadow under them
def flags(c=(0.0, 0.0, 0.0), s=1.0):
    """Black cards out of the frame, seen only in reflections: chrome on white needs dark lines (like in a photo studio)."""
    blk = mat('drapeau', (0.0, 0.0, 0.0), rough=1.0, spec=0.0)
    cx, cy, cz = c
    for loc, rot, sx, sy in (((cx - 1.6 * s, cy + 0.2, cz + 0.4 * s), (0, 90, 0), 0.5 * s, 2.5 * s),
                             ((cx + 1.6 * s, cy + 0.4, cz + 0.3 * s), (0, -90, 0), 0.4 * s, 2.5 * s),
                             ((cx, cy + 1.8 * s, cz + 0.8 * s), (70, 0, 0), 2.5 * s, 0.25 * s)):
        me = bpy.data.meshes.new('drapeau')
        me.from_pydata([(-sx, -sy, 0), (sx, -sy, 0), (sx, sy, 0), (-sx, sy, 0)], [], [(0, 1, 2, 3)])
        o = link(bpy.data.objects.new('drapeau', me)); me.materials.append(blk)
        o.location = loc; o.rotation_euler = tuple(math.radians(v) for v in rot)
        o.visible_camera = False; o.visible_shadow = False


def catalogue_light(c=(0.0, 0.0, 0.0), s=1.0):
    """The light of the models' catalogue renders: an HDRI for the reflections, a soft key from the top left,
    a top light, a rim. No floor: the objects alone, on a transparent film."""
    SC.render.film_transparent = True
    world_hdri(0.35, rot=30)
    cx, cy, cz = c
    area('key', (cx - 1.7 * s, cy - 2.0 * s, cz + 1.7 * s), (cx, cy, cz), 220 * s * s, 1.6 * s, (1.0, 0.98, 0.96))
    area('top', (cx + 0.2 * s, cy - 0.8 * s, cz + 2.4 * s), (cx, cy, cz), 35 * s * s, 2.0 * s)
    area('rim', (cx + 1.4 * s, cy + 1.4 * s, cz + 1.2 * s), (cx, cy, cz), 140 * s * s, 0.4 * s, (1, 1, 1), 'RECTANGLE', 2.4 * s)
    flags(c, s)


def shadow_pass(c=(0.0, 0.0, 0.0), s=1.0, floor=0.0):
    """Second render: the objects hidden from the camera but still casting shadows, an invisible floor that keeps
    only the shadows, one soft light from straight above: a light shadow right under each object."""
    for o in list(SC.objects):
        if o.type == 'LIGHT' or o.name.startswith('drapeau'):
            remove(o)
        elif o.type in ('MESH', 'CURVE'):
            o.visible_camera = False
    w = bpy.data.worlds.new('noir'); w.use_nodes = True    # no ambient light: only the light from above makes the shadows,
    next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND').inputs['Strength'].default_value = 0.0
    SC.world = w                                        # (the studio HDRI left a faint grey veil on the whole floor)
    cx, cy, cz = c
    k = 1.5 * s                                         # only around the objects
    me = bpy.data.meshes.new('sol')
    me.from_pydata([(cx - k, cy - k, floor), (cx + k, cy - k, floor), (cx + k, cy + k, floor), (cx - k, cy + k, floor)], [], [(0, 1, 2, 3)])
    fl = link(bpy.data.objects.new('sol', me)); fl.is_shadow_catcher = True
    sun = bpy.data.lights.new('ombre', 'SUN')           # straight down, soft: the shadow falls only right under each object
    sun.energy = 3.0; sun.angle = math.radians(28)
    link(bpy.data.objects.new('ombre', sun))


def story():
    setup_render(RES, (9, 16))


# ------------------------------------------------------------------ scenes
def S1():   # the bars standing in an arc (their coloured end caps on top), the plates floating above them
    r = 0.55
    for i, c in enumerate(COLS):
        a = math.radians(-38 + 76 * i / 7)
        b = bar(c, 'A', 'r%d' % i)
        b.location = (r * math.sin(a), r * math.cos(a) - r, 0.0)
        b.rotation_euler = Matrix(((0, 1, 0), (0, 0, 1), (1, 0, 0))).to_euler()    # axis up, the engraving reads from the camera
    for i, c in enumerate(COLS):
        pose(plate(c, name='d%d' % i), (-0.28 + 0.08 * i, 0.72 + 0.018 * (i % 2), 1.31 + 0.012 * (i % 2)), (-30, 0, -40))
    story()
    camera((0.0, -1.3, 2.45), (0.0, 0.2, 1.32), lens=40, fstop=11, focus=(0.0, 0.0, 1.15))
    return (0.0, 0.2, 1.3), 1.1, None                 # no shadow: the floor is far below the frame


def S2a():  # the dumbbells floating in a grid, the plate-loaded ones below
    for i, c in enumerate(COLS):
        r, k = divmod(i, 2)
        pose(round_db(c, 15, 'h%d' % i), (-0.2 + 0.4 * k, 0.66 - 0.185 * r, DB2[15][0] + LIFT), (0, 0, -8))
    for i, c in enumerate(('noir', 'rose')):
        e = loaded(c, 'hd%d' % i)
        pose(e, (0.0, -0.22 - 0.38 * i, e['R'] + LIFT), (0, 0, -8))
    story()
    camera((0.45, -3.0, 3.75), (0.0, 0.12, 0.16), lens=70, fstop=16)
    return (0.0, 0.1, 0.2), 1.3, 0.0


def S2b():  # the dumbbells in a floating cascade, the plate-loaded ones below
    random.seed(11)
    for i, c in enumerate(COLS):
        a, b_ = jitter(2, 14)
        x = 0.17 * (1 if i % 2 else -1)
        pose(round_db(c, 15, 'h%d' % i), (x, 0.06 * (i % 2), 0.72 + 0.135 * (7 - i)), (a, b_, -22 + (8 if i % 2 else -8)))
    for i, c in enumerate(('noir', 'rose')):
        e = loaded(c, 'hd%d' % i)
        pose(e, (-0.02 + 0.06 * i, -0.05 - 0.34 * i, e['R'] + LIFT + 0.02 * i), (0, 0, -18))
    story()
    camera((0.55, -3.9, 1.97), (0.0, 0.0, 0.93), lens=62, fstop=16)
    return (0.0, 0.0, 0.8), 1.3, 0.0


def S3a():  # the 25 mm plates in a row, the clips in two rows below, all floating
    for i, c in enumerate(COLS):
        e = vplate(c, 2.5, 'v%d' % i)
        pose(e, (-0.31 + 0.088 * i, 0.30 + 0.015 * (i % 2), e['R'] + LIFT), (0, 0, 54))
    for i, c in enumerate(COLS):
        r, k = divmod(i, 4)
        pose(clip(c, 'p%d' % i), (-0.24 + 0.175 * k + 0.06 * r, -0.12 - 0.19 * r, GROUND + LIFT * 0.6), (0, 0, -30))
    story()
    camera((0.42, -2.45, 2.45), (0.02, 0.2, 0.14), lens=74, fstop=16)
    return (0.0, 0.1, 0.12), 0.9, 0.0


def S3b():  # the 25 mm plates in a floating column, the clips on both sides
    random.seed(5)
    for i, c in enumerate(COLS):
        a, b_ = jitter(2, 6)
        e = vplate(c, 2.5, 'v%d' % i)
        pose(e, (0.0, 0.0, 0.58 + 0.11 * i), (a, 90 + b_, 30 + 12 * i))
    for i, c in enumerate(COLS):
        side = -1 if i % 2 == 0 else 1
        pose(clip(c, 'p%d' % i), (side * 0.30, 0.0, 0.62 + 0.11 * i), (62, 0, -20 + (0 if side > 0 else 180)))
    story()
    camera((0.55, -2.9, 1.6), (0.0, 0.0, 0.98), lens=76, fstop=16)
    return (0.0, 0.0, 0.95), 1.0, 0.38


SCENE_FN = {k: globals()[k] for k in ('S1', 'S2a', 'S2b', 'S3a', 'S3b')}

for sc in SCENES:
    reset()
    for w in list(bpy.data.worlds):
        bpy.data.worlds.remove(w)
    for cl in list(bpy.data.collections):
        bpy.data.collections.remove(cl)
    random.seed(7)
    c, k, floor = SCENE_FN[sc]()
    catalogue_light(c, k)
    render(os.path.join(OUT, f'story-{sc}.png'))
    if floor is not None:
        shadow_pass(c, k, floor)
        render(os.path.join(OUT, f'story-{sc}-ombre.png'))
