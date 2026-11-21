# Step 5 (21/11/2026): textures, colours and design variations of the plate and the round dumbbell (font A, Archivo).
# Reuses the models of poids2.py; this script only changes the materials, the lighting (a real studio HDRI) and the shots.
# usage: Blender -b --factory-startup -P poids3.py -- piece=disque|haltere groupe=texture|couleur|design variantes=a,b plans=face,rasant res=1400 samples=96 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB = True
ARGV_KEEP = True
exec(open(os.path.join(HERE, 'poids2.py')).read())
F_BIG = os.path.join(POL, 'Archivo-ExpandedExtraBold.ttf')
F_SMALL = os.path.join(POL, 'Archivo-ExpandedSemiBold.ttf')

GROUPE = ARGS.get('groupe', 'texture')
VARS = ARGS.get('variantes', 'moule').split(',')
PLANS = ARGS.get('plans', 'face').split(',')
HDRI = os.path.join(HERE, '..', 'assets', 'hdri', ARGS.get('hdri', 'studio_small_09_2k.hdr'))


def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


# name, colour, text colour (w = white, k = charcoal)
PALETTE = {
    'noir': ('#1B1B1D', 'w'), 'graphite': ('#3C3E42', 'w'), 'blanc': ('#E4E2DD', 'k'), 'rose': ('#D98A9B', 'w'),
    'bleu': ('#1F4B86', 'w'), 'vert': ('#5E7A62', 'w'), 'rouge': ('#8B2D32', 'w'), 'sable': ('#CBB89D', 'k'),
}
WHITE = (0.8, 0.8, 0.81)
CHARCOAL = (0.03, 0.03, 0.032)


# ------------------------------------------------------------------ materials
def N(nt, kind, **inputs):
    n = nt.nodes.new(kind)
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def math_node(nt, op, a=None, b=None, v0=None, v1=None):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op
    if a is not None: nt.links.new(a, n.inputs[0])
    elif v0 is not None: n.inputs[0].default_value = v0
    if b is not None: nt.links.new(b, n.inputs[1])
    elif v1 is not None: n.inputs[1].default_value = v1
    return n


def maprange(nt, val, a, b, c, d, clamp=True):
    n = nt.nodes.new('ShaderNodeMapRange')
    nt.links.new(val, n.inputs['Value'])
    n.inputs['From Min'].default_value, n.inputs['From Max'].default_value = a, b
    n.inputs['To Min'].default_value, n.inputs['To Max'].default_value = c, d
    n.clamp = clamp
    return n


def mix_col(nt, fac, c1, c2):
    """c1, c2: sockets or RGBA tuples."""
    n = nt.nodes.new('ShaderNodeMix'); n.data_type = 'RGBA'
    nt.links.new(fac, n.inputs['Factor'])
    for sock, c in ((n.inputs[6], c1), (n.inputs[7], c2)):
        if isinstance(c, tuple):
            sock.default_value = (*c, 1) if len(c) == 3 else c
        else:
            nt.links.new(c, sock)
    return n.outputs[2]


