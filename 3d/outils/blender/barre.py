# Step 6 (21/11/2026): the Olympic bar and the collars, following 3d/charte.md (Archivo Expanded, the 8 colours,
# the moulded black plates). Reuses poids2.py / poids3.py (plates, materials, studio HDRI, shots helpers).
# Bar finishes: A black and steel, B all steel, C all black. The colour (ID ring and end cap) is a setting.
# The collar is the spring clip of colliers.py (box() and wire() below are its building blocks).
# usage: Blender -b --factory-startup -P barre.py -- piece=barre|couleur variantes=B plans=entiere,manchon res=1400 samples=110 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_P3 = True
exec(open(os.path.join(HERE, 'poids3.py')).read())

PIECE = ARGS.get('piece', 'barre')
VARS = ARGS.get('variantes', 'A').split(',')
PLANS = ARGS.get('plans', 'entiere').split(',')
COLOUR = ARGS.get('couleur', 'noir')


def lin(name):
    return srgb(PALETTE[name][0])


def text_colour(name):
    return WHITE if PALETTE[name][1] == 'w' else CHARCOAL


# ------------------------------------------------------------------ bar materials
FINITIONS = {
    # shaft, sleeve, inner collar
    'A': dict(arbre='noir', manchon='chrome', bague_arret='chrome'),
    'B': dict(arbre='chrome', manchon='chrome', bague_arret='chrome'),
    'C': dict(arbre='noir', manchon='noir', bague_arret='noir'),
}


def bar_mats(fin='A', colour='noir', femme=False):
    f = FINITIONS[fin]
    M = {}
    bands = [(0.0, 0.06), (0.215, 0.4025), (0.4075, 0.4525), (0.4575, 0.625)] if not femme else [(0.215, 0.4025), (0.4075, 0.4525), (0.4575, 0.625)]
    if f['arbre'] == 'noir':     # black cerakote: a ceramic satin coat, not a metal
        M['arbre'] = mat_knurl('arbre', (0.03, 0.03, 0.033), 0.42, 0.0, 1.31, bands=bands, depth=0.7)
    else:                        # satin hard chrome
        M['arbre'] = mat_knurl('arbre', (0.75, 0.75, 0.77), 0.2, 1.0, 1.31, bands=bands, depth=0.7)
    M['chrome'] = metal('chrome', (0.86, 0.86, 0.88), 'X', rough=0.12)
    M['noir_m'] = metal('noir_m', (0.06, 0.06, 0.065), 'X', rough=0.2)
    M['manchon'] = M['chrome'] if f['manchon'] == 'chrome' else M['noir_m']
    M['arret'] = M['chrome'] if f['bague_arret'] == 'chrome' else M['noir_m']
    c = lin(colour)
    M['bague_id'] = mat('bague_id', c, rough=0.3, metal=1.0 if colour != 'noir' else 0.6)
    M['embout'] = mat('embout', c, rough=0.35, metal=0.5)
    M['texte'] = mat('texte', text_colour(colour), rough=0.5)
    return M


