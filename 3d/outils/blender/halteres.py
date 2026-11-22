# Step 8 (22/11/2026): the plate-loaded dumbbell, after the user's photo (3d/references/halteres-disques/).
# - a 25 mm handle: knurled grip, two stop collars, smooth sleeves, a bare steel end (no cap, the user's choice of
#   22/11: all steel, finish B); three ways to finish that end: chamfer, rounded, recessed. Finishes A, B, C like the bar;
# - cement-vinyl plates (1.25, 2.5 and 5 kg, common sizes for 25 mm bars, see 3d/recherche/7-halteres-disques):
#   a rounded rim with a mould seam, a flat face with the weight embossed along the ring (twice) and eight
#   holes, a smooth recessed centre around the bore;
# - our spring clip (colliers.py, pince3) at the size of a 25 mm bar, which is the reference model's own size.
# The colour (plates, clip sleeves) is a setting (3d/charte.md). Reuses colliers.py, barre.py, poids3.py, poids2.py, base.py.
# usage: Blender -b --factory-startup -P halteres.py -- plans=paire,haltere couleur=noir finition=B texture=gros marquage=blanc bout=chanfrein res=1400 samples=128 out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_COLLIERS = True
exec(open(os.path.join(HERE, 'colliers.py')).read())

PLANS = ARGS.get('plans', 'paire').split(',')
COLOUR = ARGS.get('couleur', 'noir')
FIN = ARGS.get('finition', 'B')
TEX = ARGS.get('texture', 'gros')         # the sandy grain of the photo
MARK = ARGS.get('marquage', 'blanc')      # blanc: white (charcoal on light colours), the user's choice | relief: same colour (the photo)
END = ARGS.get('bout', 'chanfrein')       # the steel end of the handle: chanfrein | arrondi | creux

# ------------------------------------------------------------------ dimensions
VINYL = {1.25: (0.185, 0.034), 2.5: (0.225, 0.042), 5: (0.282, 0.050)}   # diameter, thickness
BORE_V = 0.0133                         # bore: 26.6 mm, for a 25 mm bar
HR = 0.0125                             # handle: 25 mm
GRIP = 0.130                            # between the two stop collars
COL_W, COL_R = 0.015, 0.0185            # stop collars: 15 mm wide, 37 mm across
SLEEVE = 0.165                          # each side: 5 + 2.5 + 2.5 kg, the clip, then 11 mm of bare steel (like the photo)
ENDS = ('chanfrein', 'arrondi', 'creux')
CLIP_S = 0.0256 / 0.051                 # our clip, scaled to the 25 mm bar
SET = [5, 2.5, 2.5]                     # one side of the dumbbell, from the inside (like the photo)
HANDLE_FIN = {'A': dict(grip='noir', rest='chrome'),   # black grip, steel collars and sleeves
              'B': dict(grip='chrome', rest='chrome'), # all steel (like the bar's original finish)
              'C': dict(grip='noir', rest='noir')}     # all black


def label_v(w):
    return {1.25: '1,25 KG', 2.5: '2,5 KG', 5: '5 KG'}[w]


# ------------------------------------------------------------------ materials
def handle_mats(fin):
    f = HANDLE_FIN[fin]
    M = {}
    band = [(0.0, GRIP / 2 - 0.007)]
    if f['grip'] == 'noir':
        M['grip'] = mat_knurl('grip', (0.03, 0.03, 0.033), 0.42, 0.0, GRIP, bands=band, depth=0.7)
    else:
        M['grip'] = mat_knurl('grip', (0.75, 0.75, 0.77), 0.2, 1.0, GRIP, bands=band, depth=0.7)
    chrome = metal('chrome_h', (0.86, 0.86, 0.88), 'X', rough=0.12)
    noir = metal('noir_h', (0.06, 0.06, 0.065), 'X', rough=0.2)
    M['reste'] = chrome if f['rest'] == 'chrome' else noir
    return M


def plate_mats_v(colour, texture=TEX, mark=MARK):
    hexc, tc = PALETTE[colour]
    c = srgb(hexc)
    M = {'corps': surface('vinyle', c, texture, axis='X'),
         'centre': surface('centre', tuple(x * 0.85 for x in c), 'lisse', axis='X')}
    M['texte'] = M['corps'] if mark == 'relief' else mat('texte_v', WHITE if tc == 'w' else CHARCOAL, rough=0.55, spec=0.4)
    return M


