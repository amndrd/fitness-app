# Step 7 (21-22/11/2026): the spring clip, the only collar of the library (the lever collar was dropped on 22/11).
# The clip is rebuilt after the model chosen by the user (3d/recherche/6-pince-fab): satin steel wire, three tight
# turns, two legs in a V, sleeves on edge (rounded tip, slotted end). The same clip, scaled, fits the 25 mm bars.
# The colour (sleeves) is a setting (3d/charte.md). Reuses barre.py, poids3.py, poids2.py and base.py.
# usage: Blender -b --factory-startup -P colliers.py -- plans=dessus,trois-quarts couleur=noir res=1400 samples=128 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_BARRE = True
exec(open(os.path.join(HERE, 'barre.py')).read())

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
    M['acier'] = mat('acier_fil', (float(ARGS.get('acier', 0.40)),) * 2 + (float(ARGS.get('acier', 0.40)) + 0.02,), rough=float(ARGS.get('rug', 0.24)), metal=1.0)     # the clip's wire: satin steel
    return M


def shadow_floor(z):
    me = bpy.data.meshes.new('sol')
    s = 3.0
    me.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
    o = link(bpy.data.objects.new('sol', me))
    o.is_shadow_catcher = True
    return o


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
SL_L, SL_W, SL_T = 1.1 * D, 0.52 * D, 1.35 * WIRE   # sleeve: length, width (along the coil axis), thickness
SL_WALL = 0.0009                                     # sleeve wall: the wire must stay inside the slot (22/11)
LEG_UP = dict(run=0.30 * D, to=139.0, r=0.10 * D, straight=0.57 * D)     # top turn: up, then up-left
LEG_LOW = dict(run=0.03 * D, to=188.0, r=0.10 * D, straight=0.55 * D)    # bottom turn: down, then left
SL_Z0 = -TURNS * PITCH / 2 - WIRE / 2 - SL_WALL - 0.0004   # bottom of the sleeves: the bottom wire sits just inside the slot
GROUND = -SL_Z0                         # lying flat, the clip rests on its sleeves and its coil


def sleeve(name, E, d, wdir, m, L, w, t, wall=SL_WALL):
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


def cyl_x(name, r, x0, x1, pos, m, segs=32):
    """A small cylinder along X (the holes of the 25 mm plates are cut with it)."""
    o = fix_normals(lathe(name, round_poly([(0.0, x0), (r, x0), (r, x1), (0.0, x1)], [0, 0.0006, 0.0006, 0], segs=2), m, segs=segs, axis='X'))
    o.location = pos
    return o


# ------------------------------------------------------------------ shots
def out(plan):
    return os.path.join(OUT, f'pince-{COLOUR}-{plan}.png')


def shot():
    M = collar_mats(COLOUR)
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        SC.render.film_transparent = False
        M = collar_mats(COLOUR)
        if True:
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
        render(out(plan))


if not globals().get('AS_LIB_COLLIERS'):     # halteres.py uses this file as a library
    shot()
