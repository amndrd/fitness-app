# Screenshots of the models in Blender's interface, in the Instagram story format (22/11/2026).
# Opens Blender with a window in portrait (about 9:16), builds one model, lays out the interface (the 3D view on top,
# an editor below), waits for the viewport to draw, takes a screenshot of the window from Blender itself, quits.
# The window: 640 x 831 points (Blender's minimum width, the screen's height): the story puts it on a dark band.
# usage: Blender --factory-startup --window-geometry 0 0 640 831 --python captures.py -- shot=disque out=<dir>
import os
HERE = os.path.dirname(os.path.abspath(__file__))
AS_LIB_HALTERES = True
exec(open(os.path.join(HERE, 'halteres.py')).read())

SHOT = ARGS.get('shot', 'disque')
prefs = bpy.context.preferences
prefs.use_preferences_save = False                 # never touch the user's own Blender preferences
prefs.view.show_splash = False
prefs.view.ui_scale = float(ARGS.get('ui', 0.9))
prefs.view.smooth_view = 0                         # framing without animation (the window may not get events)


# shot: what to build, where the view looks (target, distance, rotation of the view in degrees), the viewport shading,
# the editor below ('ShaderNodeTree', 'OUTLINER' or 'PROPERTIES'), and whether to draw the mesh's wireframe
def build():
    reset()
    if SHOT == 'disque':
        e = disque(20, plate_mats('noir', 'moule'), name='disque_20kg')
        e.rotation_euler = (0, 0, math.radians(-30))
        return e, (0.0, 0.0, 0.0), 0.85, (78, 0, 28), 'MATERIAL', 'ShaderNodeTree', False
    if SHOT == 'haltere':
        e = haltere(15, dumbbell_mats('rose', 'fin'), 'haltere_15kg')
        e.rotation_euler = (0, 0, math.radians(-24))
        return e, (0.0, 0.0, 0.0), 0.56, (70, 0, 20), 'MATERIAL', 'OUTLINER', True
    if SHOT == 'barre':
        e = barre_olympique(bar_mats('B', 'vert'), name='barre_20kg')
        return e, (1.0, 0.0, 0.0), 0.36, (70, 0, 70), 'MATERIAL', 'PROPERTIES', False
    if SHOT == 'pince':
        e = pince3(collar_mats('rose'), 'rose', 'pince')
        return e, (-0.86 * D, 0.30 * D, 0.0), 0.28, (48, 0, 118), 'MATERIAL', 'OUTLINER', False
    if SHOT == 'haltere-disques':
        e = dumbbell(colour='noir', name='haltere_disques')
        e.rotation_euler = (0, 0, math.radians(-28))
        return e, (0.0, 0.0, 0.0), 0.78, (70, 0, 6), 'MATERIAL', 'OUTLINER', False


def view3d_setup(area, target, dist, rot, shading, wire):
    sp = area.spaces.active
    sp.shading.type = shading
    if shading == 'SOLID':
        sp.shading.light = 'MATCAP'
    sp.overlay.show_wireframes = wire
    sp.overlay.wireframe_threshold = 0.5              # the main edges only: lighter than every segment
    sp.lens = 50
    r3 = sp.region_3d
    r3.view_perspective = 'PERSP'
    r3.view_location = target
    r3.view_rotation = Euler(tuple(math.radians(a) for a in rot)).to_quaternion()
    r3.view_distance = dist


def setup():
    win = bpy.context.window_manager.windows[0]
    scr = win.screen
    for a in list(scr.areas):                     # keep only the 3D view, then split it: an editor below
        if a.type != 'VIEW_3D':
            with bpy.context.temp_override(window=win, area=a):
                bpy.ops.screen.area_close()
    v3d = next(a for a in scr.areas if a.type == 'VIEW_3D')
    with bpy.context.temp_override(window=win, area=v3d):
        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.42 if EDITOR == 'ShaderNodeTree' else 0.3)
    areas = sorted([a for a in scr.areas if a.type == 'VIEW_3D'], key=lambda a: a.y)
    low, top = areas[0], areas[-1]
    if EDITOR == 'ShaderNodeTree':
        low.type = 'NODE_EDITOR'
        low.ui_type = EDITOR
    else:
        low.type = EDITOR
    view3d_setup(top, TARGET, DIST, ROT, SHADING, WIRE)
    bpy.app.timers.register(tidy, first_interval=1.5)
    return None


