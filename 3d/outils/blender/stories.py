# Instagram stories (22/11/2026): the validated models, grouped, on white, no text. 1080 x 1920 (9:16).
# The user's direction: no floor in the picture, and no shadow on a floor either (22/11). The objects are alone on
# white, lit like the models' catalogue renders (3d/modeles/2-haltere/flottant.jpg); the bars stand in an arc,
# their coloured end caps on top (3d/modeles/3-barre/couleurs-rack.jpg).
#   1  the bars in an arc at the bottom (validated), the plates above: a stack (1a), a fan (1b), the range of weights (1c);
#   2  the round dumbbells, the whole screen: a column (2a), the faces (2b), the range of weights (2c);
#   3  the plate-loaded dumbbell: the plates (3a), exploded (3b), the pair (3c), the eight colours (3d);
#   4  the 25 mm plates in a column, the clips on both sides (chosen).
# Instagram covers the top and the bottom of a story (profile, reply bar): the models stay in the middle.
# One transparent render per story (story-X.png); outils/stories.py puts it on white.
# usage: Blender -b --factory-startup -P stories.py -- scenes=1a,2b res=1440 samples=128 out=<dir>
import os, random
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_HALTERES = True
exec(open(os.path.join(HERE, 'halteres.py')).read())

SCENES = ARGS.get('scenes', '1a').split(',')
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


# ------------------------------------------------------------------ light: isolated objects, no floor, no shadow
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


def catalogue_light(c=(0.0, 0.0, 0.0), s=1.0, side=None):
    """The light of the models' catalogue renders: an HDRI for the reflections, a soft key from the top left,
    a top light, a rim. No floor: the objects alone, on a transparent film."""
    SC.render.film_transparent = True
    world_hdri(0.35, rot=30)
    cx, cy, cz = c
    kx = 1.7 if side == 'droite' else -1.7               # the key on the side the faces are turned to
    area('key', (cx + kx * s, cy - 2.0 * s, cz + 1.7 * s), (cx, cy, cz), 220 * s * s, 1.6 * s, (1.0, 0.98, 0.96))
    area('top', (cx + 0.2 * s, cy - 0.8 * s, cz + 2.4 * s), (cx, cy, cz), 35 * s * s, 2.0 * s)
    area('rim', (cx + 1.4 * s, cy + 1.4 * s, cz + 1.2 * s), (cx, cy, cz), 140 * s * s, 0.4 * s, (1, 1, 1), 'RECTANGLE', 2.4 * s)
    flags(c, s)


def story():
    setup_render(RES, (9, 16))


# ------------------------------------------------------------------ scenes
# 1 the bars in an arc (validated) and the plates above them: a stack, a fan, the range of weights
def bars_arc():
    """The eight bars standing in an arc, their coloured end caps on top (validated by the user, 22/11)."""
    r = 0.55
    for i, c in enumerate(COLS):
        a = math.radians(-38 + 76 * i / 7)
        b = bar(c, 'A', 'r%d' % i)
        b.location = (r * math.sin(a), r * math.cos(a) - r, 0.0)
        b.rotation_euler = Matrix(((0, 1, 0), (0, 0, 1), (1, 0, 0))).to_euler()    # axis up, the engraving reads from the camera


def bars_camera():
    story()
    camera((0.0, -1.3, 2.45), (0.0, 0.2, 1.32), lens=40, fstop=11, focus=(0.0, 0.0, 1.15))
    return (0.0, 0.2, 1.3), 1.1, None                 # no shadow: the floor is far below the frame


def s1a():  # a stack of plates, each turned a little so the numbers fan out
    bars_arc()
    z = 1.17
    for i, c in enumerate(COLS):
        e = plate(c, name='d%d' % i)
        e.location = (0.0, 0.78, 0.0)
        lie_flat(e, z + e['T'] / 2, -60 + 11 * i)
        z += e['T'] + 0.002
    return bars_camera()


def s1b():  # a fan, like a colour swatch, above the arc of bars
    bars_arc()
    pivot = Vector((0.0, 0.8, 1.02))
    for i, c in enumerate(COLS):
        th = -42 + 12 * i
        e = plate(c, name='d%d' % i)
        e.matrix_world = (Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(-24), 4, 'X')
                          @ Matrix.Rotation(math.radians(th), 4, 'Y') @ Matrix.Translation((0.0, -0.016 * i, 0.47)))
    return bars_camera()


