# Step 4 (21/11/2026): the plate and the round dumbbell, reworked from the user's references.
# Plate E: black, thick, raised rim, rubber collar around a big turned-steel insert, the weight in raised white
#   on the left and right (180° symmetry), "KG" tone on tone, top and bottom left empty.
# Dumbbell B2: thick round heads, smooth recessed face medallion with a raised bezel, grainy sides,
#   the weight and "KG" printed in white, satin knurled handle with steel collars.
# Variants A, B, C = the font of the numbers (Archivo Expanded, Saira Expanded, Michroma: open fonts).
# usage: Blender -b --factory-startup -P poids2.py -- piece=disque|haltere variante=A vues=face20,face25,tq res=1600 samples=96 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'base.py')).read())

PIECE = ARGS.get('piece', 'disque')
VAR = ARGS.get('variante', 'A')
VUES = ARGS.get('vues', 'face20').split(',')
POL = os.path.join(HERE, '..', 'polices')
FONTS = {'A': ('Archivo-ExpandedExtraBold.ttf', 'Archivo-ExpandedSemiBold.ttf'),
         'B': ('Saira-ExpandedBold.ttf', 'Saira-ExpandedSemiBold.ttf'),
         'C': ('Michroma-Regular.ttf', 'Michroma-Regular.ttf')}
F_BIG, F_SMALL = (os.path.join(POL, f) for f in FONTS[VAR])
BORE = 0.0254


def fix_normals(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free()
    return o


def sharp(o, angle):
    """Smooth shading, but edges sharper than the angle stay crisp (grooves, steps)."""
    for f in o.data.polygons:
        f.use_smooth = True
    try:
        o.data.set_sharp_from_angle(angle=math.radians(angle))
    except AttributeError:
        pass
    return o


def place(o, center, right, up):
    r, u = Vector(right).normalized(), Vector(up).normalized()
    m = Matrix((r, u, r.cross(u))).transposed().to_4x4()
    m.translation = Vector(center)
    o.matrix_world = m
    return o


def arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def label(w):
    return ('%g' % w).replace('.', ',')


# ------------------------------------------------------------------ materials
def mat_rubber(name, base=0.018, rough=0.6, mottle=0.25, grain=0.35, grain_scale=2600):
    """Black molded rubber: a faint mottle in the colour (like the references), fine grain."""
    m = mat(name, (base, base, base * 1.05), rough=rough, spec=0.28, grain=grain, grain_scale=grain_scale)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 22.0; nz.inputs['Detail'].default_value = 4.0
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (base * (1 - mottle), base * (1 - mottle), base * (1 - mottle) * 1.05, 1)
    cr.color_ramp.elements[1].color = (base * (1 + mottle), base * (1 + mottle), base * (1 + mottle) * 1.05, 1)
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], p.inputs['Base Color'])
    return m