# ------------------------------------------------------------------ the handle (axis X, centred)
def sleeve_end(x0, xe, end):
    """Profile (r, x) of a sleeve from x0 to its bare steel end xe. Solid steel, turned:
    chanfrein: a 1.5 mm 45-degree chamfer, flat end (like the bar's sleeves);
    arrondi: a 5.5 mm round, the end face slightly domed;
    creux: the chamfer and a shallow recess in the end face (the bar's sleeve end, without its cap).
    (Two fine grooves near the end, like the bar's sleeves, were tried: next to the clip they read as extra coils.)"""
    if end == 'arrondi':
        return round_poly([(0.0, x0), (HR, x0), (HR, xe - 0.0008), (0.0, xe)], [0, 0, 0.0055, 0], segs=10)
    pts = [(0.0, x0), (HR, x0), (HR, xe - 0.0015), (HR - 0.0015, xe)]
    rad = [0, 0, 0.0002, 0.0002]
    if end == 'creux':
        pts += [(0.0095, xe), (0.0095, xe - 0.0015), (0.0, xe - 0.0015)]
        rad += [0.0003, 0.0004, 0]
    else:
        pts += [(0.0, xe)]
        rad += [0]
    return round_poly(pts, rad, segs=3)


def poignee(M, name='poignee', end=END):
    parts = []
    xg = GRIP / 2 + COL_W                              # end of the grip tube, under the collars
    xe = xg + SLEEVE                                   # end of the sleeves
    parts.append(fix_normals(lathe(name + '_grip', round_poly([(0.0, -xg), (HR, -xg), (HR, xg), (0.0, xg)], [0, 0, 0, 0], segs=1),
                                   M['grip'], segs=64, axis='X')))
    for sg in (-1, 1):
        cp = round_poly([(HR - 0.0004, GRIP / 2), (COL_R, GRIP / 2), (COL_R, GRIP / 2 + COL_W), (HR - 0.0004, GRIP / 2 + COL_W)],
                        [0.0004, 0.0018, 0.0018, 0.0004], segs=4)
        parts.append(sharp(fix_normals(lathe(name + '_bague', [(r, sg * h) for r, h in cp], M['reste'], segs=96, axis='X')), 30))
        sp = sleeve_end(xg - 0.001, xe, end)
        parts.append(sharp(fix_normals(lathe(name + '_manchon', [(r, sg * h) for r, h in sp], M['reste'], segs=96, axis='X')), 30))
    e = group(name, parts)
    e['x_plates'] = GRIP / 2 + COL_W + 0.0005
    return e


# ------------------------------------------------------------------ the cement-vinyl plate (axis X, centred)
def arc_text(name, body, font, cap, rho, phi0, xf, depth, m, side):
    """Embossed text bent along a circle of radius rho, centred on the angle phi0 (degrees), letters' tops
    towards the centre (readable at the bottom, upside down at the top, like the photo). side = +1/-1: face."""
    o = text_mesh(name, body, 0.02, depth, m, font=font, fit_h=cap)
    me = o.data
    p0 = math.radians(phi0)
    for v in me.vertices:
        u, w, z = v.co
        phi = p0 + u / rho
        rr = rho - w
        y, zz = rr * math.cos(phi), rr * math.sin(phi)
        x = xf + depth + z
        v.co = (side * x, y * side, zz)            # mirrored on the back face, so it reads from that side too
    me.update()
    return fix_normals(o)