def s1c():  # the range of weights in a pyramid: 25 kg at the bottom up to 1.25 kg, one colour each
    bars_arc()
    z = 1.18
    for i, (w, c) in enumerate(((25, 'noir'), (20, 'blanc'), (15, 'rose'), (10, 'bleu'), (5, 'vert'), (2.5, 'rouge'), (1.25, 'sable'))):
        e = plate(c, w, name='d%d' % i)
        e.location = (0.0, 0.78, 0.0)
        lie_flat(e, z + e['T'] / 2, -50 + 17 * i)
        z += e['T'] + 0.002
    return bars_camera()


def sbarres():  # the bars alone (the bottom layer of story 1d)
    bars_arc()
    return bars_camera()


def s1d():  # the plates standing in a straight row, all turned the same way, a little air between them
    # (the user's reference: the step-8 colour row, more turned and closer); rendered with its own camera, nearly
    # level with the plates, then laid over the bars (sbarres): no floor, no shadow, so the two layers match.
    yaw = float(ARGS.get('yaw', 80))                    # 22/11: 74, then 'a bit more to the left'
    roll = float(ARGS.get('roll', 0))                   # leaning the plates' tops (negative: to the left)
    p = 0.45 * abs(math.cos(math.radians(yaw))) + 0.058 * abs(math.sin(math.radians(yaw)))   # width of a plate seen from the front
    step = p * float(ARGS.get('gap', 1.13))                 # a small gap between the plates
    for i, c in enumerate(COLS):
        e = plate(c, name='d%d' % i)                     # the face turned to the right, the rim seen on the left (the reference)
        e.matrix_world = Matrix.Translation(((i - 3.5) * step, 0.0, 0.0)) @ Matrix.Rotation(math.radians(roll), 4, 'Y') @ Matrix.Rotation(math.radians(yaw), 4, 'Z')
    story()
    width = 8 * step / 0.86                                  # the row fills 86 % of the width
    dist = width / 2 / (10.125 / 135)                         # lens 135 (a flat perspective), the width of a 9:16 sensor is 36 x 9 / 16 mm
    el = math.radians(7)
    camera((0.0, -dist * math.cos(el), dist * math.sin(el)), (0.0, 0.0, 0.0), lens=135, fstop=32, shift_y=-0.08)
    return (0.0, 0.0, 0.0), 1.0, ('droite' if yaw > 0 else None)      # the key on the side the faces are turned to


# 2 the round dumbbells, the whole screen: a column, the faces, the range of weights
def s2a():  # one aligned column, the eight colours
    for i, c in enumerate(COLS):
        pose(round_db(c, 25, 'h%d' % i), (0.0, 0.0, 0.32 + 0.19 * (7 - i)), (0, 0, -24))
    story()
    camera((0.45, -3.9, 1.5), (0.0, 0.0, 0.98), lens=70, fstop=16)
    return (0.0, 0.0, 1.0), 1.2, 0.12


def s2b():  # the faces turned towards the camera, in a grid: the medallion and "15 KG"
    for i, c in enumerate(COLS):
        r, k = divmod(i, 2)
        pose(round_db(c, 15, 'h%d' % i), (-0.13 + 0.26 * k, 0.04 * k, 0.30 + 0.225 * (3 - r)), (0, 0, 62 if k else 118))
    story()
    camera((0.0, -2.35, 0.98), (0.0, 0.0, 0.66), lens=72, fstop=16)
    return (0.0, 0.0, 0.66), 0.9, 0.12


def s2c():  # the range of weights, from 5 to 40 kg, the small ones on top
    z = 0.14
    for i, (w, c) in enumerate(((40, 'noir'), (30, 'graphite'), (25, 'bleu'), (15, 'rose'), (5, 'sable'))):
        R = DB2[w][0]
        z += R
        pose(round_db(c, w, 'h%d' % i), (0.0, 0.0, z), (0, 0, -24))
        z += R + 0.07
    story()
    camera((0.45, -3.4, 1.15), (0.0, 0.0, 0.70), lens=84, fstop=16)
    return (0.0, 0.0, 0.70), 1.2, 0.04


