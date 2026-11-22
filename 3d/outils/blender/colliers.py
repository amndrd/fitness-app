# Step 7 (21/11/2026): the two collars reworked from the user's references (3d/references/colliers/).
# pince  = the spring clip: chrome wire, two tight turns, flat black sleeves (open square end, rounded tip).
# levier = the quick-release lever collar: two lobed C jaws hinged at the bottom, rubber lining,
#          a three-knuckle hinge on top, a curved lever with a grid pad, black cross-head screws.
# The colour (sleeves, plastic) is a setting (3d/charte.md). Reuses barre.py, poids3.py, poids2.py and base.py.
# usage: Blender -b --factory-startup -P colliers.py -- piece=pince|levier plans=paire,macro couleur=noir res=1400 samples=128 out=<dir>
# 22/11: the clip's sleeves now lie flat in the plane of the ring, as on the user's photo of the pair.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_BARRE = True
exec(open(os.path.join(HERE, 'barre.py')).read())

PIECE = ARGS.get('piece', 'pince')
PLANS = ARGS.get('plans', 'paire').split(',')
COLOUR = ARGS.get('couleur', 'noir')


# ------------------------------------------------------------------ materials
def plastic(colour, name='plastique'):
    """Satin moulded plastic (the sleeves, the collar body)."""
    c = lin(colour)
    black = (0.015, 0.015, 0.016) if name == 'gaine' else (0.008, 0.008, 0.009)   # the sleeves: a dark grey rubber, as on the photos
    m = mat(name, tuple(x * 0.92 for x in c) if colour != 'noir' else black, rough=0.5 if name == 'gaine' else 0.44, spec=0.36, grain=0.12, grain_scale=3000)
    return m


def collar_mats(colour='noir'):
    M = {}
    M['plastique'] = plastic(colour)
    M['caoutchouc'] = surface('liner', (0.008, 0.008, 0.009), 'mouchete' if False else 'moule', axis='X')
    M['vis'] = mat('vis', (0.03, 0.03, 0.032), rough=0.32, metal=0.6)
    M['chrome'] = mat('chrome_fil', (0.93, 0.93, 0.94), rough=0.045, metal=1.0)
    M['axe'] = mat('axe', (0.6, 0.6, 0.62), rough=0.25, metal=1.0)
    return M


def flags(center, d=0.6):
    """Black cards out of the frame: chrome needs dark things to reflect, like in a product photo studio."""
    blk = mat('drapeau', (0.0, 0.0, 0.0), rough=1.0, spec=0.0)
    c = Vector(center)
    for loc, rot in (((-d, 0.1, 0.05), (0, math.radians(90), 0)), ((d * 0.9, 0.25, -0.05), (0, math.radians(-90), 0)), ((0.0, 0.0, -d * 0.7), (0, 0, 0))):
        me = bpy.data.meshes.new('drapeau')
        s = 0.35
        me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
        o = link(bpy.data.objects.new('drapeau', me)); me.materials.append(blk)
        o.location = c + Vector(loc); o.rotation_euler = rot
        o.visible_camera = False


def chrome_studio(k=1.0):
    """How chrome is photographed: a white room (bright reflections) and a few black strips (the dark lines)."""
    w = bpy.data.worlds.new('w'); w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.5 * k
    SC.world = w
    SC.render.film_transparent = True
    area('key', (-0.8, -1.0, 1.0), (0, 0, 0), 60 * k, 1.2, (1.0, 0.99, 0.98))
    blk = mat('bande', (0.0, 0.0, 0.0), rough=1.0, spec=0.0)
    for loc, rot, sx, sy in (((-0.5, 0.05, 0.1), (0, math.radians(90), 0), 0.09, 0.6), ((0.45, 0.3, 0.05), (0, math.radians(-90), math.radians(20)), 0.07, 0.6),
                             ((0.0, 0.5, 0.35), (math.radians(70), 0, 0), 0.6, 0.06), ((0.05, -0.6, -0.3), (math.radians(-60), 0, 0), 0.5, 0.05),
                             ((-0.3, -0.5, 0.4), (math.radians(-50), math.radians(30), 0), 0.04, 0.4), ((0.0, 0.0, -0.45), (0, 0, 0), 0.25, 0.25)):
        me = bpy.data.meshes.new('bande')
        me.from_pydata([(-sx, -sy, 0), (sx, -sy, 0), (sx, sy, 0), (-sx, sy, 0)], [], [(0, 1, 2, 3)])
        o = link(bpy.data.objects.new('bande', me)); me.materials.append(blk)
        o.location = loc; o.rotation_euler = rot; o.visible_camera = False; o.visible_shadow = False


