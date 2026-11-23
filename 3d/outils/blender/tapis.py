# Cardio 1 (22/11/2026): the treadmill, after the user's reference, the Landice L8 in black (3d/references/tapis/).
# The design logic is in 3d/recherche/9-tapis-de-course/analyse.md:
# - a long low chassis, a flat rail each side of the belt (the step), a smooth skirt outside, angled end caps at the rear;
# - the motor hood at the front, its top sloping towards the user, two vent grilles in front;
# - the portal: two wide flat uprights from the front corners, leaning back, joined at the top by a big round bend
#   (an upside-down U seen from the front), one thick piece;
# - on top of it, a shell that reaches towards the user: cup holders at both ends, the keypad in the middle,
#   two chrome heart-rate grips; two flat handrails going back from the corners; the console (a tablet) above.
# No brand: no logo, no model name; the screen stays off. Sizes: 2.11 x 0.89 x 1.56 m, belt 0.56 x 1.60 m, step 0.19 m.
# Axes: X across (the user's right is +X), Y along (the hood is at +Y, the user runs towards +Y), Z up, floor z = 0.
# usage: Blender -b --factory-startup -P tapis.py -- plans=reference,avant couleur=noir res=1400 samples=128 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_P3 = True
exec(open(os.path.join(HERE, 'poids3.py')).read())

PLANS = ARGS.get('plans', 'reference').split(',')
FINISH = ARGS.get('couleur', 'noir')       # the portal's finish: noir (the user's choice, 23/11), graphite, argent
GRILLES = ARGS.get('grilles', 'fines')     # the hood's grilles: fines (the black original) | cloisons (the silver one)

# ------------------------------------------------------------------ dimensions (metres)
L2, W2 = 1.055, 0.445          # half length, half width
BELT_W2 = 0.28                 # belt: 0.56 m wide
BELT_Z = 0.19                  # step-up height: the top of the belt
RAIL_Z = 0.205                 # the top of the side rails
REAR = -1.0                    # the rear roller's axis (y)
HOOD_Y = 0.63                  # where the hood starts (the front end of the belt)
UP_X = 0.4075                  # the uprights: axis
UP_W2, UP_D2 = 0.04, 0.08      # their section: 80 mm wide, 160 mm deep (front to back)
LEAN = math.radians(20)        # leaning back towards the user
BASE_Y = 0.97                  # the uprights' feet: their front face flush with the hood
TOP_Z = 1.21                   # the axis of the portal's top bar
CORNER = float(ARGS.get('coin', 0.27))   # the portal's top corners: the big round bend (the user's choice, 23/11)
EDGE = float(ARGS.get('arete', 0.007))   # the portal's edges: crisp like the original (23/11; they were 0.026, too soft)
GRIPS = ARGS.get('poignees', 'droites')  # heart-rate grips: droites (like the original, the user's choice 23/11) | galbees


# ------------------------------------------------------------------ materials
FINISHES = {   # the portal: satin metallic paint
    'noir': dict(c=(0.032, 0.033, 0.037), metal=0.55, rough=0.40),
    'graphite': dict(c=(0.11, 0.115, 0.125), metal=0.65, rough=0.38),
    'argent': dict(c=(0.62, 0.63, 0.65), metal=0.9, rough=0.30),
}


def mats(finish=FINISH):
    f = FINISHES[finish]
    M = {}
    M['portique'] = mat('portique', f['c'], rough=f['rough'], metal=f['metal'], coat=0.35, coat_rough=0.22,
                        grain=0.05, grain_scale=1200, peel=0.15, peel_scale=160)
    M['jupe'] = mat('jupe', f['c'], rough=f['rough'] + 0.04, metal=f['metal'] * 0.9, coat=0.2, coat_rough=0.3)
    M['rail'] = mat('rail', (0.03, 0.03, 0.033), rough=0.36, metal=0.7, grain=0.1, grain_scale=1500)
    M['plastique'] = mat('plastique', (0.017, 0.017, 0.019), rough=0.52, spec=0.42, grain=0.25, grain_scale=2200)
    M['capot'] = mat('capot', (0.013, 0.013, 0.015), rough=0.62, spec=0.26, grain=0.3, grain_scale=2200)
    M['mat'] = mat('plastique_mat', (0.012, 0.012, 0.013), rough=0.7, spec=0.3, grain=0.3, grain_scale=2200)
    M['bande'] = mat('bande', (0.011, 0.011, 0.012), rough=0.82, spec=0.25, grain=0.7, grain_scale=900)
    M['grille'] = mat('grille', (0.004, 0.004, 0.005), rough=0.9, spec=0.1)
    M['chrome'] = mat('chrome', (0.86, 0.86, 0.88), rough=0.07, metal=1.0)
    M['ecran'] = mat('ecran', (0.004, 0.004, 0.006), rough=0.04, spec=0.6, coat=1.0, coat_rough=0.02)
    M['stop'] = mat('stop', (0.55, 0.04, 0.045), rough=0.3, spec=0.5, coat=0.5, coat_rough=0.1)
    M['caoutchouc'] = mat('pied', (0.015, 0.015, 0.016), rough=0.8, spec=0.25)
    return M


