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
# usage: Blender -b --factory-startup -P tapis.py -- plans=reference,profil couleur=noir res=1400 samples=128 out=<dir>
# The current views: rendus-tapis.sh (they go to 3d/prototypes/tapis-de-course/).
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
HAUTES = ARGS.get('poignees_hautes', 'oui')   # the dashboard's two tall upright handles: oui | non


# ------------------------------------------------------------------ materials
FINISHES = {   # the portal: satin metallic paint
    'noir': dict(c=(0.032, 0.033, 0.037), metal=0.55, rough=0.40),
    'graphite': dict(c=(0.11, 0.115, 0.125), metal=0.65, rough=0.38),
    'argent': dict(c=(0.62, 0.63, 0.65), metal=0.9, rough=0.30),
}


def mat_moule(name, color):
    """Moulded plastic: a fine stipple (the mould's texture) and a roughness that varies a little."""
    m = mat(name, color, rough=0.6, spec=0.3, grain=0.3, grain_scale=2600)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = N(nt, 'ShaderNodeTexNoise', Scale=60.0, Detail=5.0); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(maprange(nt, nz.outputs['Fac'], 0.3, 0.7, 0.57, 0.63).outputs['Result'], p.inputs['Roughness'])
    return m


def mat_moletage(name, color, R, pitch=0.0028):
    """Rubber with a diamond knurl, round the axis (local Z) of a cylinder of radius R."""
    m = mat(name, color, rough=0.7, spec=0.3)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    ang = math_node(nt, 'ARCTAN2', sep.outputs['Y'], sep.outputs['X'])
    u = math_node(nt, 'MULTIPLY', ang.outputs[0], v1=R)
    k = 2 * math.pi / pitch
    s1 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'ADD', u.outputs[0], sep.outputs['Z']).outputs[0], v1=k).outputs[0])
    s2 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'SUBTRACT', u.outputs[0], sep.outputs['Z']).outputs[0], v1=k).outputs[0])
    h = math_node(nt, 'MULTIPLY', s1.outputs[0], s2.outputs[0])
    bmp = nt.nodes.new('ShaderNodeBump'); bmp.inputs['Strength'].default_value = 0.7; bmp.inputs['Distance'].default_value = 0.0004
    nt.links.new(h.outputs[0], bmp.inputs['Height']); nt.links.new(bmp.outputs['Normal'], p.inputs['Normal'])
    return m


def mat_moletage_uv(name, color, pitch=0.0026):
    """Rubber with a diamond knurl, drawn from the UVs of sweep_var (metres round and along the tube)."""
    m = mat(name, color, rough=0.68, spec=0.3)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    uv = nt.nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(uv.outputs['UV'], sep.inputs[0])
    k = 2 * math.pi / pitch
    s1 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'ADD', sep.outputs['X'], sep.outputs['Y']).outputs[0], v1=k).outputs[0])
    s2 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'SUBTRACT', sep.outputs['X'], sep.outputs['Y']).outputs[0], v1=k).outputs[0])
    h = math_node(nt, 'MULTIPLY', s1.outputs[0], s2.outputs[0])
    bmp = nt.nodes.new('ShaderNodeBump'); bmp.inputs['Strength'].default_value = 0.75; bmp.inputs['Distance'].default_value = 0.00035
    nt.links.new(h.outputs[0], bmp.inputs['Height']); nt.links.new(bmp.outputs['Normal'], p.inputs['Normal'])
    return m


