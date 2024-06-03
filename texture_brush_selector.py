# File path: pie_menu_brush_selector.py
# Version 0.1
# License MIT

bl_info = {
  "name": "Pie Menu Texture Paint Brushes",
  "blender": (4, 1, 0),
  "category": "Paint",
}

import bpy

class TEXTUREPAINT_OT_SelectBrush(bpy.types.Operator):
  bl_idname = "texturepaint.select_brush"
  bl_label = "Select Texture Paint Brush"
  bl_description = "Select a texture paint brush"

  brush_name: bpy.props.StringProperty()

  def execute(self, context):
    brush = bpy.data.brushes.get(self.brush_name)
    if brush:
      context.tool_settings.image_paint.brush = brush
      self.report({'INFO'}, f"Brush set to {self.brush_name}")
    else:
      self.report({'ERROR'}, f"Brush {self.brush_name} not found")
    return {'FINISHED'}

class TEXTUREPAINT_MT_BrushPieMenu(bpy.types.Menu):
  bl_label = "Texture Paint Brushes"
  bl_idname = "TEXTUREPAINT_MT_brush_pie_menu"

  def draw(self, context):
    layout = self.layout
    pie = layout.menu_pie()

    brushes = [brush for brush in bpy.data.brushes if brush.use_paint_image]
    num_brushes = len(brushes)
    brushes_per_segment = 8

    for i in range(0, num_brushes, brushes_per_segment):
      column = pie.column()
      for brush in brushes[i:i + brushes_per_segment]:
        op = column.operator("texturepaint.select_brush", text=brush.name)
        op.brush_name = brush.name

def update_pie_menu(self, context):
  bpy.utils.unregister_class(TEXTUREPAINT_MT_BrushPieMenu)
  bpy.utils.register_class(TEXTUREPAINT_MT_BrushPieMenu)

addon_keymaps = []

def register():
  bpy.utils.register_class(TEXTUREPAINT_OT_SelectBrush)
  bpy.utils.register_class(TEXTUREPAINT_MT_BrushPieMenu)

  bpy.app.handlers.depsgraph_update_post.append(update_pie_menu)

  wm = bpy.context.window_manager
  kc = wm.keyconfigs.addon
  if kc:
    km = kc.keymaps.new(name="Image Paint", space_type="EMPTY")
    kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS')
    kmi.properties.name = "TEXTUREPAINT_MT_brush_pie_menu"
    addon_keymaps.append((km, kmi))

def unregister():
  bpy.utils.unregister_class(TEXTUREPAINT_OT_SelectBrush)
  bpy.utils.unregister_class(TEXTUREPAINT_MT_BrushPieMenu)

  bpy.app.handlers.depsgraph_update_post.remove(update_pie_menu)

  for km, kmi in addon_keymaps:
    km.keymap_items.remove(kmi)
  addon_keymaps.clear()

if __name__ == "__main__":
  register()