# ------------------------------------------------------------------ geometry helpers
def rbox(name, size, m, r=0.01, segs=4, loc=(0, 0, 0), rot=(0, 0, 0)):
    """A box (x, y, z sizes) with every edge rounded (radius r), centred on loc, turned by rot (degrees)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new(name, me))
    me.materials.append(m)
    if r > 0:
        md = o.modifiers.new('bevel', 'BEVEL'); md.width = min(r, min(size) * 0.499); md.segments = segs
        md.limit_method = 'NONE'
        bake(o)
    o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    return o


def fix_normals(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free()
    return o


def rounded(o, r, segs=3, angle=30):
    fix_normals(o)
    md = o.modifiers.new('bevel', 'BEVEL'); md.width = r; md.segments = segs
    md.limit_method = 'ANGLE'; md.angle_limit = math.radians(angle)
    bake(o, sharp=angle)
    return o


def cyl(name, p0, p1, r, m, segs=48):
    """A cylinder between two points."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = lathe(name, [(0.0, 0.0), (r, 0.0), (r, d.length), (0.0, d.length)], m, segs=segs, axis='Y')
    o.data.transform(Matrix.Rotation(math.radians(90), 4, 'X'))       # axis Y -> Z
    q = d.normalized().to_track_quat('Z', 'X' if abs(d.normalized().y) > 0.9 else 'Y')
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = q; o.location = p0
    try:
        o.data.set_sharp_from_angle(angle=math.radians(40))
    except AttributeError:
        pass
    return o


