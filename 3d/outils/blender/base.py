# Shared Blender helpers for the fitness app's 3D library: arguments, scene reset, materials, meshes, text,
# studio (cyclorama + lights), camera and render settings. Every model script starts with: exec(open(base.py).read()).
# Run in the background:  Blender -b --factory-startup -P <script.py> -- key=value ...
import bpy, bmesh, math, sys, os
from mathutils import Vector, Matrix, Euler

ARGS = {}
if '--' in sys.argv:
    for a in sys.argv[sys.argv.index('--') + 1:]:
        if '=' in a:
            k, v = a.split('=', 1)
            ARGS[k] = v
RES = int(ARGS.get('res', 960))
SAMPLES = int(ARGS.get('samples', 32))
OUT = ARGS.get('out', '/tmp/fitness-3d')
SC = bpy.context.scene
FONT_NUM = '/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'   # prototypes only (Apple font): an open font for the app


def reset():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.curves):
        for d in list(coll):
            coll.remove(d)


def link(o):
    SC.collection.objects.link(o)
    return o


# ------------------------------------------------------------------ materials
def _in(p, names, v):
    for n in names:
        if n in p.inputs:
            p.inputs[n].default_value = v
            return


def mat(name, color, rough=0.5, metal=0.0, coat=0.0, coat_rough=0.1, spec=0.5, aniso=0.0,
        grain=0.0, grain_scale=1500.0, peel=0.0, peel_scale=300.0):
    """Principled material. grain = fine noise bump (rubber, cast), peel = larger soft bump (paint orange peel)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    _in(p, ('Specular IOR Level', 'Specular'), spec)
    _in(p, ('Coat Weight', 'Clearcoat'), coat)
    _in(p, ('Coat Roughness', 'Clearcoat Roughness'), coat_rough)
    _in(p, ('Anisotropic',), aniso)
    if grain or peel:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        last = None
        for amt, scale, dist in ((grain, grain_scale, 0.00015), (peel, peel_scale, 0.0006)):
            if not amt:
                continue
            nz = nt.nodes.new('ShaderNodeTexNoise')
            nz.inputs['Scale'].default_value = scale
            nz.inputs['Detail'].default_value = 6.0
            b = nt.nodes.new('ShaderNodeBump')
            b.inputs['Strength'].default_value = amt
            b.inputs['Distance'].default_value = dist
            nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
            nt.links.new(nz.outputs['Fac'], b.inputs['Height'])
            if last:
                nt.links.new(last.outputs['Normal'], b.inputs['Normal'])
            last = b
        nt.links.new(last.outputs['Normal'], p.inputs['Normal'])
    return m


def mat_knurl(name, color, rough, metal, axis_len, pitch=0.0011, depth=0.6, bands=None):
    """Steel with a diamond knurl along the object's X axis (bars, dumbbell handles).
    bands = list of (x0, x1) where the knurl is cut; elsewhere the steel stays smooth."""
    m = mat(name, color, rough=rough, metal=metal)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    N = nt.nodes.new
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    at = N('ShaderNodeMath'); at.operation = 'ARCTAN2'
    nt.links.new(sep.outputs['Z'], at.inputs[0]); nt.links.new(sep.outputs['Y'], at.inputs[1])
    # u = angle * r (r ~ handle radius, so the diamonds stay square), v = x
    u = N('ShaderNodeMath'); u.operation = 'MULTIPLY'; u.inputs[1].default_value = 0.016
    nt.links.new(at.outputs[0], u.inputs[0])
    k = 2 * math.pi / pitch
    def wave(sign):
        s = N('ShaderNodeMath'); s.operation = 'ADD' if sign > 0 else 'SUBTRACT'
        nt.links.new(u.outputs[0], s.inputs[0]); nt.links.new(sep.outputs['X'], s.inputs[1])
        mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = k
        nt.links.new(s.outputs[0], mu.inputs[0])
        si = N('ShaderNodeMath'); si.operation = 'SINE'
        nt.links.new(mu.outputs[0], si.inputs[0])
        ab = N('ShaderNodeMath'); ab.operation = 'ABSOLUTE'
        nt.links.new(si.outputs[0], ab.inputs[0])
        return ab
    a, b = wave(1), wave(-1)
    mn = N('ShaderNodeMath'); mn.operation = 'MINIMUM'
    nt.links.new(a.outputs[0], mn.inputs[0]); nt.links.new(b.outputs[0], mn.inputs[1])
    h = mn
    if bands:
        # mask = 1 inside any band (|x| between x0 and x1)
        ax = N('ShaderNodeMath'); ax.operation = 'ABSOLUTE'
        nt.links.new(sep.outputs['X'], ax.inputs[0])
        acc = None
        for x0, x1 in bands:
            g = N('ShaderNodeMath'); g.operation = 'GREATER_THAN'; g.inputs[1].default_value = x0
            l = N('ShaderNodeMath'); l.operation = 'LESS_THAN'; l.inputs[1].default_value = x1
            nt.links.new(ax.outputs[0], g.inputs[0]); nt.links.new(ax.outputs[0], l.inputs[0])
            mm = N('ShaderNodeMath'); mm.operation = 'MULTIPLY'
            nt.links.new(g.outputs[0], mm.inputs[0]); nt.links.new(l.outputs[0], mm.inputs[1])
            if acc is None:
                acc = mm
            else:
                mx = N('ShaderNodeMath'); mx.operation = 'MAXIMUM'
                nt.links.new(acc.outputs[0], mx.inputs[0]); nt.links.new(mm.outputs[0], mx.inputs[1]); acc = mx
        hm = N('ShaderNodeMath'); hm.operation = 'MULTIPLY'
        nt.links.new(mn.outputs[0], hm.inputs[0]); nt.links.new(acc.outputs[0], hm.inputs[1])
        inv = N('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
        nt.links.new(acc.outputs[0], inv.inputs[1])
        h = N('ShaderNodeMath'); h.operation = 'ADD'
        nt.links.new(hm.outputs[0], h.inputs[0]); nt.links.new(inv.outputs[0], h.inputs[1])
        # the knurled band is a bit rougher and darker in the grooves
        rr = N('ShaderNodeMapRange')
        nt.links.new(acc.outputs[0], rr.inputs['Value'])
        rr.inputs['To Min'].default_value = rough
        rr.inputs['To Max'].default_value = min(1.0, rough + 0.18)
        nt.links.new(rr.outputs['Result'], p.inputs['Roughness'])
    bu = N('ShaderNodeBump'); bu.inputs['Strength'].default_value = depth; bu.inputs['Distance'].default_value = 0.0004
    nt.links.new(h.outputs[0], bu.inputs['Height'])
    nt.links.new(bu.outputs['Normal'], p.inputs['Normal'])
    return m


# ------------------------------------------------------------------ meshes
def mesh_obj(name, verts, faces, m=None, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    o = link(bpy.data.objects.new(name, me))
    if m:
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


def round_poly(pts, radius, segs=6, closed=True):
    """Rounds the corners of a 2D polyline (list of (a, b)). radius = float or list per point (0 = sharp)."""
    n = len(pts)
    out = []
    for i in range(n):
        r = radius[i] if isinstance(radius, (list, tuple)) else radius
        p = Vector(pts[i])
        if (not closed and i in (0, n - 1)) or r <= 0:
            out.append(tuple(p)); continue
        a, c = Vector(pts[i - 1]), Vector(pts[(i + 1) % n])
        da, dc = (a - p), (c - p)
        la, lc = da.length, dc.length
        d = min(r, la * 0.49, lc * 0.49)
        p0, p2 = p + da.normalized() * d, p + dc.normalized() * d
        for s in range(segs + 1):            # quadratic Bezier between the two tangent points
            t = s / segs
            q = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p + t ** 2 * p2
            out.append((q.x, q.y))
    return out


def lathe(name, profile, m=None, segs=128, axis='Y', edge_mats=None, mats=None):
    """Revolves a closed profile [(r, h)] around an axis (Y: plates standing up, X: dumbbells/bars).
    edge_mats = material index per profile edge (edge i goes from point i to i+1), mats = the materials."""
    verts, faces = [], []
    n = len(profile)
    for j in range(segs):
        a = 2 * math.pi * j / segs
        ca, sa = math.cos(a), math.sin(a)
        for r, h in profile:
            if axis == 'Y':
                verts.append((r * ca, h, r * sa))
            else:
                verts.append((h, r * ca, r * sa))
    for j in range(segs):
        j2 = (j + 1) % segs
        for i in range(n):
            i2 = (i + 1) % n
            faces.append((j * n + i, j * n + i2, j2 * n + i2, j2 * n + i))
    o = mesh_obj(name, verts, faces, m)
    if edge_mats and mats:
        o.data.materials.clear()
        for mm in mats:
            o.data.materials.append(mm)
        for f in o.data.polygons:
            f.material_index = edge_mats[f.index % n]
    if any(r < 1e-9 for r, h in profile):       # points on the axis: merge the duplicates
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
        bm.to_mesh(o.data)
        bm.free()
    return o


def prism(name, outline, y0, y1, m=None, axis='Y'):
    """Extrudes a closed 2D outline [(x, z)] between y0 and y1 (axis Y), or [(y, z)] between x0, x1 (axis X)."""
    n = len(outline)
    verts = []
    for y in (y0, y1):
        for a, b in outline:
            verts.append((a, y, b) if axis == 'Y' else (y, a, b))
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    for i in range(n):
        i2 = (i + 1) % n
        faces.append((i, i2, n + i2, n + i))
    o = mesh_obj(name, verts, faces, m, smooth=False)
    return o


def regular_outline(r, sides, rot=0.0):
    return [(r * math.cos(rot + 2 * math.pi * i / sides), r * math.sin(rot + 2 * math.pi * i / sides)) for i in range(sides)]


def boolean(o, cutter, op='DIFFERENCE'):
    md = o.modifiers.new('bool', 'BOOLEAN')
    md.operation = op
    md.solver = 'EXACT'
    md.object = cutter
    cutter.hide_render = True
    cutter.hide_viewport = True
    return md


def bevel(o, width, segs=3, angle=40):
    md = o.modifiers.new('bevel', 'BEVEL')
    md.width = width
    md.segments = segs
    md.limit_method = 'ANGLE'
    md.angle_limit = math.radians(angle)
    md.harden_normals = False
    return md


def bake(o, sharp=40):
    """Applies the modifiers (new mesh from the evaluated object) and smooths by angle."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    old = o.data
    o.modifiers.clear()
    o.data = me
    bpy.data.meshes.remove(old)
    for p in me.polygons:
        p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(sharp))
    except AttributeError:
        pass
    return o