def mat_stipple(name, base=0.02, rough=0.58):
    """The grainy, sand-blasted rubber of the dumbbell sides: small round bumps with tiny highlights."""
    m = mat(name, (base, base, base * 1.05), rough=rough, spec=0.5)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 1500.0
    try:
        vo.feature = 'F1'
    except Exception:
        pass
    b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = 0.8; b.inputs['Distance'].default_value = 0.0004
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    nt.links.new(vo.outputs['Distance'], b.inputs['Height'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900.0
    rr = nt.nodes.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = rough - 0.08; rr.inputs['To Max'].default_value = rough + 0.1
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], rr.inputs['Value'])
    nt.links.new(rr.outputs['Result'], p.inputs['Roughness'])
    nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def mat_turned(name, axis='Y', rough=0.3, polished=False):
    """Turned steel: anisotropic highlights that go round the axis, fine concentric lathe marks."""
    m = mat(name, (0.8, 0.8, 0.82), rough=0.07 if polished else rough, metal=1.0, aniso=0.0 if polished else 0.92)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    if polished:
        return m
    tg = nt.nodes.new('ShaderNodeTangent'); tg.direction_type = 'RADIAL'; tg.axis = axis
    nt.links.new(tg.outputs['Tangent'], p.inputs['Tangent'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    a, c = ('X', 'Z') if axis == 'Y' else ('Y', 'Z')
    def sq(o):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = 'MULTIPLY'
        nt.links.new(sep.outputs[o], n.inputs[0]); nt.links.new(sep.outputs[o], n.inputs[1]); return n
    s = nt.nodes.new('ShaderNodeMath'); s.operation = 'ADD'
    nt.links.new(sq(a).outputs[0], s.inputs[0]); nt.links.new(sq(c).outputs[0], s.inputs[1])
    r = nt.nodes.new('ShaderNodeMath'); r.operation = 'SQRT'; nt.links.new(s.outputs[0], r.inputs[0])
    k = nt.nodes.new('ShaderNodeMath'); k.operation = 'MULTIPLY'; k.inputs[1].default_value = 2 * math.pi / 0.00022
    nt.links.new(r.outputs[0], k.inputs[0])
    si = nt.nodes.new('ShaderNodeMath'); si.operation = 'SINE'; nt.links.new(k.outputs[0], si.inputs[0])
    b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = 0.08; b.inputs['Distance'].default_value = 0.0001
    nt.links.new(si.outputs[0], b.inputs['Height'])
    nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def materials():
    M = {}
    M['caoutchouc'] = mat_rubber('caoutchouc', base=0.014, rough=0.64)
    M['blanc'] = mat('blanc', (0.78, 0.78, 0.79), rough=0.55, spec=0.4)
    M['acier'] = mat_turned('acier', 'Y')
    M['poli'] = mat_turned('poli', 'Y', polished=True)
    M['grain'] = mat_stipple('grain', base=0.013, rough=0.46)
    M['lisse'] = mat('lisse', (0.014, 0.014, 0.015), rough=0.52, spec=0.38)
    M['satin'] = mat('satin', (0.72, 0.72, 0.74), rough=0.24, metal=1.0)
    M['plastique'] = mat('plastique', (0.02, 0.02, 0.022), rough=0.45)
    M['acier_x'] = mat_turned('acier_x', 'X')
    return M


# ------------------------------------------------------------------ plate E
# weight -> (diameter mm, thickness mm)
PLATE = {25: (450, 66), 20: (450, 58), 15: (450, 48), 10: (450, 38), 5: (300, 30), 2.5: (240, 24), 1.25: (200, 18)}


def text_on_face(name, body, font, h, max_w, center_xz, face_y, m, raised, front, flip):
    """Text on one face of a plate. flip = turned 180° (reads upside down)."""
    depth = raised / 2 if raised else 0.0001
    o = text_mesh(name, body, 0.05, depth, m, font=font, bevel=0.00022 if raised else 0.0, fit_h=h, max_w=max_w)
    sgn = -1 if front else 1
    y = sgn * (face_y + (depth * 0.7 if raised else 0.00015))
    x, z = center_xz
    right = Vector((1, 0, 0)) if front else Vector((-1, 0, 0))
    up = Vector((0, 0, 1))
    if flip:
        right, up = -right, -up
    if not front:
        x = -x
    place(o, (x, y, z), right, up)
    return o


def disque(w, M, name='disque', sides=True):
    D, Tmm = PLATE[w]
    R, T = D / 2000, Tmm / 1000
    s = R / 0.225
    big = D >= 450
    r_ins = 0.076 if big else max(0.048, 0.076 * s)
    r_col = r_ins + (0.016 if big else 0.012)
    r_rim = R - (0.02 if big else 0.014)
    ec, df = 0.0006, 0.0016            # collar above the rim, face below the rim
    front = [(r_ins, -(T / 2 + ec)), (r_col, -(T / 2 + ec)), (r_col + 0.0025, -(T / 2 - df))]
    if big:                             # the fine parting line around the hub (visible on the references)
        rp = 0.1
        front += [(rp - 0.0006, -(T / 2 - df)), (rp, -(T / 2 - df - 0.0004)), (rp + 0.0006, -(T / 2 - df))]
    front += [(r_rim - 0.0016, -(T / 2 - df)), (r_rim, -T / 2), (R, -T / 2)]
    back = [(r, -y) for r, y in reversed(front)]
    prof = front + back
    rad = []
    for r, y in prof:
        if abs(r - R) < 1e-6:
            rad.append(0.0045)
        elif abs(r - r_ins) < 1e-6:
            rad.append(0.0006)
        elif abs(r - r_col) < 1e-6:
            rad.append(0.0016)
        elif big and abs(r - 0.1) < 0.001:
            rad.append(0.0)
        else:
            rad.append(0.0009)
    body = sharp(fix_normals(lathe(name, round_poly(prof, rad, segs=4), M['caoutchouc'], segs=200)), 30)
    # the steel insert: turned face, two polished grooves, a chamfer into the bore
    yf = T / 2 + ec - 0.001
    g1, g2 = (0.058, 0.041) if big else (r_ins * 0.76, r_ins * 0.54)
    fr = [(r_ins - 0.0002, -yf)]
    for g in (g1, g2):
        fr += [(g + 0.0006, -yf), (g, -yf + 0.00035), (g - 0.0006, -yf)]
    fr += [(BORE + 0.0022, -yf), (BORE, -yf + 0.0022)]
    pr = fr + [(r, -y) for r, y in reversed(fr)]
    n = len(pr)
    # edges that belong to the grooves and the bore chamfer are polished (material 1)
    em = [0] * n
    half = len(fr)
    for i in range(n):
        j = i if i < half else n - 2 - i
        em[i] = 1 if j in (1, 2, 4, 5, half - 2) else 0
    ins = sharp(fix_normals(lathe(name + '_insert', pr, M['acier'], segs=200, edge_mats=em, mats=[M['acier'], M['poli']])), 12)
    parts = [body, ins]
    if sides:
        xn = 0.143 if big else (r_col + r_rim) / 2
        hn = (0.036 if big else 0.024 * max(s, 0.75))
        wmax = 0.078 if big else (r_rim - r_col) * 0.8
        for front_face in (True, False):
            for flip in (False, True):
                cx = xn if not flip else -xn
                parts.append(text_on_face(name + '_n', label(w), F_BIG, hn, wmax, (cx, 0.004 if not flip else -0.004), T / 2 - df, M['blanc'], 0.0016, front_face, flip))
                if big:
                    kz = -0.025 if not flip else 0.025
                    parts.append(text_on_face(name + '_kg', 'KG', F_SMALL, 0.0105, 0.05, (cx, kz), T / 2 - df, M['caoutchouc'], 0.0011, front_face, flip))
    e = group(name, parts)
    e['R'], e['T'] = R, T
    return e


# ------------------------------------------------------------------ bar
def barre(M):
    parts = []
    shaft = mat_knurl('arbre', (0.05, 0.05, 0.055), 0.32, 1.0, 1.31, bands=[(0.0, 0.06), (0.2, 0.62)])
    prof = round_poly([(0.0, -0.655), (0.014, -0.655), (0.014, 0.655), (0.0, 0.655)], [0, 0.001, 0.001, 0], segs=2)
    parts.append(fix_normals(lathe('arbre', prof, shaft, segs=48, axis='X')))
    for sg in (-1, 1):
        c = [(0.0, 0.0), (0.03, 0.0), (0.03, 0.028), (0.0251, 0.031), (0.0251, 0.445), (0.0, 0.445)]
        prof = round_poly(c, [0, 0.002, 0.002, 0.001, 0.0015, 0], segs=3)
        parts.append(fix_normals(lathe('manchon', [(r, sg * (0.655 + h)) for r, h in prof], M['acier_x'], segs=64, axis='X')))
    return group('barre', parts)


def collier(M, x):
    prof = round_poly([(0.0256, -0.018), (0.04, -0.018), (0.04, 0.018), (0.0256, 0.018)], [0.001, 0.004, 0.004, 0.001], segs=3)
    return fix_normals(lathe('collier', [(r, x + h) for r, h in prof], M['plastique'], segs=64, axis='X'))


# ------------------------------------------------------------------ dumbbell B2
DB2 = {5: (0.05, 0.056), 15: (0.068, 0.078), 25: (0.078, 0.09), 30: (0.083, 0.096), 40: (0.094, 0.108)}


def haltere(w, M, name='haltere'):
    R, L = DB2[w]
    G, hr = 0.132, 0.0165
    parts = []
    handle = mat_knurl('poignee', (0.72, 0.72, 0.74), 0.24, 1.0, G, bands=[(0.0, 0.055)])
    parts.append(fix_normals(lathe(name + '_poignee', [(0.0, -G / 2 - 0.03), (hr, -G / 2 - 0.03), (hr, G / 2 + 0.03), (0.0, G / 2 + 0.03)], handle, segs=48, axis='X')))
    ri, ro = 0.13 * R, 0.15 * R
    rb = 0.79 * R
    for sg in (-1, 1):
        x0 = G / 2 + 0.005
        # steel collar: a flange against the head and a short cone towards the grip
        cp = round_poly([(0.0, G / 2 - 0.002), (hr + 0.001, G / 2 - 0.002), (0.024, G / 2 + 0.0015), (0.029, G / 2 + 0.002), (0.029, x0 + 0.001), (0.0, x0 + 0.001)],
                        [0, 0.001, 0.002, 0.001, 0.001, 0], segs=3)
        parts.append(fix_normals(lathe(name + '_collerette', [(r, sg * h) for r, h in cp], M['satin'], segs=64, axis='X')))
        # head profile (r, x): inner face, rounded corners, bezel, recessed face
        pts = [(0.0, x0)]
        pts += arc(R - ri, x0 + ri, ri, -math.pi / 2, 0.0, 10)
        pts += arc(R - ro, x0 + L - ro, ro, 0.0, math.pi / 2, 12)
        b0 = len(pts) - 1
        pts += [(rb + 0.0045, x0 + L), (rb + 0.003, x0 + L + 0.0009), (rb - 0.0002, x0 + L + 0.0009), (rb - 0.0016, x0 + L - 0.0012), (0.0, x0 + L - 0.0012)]
        n = len(pts)
        em = [0] * n
        for i in range(b0 + 1, n - 1):         # bezel and face: smooth (material 1)
            em[i] = 1
        prof = [(r, sg * x) for r, x in pts]
        if sg < 0:
            prof = list(reversed(prof)); em = list(reversed(em[:-1])) + [em[-1]]
        o = sharp(fix_normals(lathe(name + '_tete', prof, M['grain'], segs=160, axis='X', edge_mats=em, mats=[M['grain'], M['lisse']])), 30)
        parts.append(o)
        # printed white number and unit on the face medallion
        fx = x0 + L - 0.0012 + 0.00012
        right = (0, 1, 0) if sg > 0 else (0, -1, 0)
        for body, font, hh, wmax, zc in ((label(w), F_BIG, 0.36 * R, 1.1 * R, 0.08 * R), ('KG', F_SMALL, 0.11 * R, 0.45 * R, -0.36 * R)):
            t = text_mesh(name + '_t', body, 0.05, 0.0001, M['blanc'], font=font, fit_h=hh, max_w=wmax, spacing=1.0 if body != 'KG' else 1.35)
            place(t, (sg * fx, 0, zc), right, (0, 0, 1))
            parts.append(t)
    return group(name, parts)


# ------------------------------------------------------------------ scenes
def catalog_lights(k=1.0, top_left=True):
    """Soft catalogue lighting on a bright environment (transparent film, the background is added later)."""
    w = bpy.data.worlds.new('w'); w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs['Color'].default_value = (1, 1, 1, 1)
    bg.inputs['Strength'].default_value = float(ARGS.get('monde', 0.07)) * k
    SC.world = w
    SC.render.film_transparent = True
    area('key', (-1.7, -2.0, 1.7), (0, 0, 0), float(ARGS.get('cle', 300)) * k, 1.6, (1.0, 0.98, 0.96))
    area('fill', (2.4, -1.4, -0.9), (0, 0, 0), 14 * k, 3.0, (0.95, 0.97, 1.0))
    area('top', (0.2, -0.8, 2.4), (0, 0, 0), 45 * k, 2.0)
    area('rim', (1.4, 1.4, 1.2), (0, 0, 0), 160 * k, 0.4, (1, 1, 1), 'RECTANGLE', 2.4)


def ortho_camera(loc, target, width, res_w, res_h):
    cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'
    cd.sensor_fit = 'HORIZONTAL'; cd.ortho_scale = width
    o = link(bpy.data.objects.new('cam', cd)); o.location = loc; aim(o, target)
    SC.camera = o
    SC.render.resolution_x, SC.render.resolution_y = res_w, res_h
    return o


def out(vue):
    return os.path.join(OUT, f'{PIECE}-{VAR}-{vue}.png')


def scene_disque(vue):
    M = materials()
    if vue in ('face20', 'face25'):
        disque(20 if vue == 'face20' else 25, M)
        catalog_lights()
        setup_render(RES, (4, 5))
        ortho_camera((0, -4, 0), (0, 0, 0), 0.5625, RES, int(RES * 5 / 4))
    elif vue == 'tq':
        e = disque(20, M)
        e.rotation_euler = (0, 0, math.radians(38))
        catalog_lights()
        setup_render(RES, (4, 5))
        camera((0.0, -1.55, 0.18), (0.0, 0, 0.0), lens=80, fstop=16)
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif vue == 'gamme':
        x = -0.62
        for i, w in enumerate((25, 20, 15, 10, 5, 2.5, 1.25)):
            e = disque(w, M, name='d%d' % i)
            e.location = (x, 0.0, e['R'])
            e.rotation_euler = (0, 0, math.radians(-36))
            x += e['T'] + 0.14
        studio(dark=False, center=(0.0, 0, 0.2), k=1.2)
        camera((0.2, -2.25, 0.62), (0.02, 0.0, 0.17), lens=50, fstop=10)
        setup_render()
    elif vue == 'barre':
        b = barre(M)
        R0 = 0.225
        b.location = (0, 0, R0)
        for sg in (-1, 1):
            x = 0.655 + 0.031 + 0.002
            for i, w in enumerate((25, 20)):
                e = disque(w, M, name='b%d%d' % (sg, i))
                x += e['T'] / 2
                e.location = (sg * x, 0, R0)
                e.rotation_euler = (0, 0, math.radians(90))
                x += e['T'] / 2 + 0.0015
            c = collier(M, sg * (x + 0.02)); c.location.z += R0
        studio(dark=False, center=(0.5, 0, 0.22), k=1.25)
        camera((2.3, -1.15, 0.62), (0.5, 0.0, 0.2), lens=40, fstop=9, focus=(0.8, 0, 0.22))
        setup_render()
    elif vue == 'sombre':
        e = disque(20, M)
        e.location = (0, 0, 0.225)
        e.rotation_euler = (0, 0, math.radians(34))
        studio(dark=True, center=(0, 0, 0.22))
        camera((-0.36, -1.32, 0.36), (0.0, 0, 0.215), lens=58, fstop=7)
        setup_render()
    render(out(vue))


def scene_haltere(vue):
    M = materials()
    M['acier'] = M['acier_x']
    def ground(w):
        return DB2[w][0]
    if vue == 'flottant':
        a = haltere(40, M, 'h1')
        a.location = (0.02, 0.18, 0.15)
        a.rotation_euler = (math.radians(-8), math.radians(4), math.radians(-28))
        b = haltere(40, M, 'h2')
        b.location = (-0.03, -0.12, -0.14)
        b.rotation_euler = (math.radians(6), math.radians(-5), math.radians(208))
        catalog_lights(k=1.05)
        setup_render(RES, (4, 5))
        camera((0.0, -1.5, 0.06), (0.0, 0.0, 0.0), lens=66, fstop=22)
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif vue == 'face':
        a = haltere(25, M, 'h1')
        a.rotation_euler = (0, 0, math.radians(-32))
        catalog_lights(k=1.05)
        setup_render(RES, (4, 5))
        camera((0.36, -0.52, 0.12), (0.12, -0.02, 0.0), lens=85, fstop=5.6, focus=(0.15, -0.08, 0.0))
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif vue == 'heros':
        a = haltere(15, M, 'h1'); a.location = (-0.11, 0.0, ground(15)); a.rotation_euler = (0, 0, math.radians(90 - 14))
        b = haltere(15, M, 'h2'); b.location = (0.12, 0.12, ground(15)); b.rotation_euler = (0, 0, math.radians(90 + 8))
        studio(dark=False, center=(0, 0.05, 0.08))
        camera((-0.42, -0.95, 0.46), (0.0, 0.04, 0.06), lens=62, fstop=6, focus=(-0.11, -0.2, 0.07))
        setup_render()
    elif vue == 'gamme':
        x = -0.3
        for i, w in enumerate((5, 15, 30)):
            o = haltere(w, M, 'g%d' % i); o.location = (x, 0.0, ground(w)); o.rotation_euler = (0, 0, math.radians(90 - 10))
            x += 0.2 + DB2[w][0] * 1.4
        studio(dark=False, center=(0.05, 0.0, 0.08), k=1.1)
        camera((0.05, -1.35, 0.52), (0.09, 0.03, 0.06), lens=52, fstop=9)
        setup_render()
    elif vue == 'sombre':
        a = haltere(15, M, 'h1'); a.location = (-0.11, 0.0, ground(15)); a.rotation_euler = (0, 0, math.radians(90 - 14))
        b = haltere(15, M, 'h2'); b.location = (0.12, 0.12, ground(15)); b.rotation_euler = (0, 0, math.radians(90 + 8))
        studio(dark=True, center=(0, 0.05, 0.08))
        camera((-0.42, -0.95, 0.46), (0.0, 0.04, 0.06), lens=62, fstop=6, focus=(-0.11, -0.2, 0.07))
        setup_render()
    render(out(vue))


for v in VUES:
    reset()
    for w in list(bpy.data.worlds):
        bpy.data.worlds.remove(w)
    SC.render.film_transparent = False
    (scene_disque if PIECE == 'disque' else scene_haltere)(v)