def mats(finish=FINISH):
    f = FINISHES[finish]
    M = {}
    M['portique'] = mat('portique', f['c'], rough=f['rough'], metal=f['metal'], coat=0.35, coat_rough=0.22,
                        grain=0.05, grain_scale=1200, peel=0.15, peel_scale=160)
    M['jupe'] = mat('jupe', f['c'], rough=f['rough'] + 0.04, metal=f['metal'] * 0.9, coat=0.2, coat_rough=0.3)
    M['rail'] = mat('rail', (0.03, 0.03, 0.033), rough=0.36, metal=0.7, grain=0.1, grain_scale=1500)
    # moulded plastic: matte, a fine grain (the mould's texture), the roughness changes a little: not a toy
    M['plastique'] = mat_moule('plastique', (0.0135, 0.0135, 0.015))
    M['tube'] = mat('tube', (0.017, 0.017, 0.019), rough=0.4, metal=0.35, spec=0.45, coat=0.15, coat_rough=0.3,
                    grain=0.12, grain_scale=1800, peel=0.22, peel_scale=220)          # powder-coated steel
    M['grip'] = mat_moletage_uv('grip', (0.015, 0.015, 0.016))                     # rubber, a diamond knurl
    M['satin'] = mat('satin', (0.016, 0.016, 0.018), rough=0.45, spec=0.4, coat=0.1, coat_rough=0.3, grain=0.15, grain_scale=2600)
    M['cadre_ecran'] = mat('cadre_ecran', (0.025, 0.025, 0.028), rough=0.32, metal=0.6, spec=0.5)   # the rim: dark anodised
    M['gris'] = mat('gris', (0.07, 0.07, 0.075), rough=0.45, spec=0.4)   # printed icons, dark grey
    M['capot'] = mat('capot', (0.013, 0.013, 0.015), rough=0.62, spec=0.26, grain=0.3, grain_scale=2200)
    M['mat'] = mat('plastique_mat', (0.012, 0.012, 0.013), rough=0.7, spec=0.3, grain=0.3, grain_scale=2200)
    M['bande'] = mat('bande', (0.011, 0.011, 0.012), rough=0.82, spec=0.25, grain=0.7, grain_scale=900)
    M['grille'] = mat('grille', (0.004, 0.004, 0.005), rough=0.9, spec=0.1)
    M['chrome'] = mat('chrome', (0.86, 0.86, 0.88), rough=0.07, metal=1.0)
    M['ecran'] = mat('ecran', (0.002, 0.002, 0.0025), rough=0.14, spec=0.5, coat=1.0, coat_rough=0.09)   # the glass over the black print
    M['dalle'] = mat('dalle', (0.007, 0.0075, 0.009), rough=0.14, spec=0.5, coat=1.0, coat_rough=0.09)   # the active area, off
    M['stop'] = mat('stop', (0.36, 0.004, 0.006), rough=0.5, spec=0.28, grain=0.2, grain_scale=2400)   # bright red rubber, satin (stays red under the light)
    M['blanc'] = mat('marquage', (0.78, 0.78, 0.79), rough=0.5, spec=0.4)
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


def resample(P, step):
    """Points every `step` metres along a polyline."""
    out = [P[0]]
    acc = 0.0
    for i in range(1, len(P)):
        a, b = P[i - 1], P[i]
        seg = (b - a).length
        t = step - acc
        while t <= seg:
            out.append(a.lerp(b, t / seg)); t += step
        acc = seg - (t - step)
    if (out[-1] - P[-1]).length > 1e-6:
        out.append(P[-1])
    return out


