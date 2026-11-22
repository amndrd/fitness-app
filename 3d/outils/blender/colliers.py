# Step 7 (21/11/2026): the two collars reworked from the user's references (3d/references/colliers/).
# pince  = the spring clip: satin steel wire, three tight turns, two legs in a V, sleeves on edge (rounded tip, slotted end).
# levier = the quick-release lever collar: two lobed C jaws hinged at the bottom, rubber lining,
#          a three-knuckle hinge on top, a curved lever with a grid pad, black cross-head screws.
# The colour (sleeves, plastic) is a setting (3d/charte.md). Reuses barre.py, poids3.py, poids2.py and base.py.
# usage: Blender -b --factory-startup -P colliers.py -- piece=pince|levier plans=paire,macro couleur=noir res=1400 samples=128 out=<dir>
# 22/11: the clip rebuilt after the model chosen by the user (3d/recherche/6-pince-fab).
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
    black = (0.014, 0.014, 0.015) if name == 'gaine' else (0.008, 0.008, 0.009)   # the clip's sleeves: a dark grey rubber
    m = mat(name, tuple(x * 0.92 for x in c) if colour != 'noir' else black, rough=0.55 if name == 'gaine' else 0.44, spec=0.36, grain=0.12, grain_scale=3000)
    return m


def collar_mats(colour='noir'):
    M = {}
    M['plastique'] = plastic(colour)
    M['caoutchouc'] = surface('liner', (0.008, 0.008, 0.009), 'mouchete' if False else 'moule', axis='X')
    M['vis'] = mat('vis', (0.03, 0.03, 0.032), rough=0.32, metal=0.6)
    M['chrome'] = mat('chrome_fil', (0.93, 0.93, 0.94), rough=0.045, metal=1.0)
    M['acier'] = mat('acier_fil', (float(ARGS.get('acier', 0.40)),) * 2 + (float(ARGS.get('acier', 0.40)) + 0.02,), rough=float(ARGS.get('rug', 0.24)), metal=1.0)     # the clip's wire: satin steel
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
# 22/11, after the model chosen by the user (3d/recherche/6-pince-fab): the logic of the design.
# - The coil lies flat: three tight turns of a round steel wire.
# - Both ends leave the same point of the ring, tangent to it: the top turn's end goes one way, the bottom
#   turn's end the other way, each stays at its own height, then bends outwards: the two legs make a V of
#   about 50 degrees. Squeezing them opens the coil.
# - The sleeves stand on edge, in the direction of their leg: their broad faces contain the coil axis (the
#   fingers press on them). They stand on the same ground as the coil and are a little taller. Rounded tip,
#   open end with a slot where the wire goes in (at the top of the slot for one, at the bottom for the other).
# Proportions measured on the model's renders, in D (outside diameter of the coil), sized for a 50 mm sleeve.
# Local frame of the clip: coil axis = Z, the legs go towards -X, the upper leg (top turn) on the +Y side.
WIRE = 0.0078                          # wire diameter: on the model the coil is three wires tall, 0.385 D
RC = (0.051 + WIRE) / 2                # centre line of the coil: 51 mm inside
D = 2 * RC + WIRE                      # 66.6 mm outside
PITCH = WIRE + 0.0002                  # turns touching
TURNS = 3
SL_L, SL_W, SL_T = 1.1 * D, 0.49 * D, 1.35 * WIRE   # sleeve: length, width (along the coil axis), thickness
LEG_UP = dict(run=0.30 * D, to=139.0, r=0.10 * D, straight=0.57 * D)     # top turn: up, then up-left
LEG_LOW = dict(run=0.03 * D, to=188.0, r=0.10 * D, straight=0.55 * D)    # bottom turn: down, then left
SL_Z0 = -TURNS * PITCH / 2 - WIRE / 2 - 0.0012     # bottom of the sleeves: just under the coil's bottom
GROUND = -SL_Z0                         # lying flat, the clip rests on its sleeves and its coil