def fillet3(pts, d, segs=16):
    """A 3D polyline with its corners rounded (each corner cut d before and after, then a smooth curve)."""
    P = [Vector(p) for p in pts]
    out = [P[0]]
    for i in range(1, len(P) - 1):
        a, p, c = P[i - 1], P[i], P[i + 1]
        k = min(d, (a - p).length * 0.49, (c - p).length * 0.49)
        p0, p2 = p + (a - p).normalized() * k, p + (c - p).normalized() * k
        for s in range(segs + 1):
            t = s / segs
            out.append((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p + t ** 2 * p2)
    out.append(P[-1])
    return out


def rrect(w2, d2, r, n=6):
    """A rounded rectangle (half sizes w2, d2, corner radius r), as a closed list of (a, b) points."""
    pts = []
    for cx, cy, a0 in ((w2 - r, d2 - r, 0), (-w2 + r, d2 - r, 90), (-w2 + r, -d2 + r, 180), (w2 - r, -d2 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sweep(name, path, profile, normal, m):
    """Sweeps a closed profile [(a, b)] along a planar path: a runs in the path's plane (across the path),
    b along the plane's normal (fixed), so the section never twists. Both ends are closed flat."""
    nrm = Vector(normal).normalized()
    P = path
    verts, faces = [], []
    n = len(profile)
    for i, p in enumerate(P):
        t = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]).normalized()
        b = t.cross(nrm).normalized()
        for a, c in profile:
            verts.append(tuple(p + b * a + nrm * c))
    for i in range(len(P) - 1):
        for j in range(n):
            j2 = (j + 1) % n
            faces.append((i * n + j, i * n + j2, (i + 1) * n + j2, (i + 1) * n + j))
    faces.append(tuple(range(n))[::-1])
    faces.append(tuple((len(P) - 1) * n + j for j in range(n)))
    o = mesh_obj(name, verts, faces, m)
    fix_normals(o)
    try:
        o.data.set_sharp_from_angle(angle=math.radians(50))
    except AttributeError:
        pass
    return o


def slices_x(name, profile, x0, x1, n, m, deform=None):
    """A closed side profile [(y, z)] extruded along X in n slices (so it can bulge), its two ends closed.
    deform(x, y, z) -> (y, z) moves each point of each slice."""
    k = len(profile)
    verts, faces = [], []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        for y, z in profile:
            if deform:
                y, z = deform(x, y, z)
            verts.append((x, y, z))
    for i in range(n):
        for j in range(k):
            j2 = (j + 1) % k
            faces.append((i * k + j, i * k + j2, (i + 1) * k + j2, (i + 1) * k + j))
    faces.append(tuple(range(k)))
    faces.append(tuple(n * k + j for j in range(k))[::-1])
    o = mesh_obj(name, verts, faces, m, smooth=True)
    return fix_normals(o)


# ------------------------------------------------------------------ the treadmill
def build(finish=FINISH):
    M = mats(finish)
    parts = []

    # --- the chassis: the side members (rail on top, skirt outside), the base pan, the belt
    for s in (-1, 1):
        prof = [(s * 0.272, 0.185), (s * 0.272, RAIL_Z), (s * 0.425, RAIL_Z), (s * W2, RAIL_Z - 0.02),
                (s * W2, 0.058), (s * (W2 - 0.012), 0.042), (s * 0.31, 0.042), (s * 0.31, 0.185)]
        if s < 0:
            prof = prof[::-1]
        side = prism('cote', prof, REAR + 0.01, BASE_Y - 0.06, M['jupe'], axis='Y')
        rounded(side, 0.006, 3)
        parts.append(side)
        # the rail's top: black aluminium, a thin plate over the skirt
        parts.append(rbox('rail', (0.15, BASE_Y - 0.06 - REAR - 0.01, 0.006), M['rail'], r=0.002, segs=2,
                          loc=(s * 0.35, (REAR + BASE_Y - 0.05) / 2, RAIL_Z + 0.002)))
        # the rear end caps: black, cut on a slant
        cap = [(REAR + 0.012, RAIL_Z + 0.005), (REAR - 0.055, 0.15), (REAR - 0.055, 0.07), (REAR - 0.03, 0.045), (REAR + 0.012, 0.045)]
        ec = prism('embout', cap, s * 0.272 if s > 0 else -W2, W2 if s > 0 else -0.272, M['plastique'], axis='X')
        rounded(ec, 0.008, 3)
        parts.append(ec)
        # the rear feet (levelling)
        parts.append(cyl('pied_vis', (s * 0.34, REAR + 0.06, 0.012), (s * 0.34, REAR + 0.06, 0.05), 0.008, M['chrome']))
        parts.append(cyl('pied', (s * 0.34, REAR + 0.06, 0.0), (s * 0.34, REAR + 0.06, 0.014), 0.025, M['caoutchouc']))
    parts.append(rbox('cuve', (0.56, HOOD_Y - REAR, 0.09), M['mat'], r=0.01, segs=2,
                      loc=(0.0, (HOOD_Y + REAR) / 2, 0.095)))
    # the belt: a long loop round the two rollers (rounded ends)
    rr = 0.035
    loop = [(REAR + rr * math.cos(math.radians(a)), BELT_Z - rr + rr * math.sin(math.radians(a))) for a in range(90, 271, 10)]
    loop += [(HOOD_Y + 0.02, BELT_Z - 2 * rr), (HOOD_Y + 0.02, BELT_Z)]
    belt = prism('bande', loop, -BELT_W2, BELT_W2, M['bande'], axis='X')
    rounded(belt, 0.003, 2)
    parts.append(belt)

    # --- the motor hood (reworked 23/11 after the user's notes): a moulded cover over a plain plinth
    hx = UP_X - UP_W2 - 0.002                          # between the uprights
    def bump(x, w):                                    # 1 in the middle, 0 at the sides
        u = min(1.0, abs(x) / w)
        return 1.0 - u * u
    # the cover's side profile (y, z) changes across the width: in the middle its back is a hollow that goes down
    # to the belt; towards the sides it stretches back over the rails into a fender ending in a point.
    radii = [0.004, 0.01, 0.05, 0.06, 0.07, 0.03, 0.06, 0.012]
    # the front face leans back by about 23 degrees: the grilles look a little upwards, like on the original
    mid = [(0.66, 0.19), (1.058, 0.19), (1.005, 0.315), (0.96, 0.346), (0.80, 0.338), (0.735, 0.318), (0.738, 0.25), (0.655, 0.205)]
    wing = [(0.548, 0.19), (1.058, 0.19), (1.005, 0.315), (0.96, 0.346), (0.80, 0.338), (0.75, 0.316), (0.62, 0.236), (0.555, 0.214)]
    def dense(poly, ref=None):
        """Rounds the corners, then cuts every segment in pieces of ~8 mm (the same number for both profiles)."""
        r = round_poly(poly, radii, segs=12)
        out, counts = [], []
        for i in range(len(r)):
            a, b = Vector(r[i]), Vector(r[(i + 1) % len(r)])
            k = ref[i] if ref else max(1, int((b - a).length / 0.008))
            counts.append(k)
            for j in range(k):
                out.append(tuple(a.lerp(b, j / k)))
        return out, counts
    pm, cnt = dense(mid)
    pw, _ = dense(wing, cnt)
    def relax(poly, n=12):
        """Evens out the profile (a few passes of averaging), so the hollow is one smooth curve, without ripples.
        The points on the bottom and on the front face stay where they are."""
        pts = [Vector(p) for p in poly]
        fixed = [p.y < 0.2 or p.x > 1.0 for p in pts]
        for _ in range(n):
            new = []
            for i, p in enumerate(pts):
                if fixed[i]:
                    new.append(p); continue
                new.append(p * 0.5 + (pts[i - 1] + pts[(i + 1) % len(pts)]) * 0.25)
            pts = new
        return [tuple(p) for p in pts]
    pm, pw = relax(pm), relax(pw)
    def smooth(a, b, v):
        t = max(0.0, min(1.0, (v - a) / (b - a)))
        return t * t * (3 - 2 * t)
    nx = 64
    k = len(pm)
    verts, faces = [], []
    for i in range(nx + 1):
        x = -hx + 2 * hx * i / nx
        w = smooth(0.25, 0.29, abs(x))                 # 0: the hollow in the middle, 1: the fender (a clear edge between them)
        for (ym, zm), (yw, zw) in zip(pm, pw):
            y, z = ym + (yw - ym) * w, zm + (zw - zm) * w
            # the front face bulges forward in the middle; the top is domed, with a soft raised plate in the middle
            y0 = y
            y += 0.013 * bump(x, hx) * smooth(0.95, 1.01, y0) * smooth(0.36, 0.33, z)
            z += smooth(0.30, 0.335, z) * smooth(1.0, 0.95, y0) * (0.011 * bump(x, hx)
                 + 0.006 * smooth(0.29, 0.2, abs(x)) * smooth(0.77, 0.85, y0) * smooth(0.965, 0.9, y0))
            verts.append((x, y, z))
    for i in range(nx):
        for j in range(k):
            j2 = (j + 1) % k
            faces.append((i * k + j, i * k + j2, (i + 1) * k + j2, (i + 1) * k + j))
    faces.append(tuple(range(k)))
    faces.append(tuple(nx * k + j for j in range(k))[::-1])
    cover = fix_normals(mesh_obj('capot', verts, faces, M['capot'], smooth=True))
    rounded(cover, 0.035, 8, angle=35)                 # the two ends: big rounded corners all round
    parts.append(cover)
    P = {'B': mid[1], 'C': mid[2]}
    # the two grilles, high on the front face, near the corners: a frame, a dark well, fine slats
    # (cloisons: the slats cut in four by small upright walls, like the silver original)
    lean = math.atan2(P['B'][0] - P['C'][0], P['C'][1] - P['B'][1])
    gw, gh = 0.165, 0.05
    for sgn in (-1, 1):
        gx, gz = sgn * 0.21, 0.265
        gy = P['B'][0] - (gz - P['B'][1]) * math.tan(lean) + 0.013 * bump(gx, hx)
        yaw = -sgn * math.degrees(math.atan(0.026 * abs(gx) / (hx * hx)))
        rot = (math.degrees(lean), 0, yaw)
        R = Euler(tuple(math.radians(a) for a in rot)).to_matrix()
        fwd, upv, side = R @ Vector((0, 1, 0)), R @ Vector((0, 0, 1)), R @ Vector((1, 0, 0))
        base = Vector((gx, gy, gz))
        parts.append(rbox('grille_cadre', (gw, 0.01, gh), M['mat'], r=0.004, segs=2, loc=tuple(base), rot=rot))
        parts.append(rbox('grille_fond', (gw - 0.01, 0.004, gh - 0.008), M['grille'], r=0.002, segs=1, loc=tuple(base + fwd * 0.0042), rot=rot))
        n = 10
        for k in range(n):
            q = base + fwd * 0.0052 + upv * (-(gh - 0.014) / 2 + k * (gh - 0.014) / (n - 1))
            parts.append(rbox('lame', (gw - 0.012, 0.0035, 0.0012), M['capot'], r=0.0004, segs=1, loc=tuple(q), rot=(rot[0] - 35, 0, yaw)))
        if GRILLES == 'cloisons':
            for c in (-1, 0, 1):
                q = base + fwd * 0.0055 + side * (c * (gw - 0.016) / 4)
                parts.append(rbox('cloison', (0.003, 0.006, gh - 0.012), M['plastique'], r=0.001, segs=1, loc=tuple(q), rot=rot))
    # the plinth under the cover, set back: the line between the two pieces shows all round
    parts.append(rbox('socle', (2 * hx - 0.02, 0.36, 0.155), M['mat'], r=0.01, segs=3, loc=(0.0, 1.035 - 0.18, 0.03 + 0.0775)))
    # on its front, at the user's right: the power inlet and the rocker switch, two screws
    parts.append(rbox('prise', (0.03, 0.006, 0.024), M['plastique'], r=0.003, segs=2, loc=(0.245, 1.036, 0.095)))
    parts.append(rbox('prise_fond', (0.022, 0.003, 0.016), M['grille'], r=0.002, segs=1, loc=(0.245, 1.0385, 0.095)))
    parts.append(rbox('interrupteur', (0.02, 0.006, 0.032), M['plastique'], r=0.003, segs=2, loc=(0.29, 1.036, 0.098)))
    parts.append(rbox('bascule', (0.014, 0.006, 0.013), M['mat'], r=0.002, segs=1, loc=(0.29, 1.04, 0.104), rot=(14, 0, 0)))
    for sgn in (-1, 1):
        parts.append(cyl('vis', (sgn * 0.33, 1.035, 0.165), (sgn * 0.33, 1.038, 0.165), 0.0035, M['mat']))
    # the two transport wheels at the front corners, just off the floor
    for sgn in (-1, 1):
        parts.append(rbox('chape_roue', (0.034, 0.05, 0.022), M['mat'], r=0.004, segs=2, loc=(sgn * 0.31, 1.0, 0.035)))
        parts.append(cyl('roue', (sgn * 0.31 - 0.011, 1.0, 0.029), (sgn * 0.31 + 0.011, 1.0, 0.029), 0.024, M['caoutchouc']))
        parts.append(cyl('moyeu_roue', (sgn * 0.31 - 0.0125, 1.0, 0.029), (sgn * 0.31 + 0.0125, 1.0, 0.029), 0.008, M['mat']))
    # the frame's rubber pads, under the side members just behind the uprights
    for sgn in (-1, 1):
        parts.append(rbox('patin', (0.07, 0.1, 0.042), M['caoutchouc'], r=0.005, segs=2, loc=(sgn * 0.36, 0.79, 0.021)))

    # --- the portal: one swept piece, an upside-down U leaning back
    up = Vector((0.0, -math.sin(LEAN), math.cos(LEAN)))
    top_y = BASE_Y - (TOP_Z - 0.0) * math.tan(LEAN)
    below = 0.06 * math.tan(LEAN)                       # the legs start under the floor, then are cut flat
    path = fillet3([(-UP_X, BASE_Y + below, -0.06), (-UP_X, top_y, TOP_Z), (UP_X, top_y, TOP_Z), (UP_X, BASE_Y + below, -0.06)], CORNER, segs=28)
    # more points on the straight runs, so the shading stays smooth
    dense = []
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        k = max(1, int((b - a).length / 0.05))
        for j in range(k):
            dense.append(a.lerp(b, j / k))
    dense.append(path[-1])
    normal = Vector((1, 0, 0)).cross(up)                # perpendicular to the portal's plane (front-back)
    portal = sweep('portique', dense, rrect(UP_W2, UP_D2, EDGE, 4), normal, M['portique'])
    floor_cut = rbox('sol', (2.0, 2.0, 0.2), M['mat'], r=0, loc=(0.0, BASE_Y, 0.006 - 0.1))
    boolean(portal, floor_cut); bake(portal, sharp=50); remove(floor_cut)
    parts.append(portal)
    # the feet: a thin rubber pad under each leg, set in; two bolts on the outside, into the frame
    foot_d = UP_D2 / math.cos(LEAN)
    for s in (-1, 1):
        parts.append(rbox('pied_montant', (2 * UP_W2 - 0.01, 2 * foot_d - 0.012, 0.006), M['caoutchouc'], r=0.002, segs=1,
                          loc=(s * UP_X, BASE_Y, 0.003)))
        for zb in (0.075, 0.15):
            yb = BASE_Y - zb * math.tan(LEAN)
            parts.append(cyl('boulon', (s * (UP_X + UP_W2 - 0.001), yb, zb), (s * (UP_X + UP_W2 + 0.003), yb, zb), 0.007, M['mat']))

    # --- on top (reworked 23/11 after the user's notes, like the original):
    #     a shell behind the portal's bar; at each corner an end block with its cup holder, which covers the root of
    #     the handrail; the handrails are big flat paddles, about 7 cm lower than the bar; the heart-rate grips go from
    #     the sides of the keypad, back and out, into the roots of the handrails.
    st = TOP_Z + UP_W2                                  # top of the portal's bar
    hz = st - 0.105                                     # handrails: their axis (their top is 7 cm under the bar)
    hxa = UP_X - 0.004                                  # handrails: their axis across
    shell_xy = round_poly([(-0.36, top_y - 0.03), (0.36, top_y - 0.03), (0.36, top_y - 0.15), (0.17, top_y - 0.15), (0.115, top_y - 0.19),
                           (-0.115, top_y - 0.19), (-0.17, top_y - 0.15), (-0.36, top_y - 0.15)], [0.02, 0.02, 0.03, 0.05, 0.04, 0.04, 0.05, 0.03], segs=10)
    n = len(shell_xy)
    shell = mesh_obj('coque', [(x, y, z) for z in (st - 0.075, st - 0.012) for x, y in shell_xy],
                     [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)],
                     M['plastique'], smooth=False)
    rounded(shell, 0.02, 5)
    parts.append(shell)
    for sg in (-1, 1):
        # the end block over the corner of the portal, with its deep cup holder
        top_b = st - 0.004                                # just under the top of the portal's bar
        bot_b = st - 0.085
        parts.append(rbox('bout_coque', (0.125, 0.2, top_b - bot_b), M['plastique'], r=0.0395, segs=9,
                          loc=(sg * hxa, top_y - 0.07, (top_b + bot_b) / 2)))
        c = Vector((sg * hxa, top_y - 0.07, top_b))
        parts.append(cyl('gobelet_bord', c - Vector((0, 0, 0.006)), c + Vector((0, 0, 0.004)), 0.046, M['plastique']))
        parts.append(cyl('gobelet_fond', c - Vector((0, 0, 0.004)), c + Vector((0, 0, 0.0052)), 0.038, M['grille']))
        # the handrail: an upright flat paddle (5 cm thick), 10 cm tall at its root and 7.5 cm at its end, which is
        # rounded like a D; its big inner face looks at the runner's hands. The top stays level, the underside rises.
        y0, y1 = top_y - 0.03, top_y - 0.68
        zt = st - 0.05
        prof = round_poly([(y0, zt - 0.13), (y1, zt - 0.095), (y1, zt), (y0, zt)], [0.0, 0.045, 0.045, 0.0], segs=12)
        th2 = 0.026
        xa, xb = (sg * hxa - th2, sg * hxa + th2)
        pad = prism('main_courante', prof, xa, xb, M['plastique'], axis='X')
        rounded(pad, 0.014, 6, angle=35)
        parts.append(pad)
        # a thin lip along the top of the inner face, round the end too
        lip = [(y0, zt - 0.004), (y1 + 0.03, zt - 0.004)]
        parts.append(rbox('levre', (0.006, y0 - y1 - 0.03, 0.01), M['plastique'], r=0.0028, segs=2,
                          loc=(sg * (hxa - th2 - 0.001), (y0 + y1 + 0.03) / 2, zt - 0.006)))
    # the keypad, under the back edge of the shell, turned towards the runner: + and - on each side, STOP in the middle
    kp = Vector((0.0, top_y - 0.185, st - 0.07))
    tilt_k = 35
    Rk = Euler((math.radians(tilt_k), 0, 0)).to_matrix()
    nk, uk = Rk @ Vector((0, -1, 0)), Rk @ Vector((0, 0, 1))
    parts.append(rbox('clavier', (0.3, 0.048, 0.078), M['plastique'], r=0.014, segs=4, loc=kp, rot=(tilt_k, 0, 0)))
    parts.append(rbox('clavier_face', (0.27, 0.004, 0.056), M['mat'], r=0.008, segs=2, loc=kp + nk * 0.024, rot=(tilt_k, 0, 0)))
    parts.append(cyl('stop', kp + nk * 0.024, kp + nk * 0.031, 0.019, M['stop']))
    for sg in (-1, 1):
        for dz in (0.014, -0.014):
            q = kp + Vector((sg * 0.095, 0, 0)) + nk * 0.025 + uk * dz
            parts.append(rbox('touche', (0.024, 0.006, 0.022), M['plastique'], r=0.005, segs=2, loc=q, rot=(tilt_k, 0, 0)))
    parts.append(rbox('cle', (0.014, 0.02, 0.03), M['stop'], r=0.003, segs=2, loc=kp + Vector((0.035, -0.012, -0.05))))
    # the heart-rate grips, into the roots of the handrails
    for sg in (-1, 1):
        a = kp + Vector((sg * 0.152, 0.004, -0.006))
        c = Vector((sg * (hxa - 0.026), top_y - 0.19, st - 0.05 - 0.08))        # into the lower part of the handrail's root
        if GRIPS == 'droites':                             # a straight bar: black ends, a long chrome sleeve (the original)
            parts.append(cyl('poignee_cardio', a, c, 0.0155, M['plastique']))
            parts.append(cyl('capteur', a.lerp(c, 0.16), a.lerp(c, 0.84), 0.0172, M['chrome']))
            for e0, e1 in ((a, a.lerp(c, 0.16)), (c, c.lerp(a, 0.12))):
                parts.append(cyl('bague', e0, e1, 0.02, M['plastique']))
        else:                                              # a moulded grip, bent where the hand goes, two steel pads
            b = a.lerp(c, 0.35) + Vector((0, -0.03, -0.025))
            path = fillet3([a, b, c], 0.06, segs=16)
            nrm_g = (b - a).cross(c - b).normalized()
            parts.append(sweep('poignee_cardio', path, rrect(0.017, 0.017, 0.0169, 6), nrm_g, M['plastique']))
            d = (c - b).normalized()
            for t0, t1 in ((0.12, 0.47), (0.53, 0.88)):
                parts.append(cyl('capteur', b.lerp(c, t0), b.lerp(c, t1), 0.0182, M['chrome']))
            parts.append(cyl('bague', c - d * 0.03, c, 0.021, M['plastique']))

    # --- the console: a tablet on a short neck, tilted back towards the user
    neck = Vector((0.0, top_y + 0.015, st + 0.02))
    parts.append(rbox('cou', (0.2, 0.08, 0.07), M['plastique'], r=0.02, segs=3, loc=neck))
    tilt = 18
    cc = Vector((0.0, top_y + 0.035, st + 0.185))
    parts.append(rbox('console', (0.44, 0.058, 0.29), M['plastique'], r=0.026, segs=5, loc=cc, rot=(-tilt, 0, 0)))
    nrm = Vector((0, -math.cos(math.radians(tilt)), math.sin(math.radians(tilt))))
    parts.append(rbox('ecran', (0.38, 0.004, 0.225), M['ecran'], r=0.004, segs=2, loc=cc + nrm * 0.0285, rot=(-tilt, 0, 0)))
    parts.append(rbox('dos_console', (0.28, 0.006, 0.17), M['mat'], r=0.004, segs=2, loc=cc - nrm * 0.03, rot=(-tilt, 0, 0)))
    for k in range(5):                     # vents on the back of the console
        parts.append(rbox('event', (0.05, 0.004, 0.004), M['grille'], r=0.0015, segs=1,
                          loc=cc - nrm * 0.03 + Vector((0.17, 0, 0)) + Vector((0, math.sin(math.radians(tilt)), math.cos(math.radians(tilt)))) * (0.05 - k * 0.012),
                          rot=(-tilt, 0, 0)))
    return parts