def shadow_floor(z):
    me = bpy.data.meshes.new('sol')
    s = 3.0
    me.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
    o = link(bpy.data.objects.new('sol', me))
    o.is_shadow_catcher = True
    return o


def softbox(k=1.0):
    world_hdri(0.05 * k, rot=30)
    SC.render.film_transparent = True
    area('dessus', (0.0, -0.1, 1.2), (0.0, 0.0, 0.0), 58 * k, 1.8, (1.0, 0.99, 0.98))
    for nm, loc, pw, sz in (('face', (-0.45, -1.1, 0.55), 16, 1.6), ('contre', (0.6, 0.8, 0.5), 22, 0.5)):
        o = area(nm, loc, (0.0, 0.0, 0.0), pw * k, sz, (1.0, 0.98, 0.96))
        o.data.use_shadow = False                    # only the top light casts the (short, soft) shadows


def square():
    setup_render(RES, (1, 1))


# ------------------------------------------------------------------ the spring clip
def sleeve(name, E, d, wdir, m, L=0.084, w=0.026, t=None):
    """Flat sleeve: open rectangular end at E, rounded tip, pointing along d, its width along wdir.
    As on the user's photos (22/11), the sleeves lie flat: the width stays in the plane of the ring.
    Local axes: X = thickness, Y = along the sleeve, Z = width."""
    t = t or P_THICK
    out = [(0.0, -w / 2), (L - w / 2, -w / 2)] + [((L - w / 2) + (w / 2) * math.cos(a), (w / 2) * math.sin(a))
                                                  for a in [math.radians(-90 + 180 * i / 24) for i in range(1, 24)]] + [(L - w / 2, w / 2), (0.0, w / 2)]
    o = fix_normals(prism(name, out, -t / 2, t / 2, m, axis='X'))
    d = d.normalized()
    wv = (wdir - d * wdir.dot(d)).normalized()
    mtx = Matrix((d.cross(wv), d, wv)).transposed().to_4x4()
    mtx.translation = Vector(E)
    o.matrix_world = mtx
    cav = box(name + '_creux', (t - 0.0026, 0.04, w - 0.0026), (0, 0, 0), m)
    cav.matrix_world = mtx @ Matrix.Translation((0.0, 0.019 - 0.0011, 0.0))
    boolean(o, cav)
    bevel(o, float(ARGS.get('arrondi', 0.0026)), segs=4, angle=35)
    o = bake(o, 35)
    remove(cav)
    return o


def bez(a, c, b, n=10):
    return [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b) for t in [i / n for i in range(1, n + 1)]]


def unit(deg):
    """A direction in the plane of the ring (YZ), by its angle."""
    return Vector((0.0, math.cos(math.radians(deg)), math.sin(math.radians(deg))))