def sweep_var(name, P, rfun, mats_list, mfun, ring=56, rnom=0.0175):
    """One moulded piece: a tube along the dense path P, its radius rfun(s) changing along it (s: metres from the
    start). mfun(s) gives the material index of each ring of faces. The UVs run round (metres, at rnom) and along,
    so a knurl can be drawn on the grips. Its two ends are closed. Returns the object and the length of each point."""
    S = [0.0]
    for i in range(1, len(P)):
        S.append(S[-1] + (P[i] - P[i - 1]).length)
    T = [(P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]).normalized() for i in range(len(P))]
    up = Vector((0, 0, 1))
    Ns = [(up - T[0] * up.dot(T[0])).normalized()]
    for i in range(1, len(P)):
        Ns.append((Ns[-1] - T[i] * Ns[-1].dot(T[i])).normalized())     # parallel transport: no twist
    verts, faces, fmat, uvs = [], [], [], []
    for i, p in enumerate(P):
        n, b = Ns[i], T[i].cross(Ns[i])
        r = rfun(S[i])
        for k in range(ring):
            a = 2 * math.pi * k / ring
            verts.append(tuple(p + (n * math.cos(a) + b * math.sin(a)) * r))
    for i in range(len(P) - 1):
        mi = mfun((S[i] + S[i + 1]) / 2)
        for k in range(ring):
            k2 = (k + 1) % ring
            faces.append((i * ring + k, i * ring + k2, (i + 1) * ring + k2, (i + 1) * ring + k))
            fmat.append(mi)
            u0, u1 = rnom * 2 * math.pi * k / ring, rnom * 2 * math.pi * (k + 1) / ring
            uvs.append([(u0, S[i]), (u1, S[i]), (u1, S[i + 1]), (u0, S[i + 1])])
    c0 = len(verts); verts.append(tuple(P[0])); c1 = len(verts); verts.append(tuple(P[-1]))
    last = (len(P) - 1) * ring
    for k in range(ring):
        k2 = (k + 1) % ring
        faces.append((c0, k2, k)); fmat.append(mfun(0.0)); uvs.append([(0, 0)] * 3)
        faces.append((c1, last + k, last + k2)); fmat.append(mfun(S[-1])); uvs.append([(0, 0)] * 3)
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
    uvl = me.uv_layers.new(name='UVMap')
    for f, uvq in zip(me.polygons, uvs):
        for li, uv in zip(f.loop_indices, uvq):
            uvl.data[li].uv = uv
    for m in mats_list:
        me.materials.append(m)
    for f, mi in zip(me.polygons, fmat):
        f.material_index = mi; f.use_smooth = True
    o = link(bpy.data.objects.new(name, me))
    fix_normals(o)
    return o, S