def vinyl_plate(w, M, name='disque_v'):
    Dm, T = VINYL[w]
    R, f = Dm / 2, T / 2
    r_rim, r_in = 0.90 * R, 0.42 * R
    xf, xc = f - 0.0030, f - 0.0060                 # main face under the rim, recessed centre
    rim_r = min(0.3 * T, 0.9 * (R - r_rim))
    pts = [(BORE_V, -(xc - 0.0015)), (BORE_V + 0.0015, -xc), (r_in, -xc), (r_in + 0.0015, -xf), (r_rim - 0.0015, -xf), (r_rim, -f), (R, -f),
           (R, -0.0007), (R - 0.0008, 0.0), (R, 0.0007),
           (R, f), (r_rim, f), (r_rim - 0.0015, xf), (r_in + 0.0015, xf), (r_in, xc), (BORE_V + 0.0015, xc), (BORE_V, xc - 0.0015)]
    rad = [0, 0.0006, 0.001, 0.001, 0.0012, 0.0022, rim_r, 0, 0.0003, 0, rim_r, 0.0022, 0.0012, 0.001, 0.001, 0.0006, 0]
    rp = round_poly(pts, rad, segs=5)
    n = len(rp)
    # the smooth recessed centre (and the bore) gets its own material
    em = [1 if (rp[i][0] < r_in + 0.0008 and rp[(i + 1) % n][0] < r_in + 0.0008) else 0 for i in range(n)]
    body = fix_normals(lathe(name, rp, M['corps'], segs=220, axis='X', edge_mats=em, mats=[M['corps'], M['centre']]))
    # eight holes on the face, both sides
    rh, rc, dep = 0.045 * R, 0.62 * R, 0.0026
    cutters = []
    for sg in (-1, 1):
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            x0, x1 = (xf - dep, xf + 0.003) if sg > 0 else (-xf - 0.003, -xf + dep)
            cutters.append(cyl_x(name + '_trou', rh, x0, x1, (0.0, rc * math.cos(a), rc * math.sin(a)), M['corps'], segs=24))
    bpy.context.view_layer.update()                 # (join reads the cutters' world matrices)
    cut = join(cutters, name + '_trous')
    boolean(body, cut)
    body = bake(body, 30)
    remove(cut)
    parts = [body]
    cap = 0.105 * R
    rho = 0.79 * R
    for side in (1, -1):
        for phi0 in (225.0, 45.0):
            parts.append(arc_text(name + "_kg", label_v(w), F_BIG, cap, rho, phi0, xf, 0.0004, M['texte'], side))
    e = group(name, parts)
    e['R'], e['T'] = R, T
    return e


# ------------------------------------------------------------------ the dumbbell
def haltere_v(MH, MP, MC, colour, name='haltere', config=SET, clip_turn=35.0):
    """Handle + plates (config: one side, from the inside) + one clip on each side. Axis X, centred."""
    h = poignee(MH, name + '_poignee')
    parts = [h]
    rmax = 0.0
    x0 = GRIP / 2 + COL_W + 0.0005
    for sg in (-1, 1):
        x = x0
        for i, w in enumerate(config):
            T = VINYL[w][1]
            p = vinyl_plate(w, MP, f'{name}_d{sg}{i}')
            p.location = (sg * (x + T / 2), 0.0, 0.0)
            p.rotation_euler = (math.radians(11 * i + (0 if sg > 0 else 7)), 0, 0)   # plates never line up exactly
            parts.append(p)
            rmax = max(rmax, p['R'])
            x += T + 0.0006
        c = pince3(MC, colour, f'{name}_pince{sg}')
        xc = x + (-SL_Z0) * CLIP_S + 0.0006
        c.matrix_world = (Matrix.Translation((sg * xc, 0.0, 0.0)) @ Matrix.Rotation(math.radians(clip_turn * sg), 4, 'X')
                          @ Matrix.Rotation(math.radians(90 * sg), 4, 'Y') @ Matrix.Scale(CLIP_S, 4))
        parts.append(c)
    e = group(name, parts)
    e['R'] = rmax
    return e


def dumbbell(colour=COLOUR, fin=FIN, name='haltere', config=SET, texture=TEX, mark=MARK, clip_turn=35.0):
    return haltere_v(handle_mats(fin), plate_mats_v(colour, texture, mark), collar_mats(colour), colour, name, config, clip_turn)


# ------------------------------------------------------------------ shots
def out_h(plan):
    return os.path.join(OUT, f'haltere-{plan}-{COLOUR}-{FIN}-{TEX}-{MARK}-{END}.png')


def on_floor(o, x=0.0, y=0.0, yaw=0.0):
    o.rotation_euler = (0, 0, math.radians(yaw))
    o.location = (x, y, o['R'])
    return o


