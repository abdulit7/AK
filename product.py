

# import flet as ft

# MENU_ITEMS = []

# def product_view(page: ft.Page, db: 'Database'):
#     page.title = "Manage Products"
#     page.bgcolor = ft.Colors.ORANGE_50
#     page.padding = 5

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()

#     # Input fields for adding new product
#     name_field = ft.TextField(
#         label="Product Name",
#         width=180,
#         text_style=ft.TextStyle(size=12),
#         color=ft.Colors.BLUE_GREY_900,
#         border_color=ft.Colors.AMBER_400,
#         focused_border_color=ft.Colors.AMBER_600,
#     )
#     price_field = ft.TextField(
#         label="Price (Rs)",
#         width=100,
#         text_style=ft.TextStyle(size=12),
#         color=ft.Colors.BLUE_GREY_900,
#         border_color=ft.Colors.AMBER_400,
#         focused_border_color=ft.Colors.AMBER_600,
#         keyboard_type=ft.KeyboardType.NUMBER,
#     )

#     def add_product(e):
#         name = name_field.value.strip()
#         try:
#             price = float(price_field.value.strip())
#         except ValueError:
#             page.snack_bar = ft.SnackBar(ft.Text("Price must be a valid number!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return

#         if not name:
#             page.snack_bar = ft.SnackBar(ft.Text("Product name is required!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         if price <= 0:
#             page.snack_bar = ft.SnackBar(ft.Text("Price must be greater than 0!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return

#         try:
#             db.initialize_menu([{"name": name, "price": price}])
#             global MENU_ITEMS
#             MENU_ITEMS = db.get_menu()
#             update_product_table()
#             name_field.value = ""
#             price_field.value = ""
#             page.snack_bar = ft.SnackBar(ft.Text(f"Added {name} to menu!", color=ft.Colors.GREEN_600), open=True)
#             page.update()
#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(ft.Text(f"Error adding product: {str(ex)}", color=ft.Colors.RED_500), open=True)
#             page.update()

#     # Product table
#     product_table = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Name", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
#             ft.DataColumn(ft.Text("Rs", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
#             ft.DataColumn(ft.Text("Action", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
#         ],
#         rows=[],
#         heading_row_color=ft.Colors.ORANGE_200,
#         border=ft.BorderSide(1, ft.Colors.GREY_400),
#         divider_thickness=1,
#         column_spacing=5,
#         horizontal_margin=5,
#         expand=True,
#     )

#     def update_product_table():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         product_table.rows.clear()
#         for item in MENU_ITEMS:
#             product_table.rows.append(
#                 ft.DataRow(
#                     cells=[
#                         ft.DataCell(ft.Text(item["name"], color=ft.Colors.DEEP_ORANGE_900, size=10, max_lines=1)),
#                         ft.DataCell(ft.Text(f"Rs{item['price']:.2f}", color=ft.Colors.AMBER_800, size=10)),
#                         ft.DataCell(
#                             ft.Row(
#                                 [
#                                     ft.IconButton(
#                                         ft.Icons.EDIT,
#                                         icon_color=ft.Colors.BLUE_500,
#                                         tooltip="Edit",
#                                         icon_size=16,
#                                         on_click=lambda e, n=item["name"], p=item["price"]: show_edit_dialog(n, p),
#                                     ),
#                                     ft.IconButton(
#                                         ft.Icons.DELETE,
#                                         icon_color=ft.Colors.RED_500,
#                                         tooltip="Delete",
#                                         icon_size=16,
#                                         on_click=lambda e, n=item["name"]: show_delete_dialog(n),
#                                     ),
#                                 ],
#                                 spacing=0,
#                             )
#                         ),
#                     ]
#                 )
#             )
#         page.update()

#     def show_edit_dialog(name, price):
#         edit_name_field = ft.TextField(
#             label="Product Name",
#             value=name,
#             width=180,
#             text_style=ft.TextStyle(size=12),
#             color=ft.Colors.BLUE_GREY_900,
#             border_color=ft.Colors.AMBER_400,
#             focused_border_color=ft.Colors.AMBER_600,
#         )
#         edit_price_field = ft.TextField(
#             label="Price (Rs)",
#             value=str(price),
#             width=100,
#             text_style=ft.TextStyle(size=12),
#             color=ft.Colors.BLUE_GREY_900,
#             border_color=ft.Colors.AMBER_400,
#             focused_border_color=ft.Colors.AMBER_600,
#             keyboard_type=ft.KeyboardType.NUMBER,
#         )