# ------------------------------------------------------------------ light and cameras (alone on white, no floor)
def flags(c, s):
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


def light(cam_loc, c=(0.0, 0.0, 0.7), s=2.0):
    """The catalogue light of the models, turned with the camera: a big soft key above the camera's side,
    a top light, two rims behind. The HDRI gives the reflections."""
    SC.render.film_transparent = True
    world_hdri(0.45, rot=30)
    C = Vector(c)
    d = (Vector(cam_loc) - C); d.z = 0; d.normalize()
    side = Vector((-d.y, d.x, 0))
    area('key', C + d * 2.2 * s + side * 1.6 * s + Vector((0, 0, 1.9 * s)), C, 300 * s * s, 2.6 * s, (1.0, 0.98, 0.96))
    area('top', C + Vector((0, 0, 2.6 * s)) + d * 0.6 * s, C, 90 * s * s, 3.0 * s)
    area('rim', C - d * 1.6 * s - side * 1.4 * s + Vector((0, 0, 1.2 * s)), C, 170 * s * s, 0.4 * s, (1, 1, 1), 'RECTANGLE', 2.6 * s)
    area('rim2', C - d * 1.4 * s + side * 1.6 * s + Vector((0, 0, 1.0 * s)), C, 110 * s * s, 0.3 * s, (1, 1, 1), 'RECTANGLE', 2.2 * s)
    flags(c, s)