def shots():
    for plan in PLANS:
        reset()
        for w in list(bpy.data.worlds):
            bpy.data.worlds.remove(w)
        SC.render.film_transparent = False
        if plan == 'paire':                          # like the user's photo: two dumbbells, seen from the front, above
            a = on_floor(dumbbell(name='ha'), 0.0, 0.0, -52)
            b = on_floor(dumbbell(name='hb'), 0.27, 0.20, -52)
            fab_studio(); square()
            camera((-0.16, -0.82, 0.58), (0.12, 0.10, 0.07), lens=50, fstop=11)
        elif plan == 'haltere':                       # one dumbbell, three-quarters
            on_floor(dumbbell(name='h'), 0.0, 0.0, -30)
            fab_studio(); setup_render()
            camera((0.08, -1.05, 0.47), (0.0, 0.0, 0.11), lens=50, fstop=11)
        elif plan == 'disques':                      # the three plates standing, faces towards the camera
            MP = plate_mats_v(COLOUR)
            xs = (-0.30, -0.02, 0.29)
            for x, w in zip(xs, (1.25, 2.5, 5)):
                p = vinyl_plate(w, MP, 'p%s' % w)
                p.rotation_euler = (0, 0, math.radians(90 - 18)); p.location = (x, 0.0, p['R'])
            fab_studio(); setup_render()
            camera((0.02, -1.22, 0.34), (0.02, 0.0, 0.12), lens=50, fstop=11)
        elif plan == 'detail':                       # the end of the dumbbell: outer plate and clip
            on_floor(dumbbell(name='h'), 0.0, 0.0, -50)
            fab_studio(); square()
            camera((0.40, -0.50, 0.33), (0.16, -0.08, 0.13), lens=60, fstop=8, focus=(0.18, -0.17, 0.14))
        elif plan == 'poignees':                     # three handles, one per steel end (front to back: chanfrein, arrondi, creux)
            for i, end in enumerate(ENDS):
                h = poignee(handle_mats(FIN), 'po' + end, end)
                h.rotation_euler = (0, 0, math.radians(-12)); h.location = (0.0, 0.11 * (i - 1), COL_R)
            fab_studio(); setup_render()
            camera((0.05, -0.68, 0.52), (0.0, 0.0, 0.0), lens=50, fstop=11)
        elif plan == 'bout':                         # the end of the dumbbell at three-quarters: plate, clip, bare steel end
            on_floor(dumbbell(name='h'), 0.0, 0.0, 0.0)
            xe = GRIP / 2 + COL_W + SLEEVE
            fab_studio(); square()
            camera((xe + 0.15, -0.30, 0.25), (xe - 0.012, 0.0, 0.13), lens=70, fstop=8, focus=(xe - 0.01, -0.005, 0.141))
        elif plan == 'bouts':                        # macro: the three steel ends side by side (front to back: chanfrein, arrondi, creux)
            xe = GRIP / 2 + COL_W + SLEEVE
            for i, end in enumerate(ENDS):
                h = poignee(handle_mats(FIN), 'pb' + end, end)
                h.location = (-xe, 0.05 * (i - 1), COL_R)
            fab_studio(); square()
            camera((0.17, -0.24, 0.13), (-0.03, 0.004, COL_R - 0.004), lens=70, fstop=11, focus=(0.0, 0.0, COL_R))
        elif plan == 'eclate':                       # exploded along the bar
            h = poignee(handle_mats(FIN), 'pe'); h.location = (0, 0, 0.16)
            MP = plate_mats_v(COLOUR)
            x = GRIP / 2 + COL_W + 0.04
            for sg in (-1, 1):
                xx = x
                for i, w in enumerate(SET):
                    T = VINYL[w][1]
                    p = vinyl_plate(w, MP, f'e{sg}{i}'); p.location = (sg * (xx + T / 2), 0, 0.16)
                    xx += T + 0.035
                c = pince3(collar_mats(COLOUR), COLOUR, f'ep{sg}')
                c.matrix_world = Matrix.Translation((sg * (xx + 0.02), 0, 0.16)) @ Matrix.Rotation(math.radians(35 * sg), 4, 'X') @ Matrix.Rotation(math.radians(90 * sg), 4, 'Y') @ Matrix.Scale(CLIP_S, 4)
            fab_studio(); setup_render()
            camera((0.10, -1.30, 0.42), (0.0, 0.0, 0.15), lens=50, fstop=11)
        elif plan == 'gros-plan':                    # the face of a 2.5 kg plate: texture and marking
            p = vinyl_plate(2.5, plate_mats_v(COLOUR), 'g')
            p.rotation_euler = (0, 0, math.radians(90 - 28)); p.location = (0, 0, p['R'])
            fab_studio(); square()
            camera((0.12, -0.46, 0.24), (0.0, 0.0, 0.11), lens=60, fstop=8)
        elif plan == 'couleurs':                     # one 2.5 kg plate in each colour
            for i, cname in enumerate(PALETTE):
                p = vinyl_plate(2.5, plate_mats_v(cname), 'c%d' % i)
                p.rotation_euler = (0, 0, math.radians(90 - 25)); p.location = (-0.56 + 0.16 * i, 0.0, p['R'])
            light_floor(center=(0.0, 0.0, 0.1), k=1.1); setup_render()
            camera((0.0, -1.7, 0.45), (0.0, 0.0, 0.11), lens=45, fstop=11)
        render(out_h(plan))


shots()