def remove(o):
    bpy.data.objects.remove(o, do_unlink=True)


def text_mesh(name, body, size, depth, m, font=FONT_NUM, spacing=1.0, bevel=0.0, fit_h=None, max_w=None):
    """Centered text as a mesh in its local XY plane, extruded along Z (total thickness 2*depth).
    fit_h: scales the glyphs so the text is exactly that tall (same size whatever the font); max_w caps the width."""
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.font = bpy.data.fonts.load(font, check_existing=True)
    cu.size = size
    cu.extrude = depth
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.space_character = spacing
    cu.resolution_u = 6
    if bevel:
        cu.bevel_depth = bevel
        cu.bevel_resolution = 2
    tmp = link(bpy.data.objects.new(name + '_c', cu))
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    remove(tmp)
    if fit_h or max_w:
        xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        k = (fit_h / h) if fit_h else 1.0
        if max_w:
            k = min(k, max_w / w) if fit_h else max_w / w
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        me.transform(Matrix.Translation((-cx, -cy, 0)))
        me.transform(Matrix.Diagonal((k, k, 1.0, 1.0)))
    o = link(bpy.data.objects.new(name, me))
    me.materials.append(m)
    return o


def join(objs, name):
    """Joins meshes into the first one (keeps their transforms)."""
    base = objs[0]
    bm = bmesh.new()
    mats = []
    for o in objs:
        me = o.data.copy()
        me.transform(o.matrix_world)
        offset = len(mats)
        for mm in me.materials:
            mats.append(mm)
        for p in me.polygons:
            p.material_index += offset
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for mm in mats:
        me.materials.append(mm)
    for o in objs:
        remove(o)
    out = link(bpy.data.objects.new(name, me))
    return out