#         def save_edit(e):
#             new_name = edit_name_field.value.strip()
#             try:
#                 new_price = float(edit_price_field.value.strip())
#             except ValueError:
#                 page.snack_bar = ft.SnackBar(ft.Text("Price must be a valid number!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return

#             if not new_name:
#                 page.snack_bar = ft.SnackBar(ft.Text("Product name is required!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return
#             if new_price <= 0:
#                 page.snack_bar = ft.SnackBar(ft.Text("Price must be greater than 0!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return

#             try:
#                 db.edit_product(name, new_name, new_price)
#                 global MENU_ITEMS
#                 MENU_ITEMS = db.get_menu()
#                 update_product_table()
#                 dialog.open = False
#                 # if dialog in page.overlay:
#                 #     page.overlay.remove(dialog)
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Updated {new_name}!", color=ft.Colors.GREEN_600), open=True)
#                 page.update()
#                 print(f"Edit dialog closed, overlay size: {len(page.overlay)}")
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Error updating product: {str(ex)}", color=ft.Colors.RED_500), open=True)
#                 page.update()

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Edit Product: {name}", color=ft.Colors.BROWN_800, size=16),
#             content=ft.Column(
#                 [
#                     edit_name_field,
#                     edit_price_field,
#                 ],
#                 tight=True,
#                 spacing=10,
#             ),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
#                 ft.TextButton("Save", on_click=save_edit),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         # page.overlay.clear()
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"Edit dialog opened, overlay size: {len(page.overlay)}")

#     def show_delete_dialog(name):
#         def confirm_delete(e):
#             try:
#                 db.delete_product(name)
#                 global MENU_ITEMS
#                 MENU_ITEMS = db.get_menu()
#                 update_product_table()
#                 dialog.open = False
#                 # if dialog in page.overlay:
#                 #     page.overlay.remove(dialog)
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Deleted {name}!", color=ft.Colors.GREEN_600), open=True)
#                 page.update()
#                 print(f"Delete dialog closed, overlay size: {len(page.overlay)}")
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Error deleting product: {str(ex)}", color=ft.Colors.RED_500), open=True)
#                 page.update()

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Delete Product: {name}", color=ft.Colors.BROWN_800, size=16),
#             content=ft.Text(f"Are you sure you want to delete {name}?"),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
#                 ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED_500)),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         # page.overlay.clear()
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"Delete dialog opened, overlay size: {len(page.overlay)}")

#     def close_dialog(dialog):
#         dialog.open = False
#         # if dialog in page.overlay:
#         #     page.overlay.remove(dialog)
#         page.update()
#         print(f"Dialog closed, overlay size: {len(page.overlay)}")

#     # Initialize product table
#     update_product_table()