def barre_olympique(M, femme=False, name='barre'):
    """Men's 20 kg: 2.20 m, shaft 28 mm, 1310 mm between the inner collars, sleeves 50 mm x 415 mm.
    Women's 15 kg: 2.01 m, shaft 25 mm, sleeves 320 mm, no centre knurl. Axis X, centred on the origin."""
    parts = []
    rs = 0.0125 if femme else 0.014
    sl = 0.32 if femme else 0.415
    parts.append(fix_normals(lathe(name + '_arbre', round_poly([(0.0, -0.656), (rs, -0.656), (rs, 0.656), (0.0, 0.656)], [0, 0.0006, 0.0006, 0], segs=2),
                                   M['arbre'], segs=64, axis='X')))
    for sg in (-1, 1):
        # ID ring, on the shaft side of the inner collar
        pr = round_poly([(0.0, 0.645), (0.0215, 0.645), (0.0215, 0.656), (0.0, 0.656)], [0, 0.0006, 0.0006, 0], segs=2)
        parts.append(sharp(fix_normals(lathe(name + '_bague', [(r, sg * h) for r, h in pr], M['bague_id'], segs=96, axis='X')), 30))
        # inner collar: a thick polished disc with chamfers
        pr = round_poly([(0.0, 0.655), (0.0305, 0.655), (0.0305, 0.685), (0.0, 0.685)], [0, 0.0018, 0.0018, 0], segs=3)
        parts.append(sharp(fix_normals(lathe(name + '_arret', [(r, sg * h) for r, h in pr], M['arret'], segs=128, axis='X')), 30))
        # sleeve: dust seal, two fine grooves, chamfered end with a recess for the end cap
        x0, x1 = 0.685, 0.685 + sl
        rv = 0.025
        pts = [(0.0, x0), (0.0215, x0), (0.0215, x0 + 0.004), (rv, x0 + 0.004)]
        for gx in (x0 + 0.03, x0 + 0.036):
            pts += [(rv, gx - 0.0006), (rv - 0.0005, gx), (rv, gx + 0.0006)]
        pts += [(rv, x1 - 0.002), (rv - 0.002, x1), (0.0195, x1), (0.0195, x1 - 0.002), (0.0, x1 - 0.002)]
        rad = [0] * len(pts)
        o = sharp(fix_normals(lathe(name + '_manchon', [(r, sg * h) for r, h in pts], M['manchon'], segs=128, axis='X')), 25)
        parts.append(o)
        # end cap: a coloured disc in the recess, the weight engraved in it
        pr = round_poly([(0.0, x1 - 0.0021), (0.0188, x1 - 0.0021), (0.0188, x1 - 0.0006), (0.0, x1 - 0.0006)], [0, 0.0004, 0.0006, 0], segs=2)
        parts.append(sharp(fix_normals(lathe(name + '_embout', [(r, sg * h) for r, h in pr], M['embout'], segs=96, axis='X')), 30))
        fx = sg * (x1 - 0.0006 + 0.00012)
        right = (0, 1, 0) if sg > 0 else (0, -1, 0)
        for body, font, hh, zc in (('15' if femme else '20', F_BIG, 0.0085, 0.0028), ('KG', F_SMALL, 0.0028, -0.0068)):
            t = text_mesh(name + '_t', body, 0.01, 0.0001, M['texte'], font=font, fit_h=hh, max_w=0.03, spacing=1.0 if body != 'KG' else 1.35)
            place(t, (fx, 0, zc), right, (0, 0, 1))
            parts.append(t)
    e = group(name, parts)
    e['sleeve'] = (0.685, 0.685 + sl)
    return e