def group(name, objs):
    """An empty parent so a whole piece can be moved and turned."""
    e = link(bpy.data.objects.new(name, None))
    for o in objs:
        o.parent = e
    return e


# ------------------------------------------------------------------ studio
def cyclo(tone, dark=False):
    """Curved studio backdrop (floor that bends up into a back wall), facing -Y."""
    rr, cy = 1.2, 2.2
    prof = [(-14.0, 0.0)] + [(cy + rr * math.sin(math.pi / 2 * i / 16), rr - rr * math.cos(math.pi / 2 * i / 16)) for i in range(17)] + [(cy + rr, 12.0)]
    verts, faces = [], []
    for x in (-30.0, 30.0):
        for y, z in prof:
            verts.append((x, y, z))
    n = len(prof)
    for j in range(n - 1):
        faces.append((j, n + j, n + j + 1, j + 1))
    m = mat('cyclo', (tone, tone, tone * 1.02), rough=0.95 if dark else 0.75, spec=0.04 if dark else 0.3)
    return mesh_obj('cyclo', verts, faces, m)


def area(name, loc, target, power, size, color=(1, 1, 1), shape='SQUARE', size_y=None):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = power
    ld.color = color
    ld.shape = shape
    ld.size = size
    if size_y:
        ld.size_y = size_y
    o = link(bpy.data.objects.new(name, ld))
    o.location = loc
    aim(o, target)
    return o