def sleeve(name, E, d, wdir, m, L, w, t, wall=0.0009):
    """Sleeve: open end (with a slot) at E, rounded tip, pointing along d, its width along wdir.
    Local axes: X = thickness, Y = along the sleeve, Z = width."""
    out = [(0.0, -w / 2), (L - w / 2, -w / 2)] + [((L - w / 2) + (w / 2) * math.cos(a), (w / 2) * math.sin(a))
                                                  for a in [math.radians(-90 + 180 * i / 24) for i in range(1, 24)]] + [(L - w / 2, w / 2), (0.0, w / 2)]
    o = fix_normals(prism(name, out, -t / 2, t / 2, m, axis='X'))
    d = d.normalized()
    wv = (wdir - d * wdir.dot(d)).normalized()
    mtx = Matrix((d.cross(wv), d, wv)).transposed().to_4x4()
    mtx.translation = Vector(E)
    o.matrix_world = mtx
    depth = 0.45 * L
    cav = box(name + '_creux', (t - 2 * wall, depth + 0.002, w - 2 * wall), (0, 0, 0), m)
    cav.matrix_world = mtx @ Matrix.Translation((0.0, depth / 2 - 0.001, 0.0))
    boolean(o, cav)
    bevel(o, 0.0024, segs=4, angle=35)
    o = bake(o, 35)
    remove(cav)
    return o


def heading(deg):
    return Vector((math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0.0))


def leg(P, first, run, to, r, straight, n=14):
    """A leg at constant height: a straight run along `first` (tangent to the coil), a bend of radius r
    to the direction `to`, then straight. Returns its points, the sleeve's open end and the direction."""
    pts = []
    pos = P + heading(first) * run
    pts.append(pos.copy())
    delta = (to - first + 180) % 360 - 180
    side = 1 if delta > 0 else -1
    centre = pos + heading(first + 90 * side) * r
    for k in range(1, n + 1):
        ang = first + delta * k / n
        pts.append(centre + heading(ang - 90 * side) * r)
    E = pts[-1] + heading(to) * straight
    return pts + [E, E + heading(to) * 0.4 * SL_L], E, heading(to)


def pince3(M, colour='noir', name='pince'):
    rw = WIRE / 2
    z0, z1 = -TURNS * PITCH / 2, TURNS * PITCH / 2
    n = 240
    coil = []
    for k in range(n + 1):                 # from the bottom end, clockwise (seen from above) while going up
        t = k / n
        th = math.radians(180.0 - 360.0 * TURNS * t)
        coil.append(Vector((RC * math.cos(th), RC * math.sin(th), z0 + (z1 - z0) * t)))
    low_pts, E_low, d_low = leg(coil[0], 270.0, **LEG_LOW)     # bottom end: leaves going down (-Y)
    up_pts, E_up, d_up = leg(coil[-1], 90.0, **LEG_UP)         # top end: leaves going up (+Y)
    path = [tuple(p) for p in reversed(low_pts)] + [tuple(p) for p in coil] + [tuple(p) for p in up_pts]
    parts = [wire(name + '_fil', path, rw, M['acier'])]
    sl = plastic(colour, 'gaine')
    Z = Vector((0.0, 0.0, 1.0))
    for k, (E, d) in enumerate(((E_low, d_low), (E_up, d_up))):
        parts.append(sleeve(f'{name}_gaine{k}', Vector((E.x, E.y, SL_Z0 + SL_W / 2)), d, Z, sl, SL_L, SL_W, SL_T))
    return group(name, parts)


def fab_studio(k=1.0):
    """Like the model's renders: a big soft light from above, soft shadows on an invisible floor; the light grey
    background is put behind later (transparent film)."""
    shadow_floor(0.0)
    SC.render.film_transparent = True
    world_hdri(0.22 * k, rot=30)
    area('dessus', (0.15, -0.35, 1.1), (0, 0, 0), 60 * k, 1.6, (1.0, 0.99, 0.98))
    o = area('face', (-0.9, -1.1, 0.5), (0, 0, 0), 22 * k, 1.5, (1.0, 0.98, 0.96))
    o.data.use_shadow = False


def dark_studio(k=1.0):
    """Like the model's first picture: soft light, the dark grey background put behind later."""
    SC.render.film_transparent = True
    world_hdri(0.25 * k, rot=30)
    area('dessus', (0.1, -0.3, 1.0), (0, 0, 0), 50 * k, 1.2, (1.0, 0.99, 0.98))
    area('face', (-0.8, -1.0, 0.45), (0, 0, 0), 40 * k, 1.2, (1.0, 0.98, 0.96))
    area('contre', (0.7, 0.9, 0.5), (0, 0, 0), 45 * k, 0.6)


