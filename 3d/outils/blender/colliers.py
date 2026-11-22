# Step 7 (21/11/2026): the two collars reworked from the user's references (3d/references/colliers/).
# pince  = the spring clip: chrome wire, two tight turns, flat black sleeves (open square end, rounded tip).
# levier = the quick-release lever collar: two lobed C jaws hinged at the bottom, rubber lining,
#          a three-knuckle hinge on top, a curved lever with a grid pad, black cross-head screws.
# The colour (sleeves, plastic) is a setting (3d/charte.md). Reuses barre.py, poids3.py, poids2.py and base.py.
# usage: Blender -b --factory-startup -P colliers.py -- piece=pince|levier plans=paire,macro couleur=noir res=1400 samples=128 out=<dir>
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
    m = mat(name, tuple(x * 0.92 for x in c) if colour != 'noir' else (0.008, 0.008, 0.009), rough=0.44, spec=0.36, grain=0.12, grain_scale=3000)
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
        o.location = loc; o.rotation_euler = rot; o.visible_camera = False


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
def sleeve(name, E, h, xc, m, L=0.075, w=0.026, t=0.0105, twist=0.0):
    """Flat sleeve: open rectangular end at E, rounded tip, broad faces perpendicular to the coil plane.
    Local axes: X = thickness (in the coil plane), Y = along the sleeve (h), Z = width (world X)."""
    out = [(0.0, -w / 2), (L - w / 2, -w / 2)] + [((L - w / 2) + (w / 2) * math.cos(a), (w / 2) * math.sin(a))
                                                  for a in [math.radians(-90 + 180 * i / 24) for i in range(1, 24)]] + [(L - w / 2, w / 2), (0.0, w / 2)]
    o = fix_normals(prism(name, out, -t / 2, t / 2, m, axis='X'))
    hy, hz = h
    v = Vector((0.0, -hz, hy))               # in the coil plane, perpendicular to the sleeve
    d = Vector((0.0, hy, hz))
    mtx = Matrix((v, d, Vector((-1.0, 0.0, 0.0)))).transposed().to_4x4()
    mtx.translation = Vector((xc, E[1], E[2]))
    mtx = mtx @ Matrix.Rotation(twist, 4, 'Y')       # the sleeve turned a little on its own axis
    o.matrix_world = mtx
    cav = box(name + '_creux', (t - 0.0026, 0.04, w - 0.0026), (0, 0, 0), m)
    cav.matrix_world = mtx @ Matrix.Translation((0.0, 0.019 - 0.0011, 0.0))
    boolean(o, cav)
    bevel(o, 0.0011, segs=3, angle=35)
    o = bake(o, 35)
    remove(cav)
    return o


def bez(a, c, b, n=10):
    return [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b) for t in [i / n for i in range(1, n + 1)]]


def pince2(M, colour='noir', name='pince'):
    rw = 0.0024
    rc = 0.0255 + rw + 0.0003
    pitch = 2 * rw + 0.0002
    th0, span = math.radians(185), math.radians(615)
    xs = pitch * span / (2 * math.pi)
    n = 150
    coil = []
    for i in range(n + 1):
        th = th0 + span * i / n
        coil.append(Vector((-xs / 2 + xs * i / n, rc * math.cos(th), rc * math.sin(th))))
    th1 = th0 + span
    # leg 1 leaves the front end (going backwards round the coil), leg 2 the back end
    e1 = Vector((0.0, math.sin(th0), -math.cos(th0)))
    e2 = Vector((0.0, -math.sin(th1), math.cos(th1)))
    h1 = Vector((0.0, math.cos(math.radians(192)), math.sin(math.radians(192))))   # front end, left side: goes left
    h2 = Vector((0.0, math.cos(math.radians(122)), math.sin(math.radians(122))))   # back end, top: goes up-left
    sl = plastic(colour, 'gaine')
    parts = []
    legs = []
    for P0, e, h in ((coil[0], e1, h1), (coil[-1], e2, h2)):
        a = P0 + e * 0.004
        c = a + e * 0.007
        b = c + h * 0.007
        E = b + h * 0.006
        legs.append(([tuple(P0 + e * 0.002), tuple(a)] + bez(a, c, b) + [tuple(E), tuple(E + h * 0.016)], E, h, P0.x))
    path = list(reversed(legs[0][0])) + [tuple(p) for p in coil] + legs[1][0]
    parts.append(wire(name + '_fil', path, rw, M['chrome']))
    for k, (_, E, h, xc) in enumerate(legs):
        parts.append(sleeve(f'{name}_gaine{k}', E, (h.y, h.z), xc, sl, twist=math.radians(64)))
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
                a = pince2(M, COLOUR, 'pa'); a.location = (0.058, 0.07, 0.05); a.rotation_euler = (math.radians(-10), 0, math.radians(-104))
                b = pince2(M, COLOUR, 'pb'); b.location = (-0.045, -0.05, -0.05); b.rotation_euler = (math.radians(-10), 0, math.radians(-104))
                chrome_studio(); square()
                camera((-0.015, -0.5, 0.14), (-0.02, 0.0, 0.03), lens=66, fstop=16)
            elif plan == 'macro':
                a = pince2(M, COLOUR); a.rotation_euler = (math.radians(12), 0, math.radians(118))
                chrome_studio(); square()
                camera((0.0, -0.27, 0.06), (0.012, 0.0, 0.018), lens=80, fstop=8, focus=(0.012, -0.01, 0.02))
            elif plan == 'profil':
                a = pince2(M, COLOUR); a.rotation_euler = (math.radians(128), 0, math.radians(10))
                chrome_studio(); square()
                camera((0.0, -0.42, 0.0), (0.0, 0.0, -0.038), lens=62, fstop=16)
            elif plan == 'sur-barre':
                barre_olympique(bar_mats('B', 'noir'))
                e = disque(20, plate_mats('noir', 'moule'), name='d'); x = 0.686 + e['T'] / 2
                e.location = (x, 0, 0); e.rotation_euler = (0, 0, math.radians(90))
                c = pince2(M, COLOUR); c.location = (x + e['T'] / 2 + 0.006, 0, 0); c.rotation_euler = (0, 0, 0)
                catalog(k=1.05); flags((0.8, 0, 0)); portrait()
                camera((1.12, -0.33, 0.17), (0.8, 0.0, 0.02), lens=70, fstop=5.6, focus=(x + e['T'] / 2 + 0.01, -0.03, 0.0))
            elif plan == 'couleurs':
                for i, cname in enumerate(PALETTE):
                    c = pince2(collar_mats(cname), cname, 'k%d' % i)
                    c.location = (-0.49 + 0.15 * i, 0.0, 0.0303); c.rotation_euler = (0, 0, math.radians(90 - 20))
                light_floor(center=(0.0, 0.0, 0.04), k=1.1); flags((0, 0, 0.05), 0.9); setup_render()
                camera((0.075, -1.55, 0.5), (0.075, 0.02, 0.07), lens=45, fstop=10)
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