def surface(name, color, texture, axis='Y'):
    """A rubber or urethane surface in a given colour. texture = lisse | moule | satine | mouchete | vecu (plates),
    fin | gros (dumbbell grain). Every effect stays subtle: it must read as the same object."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord'); obj = tc.outputs['Object']
    lum = sum(color) / 3
    light = lum > 0.2
    # colour mottle, like molded rubber
    nz = N(nt, 'ShaderNodeTexNoise', Scale=22.0, Detail=4.0); nt.links.new(obj, nz.inputs['Vector'])
    mot = 0.22 if not light else 0.06
    col = mix_col(nt, nz.outputs['Fac'], tuple(c * (1 - mot) for c in color), tuple(c * (1 + mot) for c in color))
    rough = {'lisse': 0.64, 'moule': 0.6, 'satine': 0.36, 'mouchete': 0.78, 'vecu': 0.6, 'fin': 0.46, 'gros': 0.5}[texture]
    spec = 0.5 if texture == 'satine' else 0.32
    p.inputs['Specular IOR Level'].default_value = spec
    if texture == 'satine':
        p.inputs['Coat Weight'].default_value = 0.3; p.inputs['Coat Roughness'].default_value = 0.2
    bumps = []                       # (height socket, strength, distance)
    rough_sock = None
    if texture in ('lisse', 'moule', 'vecu', 'mouchete'):
        g = N(nt, 'ShaderNodeTexNoise', Scale=2600.0, Detail=6.0); nt.links.new(obj, g.inputs['Vector'])
        bumps.append((g.outputs['Fac'], 0.3, 0.00015))
    if texture in ('moule', 'vecu'):
        # fine stipple of the mould and concentric mould rings on the faces
        v = nt.nodes.new('ShaderNodeTexVoronoi'); v.inputs['Scale'].default_value = 3800.0; nt.links.new(obj, v.inputs['Vector'])
        bumps.append((v.outputs['Distance'], 0.28, 0.00012))
        sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(obj, sep.inputs[0])
        a, c = ('X', 'Z') if axis == 'Y' else ('Y', 'Z')
        r2 = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', sep.outputs[a], sep.outputs[a]).outputs[0],
                       math_node(nt, 'MULTIPLY', sep.outputs[c], sep.outputs[c]).outputs[0])
        r = math_node(nt, 'SQRT', r2.outputs[0])
        ring = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', r.outputs[0], v1=2 * math.pi / 0.0007).outputs[0])
        bumps.append((ring.outputs[0], 0.05, 0.00008))
        rn = N(nt, 'ShaderNodeTexNoise', Scale=120.0, Detail=3.0); nt.links.new(obj, rn.inputs['Vector'])
        rough_sock = maprange(nt, rn.outputs['Fac'], 0.3, 0.7, rough - 0.06, rough + 0.06).outputs['Result']
    if texture == 'satine':
        op = N(nt, 'ShaderNodeTexNoise', Scale=380.0, Detail=2.0); nt.links.new(obj, op.inputs['Vector'])
        bumps.append((op.outputs['Fac'], 0.06, 0.0004))
    if texture == 'mouchete':
        # crumb rubber: small grey flecks scattered in the mass
        v = nt.nodes.new('ShaderNodeTexVoronoi'); v.inputs['Scale'].default_value = 520.0; nt.links.new(obj, v.inputs['Vector'])
        sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(v.outputs['Color'], sp.inputs[0])
        pick = math_node(nt, 'GREATER_THAN', sp.outputs[0], v1=0.86)
        small = math_node(nt, 'LESS_THAN', v.outputs['Distance'], v1=0.34)
        fl = math_node(nt, 'MULTIPLY', pick.outputs[0], small.outputs[0])
        fleck = (0.3, 0.3, 0.31) if not light else tuple(cc * 0.55 for cc in color)
        col = mix_col(nt, fl.outputs[0], col, fleck)
        bumps.append((v.outputs['Distance'], 0.2, 0.0002))
    if texture in ('fin', 'gros'):
        v = nt.nodes.new('ShaderNodeTexVoronoi'); v.inputs['Scale'].default_value = 1500.0 if texture == 'fin' else 700.0
        nt.links.new(obj, v.inputs['Vector'])
        bumps.append((v.outputs['Distance'], 0.8 if texture == 'fin' else 1.0, 0.0004 if texture == 'fin' else 0.0006))
        rn = N(nt, 'ShaderNodeTexNoise', Scale=900.0); nt.links.new(obj, rn.inputs['Vector'])
        rough_sock = maprange(nt, rn.outputs['Fac'], 0.3, 0.7, rough - 0.08, rough + 0.1).outputs['Result']
    if texture == 'vecu':
        # lived-in: shiny scuffs, worn edges, chalk caught in the hollows
        sc = N(nt, 'ShaderNodeTexNoise', Scale=26.0, Detail=12.0, Roughness=0.7); nt.links.new(obj, sc.inputs['Vector'])
        scuff = maprange(nt, sc.outputs['Fac'], 0.64, 0.7, 0.0, 1.0).outputs['Result']
        geo = nt.nodes.new('ShaderNodeNewGeometry')
        edge = maprange(nt, geo.outputs['Pointiness'], 0.52, 0.58, 0.0, 1.0).outputs['Result']
        ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.0025; ao.samples = 8
        cav = maprange(nt, ao.outputs['AO'], 0.72, 0.97, 1.0, 0.0).outputs['Result']
        dn = N(nt, 'ShaderNodeTexNoise', Scale=260.0, Detail=8.0); nt.links.new(obj, dn.inputs['Vector'])
        chalk = math_node(nt, 'MULTIPLY', cav, maprange(nt, dn.outputs['Fac'], 0.52, 0.72, 0.0, 0.32).outputs['Result'])
        wear = math_node(nt, 'MAXIMUM', scuff, edge)
        col = mix_col(nt, wear.outputs[0], col, tuple(min(1.0, cc * 1.9 + 0.012) for cc in color))
        col = mix_col(nt, chalk.outputs[0], col, (0.62, 0.62, 0.6))
        r_base = rough_sock
        r1 = mix_col(nt, scuff, (rough, rough, rough), (0.36, 0.36, 0.36))
        rough_sock = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(r1, rough_sock.inputs[0]); rough_sock = rough_sock.outputs[0]
        rough_sock = mix_col(nt, chalk.outputs[0], rough_sock, (0.92, 0.92, 0.92))
        bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(rough_sock, bw.inputs[0]); rough_sock = bw.outputs[0]
    nt.links.new(col, p.inputs['Base Color'])
    if rough_sock is not None:
        nt.links.new(rough_sock, p.inputs['Roughness'])
    else:
        p.inputs['Roughness'].default_value = rough
    last = None
    for h, st, d in bumps:
        b = N(nt, 'ShaderNodeBump', Strength=st, Distance=d)
        nt.links.new(h, b.inputs['Height'])
        if last:
            nt.links.new(last.outputs['Normal'], b.inputs['Normal'])
        last = b
    if last:
        nt.links.new(last.outputs['Normal'], p.inputs['Normal'])
    return m


def metal(name, color, axis='Y', rough=0.3, polished=False, smudge=False):
    """Turned metal (steel, black anodised, brass): anisotropic highlights around the axis."""
    m = mat_turned(name, axis, rough=rough, polished=polished)
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*color, 1)
    if smudge:
        nt = m.node_tree
        tc = nt.nodes.new('ShaderNodeTexCoord')
        nz = N(nt, 'ShaderNodeTexNoise', Scale=45.0, Detail=6.0); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        nt.links.new(maprange(nt, nz.outputs['Fac'], 0.4, 0.65, rough - 0.04, rough + 0.1).outputs['Result'], p.inputs['Roughness'])
    return m


METALS = {'acier': (0.8, 0.8, 0.82), 'noir': (0.045, 0.045, 0.05), 'laiton': (0.78, 0.56, 0.3)}


def plate_mats(colour='noir', texture='moule', insert='acier', tranche=None, chiffres=None):
    M = materials()
    hexc, tc = PALETTE[colour]
    body = surface('corps', srgb(hexc), texture)
    M['caoutchouc'] = body
    M['kg'] = body
    M['blanc'] = mat('chiffres', chiffres or (WHITE if tc == 'w' else CHARCOAL), rough=0.55, spec=0.4)
    M['acier'] = metal('insert', METALS[insert], 'Y', smudge=(texture == 'vecu'))
    M['poli'] = metal('rainure', METALS[insert], 'Y', polished=True)
    if tranche:
        M['tranche'] = surface('tranche', srgb(PALETTE[tranche][0]), texture)
    return M


def dumbbell_mats(colour='noir', texture='fin', face_colour=None, bezel=None, handle='chrome'):
    M = materials()
    hexc, tc = PALETTE[colour]
    c = srgb(hexc)
    side_tex = 'satine' if texture == 'satine' else texture
    M['grain'] = surface('grain', c, side_tex if side_tex != 'mouchete' else 'mouchete', axis='X')
    fc = srgb(PALETTE[face_colour][0]) if face_colour else c
    M['face'] = mat('face', tuple(x * 0.9 for x in fc), rough=0.36 if texture == 'satine' else 0.52, spec=0.38,
                    coat=0.25 if texture == 'satine' else 0.0)
    M['lisse'] = M['face']
    if bezel == 'acier':
        M['liseré'] = mat('liseré', (0.8, 0.8, 0.82), rough=0.16, metal=1.0)
    else:
        M['liseré'] = mat('liseré', tuple(x * 0.9 for x in c), rough=0.45, spec=0.38)
    tcol = tc if not face_colour else PALETTE[face_colour][1]
    M['blanc'] = mat('chiffres', WHITE if tcol == 'w' else CHARCOAL, rough=0.55, spec=0.4)
    hc = {'chrome': (0.72, 0.72, 0.74), 'noir': (0.05, 0.05, 0.055), 'laiton': (0.78, 0.56, 0.3)}[handle]
    M['poignee'] = mat_knurl('poignee', hc, 0.24 if handle != 'noir' else 0.32, 1.0, 0.132, bands=[(0.0, 0.055)])
    M['satin'] = mat('collerette', hc, rough=0.24, metal=1.0)
    return M


# ------------------------------------------------------------------ lighting: a real studio HDRI + soft areas
def world_hdri(strength, rot=0.0):
    w = bpy.data.worlds.new('w'); w.use_nodes = True
    nt = w.node_tree
    bg = next(n for n in nt.nodes if n.type == 'BACKGROUND')
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(HDRI, check_existing=True)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(rot))
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    nt.links.new(env.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    SC.world = w


def catalog(k=1.0, hdri=0.35):
    """Catalogue light: transparent film (background added later), the HDRI for real reflections, a soft top-left key."""
    world_hdri(hdri * k, rot=float(ARGS.get('rot_hdri', 30)))
    SC.render.film_transparent = True
    area('key', (-1.7, -2.0, 1.7), (0, 0, 0), 220 * k, 1.6, (1.0, 0.98, 0.96))
    area('top', (0.2, -0.8, 2.4), (0, 0, 0), 35 * k, 2.0)
    area('rim', (1.4, 1.4, 1.2), (0, 0, 0), 140 * k, 0.4, (1, 1, 1), 'RECTANGLE', 2.4)


def raking(target, side=1, k=1.0):
    """Grazing light from one side: it reveals the surface texture."""
    world_hdri(0.12 * k)
    SC.render.film_transparent = True
    t = Vector(target)
    area('rasant', t + Vector((side * 0.9, -0.12, 0.18)), t, 70 * k, 0.35, (1.0, 0.97, 0.94))
    area('doux', t + Vector((-side * 0.6, -0.9, 0.5)), t, 14 * k, 1.2, (0.95, 0.97, 1.0))


def light_floor(center=(0, 0, 0.2), k=1.0, tone=0.5):
    """A light grey studio floor that curves into the wall, the HDRI and a soft key: for piles and line-ups."""
    cyclo(tone)
    world_hdri(0.45 * k, rot=30)
    c = Vector(center)
    area('key', c + Vector((-1.4, -1.8, 1.9)), c, 260 * k, 2.4, (1.0, 0.97, 0.94))
    area('rim', c + Vector((1.5, 1.2, 1.0)), c, 160 * k, 0.3, (1, 1, 1), 'RECTANGLE', 2.2)


def portrait():
    setup_render(RES, (4, 5))
    SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)


# ------------------------------------------------------------------ shots
def lie_flat(e, z, rz):
    e.rotation_euler = (math.radians(90), 0, math.radians(rz))
    e.location = (e.location.x, e.location.y, z)


def plate_shot(plan, M_of, tag):
    """M_of(i) gives the materials of the i-th plate of the shot (several colours in one shot)."""
    if plan == 'face':
        disque(20, M_of(0))
        catalog()
        portrait()
        ortho_camera((0, -4, 0), (0, 0, 0), 0.5625, RES, int(RES * 5 / 4))
    elif plan == 'rasant':
        disque(20, M_of(0))
        raking((0.12, -0.03, 0.0), side=1)
        portrait()
        camera((0.44, -0.6, 0.12), (0.11, -0.02, 0.0), lens=88, fstop=5, focus=(0.143, -0.03, 0.0))
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif plan == 'pile':
        z = 0.0
        for i, (w, rz) in enumerate(((25, 12), (20, -31), (15, 54))):
            e = disque(w, M_of(i), name='p%d' % i)
            z += e['T'] / 2
            lie_flat(e, z, rz)
            z += e['T'] / 2 + 0.0006
        light_floor(center=(0, 0, 0.08))
        setup_render()
        camera((0.66, -0.82, 0.72), (0.0, 0.0, 0.06), lens=55, fstop=8)
    elif plan == 'alignes':
        cols = list(PALETTE)
        x = -0.62
        for i, cname in enumerate(cols):
            e = disque(20, M_of(i), name='a%d' % i)
            e.location = (x, 0.0, e['R'])
            e.rotation_euler = (0, 0, math.radians(-34))
            x += 0.19
        light_floor(center=(0.0, 0, 0.22), k=1.15)
        setup_render()
        camera((0.15, -2.45, 0.7), (0.0, 0.0, 0.2), lens=50, fstop=10)
    elif plan == '3q':
        e = disque(20, M_of(0))
        e.rotation_euler = (0, 0, math.radians(34))
        catalog()
        portrait()
        camera((0.0, -1.55, 0.18), (0.0, 0, 0.0), lens=80, fstop=16)
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    render(os.path.join(OUT, f'disque-{GROUPE}-{tag}-{plan}.png'))


def dumbbell_shot(plan, M_of, tag):
    if plan == 'flottant':
        a = haltere(40, M_of(0), 'h1'); a.location = (0.02, 0.18, 0.15)
        a.rotation_euler = (math.radians(-8), math.radians(4), math.radians(-28))
        b = haltere(40, M_of(1), 'h2'); b.location = (-0.03, -0.12, -0.14)
        b.rotation_euler = (math.radians(6), math.radians(-5), math.radians(208))
        catalog(k=1.05)
        portrait()
        camera((0.0, -1.5, 0.06), (0.0, 0.0, 0.0), lens=66, fstop=22)
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif plan == 'macro':
        a = haltere(25, M_of(0), 'h1'); a.rotation_euler = (0, 0, math.radians(-10))
        raking((0.12, -0.02, 0.02), side=-1, k=1.1)
        portrait()
        camera((0.3, -0.4, 0.13), (0.11, -0.02, 0.0), lens=90, fstop=4, focus=(0.115, -0.075, 0.0))
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif plan == 'macro3q':
        a = haltere(25, M_of(0), 'h1'); a.rotation_euler = (0, 0, math.radians(-38))
        catalog(k=1.05)
        portrait()
        camera((0.44, -0.5, 0.2), (0.1, -0.04, 0.0), lens=80, fstop=5, focus=(0.14, -0.1, 0.0))
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif plan == 'entier':
        a = haltere(25, M_of(0), 'h1')
        a.rotation_euler = (math.radians(-6), math.radians(8), math.radians(-24))
        catalog(k=1.05)
        portrait()
        camera((0.06, -0.95, 0.2), (0.0, 0.0, 0.0), lens=70, fstop=11, focus=(0.07, -0.05, 0.0))
        SC.render.resolution_x, SC.render.resolution_y = RES, int(RES * 5 / 4)
    elif plan == 'rangee':
        cols = list(PALETTE)
        x = -0.68
        for i, cname in enumerate(cols):
            o = haltere(15, M_of(i), 'r%d' % i)
            o.location = (x, 0.0, DB2[15][0])
            o.rotation_euler = (0, 0, math.radians(90 - 8))
            x += 0.195
        light_floor(center=(0.0, 0.0, 0.07), k=1.1)
        setup_render()
        camera((0.1, -2.15, 0.78), (0.0, 0.04, 0.04), lens=46, fstop=10)
    render(os.path.join(OUT, f'haltere-{GROUPE}-{tag}-{plan}.png'))


# ------------------------------------------------------------------ the groups
# texture: one material set per texture, black. couleur: one colour (or "tous" = the whole palette in one shot).
# design: accents on the black model.
DISQUE_DESIGNS = {
    'insert-noir': dict(insert='noir'), 'insert-laiton': dict(insert='laiton'),
    'tranche-rose': dict(tranche='rose'), 'chiffres-bleus': dict(chiffres=srgb('#5C8FD6')),
}
HALTERE_DESIGNS = {
    'face-rose': dict(face_colour='rose'), 'liseré-acier': dict(bezel='acier'),
    'tout-noir': dict(handle='noir'), 'poignee-laiton': dict(handle='laiton', bezel=None),
}

for var in ([] if globals().get('AS_LIB_P3') else VARS):
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        SC.render.film_transparent = False
        if PIECE == 'disque':
            if GROUPE == 'texture':
                f = lambda i, v=var: plate_mats('noir', v)
            elif GROUPE == 'couleur':
                if var == 'tous':
                    f = lambda i: plate_mats(list(PALETTE)[i % len(PALETTE)], 'moule')
                elif var == 'mix':
                    f = lambda i: plate_mats(('noir', 'rose', 'bleu')[i % 3], 'moule')
                else:
                    f = lambda i, v=var: plate_mats(v, 'moule')
            else:
                f = lambda i, v=var: plate_mats('noir', 'moule', **DISQUE_DESIGNS[v])
            plate_shot(plan, f, var)
        else:
            if GROUPE == 'texture':
                f = lambda i, v=var: dumbbell_mats('noir', v)
            elif GROUPE == 'couleur':
                if var == 'tous':
                    f = lambda i: dumbbell_mats(list(PALETTE)[i % len(PALETTE)], 'fin')
                else:
                    f = lambda i, v=var: dumbbell_mats(v, 'fin')
            else:
                f = lambda i, v=var: dumbbell_mats('noir', 'fin', **HALTERE_DESIGNS[v])
            dumbbell_shot(plan, f, var)