def shot_camera(target, az, el, dist, lens):
    """az: degrees from the front (+Y), positive towards the user's right side (+X)."""
    a, e = math.radians(az), math.radians(el)
    t = Vector(target)
    loc = t + Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))) * dist
    camera(tuple(loc), tuple(t), lens=lens, fstop=22.0)
    return loc


SHOTS = {   # name: target, azimuth, elevation, distance, lens
    'reference': ((0.0, 0.0, 0.68), 48, 7, 2.85, 32),       # the angle of the user's picture (front right)
    'arriere-gauche': ((0.0, 0.0, 0.68), 236, 10, 3.2, 35),  # rear left: the screen, both handrails
    'profil': ((0.0, 0.0, 0.74), 90, 2, 6.0, 60),
    'face': ((0.0, 0.0, 0.78), 0, 5, 5.0, 60),
    'arriere': ((0.0, 0.1, 0.70), 200, 20, 4.6, 50),         # where the user steps on
    'console': ((0.0, 0.5, 1.32), 180, 30, 1.7, 50),         # what the runner sees
    'capot': ((0.1, 0.92, 0.32), 30, 16, 1.7, 50),
    'capot-ref': ((0.12, 0.9, 0.22), 48, 13, 1.45, 50),      # the original's close-up: front right
    # the top, seen from the very camera places of the manufacturer's pictures (zoomed in)
    'haut-ref': ((0.0, 0.45, 1.2), 55.5, -3.9, 2.56, 60),    # from the front right (the user's picture)
    'haut-arriere': ((0.0, 0.4, 1.2), 230, 1, 3.4, 85),      # from the runner's side, rear left
    'haut-poignee': ((0.38, 0.2, 1.15), 237, 1.5, 3.6, 170), # the right handrail and its grip, same camera
    'haut-cardio': ((0.22, 0.38, 1.14), 205, 24, 1.05, 50),  # the right heart-rate grip, from where the runner stands
    'capot-face': ((0.0, 1.0, 0.2), 0, 6, 1.6, 50),
    'capot-arriere': ((-0.05, 0.8, 0.24), 232, 11, 1.5, 50),    # from the runner's side, rear left
    'bout': ((0.22, -0.98, 0.16), 220, 18, 1.3, 50),
}


if not globals().get('AS_LIB_TAPIS'):
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        build(FINISH)
        setup_render(RES, (1, 1))
        SC.render.resolution_x = SC.render.resolution_y = RES
        tgt, az, el, dist, lens = SHOTS[plan]
        if 'cam' in ARGS:                                  # trying an angle: cam=az,el,dist,lens
            az, el, dist, lens = (float(v) for v in ARGS['cam'].split(','))
        loc = shot_camera(tgt, az, el, dist, lens)
        if plan == 'capot-arriere':                        # lit from the front, like the original picture: the hollow stays in shade
            t0, a0, e0, d0, _ = SHOTS['reference']
            a, e = math.radians(a0), math.radians(e0)
            loc = Vector(t0) + Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))) * d0
        light(loc)
        render(os.path.join(OUT, f'tapis-{plan}-{FINISH}{ARGS.get("suffixe", "")}.png'))