# 3 the plate-loaded dumbbell: the plates, exploded, the pair, the eight colours
def s3a():  # the three plates, 5 kg at the bottom, 1.25 kg on top
    z = 0.12
    for i, (w, rz) in enumerate(((5, 62), (2.5, 70), (1.25, 78))):
        e = vplate('noir', w, 'v%d' % i)
        z += e['R']
        pose(e, (0.02 * i, 0.0, z), (0, 0, rz))
        z += e['R'] + 0.10
    story()
    camera((0.35, -2.6, 1.02), (0.0, 0.0, 0.54), lens=80, fstop=16)
    return (0.0, 0.0, 0.52), 0.9, 0.0


def s3b():  # exploded along its axis, standing up: the handle, three plates each side, the clips
    MP, MC = plate_mats_v('noir'), collar_mats('noir')
    parts = [poignee(handle_mats('B'), 'pe')]
    for sg in (-1, 1):
        x = GRIP / 2 + COL_W + 0.09
        for i, w in enumerate(SET):
            T = VINYL[w][1]
            p = vinyl_plate(w, MP, f'e{sg}{i}'); p.location = (sg * (x + T / 2), 0, 0)
            p.rotation_euler = (math.radians(11 * i + (0 if sg > 0 else 7)), 0, 0)
            parts.append(p)
            x += T + 0.09
        c = pince3(MC, 'noir', f'ep{sg}')
        c.matrix_world = (Matrix.Translation((sg * (x + 0.05), 0, 0)) @ Matrix.Rotation(math.radians(35 * sg), 4, 'X')
                          @ Matrix.Rotation(math.radians(90 * sg), 4, 'Y') @ Matrix.Scale(CLIP_S, 4))
        parts.append(c)
    g = group('eclate', parts)
    g.matrix_world = (Matrix.Translation((0, 0, 0.95)) @ Matrix.Rotation(math.radians(-30), 4, 'Y') @ Matrix.Rotation(math.radians(20), 4, 'X')
                      @ Matrix.Rotation(math.radians(-90), 4, 'Y'))        # the axis on a diagonal, leaning towards the camera: the plates show their faces
    story()
    camera((0.3, -3.0, 1.35), (0.0, 0.0, 0.95), lens=56, fstop=16)
    return (0.0, 0.0, 0.95), 1.1, 0.25


def s3c():  # the pair, floating like the models' catalogue render
    a = loaded('noir', 'ha'); pose(a, (0.08, 0.35, 0.98), (4, -6, -28))
    b = loaded('noir', 'hb'); pose(b, (-0.05, -0.25, 0.42), (-5, 4, 152))
    story()
    camera((0.15, -3.1, 1.2), (0.0, 0.0, 0.7), lens=62, fstop=16)
    return (0.0, 0.0, 0.7), 1.0, 0.12


def s3d():  # the whole dumbbell in the eight colours, two columns
    for i, c in enumerate(COLS):
        r, k = divmod(i, 2)
        e = loaded(c, 'h%d' % i)
        pose(e, (-0.29 + 0.58 * k, 0.05 * k, 0.30 + 0.36 * (3 - r)), (0, 0, -22))
    story()
    camera((0.3, -3.9, 1.5), (0.0, 0.0, 0.86), lens=62, fstop=16)
    return (0.0, 0.0, 0.86), 1.3, 0.0


# 4 the 25 mm plates in a floating column, the clips on both sides (chosen by the user, 22/11)
def s4():
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


SCENE_FN = {k: globals()['s' + k] for k in ('1a', '1b', '1c', '1d', 'barres', '2a', '2b', '2c', '3a', '3b', '3c', '3d', '4')}

for sc in SCENES:
    reset()
    for w in list(bpy.data.worlds):
        bpy.data.worlds.remove(w)
    for cl in list(bpy.data.collections):
        bpy.data.collections.remove(cl)
    random.seed(7)
    c, k, side = SCENE_FN[sc]()
    catalogue_light(c, k, side)
    render(os.path.join(OUT, f'story-{sc}.png'))