def tidy():
    """Once the editor below exists: no side panel in the node editor, the right tab in the properties."""
    win = bpy.context.window_manager.windows[0]
    ob = bpy.context.view_layer.objects.active
    if ob and ob.active_material and ob.active_material.node_tree:
        arrange(ob.active_material.node_tree)        # (framed later, once drawn)
    for a in win.screen.areas:
        if a.type == 'NODE_EDITOR':
            with bpy.context.temp_override(window=win, area=a):
                a.spaces.active.show_region_ui = False
        elif a.type == 'PROPERTIES':
            a.spaces.active.context = 'MATERIAL'
        elif a.type == 'OUTLINER':
            reg = next(r for r in a.regions if r.type == 'WINDOW')
            with bpy.context.temp_override(window=win, area=a, region=reg):
                bpy.ops.outliner.show_one_level(open=True)
                bpy.ops.outliner.show_one_level(open=True)      # the collection, then the model's parts
    bpy.app.timers.register(frame_nodes, first_interval=float(ARGS.get('wait', 9)))
    return None


def arrange(nt):
    """The materials are built by script, every node at the origin: lay them out in columns, from the output
    backwards (depth = number of links to the output), like one would by hand."""
    out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None)
    if out is None:
        return
    depth = {out: 0}
    todo = [out]
    while todo:
        n = todo.pop()
        for l in nt.links:
            if l.to_node == n and depth.get(l.from_node, -1) < depth[n] + 1:
                depth[l.from_node] = depth[n] + 1
                todo.append(l.from_node)
    cols = {}
    for n, d in depth.items():
        cols.setdefault(d, []).append(n)
    tall = lambda n: 560.0 if n.type == 'BSDF_PRINCIPLED' else (n.dimensions.y if n.dimensions.y > 1 else 170.0)
    for d, ns in cols.items():
        y = 0.0
        for n in ns:
            n.location = (-d * 250.0, y)
            y -= tall(n) + 12.0
    for n in nt.nodes:                             # the unlinked ones aside
        if n not in depth:
            n.location = (260.0, -300.0)
    # the node editor opens centred on the origin and keeps that view: centre the graph on the origin
    xs0 = min(n.location.x for n in nt.nodes); xs1 = max(n.location.x + n.width for n in nt.nodes)
    ys1 = max(n.location.y for n in nt.nodes); ys0 = min(n.location.y - tall(n) for n in nt.nodes)
    cx, cy = (xs0 + xs1) / 2, (ys0 + ys1) / 2
    for n in nt.nodes:
        n.location = (n.location.x - cx, n.location.y - cy - 70.0)     # a little lower: the breadcrumbs stay clear


def frame_nodes():
    win = bpy.context.window_manager.windows[0]
    for a in win.screen.areas:
        if a.type == 'NODE_EDITOR':
            reg = next(r for r in a.regions if r.type == 'WINDOW')
            with bpy.context.temp_override(window=win, area=a, region=reg, space_data=a.spaces.active):
                bpy.ops.node.view_all()
            a.tag_redraw()
    bpy.app.timers.register(shoot, first_interval=1.5)
    return None


def shoot():
    win = bpy.context.window_manager.windows[0]
    path = os.path.join(OUT, f'blender-{SHOT}.png')
    with bpy.context.temp_override(window=win):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)     # without input events the window may not redraw
        bpy.ops.screen.screenshot(filepath=path, check_existing=False)
    print('capture', path)
    bpy.ops.wm.quit_blender()
    return None


obj, TARGET, DIST, ROT, SHADING, EDITOR, WIRE = build()
SELECT = {'barre': 'embout'}.get(SHOT, '')       # the object to select (its material is shown below)
for o in bpy.data.objects:                         # the groups' empties would draw black axes through the view
    if o.type == 'EMPTY':
        o.empty_display_size = 0.001
for o in bpy.context.view_layer.objects:
    o.select_set(False)
main = next((c for c in obj.children_recursive if c.type == 'MESH' and SELECT in c.name), None) or next((c for c in obj.children if c.type == 'MESH'), obj)
main.select_set(True)
bpy.context.view_layer.objects.active = main
bpy.app.timers.register(setup, first_interval=2.0)
