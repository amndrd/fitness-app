# Weight plates and dumbbells: the first pieces of the 3D library (21/11/2026, step 2, prototypes).
# Plates: A cast iron, B rubber grip, C urethane, D bumper. Dumbbells: A hex, B round, C 12 sides.
# Everything black and sober; real sizes (Olympic bore 50 mm, 450 mm plates, 28 mm bar).
# usage: Blender -b --factory-startup -P poids.py -- piece=disques|halteres piste=A vues=heros,gamme,barre,sombre res=1920 samples=128 out=<dir>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.py')).read())

PIECE = ARGS.get('piece', 'disques')
PISTE = ARGS.get('piste', 'A')
VUES = ARGS.get('vues', 'heros').split(',')
BORE = 0.0254          # Olympic bore: 50.8 mm


def fix_normals(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()
    return o


def place(o, center, right, up):
    r, u = Vector(right).normalized(), Vector(up).normalized()
    z = r.cross(u)
    m = Matrix((r, u, z)).transposed().to_4x4()
    m.translation = Vector(center)
    o.matrix_world = m
    return o


# ------------------------------------------------------------------ materials of each piste
def materials():
    M = {}
    M['fonte'] = mat('fonte', (0.017, 0.017, 0.019), rough=0.36, coat=0.25, coat_rough=0.2, peel=0.35, peel_scale=260, grain=0.25, grain_scale=900)
    M['caoutchouc'] = mat('caoutchouc', (0.015, 0.015, 0.016), rough=0.7, spec=0.35, grain=0.55, grain_scale=2600)
    M['urethane'] = mat('urethane', (0.017, 0.017, 0.019), rough=0.34, coat=0.22, coat_rough=0.25, grain=0.08, grain_scale=3000)
    M['bumper'] = mat('bumper', (0.021, 0.021, 0.022), rough=0.86, spec=0.28, grain=0.4, grain_scale=1600)
    M['gris'] = mat('gris', (0.26, 0.26, 0.27), rough=0.55)
    M['impression'] = mat('impression', (0.5, 0.5, 0.51), rough=0.7)
    M['chrome'] = mat('chrome', (0.9, 0.9, 0.9), rough=0.1, metal=1.0)
    M['acier'] = mat('acier', (0.62, 0.62, 0.63), rough=0.26, metal=1.0, grain=0.05, grain_scale=4000)
    M['acier_noir'] = mat('acier_noir', (0.16, 0.16, 0.17), rough=0.3, metal=1.0)
    M['embout'] = mat('embout', (0.05, 0.05, 0.055), rough=0.32, metal=0.85)
    M['plastique'] = mat('plastique', (0.02, 0.02, 0.022), rough=0.45)
    return M


# ------------------------------------------------------------------ plates
# weight -> (diameter mm, thickness mm at the rim)
PLATES = {
    'A': {25: (450, 40), 20: (450, 33), 15: (400, 31), 10: (325, 28), 5: (230, 25), 2.5: (185, 20), 1.25: (160, 16)},
    'B': {25: (450, 54), 20: (450, 46), 15: (410, 42), 10: (335, 38), 5: (255, 34), 2.5: (205, 27), 1.25: (175, 22)},
    'C': {25: (450, 52), 20: (450, 44), 15: (410, 40), 10: (335, 36), 5: (255, 31), 2.5: (205, 25), 1.25: (175, 21)},
    'D': {25: (450, 78), 20: (450, 64), 15: (450, 50), 10: (450, 36), 5: (235, 24), 2.5: (200, 19), 1.25: (170, 15)},
}


def label(w):
    return ('%g' % w).replace('.', ',')


def plate_profile(R, T, Tf, Th, rh, rb, rim_w, step=0.006, soft=1.0):
    pts = [(rb, -Th / 2), (rh, -Th / 2), (rh + step, -Tf / 2), (R - rim_w - step, -Tf / 2), (R - rim_w, -T / 2), (R, -T / 2),
           (R, T / 2), (R - rim_w, T / 2), (R - rim_w - step, Tf / 2), (rh + step, Tf / 2), (rh, Th / 2), (rb, Th / 2)]
    rad = [0.0012, 0.0025, 0.004, 0.004, 0.003, 0.007 * soft, 0.007 * soft, 0.003, 0.004, 0.004, 0.0025, 0.0012]
    return round_poly(pts, rad, segs=5)


def slot_straight(theta, rc, L, w, n=10):
    c = Vector((rc * math.cos(theta), rc * math.sin(theta)))
    t = Vector((-math.sin(theta), math.cos(theta)))
    rd = Vector((math.cos(theta), math.sin(theta)))
    h = L / 2 - w / 2
    pts = []
    for s, ang0 in ((h, -math.pi / 2), (-h, math.pi / 2)):
        for i in range(n + 1):
            a = ang0 + math.pi * i / n
            q = c + t * (s + (w / 2) * math.cos(a)) + rd * ((w / 2) * math.sin(a))
            pts.append((q.x, q.y))
    return pts


def slot_arc(theta, rc, span, w, n=24, ncap=10):
    pts = []
    for i in range(n + 1):
        a = theta - span / 2 + span * i / n
        pts.append(((rc + w / 2) * math.cos(a), (rc + w / 2) * math.sin(a)))
    for side, a_end in ((1, theta + span / 2), (-1, theta - span / 2)):
        cx, cz = rc * math.cos(a_end), rc * math.sin(a_end)
        if side == 1:
            for i in range(1, ncap):
                b = a_end + math.pi * i / ncap
                pts.append((cx + (w / 2) * math.cos(b), cz + (w / 2) * math.sin(b)))
            for i in range(n + 1):
                a = theta + span / 2 - span * i / n
                pts.append(((rc - w / 2) * math.cos(a), (rc - w / 2) * math.sin(a)))
        else:
            for i in range(1, ncap):
                b = a_end + math.pi + math.pi * i / ncap
                pts.append((cx + (w / 2) * math.cos(b), cz + (w / 2) * math.sin(b)))
    return pts


def ring(name, r_in, r_out, h, m, flange=None, segs=96):
    """A hub insert along Y. flange = (r_flange, t_flange) shows on both faces."""
    if flange:
        rf, tf = flange
        pts = [(r_in, -h), (rf, -h), (rf, -h + tf), (r_out, -h + tf), (r_out, h - tf), (rf, h - tf), (rf, h), (r_in, h)]
        rad = [0.0008, 0.001, 0.0006, 0.0, 0.0, 0.0006, 0.001, 0.0008]
    else:
        pts = [(r_in, -h), (r_out, -h), (r_out, h), (r_in, h)]
        rad = [0.0008, 0.001, 0.001, 0.0008]
    return fix_normals(lathe(name, round_poly(pts, rad, segs=3), m, segs=segs))


def plate_text(name, body, size, center_xz, face_y, m, raised, front=True):
    """Text on a plate face. raised = thickness out of the face; 0 = printed/filled flush."""
    depth = raised / 2 if raised else 0.00012
    o = text_mesh(name, body, size, depth, m)
    sgn = -1 if front else 1
    y = sgn * (face_y + (depth * 0.96 if raised else 0.00025))
    x, z = center_xz
    if front:
        place(o, (x, y, z), (1, 0, 0), (0, 0, 1))
    else:
        place(o, (-x, y, z), (-1, 0, 0), (0, 0, 1))
    return o


def disque(piste, w, M, name='disque'):
    D, Tmm = PLATES[piste][w]
    R, T = D / 2000, Tmm / 1000
    s = R / 0.225
    parts = []
    big = D >= 250
    if piste == 'A':      # cast iron: raised hub and rim, recessed face, raised numbers, raw bore
        Tf, Th, rh, rim_w = T * 0.58, T * 1.04, 0.05 + 0.012 * s, 0.022 * max(s, 0.6)
        body = fix_normals(lathe(name, plate_profile(R, T, Tf, Th, rh, BORE + 0.0004, rim_w), M['fonte'], segs=160))
        rn = (rh + R - rim_w) / 2
        txt_size = 0.095 * s if big else 0.06 * s
        for front in (True, False):
            parts.append(plate_text(name + '_n', label(w), txt_size, (0, rn), Tf / 2, M['fonte'], 0.0016, front))
            if big:
                parts.append(plate_text(name + '_kg', 'KG', 0.04 * s, (0, -rn), Tf / 2, M['fonte'], 0.0016, front))
        body = bake(body)
    elif piste == 'B':    # rubber grip: three handles near the rim, chrome insert, raised numbers
        Tf, Th, rh, rim_w = T * 0.84, T * 0.92, 0.042 + 0.02 * s, (0.05 if big else 0.02) * s
        rb = 0.034
        body = fix_normals(lathe(name, plate_profile(R, T, Tf, Th, rh, rb, rim_w, step=0.008, soft=1.6), M['caoutchouc'], segs=160))
        if big:
            wslot = 0.036 * s
            rc = R - 0.044 * s - wslot / 2
            for k, th in enumerate((math.radians(30), math.radians(150), math.radians(270))):
                c = fix_normals(prism(name + '_cut%d' % k, slot_straight(th, rc, 0.13 * s, wslot), -T, T))
                boolean(body, c)
            bevel(body, 0.004 * s, segs=4, angle=35)
            body = bake(body)
            for o in [o for o in bpy.data.objects if o.name.startswith(name + '_cut')]:
                remove(o)
        else:
            body = bake(body)
        parts.append(ring(name + '_insert', BORE, rb + 0.0004, Th / 2 + 0.0008, M['chrome']))
        rn = (rh + R - rim_w) / 2 + (0.012 * s if big else 0)
        for front in (True, False):
            parts.append(plate_text(name + '_n', label(w), (0.07 if big else 0.045) * s, (0, rn), Tf / 2, M['caoutchouc'], 0.0014, front))
            if big:
                parts.append(plate_text(name + '_kg', 'KG', 0.026 * s, (0, rn - 0.045 * s), Tf / 2, M['caoutchouc'], 0.0012, front))
    elif piste == 'C':    # urethane: two curved handles, brushed steel insert with flange, engraved grey numbers
        Tf, Th, rh, rim_w = T * 0.8, T * 0.88, 0.056 + 0.014 * s, 0.026 * s
        rb = 0.036
        body = fix_normals(lathe(name, plate_profile(R, T, Tf, Th, rh, rb, rim_w, step=0.01, soft=2.2), M['urethane'], segs=160))
        if big:
            wslot = 0.032 * s
            rc = R - rim_w - 0.012 * s - wslot / 2
            for k, th in enumerate((0.0, math.pi)):
                c = fix_normals(prism(name + '_cut%d' % k, slot_arc(th, rc, math.radians(48), wslot), -T, T))
                boolean(body, c)
            bevel(body, 0.005 * s, segs=4, angle=35)
            body = bake(body)
            for o in [o for o in bpy.data.objects if o.name.startswith(name + '_cut')]:
                remove(o)
        else:
            body = bake(body)
        parts.append(ring(name + '_insert', BORE, rb + 0.0004, Th / 2 + 0.0024, M['acier'], flange=(0.05 * max(s, 0.75), 0.0024)))
        rn = (rh + R - rim_w) / 2 + 0.01 * s
        for front in (True, False):
            parts.append(plate_text(name + '_n', label(w), (0.066 if big else 0.042) * s, (0, rn), Tf / 2, M['gris'], 0, front))
            if big:
                parts.append(plate_text(name + '_kg', 'KG', 0.024 * s, (0, -rn), Tf / 2, M['gris'], 0, front))
    else:                 # D bumper: thick and flat, all the same diameter, chrome insert with flange, printed numbers
        Tf, Th, rh, rim_w = T * 0.97, T * 0.985, 0.075, 0.012
        rb = 0.045
        body = fix_normals(lathe(name, plate_profile(R, T, Tf, Th, rh, rb, rim_w, step=0.004, soft=1.4), M['bumper'], segs=160))
        body = bake(body)
        parts.append(ring(name + '_insert', BORE, rb + 0.0004, Th / 2 + 0.0015, M['chrome'], flange=(0.064 if D >= 450 else 0.054, 0.0015)))
        rn = 0.15 * s
        for front in (True, False):
            for side in (-1, 1):
                if big:
                    parts.append(plate_text(name + '_n', label(w), 0.062 * s, (side * rn, 0.008), Tf / 2, M['impression'], 0, front))
                    parts.append(plate_text(name + '_kg', 'KG', 0.02 * s, (side * rn, -0.038 * s), Tf / 2, M['impression'], 0, front))
                elif side == 1:
                    parts.append(plate_text(name + '_n', label(w), 0.04 * s, (0, 0.085 * s), Tf / 2, M['impression'], 0, front))
    e = group(name, [body] + parts)
    e['R'], e['T'] = R, T
    return e


# ------------------------------------------------------------------ bar and collars
def barre(M):
    """Olympic bar along X, 2.20 m: knurled black shaft (28 mm), steel sleeves (50 mm)."""
    parts = []
    shaft = mat_knurl('arbre', (0.05, 0.05, 0.055), 0.32, 1.0, 1.31, bands=[(0.0, 0.06), (0.2, 0.62)])
    prof = round_poly([(0.0, -0.655), (0.014, -0.655), (0.014, 0.655), (0.0, 0.655)], [0, 0.001, 0.001, 0], segs=2)
    parts.append(fix_normals(lathe('arbre', [(r, h) for r, h in prof], shaft, segs=48, axis='X')))
    for sg in (-1, 1):
        c = [(0.0, 0.0), (0.03, 0.0), (0.03, 0.028), (0.0251, 0.031), (0.0251, 0.445), (0.0, 0.445)]
        prof = round_poly(c, [0, 0.002, 0.002, 0.001, 0.0015, 0], segs=3)
        o = lathe('manchon', [(r, sg * (0.655 + h)) for r, h in prof], M['acier'], segs=64, axis='X')
        parts.append(fix_normals(o))
    return group('barre', parts)


def collier(M, x):
    prof = round_poly([(0.0256, -0.018), (0.04, -0.018), (0.04, 0.018), (0.0256, 0.018)], [0.001, 0.004, 0.004, 0.001], segs=3)
    o = fix_normals(lathe('collier', [(r, x + h) for r, h in prof], M['plastique'], segs=64, axis='X'))
    lev = box_lever(M, x)
    return [o, lev]


def box_lever(M, x):
    prof = [(-0.008, 0.035), (0.008, 0.035), (0.008, 0.058), (-0.008, 0.058)]
    o = prism('levier', round_poly(prof, 0.003, segs=3), -0.006, 0.006, M['acier_noir'], axis='Y')
    o.location = (x, 0, 0)
    o.rotation_euler = (0, 0, 0)
    return o


# ------------------------------------------------------------------ dumbbells
# weight -> head radius (m), head length (m)
DB = {5: (0.05, 0.052), 15: (0.066, 0.088), 30: (0.083, 0.118)}


def haltere(piste, w, M, name='haltere'):
    Rh, L = DB[w]
    parts = []
    G = 0.135
    hr = 0.0165
    handle_mat = M['handle_' + piste]
    prof = [(0.0, -G / 2 - 0.02), (hr, -G / 2 - 0.02), (hr, G / 2 + 0.02), (0.0, G / 2 + 0.02)]
    parts.append(fix_normals(lathe(name + '_poignee', prof, handle_mat, segs=48, axis='X')))
    x0 = G / 2 + 0.006
    for sg in (-1, 1):
        # neck ring between the grip and the head
        pr = round_poly([(0.0, 0.0), (0.024, 0.0), (0.024, 0.006), (0.0, 0.006)], [0, 0.0012, 0.0012, 0], segs=2)
        parts.append(fix_normals(lathe(name + '_bague', [(r, sg * (G / 2 + h)) for r, h in pr], M['chrome' if piste != 'C' else 'acier_noir'], segs=64, axis='X')))
        if piste == 'A':      # hexagonal rubber head
            out = regular_outline(Rh * 1.06, 6, rot=0.0)
            a0, a1 = (x0, x0 + L) if sg > 0 else (-x0 - L, -x0)
            o = fix_normals(prism(name + '_tete', out, a0, a1, M['caoutchouc'], axis='X'))
            bevel(o, 0.006, segs=4, angle=25)
            o = bake(o)
            parts.append(o)
            face_x = x0 + L
            parts += db_text(name, w, sg, face_x, Rh * 0.62, M['caoutchouc'], 0.0012)
        elif piste == 'B':    # round rubber head, soft edges, slightly domed face
            pr = [(0.0, x0), (Rh, x0), (Rh, x0 + L), (Rh * 0.45, x0 + L + 0.003), (0.0, x0 + L + 0.003)]
            pr = round_poly(pr, [0, 0.008, 0.013, 0.02, 0], segs=6)
            o = fix_normals(lathe(name + '_tete', [(r, sg * h) for r, h in pr], M['caoutchouc'], segs=96, axis='X'))
            parts.append(o)
            parts += db_text(name, w, sg, x0 + L + 0.0026, Rh * 0.6, M['caoutchouc'], 0.0012)
        else:                 # 12 sides urethane head with a dark steel end cap
            out = regular_outline(Rh * 1.02, 12, rot=math.radians(15))
            a0, a1 = (x0, x0 + L) if sg > 0 else (-x0 - L, -x0)
            o = fix_normals(prism(name + '_tete', out, a0, a1, M['urethane'], axis='X'))
            bevel(o, 0.003, segs=3, angle=25)
            o = bake(o, sharp=25)
            parts.append(o)
            capr = Rh * 0.72
            pr = round_poly([(0.0, 0.0), (capr, 0.0), (capr, 0.0035), (0.0, 0.0035)], [0, 0.0008, 0.0015, 0], segs=3)
            parts.append(fix_normals(lathe(name + '_embout', [(r, sg * (x0 + L - 0.0015 + h)) for r, h in pr], M['embout'], segs=96, axis='X')))
            parts += db_text(name, w, sg, x0 + L + 0.002, Rh * 0.55, M['gris'], 0)
    return group(name, parts)


def db_text(name, w, sg, face_x, size, m, raised):
    depth = raised / 2 if raised else 0.00012
    o = text_mesh(name + '_n', label(w), size, depth, m)
    x = sg * (face_x + (depth * 0.96 if raised else 0.00025))
    if sg > 0:
        place(o, (x, 0, 0), (0, 1, 0), (0, 0, 1))
    else:
        place(o, (x, 0, 0), (0, -1, 0), (0, 0, 1))
    return [o]


# ------------------------------------------------------------------ scenes
def out_path(vue, dark=False):
    return os.path.join(OUT, '%s-%s-%s%s.png' % (PIECE, PISTE, vue, '-sombre' if dark else ''))


def scene_disques(vue):
    M = materials()
    dark = vue == 'sombre'
    if vue in ('heros', 'sombre'):
        e = disque(PISTE, 20, M)
        e.location = (0, 0, e['R'])
        e.rotation_euler = (0, 0, math.radians(float(ARGS.get('rot', 34))))
        studio(dark=dark, center=(0, 0, 0.22))
        camera((-0.36, -1.32, 0.36), (0.0, 0, 0.215), lens=58, fstop=7)
    elif vue == 'gamme':
        x = -0.6
        for i, w in enumerate((25, 20, 15, 10, 5, 2.5, 1.25)):
            e = disque(PISTE, w, M, name='d%d' % i)
            e.location = (x, 0.0, e['R'])
            e.rotation_euler = (0, 0, math.radians(-38))
            x += e['T'] + 0.15
        studio(dark=False, center=(0.0, 0, 0.2), k=1.2)
        camera((0.25, -2.25, 0.62), (0.05, 0.0, 0.16), lens=50, fstop=10)
    elif vue == 'barre':
        b = barre(M)
        R0 = PLATES[PISTE][20][0] / 2000
        b.location = (0, 0, R0)
        load = (20, 10, 5) if PISTE != 'D' else (20, 10)
        for sg in (-1, 1):
            x = 0.655 + 0.031 + 0.002
            for i, w in enumerate(load):
                e = disque(PISTE, w, M, name='b%d%d' % (sg, i))
                x += e['T'] / 2
                e.location = (sg * x, 0, R0)
                e.rotation_euler = (0, 0, math.radians(90))
                x += e['T'] / 2 + 0.0015
            for o in collier(M, sg * (x + 0.02)):
                o.location.z += R0
        studio(dark=False, center=(0.5, 0, 0.22), k=1.25)
        camera((2.3, -1.15, 0.62), (0.5, 0.0, 0.2), lens=40, fstop=9, focus=(0.8, 0, 0.22))
    setup_render()
    render(out_path('heros' if vue == 'sombre' else vue, dark))


def scene_halteres(vue):
    M = materials()
    M['handle_A'] = mat_knurl('poignee_A', (0.86, 0.86, 0.86), 0.14, 1.0, 0.135, bands=[(0.0, 0.06)])
    M['handle_B'] = M['handle_A']
    M['handle_C'] = mat_knurl('poignee_C', (0.12, 0.12, 0.13), 0.24, 1.0, 0.135, bands=[(0.0, 0.06)])
    dark = vue == 'sombre'

    def ground(w):
        Rh, _ = DB[w]
        return {'A': Rh * 1.06 * math.cos(math.radians(30)), 'B': Rh, 'C': Rh * 1.02 * math.cos(math.radians(15))}[PISTE]

    if vue in ('heros', 'sombre'):
        a = haltere(PISTE, 15, M, 'h1')
        a.location = (-0.11, 0.0, ground(15))
        a.rotation_euler = (0, 0, math.radians(90 - 14))
        b = haltere(PISTE, 15, M, 'h2')
        b.location = (0.12, 0.12, ground(15))
        b.rotation_euler = (0, 0, math.radians(90 + 8))
        studio(dark=dark, center=(0, 0.05, 0.08))
        camera((-0.42, -0.95, 0.46), (0.0, 0.04, 0.06), lens=62, fstop=6, focus=(-0.11, -0.2, 0.07))
    elif vue == 'gamme':
        x = -0.28
        for i, w in enumerate((5, 15, 30)):
            o = haltere(PISTE, w, M, 'g%d' % i)
            o.location = (x, 0.0, ground(w))
            o.rotation_euler = (0, 0, math.radians(90 - 10))
            x += 0.2 + DB[w][0] * 1.4
        studio(dark=False, center=(0.05, 0.0, 0.08), k=1.1)
        camera((0.05, -1.35, 0.52), (0.09, 0.03, 0.06), lens=52, fstop=9)
    elif vue == 'detail':
        o = haltere(PISTE, 15, M, 'd')
        o.location = (0, 0, ground(15))
        o.rotation_euler = (0, 0, math.radians(90 - 35))
        studio(dark=False, center=(0, 0, 0.07))
        camera((-0.4, -0.5, 0.2), (-0.04, -0.07, 0.065), lens=72, fstop=4, focus=(-0.09, -0.13, 0.066))
    setup_render()
    render(out_path('heros' if vue == 'sombre' else vue, dark))


for v in VUES:
    reset()
    (scene_disques if PIECE == 'disques' else scene_halteres)(v)