def aim(o, target):
    d = Vector(target) - Vector(o.location)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def studio(dark=False, center=(0, 0, 0.2), k=1.0):
    """Product studio. Light grey or near-black backdrop; big soft key, strip rims for black objects."""
    tone = 0.0035 if dark else 0.26
    k = k * float(ARGS.get('lum', 1.0))
    cyclo(tone, dark)
    w = bpy.data.worlds.new('w')
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs['Color'].default_value = (tone * 0.6, tone * 0.6, tone * 0.62, 1)
    bg.inputs['Strength'].default_value = 1.0
    SC.world = w
    c = Vector(center)
    area('key', c + Vector((-1.6, -1.9, 1.7)), c, (125 if dark else 150) * k, 2.2, (1.0, 0.97, 0.94))
    area('fill', c + Vector((2.2, -1.6, 0.5)), c, (8 if dark else 22) * k, 2.6, (0.94, 0.97, 1.0))
    area('rim_r', c + Vector((1.5, 1.2, 0.9)), c, (260 if dark else 130) * k, 0.25, (0.95, 0.97, 1.0), 'RECTANGLE', 2.2)
    area('rim_l', c + Vector((-1.7, 1.0, 1.1)), c, (180 if dark else 70) * k, 0.25, (1.0, 0.98, 0.96), 'RECTANGLE', 2.0)
    area('top', c + Vector((0.2, 0.1, 2.4)), c, (30 if dark else 55) * k, 1.6, (1, 1, 1))


def camera(loc, target, lens=70, fstop=8.0, focus=None, shift_y=0.0):
    cd = bpy.data.cameras.new('cam')
    cd.lens = lens
    cd.sensor_width = 36
    cd.shift_y = shift_y
    o = link(bpy.data.objects.new('cam', cd))
    o.location = loc
    aim(o, target)
    cd.dof.use_dof = fstop < 30
    cd.dof.aperture_fstop = fstop
    cd.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    SC.camera = o
    return o


def setup_render(res=None, aspect=(16, 9)):
    try:
        SC.render.engine = 'CYCLES'
    except TypeError:
        pass
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        SC.cycles.device = 'GPU'
    except Exception as e:
        print('GPU indisponible', e)
    SC.cycles.samples = SAMPLES
    SC.cycles.use_denoising = True
    SC.cycles.max_bounces = 10
    SC.cycles.glossy_bounces = 6
    SC.cycles.sample_clamp_indirect = 8.0
    SC.cycles.blur_glossy = 0.5
    r = res or RES
    SC.render.resolution_x = r
    SC.render.resolution_y = int(r * aspect[1] / aspect[0])
    SC.render.resolution_percentage = 100
    try:
        SC.view_settings.view_transform = 'AgX'
    except TypeError:
        pass
    for lk in ('AgX - Medium High Contrast', 'Medium High Contrast'):
        try:
            SC.view_settings.look = lk
            break
        except TypeError:
            continue
    SC.render.image_settings.file_format = 'PNG'
    SC.render.image_settings.color_mode = 'RGB'


def render(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    SC.render.filepath = path
    SC.render.image_settings.color_mode = 'RGBA' if SC.render.film_transparent else 'RGB'
    bpy.ops.render.render(write_still=True)
    print('rendu', path)