# ------------------------------------------------------------------ building blocks of the clip
def box(name, size, loc, m, bev=0.0):
    """A block (rounded edges if bev > 0)."""
    sx, sy, sz = (v / 2 for v in size)
    verts = [(x * sx, y * sy, z * sz) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    o = fix_normals(mesh_obj(name, verts, faces, m, smooth=False))
    o.location = loc
    if bev:
        bevel(o, bev, segs=3, angle=30)
        o = bake(o, 35)
    return o


def wire(name, pts, r, m):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (*p, 1)
    cu.bevel_depth = r; cu.bevel_resolution = 4; cu.use_fill_caps = True
    tmp = link(bpy.data.objects.new(name + '_c', cu))
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    remove(tmp)
    o = link(bpy.data.objects.new(name, me)); me.materials.append(m)
    for f in me.polygons:
        f.use_smooth = True
    return o


# ------------------------------------------------------------------ shots
def floor_or_catalog(catalogue, center=(0, 0, 0.2), k=1.0):
    if catalogue:
        catalog(k=k)
    else:
        light_floor(center=center, k=k)


def load_bar(Mb, plates_colour, collar=None, femme=False, y=0.0, plates=(20, 10)):
    """A loaded bar lying on the floor: 20 + 10 kg each side. collar(name, sign, x) places a collar against
    the last plate (colliers.py gives the clip)."""
    R0 = 0.225
    b = barre_olympique(Mb, femme)
    b.location = (0, y, R0)
    for sg in (-1, 1):
        x = 0.685 + 0.001
        for i, w in enumerate(plates):
            e = disque(w, plate_mats(plates_colour, 'moule'), name='c%d%d' % (sg, i))
            x += e['T'] / 2
            e.location = (sg * x, y, R0)
            e.rotation_euler = (0, 0, math.radians(90))
            x += e['T'] / 2 + 0.001
        if collar:
            collar('col%d' % sg, sg, x)
    return b


def wide():
    setup_render(RES, (16, 9))


def bar_shot(plan, fin):
    tag = fin
    Mb = bar_mats(fin, COLOUR)
    if plan == 'entiere':
        b = barre_olympique(Mb); b.rotation_euler = (0, 0, math.radians(-16))
        catalog(k=1.05); wide()
        camera((0.0, -2.9, 0.62), (0.0, 0.0, -0.02), lens=40, fstop=22)
    elif plan == 'manchon':
        barre_olympique(Mb)
        catalog(k=1.05); portrait()
        camera((0.97, -0.36, 0.13), (0.7, 0.0, 0.0), lens=58, fstop=6.3, focus=(0.672, -0.03, 0.0))
    elif plan == 'embout':
        barre_olympique(Mb)
        catalog(k=1.05); portrait()
        camera((1.3, -0.17, 0.07), (1.09, 0.0, 0.0), lens=95, fstop=6.3, focus=(1.1, -0.01, 0.0))
    elif plan == 'moletage':
        barre_olympique(Mb)
        raking((0.43, 0.0, 0.0), side=1, k=0.9); portrait()
        camera((0.52, -0.15, 0.06), (0.43, 0.0, 0.0), lens=100, fstop=9, focus=(0.44, -0.014, 0.0))
    elif plan == 'gamme':
        a = barre_olympique(bar_mats(fin, COLOUR), name='h'); a.location = (0, 0.07, 0)
        f = barre_olympique(bar_mats(fin, COLOUR, femme=True), femme=True, name='f'); f.location = (0, -0.07, 0)
        for o in (a, f):
            o.rotation_euler = (0, 0, math.radians(-14))
        catalog(k=1.05); wide()
        camera((0.0, -2.7, 0.9), (0.0, 0.0, -0.04), lens=40, fstop=22)
    render(os.path.join(OUT, f'barre-{tag}-{plan}.png'))


def colour_shot(plan, colour):
    if plan == 'rack':          # eight bars standing up, the coloured end caps on top
        cols = list(PALETTE)
        for i, c in enumerate(cols):
            b = barre_olympique(bar_mats('A', c), name='r%d' % i)
            ang = math.radians(-38 + 76 * i / (len(cols) - 1))
            b.location = (0.62 * math.sin(ang), 0.62 * math.cos(ang) - 0.62, 0.0)
            # bar axis up, the engraving on the top end cap reads normally from the camera
            b.rotation_euler = Matrix(((0, 1, 0), (0, 0, 1), (1, 0, 0))).to_euler()
        catalog(k=1.1); wide()
        camera((0.0, -0.88, 2.12), (0.0, -0.12, 1.07), lens=50, fstop=10, focus=(0.0, -0.08, 1.1))
    render(os.path.join(OUT, f'barre-couleur-{colour}-{plan}.png'))


for var in ([] if globals().get('AS_LIB_BARRE') else VARS):
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        SC.render.film_transparent = False
        if PIECE == 'barre':
            bar_shot(plan, var)
        else:
            colour_shot(plan, var)