# The geometry read on the user's photos (22/11): seen face on, the upper sleeve goes up-left at about 45°,
# the lower one goes left, so the two sleeves make a V of about 40°. Both lie flat (their width in the plane
# of the ring, not across it); the lower one is bent out of that plane, towards the back of the clip, so on
# the photo of the pair it looks shorter and shows its open end. Tuned against the photo (keys for tests).
P_UP = float(ARGS.get('haut', 141))       # upper sleeve, angle in the ring plane
P_LO = float(ARGS.get('bas', 176))        # lower sleeve, angle in the ring plane
P_TILT = float(ARGS.get('recul', 45))     # lower sleeve, bent towards the back (-X)
P_EXIT = float(ARGS.get('sortie', 124))   # where the upper leg leaves the ring
P_STUB = float(ARGS.get('tige', 121))     # the upper leg's straight stub, out of the ring (about radial)
P_START = float(ARGS.get('debut', 210))   # where the lower leg leaves the ring
P_ROLL = float(ARGS.get('vrille', 60))    # lower sleeve, turned on its own axis (the sleeve turns freely on the wire)
P_ROLL_UP = float(ARGS.get('vrille_haut', 15))  # upper sleeve, turned on its own axis
P_TILT_UP = float(ARGS.get('recul_haut', 0))    # upper sleeve, bent towards the back (-X)
P_THICK = float(ARGS.get('epaisseur', 0.013))   # sleeve thickness (26 mm wide)
P_ELEV = float(ARGS.get('elev', 30))      # the pair: how much the camera looks down (the rings lean back to face it)


def pince2(M, colour='noir', name='pince', roll=None, roll_up=None):
    """The spring clip. The sleeves turn freely on the wire: roll / roll_up turn them for a given shot."""
    roll = P_ROLL if roll is None else roll
    roll_up = P_ROLL_UP if roll_up is None else roll_up
    rw = 0.0027                     # a 5.4 mm wire: on the photos the coil looks massive
    rc = 0.0255 + rw + 0.0003
    pitch = 2 * rw + float(ARGS.get('jeu', 0.0025))     # a small gap between the two turns, as on the photos
    th0 = math.radians(P_START)
    th1 = math.radians(P_EXIT + 720)
    span = th1 - th0
    xs = pitch * span / (2 * math.pi)
    n = 160
    coil = []
    for i in range(n + 1):
        th = th0 + span * i / n
        coil.append(Vector((-xs / 2 + xs * i / n, rc * math.cos(th), rc * math.sin(th))))
    # leg 1 leaves the back end (going backwards round the coil, then an S to the left), leg 2 the front end (up)
    e1 = Vector((0.0, math.sin(th0), -math.cos(th0)))
    e2 = Vector((0.0, -math.sin(th1), math.cos(th1)))
    h1, h2 = unit(P_LO), unit(P_UP)
    t = math.radians(P_TILT)
    d1 = h1 * math.cos(t) + Vector((-1.0, 0.0, 0.0)) * math.sin(t)
    tu = math.radians(P_TILT_UP)
    d2 = h2 * math.cos(tu) + Vector((-1.0, 0.0, 0.0)) * math.sin(tu)
    sl = plastic(colour, 'gaine')
    parts = []
    legs = []
    for P0, e, d, h, runs in ((coil[0], e1, d1, h1, (0.002, 0.003, 0.005, 0.005)),
                              (coil[-1], e2, d2, h2, (0.0012, 0.0028, 0.004, 0.004))):
        r0, r1, r2, r3 = runs
        a = P0 + e * r0
        c = a + e * r1
        b = c + d * r2
        E = b + d * r3
        pts = ([tuple(P0 + e * r0 * 0.5)] if r0 > 0.002 else []) + [tuple(a)] + bez(a, c, b) + [tuple(E), tuple(E + d * 0.016)]
        if d is d2:
            # the upper leg, as on the photo: a sharp bend at the ring, a straight stub going out (about 12 mm),
            # then a soft bend into the sleeve
            s2 = unit(P_STUB)
            b1 = a + e * 0.002 + s2 * 0.003
            q = b1 + s2 * 0.0065
            E = q + s2 * 0.003 + d * 0.003
            pts = [tuple(a)] + bez(a, a + e * 0.002, b1, 6) + [tuple(q)] + bez(q, q + s2 * 0.003, E, 6) + [tuple(E + d * 0.016)]
        wv = Vector((0.0, -h.z, h.y))
        wv = Matrix.Rotation(math.radians(roll if d is d1 else roll_up), 3, d) @ wv
        legs.append((pts, E, d, wv))
    path = list(reversed(legs[0][0])) + [tuple(p) for p in coil] + legs[1][0]
    parts.append(wire(name + '_fil', path, rw, M['chrome']))
    for k, (_, E, d, wv) in enumerate(legs):
        parts.append(sleeve(f'{name}_gaine{k}', E, d, wv, sl))
    return group(name, parts)