def tube(name, pts, r, m, bend=0.05, segs=14, ends=True):
    """A round tube along a 3D polyline, its corners bent, both ends closed by a half sphere (ends=False: flat)."""
    P = fillet3(pts, bend, segs)
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(P) - 1)
    for i, p in enumerate(P):
        sp.points[i].co = (p.x, p.y, p.z, 1.0)
    cu.bevel_mode = 'ROUND'; cu.bevel_depth = r; cu.bevel_resolution = 8
    cu.use_fill_caps = True; cu.twist_mode = 'MINIMUM'
    tmp = link(bpy.data.objects.new(name + '_c', cu))
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    remove(tmp)
    o = link(bpy.data.objects.new(name, me))
    me.materials.append(m)
    for p in me.polygons:
        p.use_smooth = True
    out = [o]
    for e, d in ((P[0], P[0] - P[1]), (P[-1], P[-1] - P[-2])) if ends else ():
        sph = bpy.data.meshes.new(name + '_bout'); bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r)
        bm.to_mesh(sph); bm.free()
        so = link(bpy.data.objects.new(name + '_bout', sph)); sph.materials.append(m)
        for p in sph.polygons:
            p.use_smooth = True
        so.location = e
        out.append(so)
    bpy.context.view_layer.update()
    return join(out, name)


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

    # --- on top: the ring keeps its two arms (the paddle handrails). The dashboard is new (23/11, after the user's
    #     reference, the dashboard of a Technogym Skillrun, without its brand): a wide screen on a column that sits on
    #     the ring's bar, a tray at its foot, a gull-wing handlebar held by the two arms (STOP on top, thumb paddles at
    #     its ends), and two tall upright handles beside the screen (HAUTES=non takes them away).
    st = TOP_Z + UP_W2                                  # top of the portal's bar
    hz = st - 0.105                                     # handrails: their axis
    hxa = UP_X - 0.004                                  # handrails: their axis across
    th2 = 0.026                                         # handrails: half thickness
    zt = st - 0.05                                      # handrails: their top
    for sg in (-1, 1):
        # the handrail: an upright flat paddle, 13 cm tall at its root and 9.5 cm at its D-shaped end
        y0, y1 = top_y - 0.03, top_y - 0.68
        prof = round_poly([(y0, zt - 0.13), (y1, zt - 0.095), (y1, zt), (y0, zt)], [0.0, 0.045, 0.045, 0.0], segs=12)
        pad = prism('main_courante', prof, sg * hxa - th2, sg * hxa + th2, M['plastique'], axis='X')
        rounded(pad, 0.014, 6, angle=35)
        parts.append(pad)
        parts.append(rbox('levre', (0.006, y0 - y1 - 0.03, 0.01), M['plastique'], r=0.0028, segs=2,
                          loc=(sg * (hxa - th2 - 0.001), (y0 + y1 + 0.03) / 2, zt - 0.006)))

    # ---- the dashboard (v3, 24/11, after the user's notes on the Skillrun's):
    # a console body clamped on the ring's bar (two shells, a parting line, an end block over each arm's root);
    # in front of it the tray, one moulded piece with the column: a thick rim, a floor panel with a gutter round it,
    # a slanted rest for a phone, the column's face curving down into the floor; the screen sits over the column.
    hf, hb = top_y - 0.115, top_y + 0.09                # the console body: its front (runner's side) and back
    hx2 = hxa - th2 - 0.002                             # it reaches the inner faces of the two arms
    zt_h, zb_h, zs_h = st + 0.03, st - 0.075, st - 0.02   # its top, bottom and the line between its two shells
    upper = rbox('boitier', (2 * hx2, hb - hf, zt_h - zs_h), M['plastique'], r=0.012, segs=5,
                 loc=(0.0, (hf + hb) / 2, (zt_h + zs_h) / 2))
    pocket = rbox('poche', (0.05, 0.032, 0.03), M['plastique'], r=0.006, segs=3, loc=(-0.24, top_y - 0.075, zt_h))
    boolean(upper, pocket); bake(upper, sharp=40); remove(pocket)      # a small pocket left of the column
    parts.append(upper)
    parts.append(rbox('poche_fond', (0.044, 0.026, 0.002), M['mat'], r=0.003, segs=1, loc=(-0.24, top_y - 0.075, zt_h - 0.0145)))
    parts.append(rbox('boitier_bas', (2 * hx2 - 0.006, hb - hf - 0.006, zs_h - zb_h), M['plastique'], r=0.01, segs=4,
                      loc=(0.0, (hf + hb) / 2, (zs_h + zb_h) / 2 - 0.0015)))
    for sg in (-1, 1):                                   # the two ends: a rounded block over the root of each arm
        parts.append(rbox('boitier_bout', (0.075, 0.2, zt_h - (zt - 0.03)), M['plastique'], r=0.028, segs=7,
                          loc=(sg * (hx2 + 0.012), top_y - 0.075, (zt_h + zt - 0.03) / 2)))

    # the tray: a rounded block that sticks out towards the runner; a rim band on top, the lower body set in 1.5 mm
    tx, ty0, ty1 = 0.175, top_y - 0.25, top_y - 0.06    # half width, front, back (inside the column)
    tzt, tzb, tz_line = zt_h + 0.008, zs_h - 0.03, zt_h + 0.008 - 0.024
    def plan(x2, y0, y1, r, segs=10):
        return round_poly([(-x2, y0), (x2, y0), (x2, y1), (-x2, y1)], [r, r, r * 0.3, r * 0.3], segs=segs)
    def slab_xy(name, outline, z0, z1, m, rb):
        n = len(outline)
        o = mesh_obj(name, [(x, y, z) for z in (z0, z1) for x, y in outline],
                     [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)],
                     m, smooth=False)
        return rounded(o, rb, 4, angle=30) if rb else fix_normals(o)
    rim = slab_xy('bac', plan(tx, ty0, ty1, 0.03), tz_line, tzt, M['plastique'], 0.007)
    yc = top_y - 0.095                                   # the column's face, at its foot (the back of the cavity)
    floor_z = tzt - 0.03
    cav = slab_xy('bac_creux', plan(tx - 0.022, ty0 + 0.022, yc + 0.03, 0.014), floor_z, tzt + 0.02, M['plastique'], 0.0)
    boolean(rim, cav); bake(rim, sharp=40); remove(cav)
    parts.append(rim)
    body = slab_xy('bac_corps', plan(tx - 0.0015, ty0 + 0.0015, ty1, 0.0285), tzb, tz_line - 0.0006, M['plastique'], 0.004)
    parts.append(body)
    # the floor: a panel 2.5 mm proud, a gutter all round it along the walls
    parts.append(slab_xy('bac_fond', plan(tx - 0.03, ty0 + 0.03, yc - 0.012, 0.008), floor_z - 0.002, floor_z + 0.0025, M['plastique'], 0.0012))
    parts.append(slab_xy('bac_gouttiere', plan(tx - 0.022, ty0 + 0.022, yc, 0.014), floor_z - 0.003, floor_z - 0.0015, M['mat'], 0.0))
    # the slanted rest across the back of the floor, cut by two notches (for a cable)
    rest = Vector((0.0, yc - 0.034, floor_z + 0.012))
    for x0, x1 in ((-0.13, -0.075), (-0.055, 0.055), (0.075, 0.13)):
        parts.append(rbox('cale_telephone', (x1 - x0, 0.007, 0.03), M['plastique'], r=0.0025, segs=2,
                          loc=rest + Vector(((x0 + x1) / 2, 0, 0)), rot=(-28, 0, 0)))
    parts.append(rbox('cale_pied', (0.26, 0.026, 0.006), M['plastique'], r=0.002, segs=2, loc=rest + Vector((0, 0.004, -0.009))))

    # the column, one piece with the tray: its face goes up from the floor through a concave curve; narrower and
    # lower than before (24 x 7 cm), leaning back like the screen; a seam runs down each side behind the front cover
    lean = 12
    r_f, col_h, col_d, col_w = 0.03, 0.17, 0.07, 0.24
    arc = [(yc - r_f + r_f * math.sin(math.radians(t)), floor_z + r_f - r_f * math.cos(math.radians(t))) for t in range(0, 91, 10)]
    top_f = (yc + col_h * math.sin(math.radians(lean)), floor_z + r_f + col_h)
    top_b = (top_f[0] + col_d, top_f[1] - 0.01)
    prof = arc + [top_f, top_b, (top_b[0] + 0.01, zb_h + 0.01), (yc - r_f - 0.02, zb_h + 0.01), (yc - r_f - 0.02, floor_z)]
    radii = [0.0] * len(arc) + [0.01, 0.01, 0.0, 0.0, 0.0]
    col = prism('colonne', round_poly(prof, radii, segs=8), -col_w / 2, col_w / 2, M['plastique'], axis='X')
    rounded(col, 0.006, 4, angle=35)
    parts.append(col)
    Rl = Euler((math.radians(-lean), 0, 0)).to_matrix()
    up_c, fwd_c = Rl @ Vector((0, 0, 1)), Rl @ Vector((0, -1, 0))
    foot = Vector((0.0, yc, floor_z + r_f))
    for sg in (-1, 1):
        g = foot + up_c * (col_h / 2) - fwd_c * 0.012 + Vector((sg * (col_w / 2 + 0.0003), 0, 0))
        parts.append(rbox('colonne_joint', (0.0012, 0.0016, col_h - 0.01), M['grille'], r=0, loc=g, rot=(-lean, 0, 0)))
    # on its face: the wireless charging plate (a dark plate, a ring with a phone in it) and the contactless mark
    pc = foot + up_c * 0.085 + fwd_c * 0.0008 + Vector((0.025, 0, 0))
    parts.append(rbox('recharge', (0.13, 0.002, 0.095), M['mat'], r=0.006, segs=2, loc=pc, rot=(-lean, 0, 0)))
    ring_c = pc + fwd_c * 0.0012
    parts.append(cyl('recharge_anneau', ring_c, ring_c + fwd_c * 0.0004, 0.017, M['gris']))
    parts.append(cyl('recharge_anneau_fond', ring_c + fwd_c * 0.0002, ring_c + fwd_c * 0.0006, 0.0155, M['mat']))
    parts.append(rbox('recharge_tel', (0.008, 0.0008, 0.014), M['gris'], r=0.0015, segs=1, loc=ring_c + fwd_c * 0.0007, rot=(-lean, 0, 0)))
    nfc = foot + up_c * 0.07 + fwd_c * 0.0008 + Vector((-0.09, 0, 0))
    for k, rr in enumerate((0.002, 0.004, 0.006)):
        parts.append(cyl('sans_contact', nfc + fwd_c * (0.0003 * k), nfc + fwd_c * (0.0003 * k + 0.0003), rr, M['gris'] if k % 2 == 0 else M['plastique']))
    # the safety key, red, on the console's front, left of the tray
    parts.append(rbox('cle_socle', (0.046, 0.006, 0.032), M['mat'], r=0.003, segs=1, loc=(-0.23, hf - 0.001, zs_h - 0.02)))
    parts.append(rbox('cle', (0.032, 0.012, 0.022), M['stop'], r=0.004, segs=2, loc=(-0.23, hf - 0.005, zs_h - 0.02)))

    # the screen (22 inches): a thin rim round edge-to-edge glass, the glass a hair under the rim; under the glass the
    # black border and the active area, which an off screen shows as a slightly lighter rectangle; a back shell behind.
    tilt = 16
    Rs = Euler((math.radians(-tilt), 0, 0)).to_matrix()
    up_s, fwd_s = Rs @ Vector((0, 0, 1)), Rs @ Vector((0, -1, 0))
    sw, sh, sd = 0.53, 0.32, 0.024
    col_top = Vector((0.0, top_f[0] + col_d / 2, top_f[1]))
    sc = col_top + up_s * (sh / 2 - 0.045) + fwd_s * (col_d / 2 + sd / 2 - 0.006)
    def screen_part(name, w, h, y0, y1, r, m, rb, dz=0.0):
        o = prism(name, round_poly([(-w / 2, -h / 2 + dz), (w / 2, -h / 2 + dz), (w / 2, h / 2 + dz), (-w / 2, h / 2 + dz)], r, segs=10),
                  y0, y1, m, axis='Y')
        if rb:
            rounded(o, rb, 4, angle=30)
        else:
            fix_normals(o)
        o.rotation_euler = (math.radians(-tilt), 0, 0); o.location = sc
        return o
    parts.append(screen_part('ecran_cadre', sw, sh, -sd / 2, sd / 2, 0.02, M['cadre_ecran'], 0.0035))
    parts.append(screen_part('ecran_verre', sw - 0.007, sh - 0.007, -sd / 2 - 0.0002, -sd / 2 + 0.004, 0.0165, M['ecran'], 0.0006))
    parts.append(screen_part('ecran_dalle', sw - 0.046, sh - 0.058, -sd / 2 - 0.00028, -sd / 2 - 0.00022, 0.002, M['dalle'], 0.0, dz=0.004))
    parts.append(screen_part('ecran_dos', 0.4, 0.22, sd / 2 - 0.002, sd / 2 + 0.014, 0.03, M['plastique'], 0.006, dz=-0.02))

    # the tall handles: out of the housing's two ends through a collar, a wide bend, then straight up beside the screen
    if HAUTES == 'oui':
        for sg in (-1, 1):
            zh = zt_h - 0.032
            xh = sg * 0.335                               # just outside the screen, like the Skillrun
            p0 = Vector((xh, top_y - 0.03, zs_h))         # inside the housing
            p1 = Vector((xh, top_y - 0.17, zt_h + 0.07))  # out of its top towards the runner...
            p2 = Vector((xh, top_y - 0.09, st + 0.45))    # ...then a wide bend, and straight up
            parts.append(tube('poignee_haute', [p0, p1, p2], 0.02, M['tube'], bend=0.09, ends=False))
            dq = (p1 - p0).normalized()                   # the collar where it leaves the top of the housing
            q = p0 + dq * ((zt_h - p0.z) / dq.z)
            parts.append(cyl('poignee_haute_bague', q - dq * 0.01, q + dq * 0.008, 0.026, M['plastique']))
            d = (p2 - p1).normalized()
            parts.append(cyl('poignee_haute_bouchon', p2 - d * 0.004, p2 + d * 0.006, 0.0205, M['plastique']))
            parts.append(cyl('poignee_haute_bouchon_fond', p2 + d * 0.006, p2 + d * 0.0075, 0.015, M['mat']))

    # the handlebar (v3): ONE moulded piece. An arch held by the two arms; at its top, in the middle, it swells into a
    # smooth knuckle whose top is the bright red STOP, set in and following the curve; down each side the part where
    # the hand goes is a little thicker and knurled, with a parting line at both ends; near each end a moulded collar
    # carries the thumb paddle (+ on top, - under it).
    xe = hxa - th2 + 0.004
    mid = Vector((0.0, ty0 - 0.06, st - 0.012))
    def wing(sg):
        return [Vector((sg * xe, top_y - 0.33, hz - 0.01)), Vector((sg * 0.3, top_y - 0.335, hz - 0.012)),
                Vector((sg * 0.165, mid.y + 0.01, st - 0.062)), Vector((sg * 0.05, mid.y, mid.z))]
    P = resample(fillet3(wing(-1) + wing(1)[::-1], 0.06, segs=24), 0.0018)
    S = [0.0]
    for i in range(1, len(P)):
        S.append(S[-1] + (P[i] - P[i - 1]).length)
    L = S[-1]; Lh = L / 2
    def s_of(v):
        return S[min(range(len(P)), key=lambda i: (P[i] - v).length)]
    wl = wing(-1)
    sA, sB = s_of(wl[1]), s_of(wl[2])
    sC = s_of(wl[0].lerp(wl[1], 0.5))
    grips = [(sA + 0.045, sB - 0.02), (L - (sB - 0.02), L - (sA + 0.045))]
    collars = [sC, L - sC]
    r0, r_k, k_flat, k_ramp = 0.0175, 0.037, 0.034, 0.05
    def smooth01(t):
        t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
    seams = [Lh - k_flat - k_ramp, Lh + k_flat + k_ramp] + [e for g in grips for e in g] + \
            [c + d for c in collars for d in (-0.017, 0.017)]
    def rfun(s_):
        r = r0
        d = abs(s_ - Lh)                                  # the knuckle: a flat top, smooth ramps
        r += (r_k - r0) * (1 - smooth01((d - k_flat) / k_ramp))
        for g0, g1 in grips:                              # the grips: 2 mm thicker, eased in and out
            r += 0.002 * smooth01((s_ - g0) / 0.006) * smooth01((g1 - s_) / 0.006)
        for c in collars:                                 # the paddles' collars
            r += 0.0055 * (1 - smooth01((abs(s_ - c) - 0.012) / 0.005))
        for z in seams:                                   # parting lines: a fine groove
            r -= 0.0007 * math.exp(-((s_ - z) / 0.0011) ** 2)
        return r
    def mfun(s_):
        if any(g0 <= s_ <= g1 for g0, g1 in grips):
            return 1
        if abs(s_ - Lh) < k_flat + k_ramp or any(abs(s_ - c) < 0.017 for c in collars):
            return 2
        return 0
    bar, _ = sweep_var('guidon', P, rfun, [M['tube'], M['grip'], M['satin']], mfun)
    parts.append(bar)
    # the STOP: the top of the knuckle, a skin 1.2 mm thick in bright red rubber, set on it
    bm = bmesh.new(); bm.from_mesh(bar.data); bm.faces.ensure_lookup_table()
    ring = 56
    keep = []
    for f in bm.faces:
        i = f.index // ring
        if i >= len(P) - 1:
            continue
        sm = (S[i] + S[i + 1]) / 2
        if abs(sm - Lh) < 0.044 and f.normal.z > 0.55:
            keep.append(f.index)
    bm.free()
    stop_me = bar.data.copy()
    bm = bmesh.new(); bm.from_mesh(stop_me); bm.faces.ensure_lookup_table()
    drop = [f for f in bm.faces if f.index not in set(keep)]
    bmesh.ops.delete(bm, geom=drop, context='FACES')
    for v in bm.verts:
        v.co += v.normal * 0.0002
    bm.to_mesh(stop_me); bm.free()
    stop_me.materials.clear(); stop_me.materials.append(M['stop'])
    stop = link(bpy.data.objects.new('stop', stop_me))
    sol = stop.modifiers.new('epaisseur', 'SOLIDIFY'); sol.thickness = 0.0012; sol.offset = 1.0
    bake(stop, sharp=60)
    parts.append(stop)
    top = P[min(range(len(P)), key=lambda i: abs(S[i] - Lh))]
    t = text_mesh('stop_texte', 'STOP', 0.1, 0.00025, M['blanc'], font=F_BIG, fit_h=0.0135)
    t.location = top + Vector((0, 0, rfun(Lh) + 0.0016)); parts.append(t)
    # the thumb paddles: a thin blade growing out of each collar, leaning back; + at the top, - at the bottom
    for c, sg in ((collars[0], -1), (collars[1], 1)):
        c0 = P[min(range(len(P)), key=lambda i: abs(S[i] - c))]
        blade = prism('palette', round_poly([(-0.016, -0.012), (0.016, -0.012), (0.0105, 0.072), (-0.0105, 0.072)],
                                            [0.002, 0.002, 0.0098, 0.0098], segs=10), -0.0085, 0.0085, M['satin'], axis='Y')
        for v in blade.data.vertices:                    # a blade that thins towards its top
            v.co.y *= 1.0 - 0.35 * max(0.0, v.co.z) / 0.072
        rounded(blade, 0.0035, 4, angle=30)
        blade.rotation_euler = (math.radians(-12), 0, 0)
        blade.location = c0 + Vector((0, 0.001, r0 + 0.004))
        parts.append(blade)
        Rf = Euler((math.radians(-12), 0, 0)).to_matrix()
        fu, ff = Rf @ Vector((0, 0, 1)), Rf @ Vector((0, -1, 0))
        base_f = blade.location + ff * 0.0086
        tp = text_mesh('palette_plus', '+', 0.1, 0.00025, M['blanc'], font=F_BIG, fit_h=0.013)
        tp.rotation_euler = (math.radians(78), 0, 0); tp.location = base_f + fu * 0.05 - ff * 0.0015
        parts.append(tp)
        parts.append(rbox('palette_moins', (0.01, 0.0006, 0.0024), M['blanc'], r=0, loc=base_f + fu * 0.012, rot=(-12, 0, 0)))
        parts.append(rbox('palette_trait', (0.015, 0.0006, 0.0007), M['gris'], r=0, loc=base_f + fu * 0.031 - ff * 0.0008, rot=(-12, 0, 0)))
    # the handlebar's middle is held from under the tray
    parts.append(cyl('guidon_tige', mid + Vector((0, 0.02, -0.02)), Vector((0.0, ty0 + 0.04, tzb + 0.005)), 0.016, M['tube']))
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
    world_hdri(0.38, rot=30)
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
    'plongee': ((0.0, 0.05, 0.62), 38, 34, 4.3, 40),         # from above, three-quarter front right
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
    'tdb-face': ((0.0, 0.45, 1.42), 180, 1, 2.0, 50),        # the dashboard, from where the runner stands (bar height)
    'tdb-34': ((0.0, 0.42, 1.34), 215, 14, 2.1, 50),         # the dashboard, three-quarter from the runner's left
    'tdb-detail': ((-0.06, 0.33, 1.24), 208, 30, 0.95, 50),  # the tray, the STOP, the left grip
    'tdb-dos': ((0.0, 0.5, 1.4), 20, 4, 1.7, 50),             # the back of the screen and the column
    'tdb-ecran': ((0.0, 0.52, 1.5), 180, 10, 1.05, 50),      # the screen, from the runner
    'tdb-palette': ((0.3, 0.2, 1.17), 196, 14, 0.62, 50),    # the right thumb paddle and its grip
    'tdb-stop': ((-0.03, 0.22, 1.24), 200, 34, 0.55, 50),    # the STOP and the left grip, close
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