#     # Layout
#     content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Container(
#                     content=ft.Text("Manage Products", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text("Add New Product", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
#                             name_field,
#                             price_field,
#                             ft.ElevatedButton(
#                                 "Add Product",
#                                 icon=ft.Icons.ADD,
#                                 color=ft.Colors.GREEN_600,
#                                 on_click=add_product,
#                                 style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                         spacing=10,
#                     ),
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Divider(height=1, color=ft.Colors.GREY_300),
#                 ft.Container(
#                     content=ft.Text("Product List", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=ft.ListView(
#                         controls=[product_table],
#                         expand=1,
#                         auto_scroll=True,
#                     ),
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.ElevatedButton(
#                     "Back to Dashboard",
#                     icon=ft.Icons.ARROW_BACK,
#                     color=ft.Colors.BLUE_500,
#                     on_click=lambda e: page.go("/dashboard"),
#                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=10,
#             scroll=ft.ScrollMode.AUTO,
#         ),
#         width=min(page.width, 360),
#         alignment=ft.alignment.center,
#     )

#     return content

# import flet as ft

# PRODUCT_MENU_ITEMS = []  # Line ~3: Module-level variable

# def product_view(page: ft.Page, db: 'Database'):
#     global PRODUCT_MENU_ITEMS  # Line ~6: Declare global first
#     page.title = "Manage Products"
#     page.bgcolor = ft.Colors.GREY_100
#     page.padding = 10
#     page.scroll = ft.ScrollMode.AUTO

#     try:
#         PRODUCT_MENU_ITEMS = db.get_menu()
#         print(f"Initial product load: {len(PRODUCT_MENU_ITEMS)} items: {PRODUCT_MENU_ITEMS}")
#     except Exception as ex:
#         page.snack_bar = ft.SnackBar(
#             ft.Text(f"Error loading products: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#             open=True,
#             duration=3000,
#         )
#         page.update()

#     # Input fields for adding new product
#     name_field = ft.TextField(
#         label="Product Name",
#         width=200,
#         text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800),
#         label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14),
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_600,
#         content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#         bgcolor=ft.Colors.WHITE,
#         autofocus=True,
#     )
#     price_field = ft.TextField(
#         label="Price (Rs)",
#         width=120,
#         text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800),
#         label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14),
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_600,
#         content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#         keyboard_type=ft.KeyboardType.NUMBER,
#         bgcolor=ft.Colors.WHITE,
#     )

#     def add_product(e):
#         global PRODUCT_MENU_ITEMS  # Line ~40: Declare global
#         name = name_field.value.strip()
#         try:
#             price = float(price_field.value.strip())
#         except ValueError:
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("Price must be a valid number!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return

#         if not name:
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("Product name is required!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return
#         if price <= 0:
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("Price must be greater than 0!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return
#         # Case-insensitive check for existing names
#         if any(item["name"].lower() == name.lower() for item in PRODUCT_MENU_ITEMS):
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Product '{name}' already exists!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return

#         try:
#             print(f"Attempting to add product: {name}, Price={price}")
#             db.initialize_menu([{"name": name, "price": price}])
#             PRODUCT_MENU_ITEMS = db.get_menu()
#             update_product_table()
#             name_field.value = ""
#             price_field.value = ""
#             name_field.focus()
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Added {name} to product list!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             print(f"Added product: {name}, Price={price}, Products: {PRODUCT_MENU_ITEMS}")
#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Error adding product: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             print(f"Error adding product: {str(ex)}")

#     # Product table
#     product_table = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Name", color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD, size=14)),
#         ]
#         + [
#             ft.DataColumn(ft.Text("Price (Rs)", color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD, size=14)),
#             ft.DataColumn(ft.Text("Actions", color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD, size=14)),
#         ],
#         rows=[],
#         heading_row_color=ft.Colors.GREY_200,
#         heading_row_height=48,
#         data_row_color={"hovered": ft.Colors.GREY_100, "": ft.Colors.WHITE},
#         border=ft.BorderSide(1, ft.Colors.GREY_300),
#         divider_thickness=1,
#         column_spacing=12,
#         horizontal_margin=12,
#         data_row_min_height=48,
#         expand=True,
#     )

#     def update_product_table():
#         global PRODUCT_MENU_ITEMS  # Line ~400: Declare global before use
#         try:
#             PRODUCT_MENU_ITEMS = db.get_menu()
#             product_table.rows.clear()
#             for item in PRODUCT_MENU_ITEMS:
#                 product_table.rows.append(
#                     ft.DataRow(
#                         cells=[
#                             ft.DataCell(ft.Text(item["name"], color=ft.Colors.GREY_800, size=14, weight=ft.FontWeight.W_500)),
#                             ft.DataCell(ft.Text(f"Rs{item['price']:.2f}", color=ft.Colors.BLUE_600, size=14, weight=ft.FontWeight.W_500)),
#                             ft.DataCell(
#                                 ft.Row(
#                                     [
#                                         ft.IconButton(
#                                             ft.Icons.EDIT,
#                                             icon_color=ft.Colors.BLUE_600,
#                                             tooltip="Edit Product",
#                                             icon_size=20,
#                                             on_click=lambda e, n=item["name"], p=item["price"]: show_edit_dialog(n, p),
#                                             style=ft.ButtonStyle(
#                                                 padding=8,
#                                                 shape=ft.CircleBorder(),
#                                                 bgcolor={"hovered": ft.Colors.BLUE_50},
#                                             ),
#                                         ),
#                                         ft.IconButton(
#                                             ft.Icons.DELETE_OUTLINE,
#                                             icon_color=ft.Colors.RED_600,
#                                             tooltip="Delete Product",
#                                             icon_size=20,
#                                             on_click=lambda e, n=item["name"]: show_delete_dialog(n),
#                                             style=ft.ButtonStyle(
#                                                 padding=8,
#                                                 shape=ft.CircleBorder(),
#                                                 bgcolor={"hovered": ft.Colors.RED_50},
#                                             ),
#                                         ),
#                                     ],
#                                     spacing=8,
#                                 )
#                             ),
#                         ]
#                     )
#                 )
#             page.update()
#             print(f"Updated product table with {len(PRODUCT_MENU_ITEMS)} items: {PRODUCT_MENU_ITEMS}")
#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Error updating product table: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             print(f"Error updating product table: {str(ex)}")

#     def show_edit_dialog(name, price):
#         print(f"Opening edit dialog for: name={name}, price={price}")
#         edit_name_field = ft.TextField(
#             label="Product Name",
#             value=name,
#             width=200,
#             text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800),
#             label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14),
#             border_color=ft.Colors.GREY_300,
#             focused_border_color=ft.Colors.BLUE_600,
#             content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#             bgcolor=ft.Colors.WHITE,
#             autofocus=True,  # ✅ Fix: let Flet focus it after mount; no manual focus()
#         )
#         edit_price_field = ft.TextField(
#             label="Price (Rs)",
#             value=str(price),
#             width=120,
#             text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800),
#             label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14),
#             border_color=ft.Colors.GREY_300,
#             focused_border_color=ft.Colors.BLUE_600,
#             content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#             keyboard_type=ft.KeyboardType.NUMBER,
#             bgcolor=ft.Colors.WHITE,
#         )

#         def save_edit(e):
#             global PRODUCT_MENU_ITEMS  # Line ~500: Declare global
#             new_name = edit_name_field.value.strip()
#             try:
#                 new_price = float(edit_price_field.value.strip())
#             except ValueError:
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text("Price must be a valid number!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 return

#             if not new_name:
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text("Product name is required!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 return
#             if new_price <= 0:
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text("Price must be greater than 0!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 return
#             # Case-insensitive check for existing names
#             if new_name != name and any(item["name"].lower() == new_name.lower() for item in PRODUCT_MENU_ITEMS):
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(f"Product '{new_name}' already exists!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 return

#             try:
#                 print(f"Attempting to edit product: old_name={name}, new_name={new_name}, new_price={new_price}")
#                 db.edit_product(name, new_name, new_price)
#                 PRODUCT_MENU_ITEMS = db.get_menu()
#                 print(f"Post-edit product list: {PRODUCT_MENU_ITEMS}")
#                 update_product_table()
#                 dialog.open = False
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(f"Updated {new_name}!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 print(f"Edited product: {name} -> {new_name}, Price={new_price}")
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(f"Error updating product: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 print(f"Error editing product: {str(ex)}")

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Edit Product: {name}", color=ft.Colors.GREY_800, size=16, weight=ft.FontWeight.BOLD),
#             content=ft.Column(
#                 [
#                     edit_name_field,
#                     edit_price_field,
#                 ],
#                 tight=True,
#                 spacing=12,
#                 width=280,
#             ),
#             actions=[
#                 ft.TextButton(
#                     "Cancel",
#                     style=ft.ButtonStyle(color=ft.Colors.GREY_600, padding=10),
#                     on_click=lambda e: close_dialog(dialog),
#                 ),
#                 ft.ElevatedButton(
#                     "Save",
#                     icon=ft.Icons.SAVE,
#                     style=ft.ButtonStyle(
#                         color=ft.Colors.WHITE,
#                         bgcolor=ft.Colors.BLUE_600,
#                         padding=10,
#                         shape=ft.RoundedRectangleBorder(radius=8),
#                     ),
#                     on_click=save_edit,
#                 ),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=ft.Colors.WHITE,
#             shape=ft.RoundedRectangleBorder(radius=10),
#         )
#         page.dialog = dialog
#         dialog.open = True
#         page.overlay.append(dialog)  # Ensure dialog is in overlay
#         page.update()
#         # ❌ removed: edit_name_field.focus()

#     def show_delete_dialog(name):
#         print(f"Opening delete dialog for: name={name}")
#         def confirm_delete(e):
#             global PRODUCT_MENU_ITEMS  # Line ~600: Declare global
#             try:
#                 print(f"Attempting to delete product: {name}")
#                 db.delete_product(name)
#                 PRODUCT_MENU_ITEMS = db.get_menu()
#                 print(f"Post-delete product list: {PRODUCT_MENU_ITEMS}")
#                 update_product_table()
#                 dialog.open = False
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(f"Deleted {name}!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 print(f"Deleted product: {name}")
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(f"Error deleting product: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 print(f"Error deleting product: {str(ex)}")

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Delete Product: {name}", color=ft.Colors.GREY_800, size=16, weight=ft.FontWeight.BOLD),
#             content=ft.Text(f"Are you sure you want to delete {name}?", color=ft.Colors.GREY_700, size=14),
#             actions=[
#                 ft.TextButton(
#                     "Cancel",
#                     style=ft.ButtonStyle(color=ft.Colors.GREY_600, padding=10),
#                     on_click=lambda e: close_dialog(dialog),
#                 ),
#                 ft.ElevatedButton(
#                     "Delete",
#                     icon=ft.Icons.DELETE,
#                     style=ft.ButtonStyle(
#                         color=ft.Colors.WHITE,
#                         bgcolor=ft.Colors.RED_600,
#                         padding=10,
#                         shape=ft.RoundedRectangleBorder(radius=8),
#                     ),
#                     on_click=confirm_delete,
#                 ),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=ft.Colors.WHITE,
#             shape=ft.RoundedRectangleBorder(radius=10),
#         )
#         page.dialog = dialog
#         dialog.open = True
#         page.overlay.append(dialog)  # Ensure dialog is in overlay
#         page.update()

#     def close_dialog(dialog):
#         dialog.open = False
#         page.update()

#     # Initialize product table
#     update_product_table()

#     # Layout
#     content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Container(
#                     content=ft.Row(
#                         [
#                             ft.Text(
#                                 "Manage Products",
#                                 size=24,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.GREY_800,
#                                 font_family="Roboto",
#                             ),
#                             ft.IconButton(
#                                 ft.Icons.ARROW_BACK,
#                                 icon_color=ft.Colors.BLUE_600,
#                                 tooltip="Back to Dashboard",
#                                 on_click=lambda e: page.go("/dashboard"),
#                                 style=ft.ButtonStyle(
#                                     padding=8,
#                                     shape=ft.CircleBorder(),
#                                     bgcolor={"hovered": ft.Colors.BLUE_50},
#                                 ),
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(bottom=12),
#                 ),
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text(
#                                 "Add New Product",
#                                 size=16,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.GREY_800,
#                             ),
#                             ft.Row(
#                                 [
#                                     name_field,
#                                     price_field,
#                                     ft.ElevatedButton(
#                                         "Add Product",
#                                         icon=ft.Icons.ADD,
#                                         style=ft.ButtonStyle(
#                                             color=ft.Colors.WHITE,
#                                             bgcolor=ft.Colors.GREEN_600,
#                                             padding=12,
#                                             shape=ft.RoundedRectangleBorder(radius=8),
#                                             elevation={"pressed": 2, "": 4},
#                                         ),
#                                         on_click=add_product,
#                                     ),
#                                 ],
#                                 alignment=ft.MainAxisAlignment.CENTER,
#                                 spacing=12,
#                                 wrap=True,
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         spacing=12,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(bottom=12),
#                 ),
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text(
#                                 "Product List",
#                                 size=16,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.GREY_800,
#                             ),
#                             ft.ListView(
#                                 controls=[product_table],
#                                 expand=True,
#                                 auto_scroll=True,
#                             ),
#                         ],
#                         spacing=12,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(bottom=12),
#                     height=page.height - 300,
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.START,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=12,
#             scroll=ft.ScrollMode.AUTO,
#         ),
#         width=min(page.width, 360),
#         alignment=ft.alignment.center,
#     )

#     return content




import flet as ft

PRODUCT_MENU_ITEMS = []

def product_view(page: ft.Page, db: 'Database'):
    global PRODUCT_MENU_ITEMS
    page.title = "Manage Products"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO

    COLOR_SCHEME = {
        "primary": ft.Colors.BLUE_700,
        "accent": ft.Colors.AMBER_600,
        "background": ft.Colors.WHITE,
        "text": ft.Colors.BLACK87,
        "error": ft.Colors.RED_600,
        "success": ft.Colors.GREEN_600
    }

    try:
        PRODUCT_MENU_ITEMS = db.get_menu()
        print(f"Initial product load: {len(PRODUCT_MENU_ITEMS)} items: {PRODUCT_MENU_ITEMS}")
    except Exception as ex:
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Error loading products: {str(ex)}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
            open=True,
            duration=3000,
        )
        page.update()

    # Input fields for adding new product
    name_field = ft.TextField(
        label="Product Name",
        width=200,
        text_style=ft.TextStyle(size=14, color=COLOR_SCHEME["text"]),
        label_style=ft.TextStyle(color=COLOR_SCHEME["text"], size=14),
        border_color=COLOR_SCHEME["primary"],
        focused_border_color=COLOR_SCHEME["accent"],
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        bgcolor=COLOR_SCHEME["background"],
        filled=True,
        autofocus=True,
    )
    price_field = ft.TextField(
        label="Price (Rs)",
        width=120,
        text_style=ft.TextStyle(size=14, color=COLOR_SCHEME["text"]),
        label_style=ft.TextStyle(color=COLOR_SCHEME["text"], size=14),
        border_color=COLOR_SCHEME["primary"],
        focused_border_color=COLOR_SCHEME["accent"],
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=COLOR_SCHEME["background"],
        filled=True,
    )
    category_dropdown = ft.Dropdown(
        label="Category",
        width=150,
        options=[
            ft.dropdown.Option("Appetizer"),
            ft.dropdown.Option("Main Course"),
            ft.dropdown.Option("Dessert"),
            ft.dropdown.Option("Beverage"),
            ft.dropdown.Option("Non"),
        ],
        value="Non",
        border_color=COLOR_SCHEME["primary"],
        focused_border_color=COLOR_SCHEME["accent"],
        text_style=ft.TextStyle(color=COLOR_SCHEME["text"]),
        bgcolor=COLOR_SCHEME["background"],
        filled=True,
    )

    def add_product(e):
        global PRODUCT_MENU_ITEMS
        name = name_field.value.strip()
        try:
            price = float(price_field.value.strip())
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Price must be a valid number!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            return

        category = category_dropdown.value
        if not name:
            page.snack_bar = ft.SnackBar(
                ft.Text("Product name is required!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            return
        if price <= 0:
            page.snack_bar = ft.SnackBar(
                ft.Text("Price must be greater than 0!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            return
        if any(item["name"].lower() == name.lower() for item in PRODUCT_MENU_ITEMS):
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Product '{name}' already exists!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            return

        try:
            print(f"Attempting to add product: {name}, Price={price}, Category={category}")
            db.cursor.execute('''
                INSERT INTO product (name, price, category)
                VALUES (?, ?, ?)
            ''', (name, price, category))
            db.conn.commit()
            PRODUCT_MENU_ITEMS = db.get_menu()
            update_product_table()
            name_field.value = ""
            price_field.value = ""
            category_dropdown.value = "Non"
            name_field.focus()
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Added {name} to product list!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["success"]),
                open=True,
                duration=3000,
            )
            page.update()
            print(f"Added product: {name}, Price={price}, Category={category}, Products: {PRODUCT_MENU_ITEMS}")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error adding product: {str(ex)}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            print(f"Error adding product: {str(ex)}")

    # Product table
    product_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name", color=COLOR_SCHEME["text"], weight=ft.FontWeight.BOLD, size=14)),
            ft.DataColumn(ft.Text("Price (Rs)", color=COLOR_SCHEME["text"], weight=ft.FontWeight.BOLD, size=14)),
            #ft.DataColumn(ft.Text("Category", color=COLOR_SCHEME["text"], weight=ft.FontWeight.BOLD, size=14)),
            ft.DataColumn(ft.Text("Actions", color=COLOR_SCHEME["text"], weight=ft.FontWeight.BOLD, size=14)),
        ],
        rows=[],
        heading_row_color=ft.Colors.GREY_200,
        heading_row_height=48,
        data_row_color={"hovered": ft.Colors.GREY_100, "": COLOR_SCHEME["background"]},
        border=ft.BorderSide(1, ft.Colors.GREY_300),
        divider_thickness=1,
        column_spacing=12,
        horizontal_margin=12,
        data_row_min_height=48,
        expand=True,
    )

    def update_product_table():
        global PRODUCT_MENU_ITEMS
        try:
            PRODUCT_MENU_ITEMS = db.get_menu()
            product_table.rows.clear()
            for item in PRODUCT_MENU_ITEMS:
                product_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["name"], color=COLOR_SCHEME["text"], size=14, weight=ft.FontWeight.W_500)),
                            ft.DataCell(ft.Text(f"Rs{item['price']:.2f}", color=COLOR_SCHEME["primary"], size=14, weight=ft.FontWeight.W_500)),
                            #ft.DataCell(ft.Text(item.get("category", "Non"), color=COLOR_SCHEME["text"], size=14, weight=ft.FontWeight.W_500)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            ft.Icons.EDIT,
                                            icon_color=COLOR_SCHEME["primary"],
                                            tooltip="Edit Product",
                                            icon_size=20,
                                            on_click=lambda e, n=item["name"], p=item["price"]: show_edit_dialog(n, p),
                                            style=ft.ButtonStyle(
                                                padding=8,
                                                shape=ft.CircleBorder(),
                                                bgcolor={"hovered": ft.Colors.BLUE_50},
                                            ),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE_OUTLINE,
                                            icon_color=COLOR_SCHEME["error"],
                                            tooltip="Delete Product",
                                            icon_size=20,
                                            on_click=lambda e, n=item["name"]: show_delete_dialog(n),
                                            style=ft.ButtonStyle(
                                                padding=8,
                                                shape=ft.CircleBorder(),
                                                bgcolor={"hovered": ft.Colors.RED_50},
                                            ),
                                        ),
                                    ],
                                    spacing=8,
                                )
                            ),
                        ]
                    )
                )
            page.update()
            print(f"Updated product table with {len(PRODUCT_MENU_ITEMS)} items: {PRODUCT_MENU_ITEMS}")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error updating product table: {str(ex)}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                duration=3000,
            )
            page.update()
            print(f"Error updating product table: {str(ex)}")

    def show_edit_dialog(name, price, category):
        print(f"Opening edit dialog for: name={name}, price={price}")
        edit_name_field = ft.TextField(
            label="Product Name",
            value=name,
            width=200,
            text_style=ft.TextStyle(size=14, color=COLOR_SCHEME["text"]),
            label_style=ft.TextStyle(color=COLOR_SCHEME["text"], size=14),
            border_color=COLOR_SCHEME["primary"],
            focused_border_color=COLOR_SCHEME["accent"],
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            bgcolor=COLOR_SCHEME["background"],
            filled=True,
            autofocus=True,
        )
        edit_price_field = ft.TextField(
            label="Price (Rs)",
            value=str(price),
            width=120,
            text_style=ft.TextStyle(size=14, color=COLOR_SCHEME["text"]),
            label_style=ft.TextStyle(color=COLOR_SCHEME["text"], size=14),
            border_color=COLOR_SCHEME["primary"],
            focused_border_color=COLOR_SCHEME["accent"],
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=COLOR_SCHEME["background"],
            filled=True,
        )
        edit_category_dropdown = ft.Dropdown(
            label="Category",
            width=150,
            options=[
                ft.dropdown.Option("Appetizer"),
                ft.dropdown.Option("Main Course"),
                ft.dropdown.Option("Dessert"),
                ft.dropdown.Option("Beverage"),
                ft.dropdown.Option("Non"),
            ],
            value=category,
            border_color=COLOR_SCHEME["primary"],
            focused_border_color=COLOR_SCHEME["accent"],
            text_style=ft.TextStyle(color=COLOR_SCHEME["text"]),
            bgcolor=COLOR_SCHEME["background"],
            filled=True,
        )

        def save_edit(e):
            global PRODUCT_MENU_ITEMS
            new_name = edit_name_field.value.strip()
            try:
                new_price = float(edit_price_field.value.strip())
            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Price must be a valid number!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                return

            new_category = edit_category_dropdown.value
            if not new_name:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Product name is required!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                return
            if new_price <= 0:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Price must be greater than 0!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                return
            if new_name != name and any(item["name"].lower() == new_name.lower() for item in PRODUCT_MENU_ITEMS):
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Product '{new_name}' already exists!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                return

            try:
                print(f"Attempting to edit product: old_name={name}, new_name={new_name}, new_price={new_price}, new_category={new_category}")
                db.edit_product(name, new_name, new_price, new_category)
                PRODUCT_MENU_ITEMS = db.get_menu()
                print(f"Post-edit product list: {PRODUCT_MENU_ITEMS}")
                update_product_table()
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Updated {new_name}!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["success"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                print(f"Edited product: {name} -> {new_name}, Price={new_price}, Category={new_category}")
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error updating product: {str(ex)}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                print(f"Error editing product: {str(ex)}")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit Product: {name}", color=COLOR_SCHEME["text"], size=16, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    edit_name_field,
                    edit_price_field,
                    edit_category_dropdown,
                ],
                tight=True,
                spacing=12,
                width=280,
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    style=ft.ButtonStyle(color=COLOR_SCHEME["text"], padding=10),
                    on_click=lambda e: close_dialog(dialog),
                ),
                ft.ElevatedButton(
                    "Save",
                    icon=ft.Icons.SAVE,
                    style=ft.ButtonStyle(
                        color=COLOR_SCHEME["background"],
                        bgcolor=COLOR_SCHEME["success"],
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=save_edit,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=COLOR_SCHEME["background"],
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        page.dialog = dialog
        dialog.open = True
        page.overlay.append(dialog)
        page.update()

    def show_delete_dialog(name):
        print(f"Opening delete dialog for: name={name}")
        def confirm_delete(e):
            global PRODUCT_MENU_ITEMS
            try:
                print(f"Attempting to delete product: {name}")
                db.delete_product(name)
                PRODUCT_MENU_ITEMS = db.get_menu()
                print(f"Post-delete product list: {PRODUCT_MENU_ITEMS}")
                update_product_table()
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Deleted {name}!", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["success"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                print(f"Deleted product: {name}")
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error deleting product: {str(ex)}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                    open=True,
                    duration=3000,
                )
                page.update()
                print(f"Error deleting product: {str(ex)}")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Delete Product: {name}", color=COLOR_SCHEME["text"], size=16, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete {name}?", color=COLOR_SCHEME["text"], size=14),
            actions=[
                ft.TextButton(
                    "Cancel",
                    style=ft.ButtonStyle(color=COLOR_SCHEME["text"], padding=10),
                    on_click=lambda e: close_dialog(dialog),
                ),
                ft.ElevatedButton(
                    "Delete",
                    icon=ft.Icons.DELETE,
                    style=ft.ButtonStyle(
                        color=COLOR_SCHEME["background"],
                        bgcolor=COLOR_SCHEME["error"],
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=confirm_delete,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=COLOR_SCHEME["background"],
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        page.dialog = dialog
        dialog.open = True
        page.overlay.append(dialog)
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # Initialize product table
    update_product_table()

    # Layout
    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "Manage Products",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_SCHEME["text"],
                                font_family="Roboto",
                            ),
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                icon_color=COLOR_SCHEME["primary"],
                                tooltip="Back to Dashboard",
                                on_click=lambda e: page.go("/dashboard"),
                                style=ft.ButtonStyle(
                                    padding=8,
                                    shape=ft.CircleBorder(),
                                    bgcolor={"hovered": ft.Colors.BLUE_50},
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=12,
                    bgcolor=COLOR_SCHEME["background"],
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(bottom=12),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Add New Product",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_SCHEME["text"],
                            ),
                            ft.Row(
                                [
                                    name_field,
                                    price_field,
                                    category_dropdown,
                                    ft.ElevatedButton(
                                        "Add Product",
                                        icon=ft.Icons.ADD,
                                        style=ft.ButtonStyle(
                                            color=COLOR_SCHEME["background"],
                                            bgcolor=COLOR_SCHEME["success"],
                                            padding=12,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            elevation={"pressed": 2, "": 4},
                                        ),
                                        on_click=add_product,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=12,
                                wrap=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=12,
                    bgcolor=COLOR_SCHEME["background"],
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(bottom=12),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Product List",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_SCHEME["text"],
                            ),
                            ft.ListView(
                                controls=[product_table],
                                expand=True,
                                auto_scroll=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=12,
                    bgcolor=COLOR_SCHEME["background"],
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(bottom=12),
                    height=page.height - 300,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=min(page.width, 800),
        alignment=ft.alignment.center,
    )

    return content