# ------------------------------------------------------------------ the lever collar
R_IN, R_LIN = 0.0287, 0.0255          # plastic bore, rubber lining (fits the 50 mm sleeve)
W = 0.023                             # half width along the bar


def r_out(th):
    return 0.0452 + 0.0052 * math.cos(6 * (th - math.pi / 2))


def sector(a0, a1, rin, rfun, n=60):
    outer = [(rfun(a0 + (a1 - a0) * i / n) * math.cos(a0 + (a1 - a0) * i / n), rfun(a0 + (a1 - a0) * i / n) * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    inner = [(rin * math.cos(a1 + (a0 - a1) * i / n), rin * math.sin(a1 + (a0 - a1) * i / n)) for i in range(n + 1)]
    return outer + inner


def screw(name, pos, normal_x, M):
    o = fix_normals(lathe(name, round_poly([(0.0, 0.0), (0.0034, 0.0), (0.0034, 0.0007), (0.0026, 0.0012), (0.0, 0.0013)], [0, 0.0003, 0.0004, 0.0004, 0], segs=2),
                          M['vis'], segs=32, axis='X'))
    for k, (sy, sz) in enumerate(((0.0044, 0.0009), (0.0009, 0.0044))):
        cut = box(name + '_x%d' % k, (0.002, sy, sz), (0.0011, 0.0, 0.0), M['vis'])
        boolean(o, cut)
    o = bake(o, 40)
    for ob in [ob for ob in bpy.data.objects if ob.name.startswith(name + '_x')]:
        remove(ob)
    if normal_x < 0:
        o.rotation_euler = (0, 0, math.pi)
    o.location = pos
    return o


def jaw(name, a0, a1, M, screws):
    body = fix_normals(prism(name, sector(a0, a1, R_IN, r_out), -W, W, M['plastique'], axis='X'))
    bevel(body, 0.0018, segs=3, angle=30)
    body = bake(body, 30)
    liner = fix_normals(prism(name + '_liner', sector(a0 + 0.04, a1 - 0.04, R_LIN, lambda t: R_IN + 0.0003, n=40), -W + 0.0015, W - 0.0015, M['caoutchouc'], axis='X'))
    bevel(liner, 0.0008, segs=2, angle=30)
    liner = bake(liner, 30)
    parts = [body, liner]
    for th in screws:
        for sx in (-1, 1):
            parts.append(screw(name + '_vis', (sx * W, 0.038 * math.cos(th), 0.038 * math.sin(th)), sx, M))
    return parts


def cyl_x(name, r, x0, x1, pos, m, segs=32):
    o = fix_normals(lathe(name, round_poly([(0.0, x0), (r, x0), (r, x1), (0.0, x1)], [0, 0.0006, 0.0006, 0], segs=2), m, segs=segs, axis='X'))
    o.location = pos
    return o


def lever_arm(M, name):
    """The lever, built closed: a curved band following the ring from the hinge (100°) down the right side (18°),
    two arms with a window, a pad with a grid of small raised squares; the knuckle on the hinge axis."""
    m = M['plastique']
    ri, ro = 0.0518, 0.0572
    lv = fix_normals(prism(name, sector(math.radians(100), math.radians(30), ri, lambda t: ro, n=50), -W + 0.002, W - 0.002, m, axis='X'))
    win = fix_normals(prism(name + '_fen', sector(math.radians(88), math.radians(64), ri - 0.01, lambda t: ro + 0.01, n=20), -0.0085, 0.0085, m, axis='X'))
    boolean(lv, win)
    bevel(lv, 0.0016, segs=3, angle=30)
    lv = bake(lv, 30)
    remove(win)
    parts = [lv]
    # grid pad: 6 x 6 small squares on the outer face of the pad
    for i in range(6):
        th = math.radians(55 - 4.4 * i)
        for j in range(6):
            x = -0.0105 + 0.0042 * j
            sq = box(name + '_g', (0.0034, 0.0034, 0.0008), (0, 0, 0), m)
            sq.matrix_world = Matrix.Translation((x, (ro + 0.0003) * math.cos(th), (ro + 0.0003) * math.sin(th))) @ Matrix.Rotation(th - math.pi / 2, 4, 'X')
            parts.append(sq)
    # the cam bar seen through the window
    parts.append(cyl_x(name + '_came', 0.0026, -0.0085, 0.0085, (0, 0.049 * math.cos(math.radians(76)), 0.049 * math.sin(math.radians(76))), m))
    return parts


def levier2(M, ouvert=False, name='levier'):
    hinge_b = Vector((0.0, 0.044 * math.cos(math.radians(270)), 0.044 * math.sin(math.radians(270))))
    hinge_t = Vector((0.0, 0.0545 * math.cos(math.radians(104)), 0.0545 * math.sin(math.radians(104))))
    # fixed part (right, with the screws) and moving jaw (left)
    body = jaw(name + '_corps', math.radians(-87), math.radians(87), M, (math.radians(22), math.radians(-38)))
    mob = jaw(name + '_machoire', math.radians(93), math.radians(267), M, (math.radians(205), math.radians(240)))
    # bottom hinge pin, top hinge knuckles (outer ones on the jaw), the lever
    pin = cyl_x(name + '_axe_bas', 0.0042, -W - 0.0012, W + 0.0012, hinge_b, M['plastique'])
    pin_steel = cyl_x(name + '_axe_bas_acier', 0.0016, -W - 0.0018, W + 0.0018, hinge_b, M['axe'], 16)
    knuckles = [cyl_x(name + '_charniere', 0.0068, x0, x1, hinge_t, M['plastique']) for x0, x1 in ((-W + 0.002, -0.0072), (0.0072, W - 0.002))]
    lever = lever_arm(M, name + '_levier') + [cyl_x(name + '_noeud', 0.0068, -0.0066, 0.0066, hinge_t, M['plastique'])]
    gl = group(name + '_g_levier', lever)
    if ouvert:
        # the lever flips up around the top hinge, the jaw swings out around the bottom pin
        gl.matrix_world = Matrix.Translation(hinge_t) @ Matrix.Rotation(math.radians(112), 4, 'X') @ Matrix.Translation(-hinge_t)
    gj = group(name + '_g_machoire', mob + knuckles + [gl])
    if ouvert:
        gj.matrix_world = Matrix.Translation(hinge_b) @ Matrix.Rotation(math.radians(16), 4, 'X') @ Matrix.Translation(-hinge_b)
    return group(name, body + [pin, pin_steel, gj])


# ------------------------------------------------------------------ shots
def out(plan):
    return os.path.join(OUT, f'collier2-{PIECE}-{COLOUR}-{plan}.png')


# the pair, as on the user's photo: the rings face the camera (seen a little from above)
FACE = (math.radians(-10), math.radians(-P_ELEV), math.radians(float(ARGS.get('rz', -80))))


def shot():
    M = collar_mats(COLOUR)
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        SC.render.film_transparent = False
        M = collar_mats(COLOUR)
        if PIECE == 'pince':
            if plan == 'paire':
                a = pince2(M, COLOUR, 'pa'); a.location = (0.036, 0.03, 0.015); a.rotation_euler = FACE
                b = pince2(M, COLOUR, 'pb'); b.location = (-0.036, -0.03, -0.03); b.rotation_euler = FACE
                chrome_studio(float(ARGS.get('k', 1.5))); square()
                el = math.radians(P_ELEV)
                camera((-0.029, -0.43 * math.cos(el), 0.035 + 0.43 * math.sin(el)), (-0.033, 0.0, 0.035), lens=66, fstop=16)
            elif plan == 'macro':
                # seen from the back and from the left, like the user's close-up: the upper sleeve stands
                # straight up, the bent one comes towards the camera and goes off to the right
                a = pince2(M, COLOUR); a.rotation_euler = (math.radians(-47), math.radians(5), math.radians(90))
                chrome_studio(); square()
                camera((-0.13, -0.26, 0.0), (0.02, 0.0, 0.025), lens=80, fstop=11, focus=(0.0, 0.0, 0.0))
            elif plan == 'trois-quarts':
                a = pince2(M, COLOUR); a.rotation_euler = (math.radians(-10), 0, math.radians(-35))
                chrome_studio(); square()
                camera((-0.05, -0.295, 0.137), (-0.05, 0.0, 0.03), lens=66, fstop=16)
            elif plan == 'sur-barre':
                barre_olympique(bar_mats('B', 'noir'))
                e = disque(20, plate_mats('noir', 'moule'), name='d'); x = 0.686 + e['T'] / 2
                e.location = (x, 0, 0); e.rotation_euler = (0, 0, math.radians(90))
                # the bent sleeve goes away from the plate; the sleeves turned so both show their broad face (found by probing)
                c = pince2(M, COLOUR, roll=-60, roll_up=0)
                c.location = (x + e['T'] / 2 + 0.013, 0, 0)
                c.rotation_euler = (math.radians(-60), 0, math.radians(180))
                catalog(k=1.05); flags((0.8, 0, 0)); portrait()
                camera((1.12, -0.33, 0.17), (0.8, 0.0, 0.02), lens=70, fstop=5.6, focus=(x + e['T'] / 2 + 0.01, -0.03, 0.0))
            elif plan == 'couleurs':
                for i, cname in enumerate(PALETTE):
                    c = pince2(collar_mats(cname), cname, 'k%d' % i)
                    c.location = (-0.42 + 0.14 * i, 0.0, 0.0303); c.rotation_euler = FACE
                light_floor(center=(0.0, 0.0, 0.04), k=1.1); flags((0, 0, 0.05), 0.9); setup_render()
                camera((0.035, -1.55, 0.5), (0.035, 0.02, 0.07), lens=45, fstop=10)
        else:
            if plan == 'paire':
                a = levier2(M, False, 'la'); a.location = (-0.058, -0.01, 0.0); a.rotation_euler = (0, 0, math.radians(-128))
                b = levier2(M, True, 'lb'); b.location = (0.062, 0.025, 0.0); b.rotation_euler = (0, 0, math.radians(-40))
                shadow_floor(-0.0504)
                softbox(); square()
                camera((0.0, -0.46, 0.14), (0.0, 0.0, 0.018), lens=80, fstop=16)
            elif plan == 'detail':
                a = levier2(M, False); a.rotation_euler = (0, 0, math.radians(-128))
                catalog(k=1.05); square()
                camera((0.12, -0.17, 0.1), (0.0, 0.0, 0.02), lens=70, fstop=5.6, focus=(0.02, -0.03, 0.03))
            elif plan == 'sur-barre':
                barre_olympique(bar_mats('B', 'noir'))
                e = disque(20, plate_mats('noir', 'moule'), name='d'); x = 0.686 + e['T'] / 2
                e.location = (x, 0, 0); e.rotation_euler = (0, 0, math.radians(90))
                c = levier2(M); c.location = (x + e['T'] / 2 + W + 0.001, 0, 0)
                catalog(k=1.05); portrait()
                camera((1.12, -0.33, 0.17), (0.8, 0.0, 0.02), lens=70, fstop=5.6, focus=(x + e['T'] / 2 + 0.02, -0.04, 0.0))
            elif plan == 'couleurs':
                for i, cname in enumerate(PALETTE):
                    c = levier2(collar_mats(cname), False, 'k%d' % i)
                    c.location = (-0.4 + 0.114 * i, 0.0, 0.0504); c.rotation_euler = (0, 0, math.radians(90 - 24))
                light_floor(center=(0.0, 0.0, 0.04), k=1.1); setup_render()
                camera((0.02, -1.24, 0.42), (0.02, 0.02, 0.095), lens=45, fstop=10)
        render(out(plan))


shot()