def orbit(target, az, el, dist):
    """A camera position around a target: azimuth from -Y (towards +X), elevation, distance."""
    a, e = math.radians(az), math.radians(el)
    return Vector(target) + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * dist


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
            # the views of the model's renders (lying flat unless said otherwise), then ours
            T = Vector((-0.86 * D, 0.30 * D, 0.0))      # centre of the clip seen from above
            def flat(rz=0.0, name='pince', M_=None, colour=None):
                c = pince3(M_ or M, colour or COLOUR, name)
                c.rotation_euler = (0, 0, math.radians(rz)); c.location = (0, 0, GROUND)
                return c
            def look(az, el, dist, lens, target=None, fstop=11, **kw):
                tg = Vector(target) if target is not None else Vector((T.x, T.y, GROUND))
                camera(tuple(orbit(tg, az, el, dist)), tuple(tg), lens=lens, fstop=fstop, **kw)
            if plan == 'dessus':                          # straight from above
                flat(); fab_studio(); square()
                look(0, 84, 0.23, 50)
            elif plan == 'cote':                          # low, from the side of the coil
                flat(); fab_studio(); square()
                look(20, 4, 0.30, 50, target=(-0.80 * D, 0.0, 2.2 * GROUND))
            elif plan == 'bout':                          # low, from the tips of the sleeves
                flat(); fab_studio(); square()
                look(-80, 6, 0.29, 50, target=(-0.95 * D, 0.62 * D, GROUND))
            elif plan == 'trois-quarts':                  # from above, the coil in front
                flat(); fab_studio(); square()
                look(88, 32, 0.22, 50, target=(-0.55 * D, 0.30 * D, 0.0))
            elif plan == 'arriere':                       # the coil in front, the sleeves behind
                flat(); fab_studio(); square()
                look(52, 28, 0.255, 55, target=(-0.80 * D, 0.25 * D, GROUND))
            elif plan == 'heros':                         # the model's first picture, on dark grey
                flat(); dark_studio(); setup_render()
                look(30, 30, 0.38, 50, target=(-0.75 * D, 0.30 * D, GROUND))
            elif plan == 'debout':                        # standing on its coil, the sleeves up
                c = pince3(M, COLOUR)
                # the legs (towards -X) turned upwards, the coil axis turned towards the camera, the V seen from the front
                # the V's bisector goes up; the camera sees the clip from between the coil axis and the sleeves'
                # broad faces (both at about 45 degrees), like the model's picture; then the V leans to the left
                b = heading(163.5)
                cdir = Vector((0.0, -0.7, 0.7)); cdir = (cdir - b * cdir.dot(b)).normalized()
                Ma = Matrix((b, cdir, b.cross(cdir))).transposed()
                Mw = Matrix(((0, 0, 1), (0, -1, 0), (1, 0, 0))).transposed()
                R = Matrix.Rotation(math.radians(float(ARGS.get('dy', -22))), 4, 'Y') @ (Mw @ Ma.transposed()).to_4x4()
                c.matrix_world = R
                bpy.context.view_layer.update()
                zmin = min((ch.matrix_world @ v.co).z for ch in c.children for v in ch.data.vertices)   # (not the bounding boxes: turned, they reach lower)
                c.location.z -= zmin
                fab_studio(); square()
                camera((-0.02, -0.37, 0.08), (-0.028, 0.0, 0.082), lens=55, fstop=11)
            elif plan == 'sur-barre':
                barre_olympique(bar_mats('B', 'noir'))
                e = disque(20, plate_mats('noir', 'moule'), name='d'); x = 0.686 + e['T'] / 2
                e.location = (x, 0, 0); e.rotation_euler = (0, 0, math.radians(90))
                c = pince3(M, COLOUR)
                # coil axis along the bar, the V of the sleeves upwards and a little towards the camera
                # (the clip's own frame: its coil axis is Z, so turned by 90 degrees about Y it lies along the bar)
                c.matrix_world = Matrix.Translation((x + e['T'] / 2 - SL_Z0 + 0.001, 0, 0)) @ Matrix.Rotation(math.radians(float(ARGS.get('bx', 30))), 4, 'X') @ Matrix.Rotation(math.radians(90), 4, 'Y')
                catalog(k=1.05); portrait()
                camera((1.06, -0.37, 0.21), (0.77, -0.02, 0.065), lens=55, fstop=5.6, focus=(x + e['T'] / 2 + 0.02, -0.03, 0.05))
            elif plan == 'couleurs':
                for i, cname in enumerate(PALETTE):            # each one turned like the main picture
                    c = pince3(collar_mats(cname), cname, 'k%d' % i)
                    c.rotation_euler = (0, 0, math.radians(-30)); c.location = (-0.50 + 0.165 * i, 0.0, GROUND)
                light_floor(center=(0.0, 0.0, 0.04), k=1.1); setup_render()
                camera((0.03, -1.30, 0.90), (0.03, 0.06, 0.0), lens=38, fstop=11)
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
