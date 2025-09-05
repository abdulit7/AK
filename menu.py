# import flet as ft
# import time
# from datetime import datetime
# import os
# from setting import check_permissions, print_kitchen_receipt, print_customer_bill

# MENU_ITEMS = []
# ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
# TOTAL_SALES = 0.0
# is_completing = False  # Debounce flag

# # Helper function for 5-digit order ID
# def get_next_order_id(db):
#     if 'jnius' in globals():
#         print("Using timestamp-based order ID for Android")
#         return f"{int(time.time()) % 99999:05d}"  # Use timestamp for Android
#     order_id_file = "last_order_id.txt"
#     try:
#         if os.path.exists(order_id_file):
#             with open(order_id_file, "r") as f:
#                 last_id = int(f.read().strip() or 0)
#         else:
#             last_id = 0
#         next_id = (last_id % 99999) + 1
#         with open(order_id_file, "w") as f:
#             f.write(str(next_id))
#         return f"{next_id:05d}"
#     except Exception as ex:
#         print(f"Error generating order ID: {ex}")
#         return "00001"

# def menu_view(page: ft.Page, db: 'Database'):
#     page.title = "Menu"
#     page.bgcolor = ft.Colors.ORANGE_50
#     page.padding = 5
#     page.scroll = ft.ScrollMode.AUTO

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()
#     current_order_type = page.client_storage.get("current_order_type") or "dine_in"
#     print(f"Initial order type: {current_order_type}")
#     current_order = ORDERS[current_order_type]
#     order_items = {}

#     ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]

#     def switch_order_type(e):
#         nonlocal current_order_type, current_order
#         current_order_type = ORDER_TYPES[e.control.selected_index]
#         page.client_storage.set("current_order_type", current_order_type)
#         current_order = ORDERS[current_order_type]
#         print(f"Switched to order type: {current_order_type}")
#         update_order_display()
#         update_order_summary()

#     tabs = ft.Tabs(
#         selected_index=0,
#         animation_duration=300,
#         tab_alignment=ft.TabAlignment.CENTER,
#         indicator_color=ft.Colors.AMBER_400,
#         label_color=ft.Colors.GREY_800,
#         unselected_label_color=ft.Colors.GREY_500,
#         tabs=[
#             ft.Tab(text="Dine-In", icon=ft.Icons.RESTAURANT),
#             ft.Tab(text="Takeaway", icon=ft.Icons.TAKEOUT_DINING),
#             ft.Tab(text="Delivery", icon=ft.Icons.CALL),
#         ],
#         on_change=switch_order_type,
#     )

#     order_type_display = ft.Text(
#         value=f"Current Mode: {current_order_type.replace('_', ' ').title()}",
#         size=14,
#         color=ft.Colors.BLUE_GREY_900,
#         weight=ft.FontWeight.BOLD
#     )

#     def update_order_display():
#         order_type_display.value = f"Current Mode: {current_order_type.replace('_', ' ').title()}"
#         print(f"Updated order type display: {order_type_display.value}")
#         page.update()

#     def complete_order(e):
#         global is_completing
#         if is_completing:
#             print("Debounce: Complete button already processing")
#             return
#         if not order_items:
#             print("No items in order_items")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         show_order_details_dialog("complete")

#     def complete_order_with_details(order_id, order_details, table_number, customer_name, customer_number, address):
#         print(f"Completing order ID: {order_id}, Details: {order_details}")
#         if not order_details:
#             print("No order details provided")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return

#         # Clear UI first
#         print(f"Before clear: order_items={order_items}, order_list.controls={len(order_list.controls)}")
#         order_items.clear()
#         order_list.controls = []
#         order_list.visible = False  # Force redraw
#         page.update()
#         order_list.visible = True
#         update_order_summary()
#         page.update()

#         try:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             db.add_order(order_id, current_order_type, order_details, date_time, table_number, customer_name, customer_number, address)
#             print(f"Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}, DateTime={date_time}, Table={table_number}, Name={customer_name}, Number={customer_number}, Address={address}")
#             status = print_kitchen_receipt(order_id, order_details, page, table_number, customer_name, customer_number, address)
#             print(f"Kitchen receipt status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             status = print_customer_bill(order_id, order_details, page, table_number, customer_name, customer_number, address)
#             print(f"Customer bill status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             page.snack_bar = ft.SnackBar(ft.Text(f"Order {order_id} completed!", color=ft.Colors.GREEN_600), open=True)
#             page.update()
#             print(f"Order completed: {order_id}, Order items: {len(order_items)}, Controls: {len(order_list.controls)}, Overlay size: {len(page.overlay)}")
#         except Exception as ex:
#             print(f"Error completing order: {ex}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.RED_500), open=True)
#             page.update()

#     def show_order_details_dialog(mode):
#         print(f"Opening order details dialog for mode: {mode}, order_items: {order_items}")
#         table_number_field = ft.TextField(label="Table Number", width=200, visible=current_order_type == "dine_in")
#         customer_name_field = ft.TextField(label="Customer Name", width=200, visible=current_order_type in ["takeaway", "Delivery"])
#         customer_number_field = ft.TextField(label="Customer Number", width=200, visible=current_order_type == "Delivery")
#         address_field = ft.TextField(label="Address", width=200, visible=current_order_type == "Delivery")

#         def validate_and_process(e):
#             global is_completing
#             if mode == "complete" and is_completing:
#                 print("Debounce: Complete button already processing")
#                 return
#             if mode == "complete":
#                 is_completing = True

#             table_number = table_number_field.value.strip() if current_order_type == "dine_in" else None
#             customer_name = customer_name_field.value.strip() if current_order_type in ["takeaway", "Delivery"] else None
#             customer_number = customer_number_field.value.strip() or None if current_order_type == "Delivery" else None
#             address = address_field.value.strip() or None if current_order_type == "Delivery" else None

#             print(f"Validating: Table={table_number}, Name={customer_name}, Number={customer_number}, Address={address}")

#             if current_order_type == "dine_in" and not table_number:
#                 print("Validation failed: Table number required for dine-in")
#                 page.snack_bar = ft.SnackBar(ft.Text("Table number is required for dine-in!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return
#             if current_order_type == "takeaway" and not customer_name:
#                 print("Validation failed: Customer name required for takeaway")
#                 page.snack_bar = ft.SnackBar(ft.Text("Customer name is required for takeaway!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return

#             dialog.open = False
#             page.update()
#             print(f"Order details dialog closed, overlay size: {len(page.overlay)}")

#             order_id = get_next_order_id(db)
#             order_details = [
#                 {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
#                 for name, qty in order_items.items() if qty > 0
#             ]
#             print(f"Generated order details: {order_details}")

#             if mode == "receipt":
#                 status = print_kitchen_receipt(order_id, order_details, page, table_number, customer_name, customer_number, address)
#                 print(f"Receipt print status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "bill":
#                 status = print_customer_bill(order_id, order_details, page, table_number, customer_name, customer_number, address)
#                 print(f"Bill print status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "complete":
#                 complete_order_with_details(order_id, order_details, table_number, customer_name, customer_number, address)
#                 is_completing = False

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Enter {current_order_type.replace('_', ' ').title()} Details for {mode.title()}", size=16),
#             content=ft.Column(
#                 [
#                     table_number_field,
#                     customer_name_field,
#                     customer_number_field,
#                     address_field,
#                 ],
#                 tight=True,
#                 spacing=10,
#             ),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_quantity_dialog(page, dialog)),
#                 ft.TextButton("OK", on_click=validate_and_process),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"Order details dialog opened for {mode}, overlay size: {len(page.overlay)}")

#     menu_title = ft.Text("Menu", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
#     menu_container = ft.ListView(
#         expand=1,
#         spacing=10,
#         padding=10,
#         auto_scroll=True,
#     )

#     def update_menu_container():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         print(f"Updating menu container with {len(MENU_ITEMS)} items")
#         menu_container.controls.clear()
#         for item in MENU_ITEMS:
#             menu_container.controls.append(
#                 ft.Card(
#                     elevation=4,
#                     color=ft.Colors.WHITE,
#                     content=ft.Container(
#                         content=ft.Column(
#                             [
#                                 ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE_900, text_align=ft.TextAlign.CENTER),
#                                 ft.Text(f"Rs{item['price']:.2f}", size=12, color=ft.Colors.AMBER_800, text_align=ft.TextAlign.CENTER),
#                                 ft.ElevatedButton(
#                                     "Select Quantity",
#                                     icon=ft.Icons.ADD_SHOPPING_CART,
#                                     color=ft.Colors.GREEN_500,
#                                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#                                     on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                                     width=250,
#                                     height=36
#                                 ),
#                             ],
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                             spacing=8,
#                         ),
#                         padding=10,
#                         width=360,
#                     ),
#                     key=item["name"],
#                 )
#             )
#         page.update()

#     update_menu_container()

#     display_value = ft.TextField(
#         value="0",
#         label="Quantity",
#         text_size=14,
#         text_align=ft.TextAlign.CENTER,
#         read_only=True,
#         color=ft.Colors.BLUE_GREY_900,
#         border_color=ft.Colors.AMBER_400,
#         focused_border_color=ft.Colors.AMBER_600,
#         width=150,
#         key="qty_display",
#     )

#     def update_display(e, digit):
#         current = display_value.value
#         if current == "0":
#             display_value.value = digit
#         else:
#             display_value.value = current + digit
#         print(f"Updated quantity display: {display_value.value}")
#         page.update()

#     def close_quantity_dialog(page, dialog):
#         dialog.open = False
#         display_value.value = "0"
#         print("Quantity dialog closed")
#         page.update()

#     def add_quantity(page, dialog, item_name, qty):
#         try:
#             quantity = int(qty)
#             if quantity <= 0:
#                 print("Invalid quantity: must be greater than 0")
#                 page.snack_bar = ft.SnackBar(ft.Text("Quantity must be greater than 0", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return
#             if item_name not in order_items:
#                 order_items[item_name] = 0
#             order_items[item_name] = quantity
#             print(f"Added {quantity} {item_name} to order_items")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.GREEN_600), open=True)
#             update_order_summary()
#         except ValueError:
#             print("Invalid quantity: not a number")
#             page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid number", color=ft.Colors.RED_500), open=True)
#         close_quantity_dialog(page, dialog)

#     def show_quantity_dialog(page, item_name):
#         print(f"Opening quantity dialog for {item_name}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Select Quantity for {item_name}", color=ft.Colors.BROWN_800, size=16),
#             content=ft.Column(
#                 [
#                     ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("7", on_click=lambda e: update_display(e, "7"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("8", on_click=lambda e: update_display(e, "8"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("9", on_click=lambda e: update_display(e, "9"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("4", on_click=lambda e: update_display(e, "4"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("5", on_click=lambda e: update_display(e, "5"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("6", on_click=lambda e: update_display(e, "6"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("1", on_click=lambda e: update_display(e, "1"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("2", on_click=lambda e: update_display(e, "2"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("3", on_click=lambda e: update_display(e, "3"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("0", on_click=lambda e: update_display(e, "0"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("OK", on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value), color=ft.Colors.GREEN_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("Cancel", on_click=lambda e: close_quantity_dialog(page, dialog), color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     display_value,
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=10,
#                 width=300,
#             ),
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"Quantity dialog opened, overlay size: {len(page.overlay)}")

#     order_title = ft.Text("Current Order", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
#     order_list = ft.ListView(expand=1, spacing=8, padding=10)
#     total_text = ft.Text(value="Total: Rs0.0", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)

#     # Buttons with initial disabled state
#     receipt_button = ft.ElevatedButton(
#         "Receipt",
#         icon=ft.Icons.PRINT,
#         color=ft.Colors.BLUE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("receipt"),
#     )
#     bill_button = ft.ElevatedButton(
#         "Bill",
#         icon=ft.Icons.RECEIPT,
#         color=ft.Colors.GREEN_600,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("bill"),
#     )
#     complete_button = ft.ElevatedButton(
#         "Complete",
#         icon=ft.Icons.DONE,
#         color=ft.Colors.PURPLE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=complete_order,
#     )

#     def update_order_summary():
#         order_list.controls = []
#         subtotal = 0.0
#         for item_name, qty in order_items.items():
#             if qty > 0:
#                 item = next((i for i in MENU_ITEMS if i["name"] == item_name), None)
#                 if item:
#                     item_total = qty * item["price"]
#                     subtotal += item_total
#                     order_list.controls.append(
#                         ft.Card(
#                             elevation=4,
#                             color=ft.Colors.WHITE,
#                             content=ft.Container(
#                                 content=ft.Row(
#                                     [
#                                         ft.Text(f"{item_name} x {qty}", size=14, color=ft.Colors.DEEP_ORANGE_900),
#                                         ft.Text(f"Rs{item_total:.2f}", size=14, color=ft.Colors.AMBER_800),
#                                     ],
#                                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                 ),
#                                 padding=8,
#                             ),
#                         )
#                     )
#         total_text.value = f"Total: Rs{subtotal:.2f}"
#         global TOTAL_SALES
#         TOTAL_SALES = subtotal
#         has_items = len(order_items) > 0
#         receipt_button.disabled = not has_items
#         bill_button.disabled = not has_items
#         complete_button.disabled = not has_items
#         print(f"Order summary updated: {len(order_list.controls)} items, Total: {total_text.value}, Order items: {order_items}, Buttons enabled: {has_items}")
#         page.update()

#     # Check permissions when the view is loaded or resumed
#     page.on_resume = lambda e: setattr(page, 'snack_bar', ft.SnackBar(ft.Text(check_permissions(page), color=ft.Colors.BLUE_600), open=True)) or page.update()

#     menu_content = ft.Container(
#         content=ft.Column(
#             [
#                 tabs,
#                 order_type_display,
#                 ft.Container(
#                     content=menu_title,
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=menu_container,
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Divider(height=1, color=ft.Colors.GREY_300),
#                 ft.Container(
#                     content=order_title,
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=order_list,
#                     padding=8,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=total_text,
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_200,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Row(
#                     [
#                         receipt_button,
#                         bill_button,
#                         complete_button,
#                     ],
#                     alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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

#     return menu_content



# import flet as ft
# import time
# from datetime import datetime
# import os
# from setting import check_permissions, print_kitchen_receipt, print_customer_bill

# MENU_ITEMS = []
# ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
# TOTAL_SALES = 0.0
# is_completing = False  # Debounce flag

# def get_next_order_id(db):
#     print("DEBUG: Generating next order ID")
#     if 'jnius' in globals():
#         order_id = f"{int(time.time()) % 99999:05d}"
#         print(f"DEBUG: Using timestamp-based order ID: {order_id}")
#         return order_id
#     order_id_file = "last_order_id.txt"
#     try:
#         if os.path.exists(order_id_file):
#             with open(order_id_file, "r") as f:
#                 last_id = int(f.read().strip() or 0)
#         else:
#             last_id = 0
#         next_id = (last_id % 99999) + 1
#         with open(order_id_file, "w") as f:
#             f.write(str(next_id))
#         print(f"DEBUG: Generated file-based order ID: {next_id:05d}")
#         return f"{next_id:05d}"
#     except Exception as ex:
#         print(f"DEBUG: Error generating order ID: {ex}")
#         return "00001"

# def menu_view(page: ft.Page, db: 'Database'):
#     page.title = "Menu"
#     page.bgcolor = ft.Colors.ORANGE_50
#     page.padding = 5
#     page.scroll = ft.ScrollMode.AUTO

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()
#     print(f"DEBUG: Loaded menu items: {MENU_ITEMS}")
#     current_order_type = page.client_storage.get("current_order_type") or "dine_in"
#     print(f"DEBUG: Initial order type: {current_order_type}")
#     current_order = ORDERS[current_order_type]
#     order_items = {}
#     selected_waiter = page.client_storage.get("selected_waiter") or None
#     print(f"DEBUG: Initial waiter: {selected_waiter}")

#     ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]
#     WAITERS = ["Ali", "Ahmed", "Sara", "Zain"]
#     # Color palette for menu item cards
#     CARD_COLORS = [ft.Colors.RED_200, ft.Colors.BLUE_200, ft.Colors.GREEN_200, ft.Colors.YELLOW_200, ft.Colors.PURPLE_200]

#     # Waiter and Order Type Dropdowns
#     waiter_dropdown = ft.Dropdown(
#         label="Select Waiter",
#         width=180,
#         options=[ft.dropdown.Option(w) for w in WAITERS],
#         value=selected_waiter,
#         on_change=lambda e: save_waiter(e.control.value),
#     )

#     order_type_dropdown = ft.Dropdown(
#         label="Order Type",
#         width=180,
#         options=[
#             ft.dropdown.Option("dine_in", "Dine-In"),
#             ft.dropdown.Option("takeaway", "Takeaway"),
#             ft.dropdown.Option("Delivery", "Delivery"),
#         ],
#         value=current_order_type,
#         on_change=lambda e: switch_order_type(e.control.value),
#     )

#     def save_waiter(waiter_name):
#         nonlocal selected_waiter
#         selected_waiter = waiter_name
#         page.client_storage.set("selected_waiter", waiter_name)
#         print(f"DEBUG: Saved waiter: {waiter_name}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"Waiter set to: {waiter_name}", color=ft.Colors.GREEN_600), open=True)
#         page.update()

#     def switch_order_type(order_type):
#         nonlocal current_order_type, current_order
#         current_order_type = order_type
#         page.client_storage.set("current_order_type", order_type)
#         current_order = ORDERS[current_order_type]
#         print(f"DEBUG: Switched to order type: {current_order_type}")
#         page.update()

#     def reset_order(e):
#         order_items.clear()
#         print("DEBUG: Reset order_items")
#         page.snack_bar = ft.SnackBar(ft.Text("Order reset!", color=ft.Colors.GREEN_600), open=True)
#         update_menu_container()
#         page.update()

#     def complete_order(e):
#         global is_completing
#         if is_completing:
#             print("DEBUG: Debounce: Complete button already processing")
#             return
#         if not order_items:
#             print("DEBUG: No items in order_items")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         if not selected_waiter:
#             print("DEBUG: No waiter selected")
#             page.snack_bar = ft.SnackBar(ft.Text("Please select a waiter!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         show_order_details_dialog("complete")

#     def complete_order_with_details(order_id, order_details):
#         print(f"DEBUG: Completing order ID: {order_id}, Details: {order_details}")
#         if not order_details:
#             print("DEBUG: No order details provided")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return

#         # Clear order
#         order_items.clear()
#         update_menu_container()  # Refresh to reset quantities
#         try:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             db.add_order(order_id, current_order_type, order_details, date_time)
#             print(f"DEBUG: Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}")
#             status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Kitchen receipt status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             status = print_customer_bill(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Customer bill status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             page.snack_bar = ft.SnackBar(ft.Text(f"Order {order_id} completed!", color=ft.Colors.GREEN_600), open=True)
#             page.update()
#         except Exception as ex:
#             print(f"DEBUG: Error completing order: {str(ex)}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.RED_500), open=True)
#             page.update()

#     def show_order_details_dialog(mode):
#         print(f"DEBUG: Opening order details dialog for mode: {mode}, order_items: {order_items}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Confirm {current_order_type.replace('_', ' ').title()} {mode.title()}", size=16),
#             content=ft.Text("Proceed with this order?", size=14, color=ft.Colors.GREY_800),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_dialog(page, dialog)),
#                 ft.TextButton("OK", on_click=lambda e: validate_and_process(mode)),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Order details dialog opened for {mode}")

#         def validate_and_process(mode):
#             global is_completing
#             if mode == "complete" and is_completing:
#                 print("DEBUG: Debounce: Complete button already processing")
#                 return
#             if mode == "complete":
#                 is_completing = True

#             dialog.open = False
#             page.update()
#             print(f"DEBUG: Order details dialog closed")

#             order_id = get_next_order_id(db)
#             order_details = [
#                 {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
#                 for name, qty in order_items.items() if qty > 0
#             ]
#             print(f"DEBUG: Generated order details: {order_details}")

#             if not order_details:
#                 print("DEBUG: No valid order details generated")
#                 page.snack_bar = ft.SnackBar(ft.Text("No valid items in order!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return

#             if mode == "receipt":
#                 status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Receipt print status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "bill":
#                 status = print_customer_bill(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Customer bill status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "complete":
#                 complete_order_with_details(order_id, order_details)
#                 is_completing = False

#     menu_title = ft.Text("Menu", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
#     menu_container = ft.GridView(
#         runs_count=2,  # 2 items per row
#         max_extent=180,  # Square card size
#         spacing=10,
#         padding=10,
#         auto_scroll=True,
#     )

#     reset_button = ft.ElevatedButton(
#         "\n",
#         icon=ft.Icons.RESTART_ALT,
#         color=ft.Colors.ORANGE_500,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=reset_order,
#     )
#     receipt_button = ft.ElevatedButton(
#         "QT",
#         icon=ft.Icons.PRINT,
#         color=ft.Colors.BLUE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("receipt"),
#     )
#     bill_button = ft.ElevatedButton(
#         "Bill",
#         icon=ft.Icons.RECEIPT,
#         color=ft.Colors.GREEN_600,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("bill"),
#     )
#     complete_button = ft.ElevatedButton(
#         "Save",
#         icon=ft.Icons.DONE,
#         color=ft.Colors.PURPLE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=complete_order,
#     )

#     def update_buttons():
#         has_items = len(order_items) > 0
#         receipt_button.disabled = not has_items
#         bill_button.disabled = not has_items
#         complete_button.disabled = not has_items
#         print(f"DEBUG: Updated buttons: enabled={has_items}, order_items={order_items}")
#         page.update()

#     def update_menu_container():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         print(f"DEBUG: Updating menu container with {len(MENU_ITEMS)} items")
#         menu_container.controls.clear()
#         for idx, item in enumerate(MENU_ITEMS):
#             quantity = order_items.get(item["name"], 0)
#             quantity_text = ft.Container(
#                 content=ft.Text(
#                     f"Qty: {quantity}" if quantity > 0 else "",
#                     size=12,
#                     color=ft.Colors.WHITE,
#                     weight=ft.FontWeight.BOLD,
#                     bgcolor=ft.Colors.RED_500 if quantity > 0 else ft.Colors.TRANSPARENT,
#                     visible=quantity > 0,
#                 ),
#                 padding=ft.padding.symmetric(horizontal=6, vertical=4),
#                 margin=ft.margin.only(top=8, right=8),
#                 border_radius=8,
#                 width=50,
#                 height=24,
#                 alignment=ft.alignment.center,
#             )
#             # Assign a unique color to each card
#             card_color = CARD_COLORS[idx % len(CARD_COLORS)]
#             name_container = ft.Container(
#                 content=ft.Text(
#                     item["name"],
#                     size=16,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK,
#                     text_align=ft.TextAlign.CENTER,
#                 ),
#                 bgcolor=card_color,
#                 padding=10,
#                 width=150,
#                 height=150,
#                 alignment=ft.alignment.center,
#             )
#             menu_container.controls.append(
#                 ft.Container(
#                     content=ft.Stack(
#                         [
#                             name_container,
#                             ft.Container(
#                                 content=quantity_text,
#                                 alignment=ft.alignment.top_right,
#                             ),
#                         ]
#                     ),
#                     width=150,
#                     height=150,
#                     border_radius=8,  # Square with slight rounding
#                     bgcolor=card_color,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                 )
#             )
#         update_buttons()
#         page.update()

#     update_menu_container()

#     display_value = ft.TextField(
#         value="0",
#         label="Quantity",
#         text_size=14,
#         text_align=ft.TextAlign.CENTER,
#         read_only=True,
#         color=ft.Colors.BLUE_GREY_900,
#         border_color=ft.Colors.AMBER_400,
#         focused_border_color=ft.Colors.AMBER_600,
#         width=150,
#         key="qty_display",
#     )

#     def update_display(e, digit):
#         current = display_value.value
#         if current == "0":
#             display_value.value = digit
#         else:
#             display_value.value = current + digit
#         print(f"DEBUG: Updated quantity display: {display_value.value}")
#         page.update()

#     def backspace_quantity(e):
#         current = display_value.value
#         if current == "0":
#             print("DEBUG: Backspace ignored: quantity is already 0")
#             return
#         display_value.value = current[:-1] or "0"
#         print(f"DEBUG: Backspace applied: {display_value.value}")
#         page.update()

#     def close_dialog(page, dialog):
#         dialog.open = False
#         display_value.value = "0"
#         print("DEBUG: Dialog closed")
#         page.update()

#     def add_quantity(page, dialog, item_name, qty):
#         try:
#             quantity = int(qty)
#             if quantity <= 0:
#                 print("DEBUG: Invalid quantity: must be greater than 0")
#                 page.snack_bar = ft.SnackBar(ft.Text("Quantity must be greater than 0", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return
#             if item_name not in order_items:
#                 order_items[item_name] = 0
#             order_items[item_name] = quantity
#             print(f"DEBUG: Added {quantity} {item_name} to order_items: {order_items}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.GREEN_600), open=True)
#             update_menu_container()
#         except ValueError:
#             print("DEBUG: Invalid quantity: not a number")
#             page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid number", color=ft.Colors.RED_500), open=True)
#         close_dialog(page, dialog)

#     def show_quantity_dialog(page, item_name):
#         print(f"DEBUG: Opening quantity dialog for {item_name}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Select Quantity for {item_name}", color=ft.Colors.BROWN_800, size=16),
#             content=ft.Column(
#                 [
#                     ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("7", on_click=lambda e: update_display(e, "7"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("8", on_click=lambda e: update_display(e, "8"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("9", on_click=lambda e: update_display(e, "9"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("4", on_click=lambda e: update_display(e, "4"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("5", on_click=lambda e: update_display(e, "5"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("6", on_click=lambda e: update_display(e, "6"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("1", on_click=lambda e: update_display(e, "1"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("2", on_click=lambda e: update_display(e, "2"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("3", on_click=lambda e: update_display(e, "3"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("0", on_click=lambda e: update_display(e, "0"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("\n",icon=ft.Icons.BACKSPACE, on_click=backspace_quantity, color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),

#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                     ),
                    
#                     display_value,

#                     ft.Row(
#                         [
                          
#                             ft.ElevatedButton("OK", on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value), color=ft.Colors.GREEN_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("Cancel", on_click=lambda e: close_dialog(page, dialog), color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=10,
#                 width=300,
#             ),
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Quantity dialog opened")

#     menu_content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Row(
#                     [waiter_dropdown, order_type_dropdown],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     spacing=10,
#                 ),
#                 ft.Container(
#                     content=menu_title,
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=menu_container,
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Row(
#                     [reset_button, receipt_button, bill_button, complete_button],
#                     alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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

#     return menu_content


# import flet as ft
# import time
# from datetime import datetime
# import os
# from setting import check_permissions, print_kitchen_receipt, print_customer_bill

# MENU_ITEMS = []
# ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
# TOTAL_SALES = 0.0
# is_completing = False  # Debounce flag

# def get_next_order_id(db):
#     print("DEBUG: Generating next order ID")
#     if 'jnius' in globals():
#         order_id = f"{int(time.time()) % 99999:05d}"
#         print(f"DEBUG: Using timestamp-based order ID: {order_id}")
#         return order_id
#     order_id_file = "last_order_id.txt"
#     try:
#         if os.path.exists(order_id_file):
#             with open(order_id_file, "r") as f:
#                 last_id = int(f.read().strip() or 0)
#         else:
#             last_id = 0
#         next_id = (last_id % 99999) + 1
#         with open(order_id_file, "w") as f:
#             f.write(str(next_id))
#         print(f"DEBUG: Generated file-based order ID: {next_id:05d}")
#         return f"{next_id:05d}"
#     except Exception as ex:
#         print(f"DEBUG: Error generating order ID: {ex}")
#         return "00001"

# def menu_view(page: ft.Page, db: 'Database'):
#     page.title = "Menu"
#     page.bgcolor = ft.Colors.ORANGE_50
#     page.padding = 5
#     page.scroll = ft.ScrollMode.AUTO

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()
#     print(f"DEBUG: Loaded menu items: {MENU_ITEMS}")
#     current_order_type = page.client_storage.get("current_order_type") or "dine_in"
#     print(f"DEBUG: Initial order type: {current_order_type}")
#     current_order = ORDERS[current_order_type]
#     order_items = {}
#     selected_waiter = page.client_storage.get("selected_waiter") or None
#     print(f"DEBUG: Initial waiter: {selected_waiter}")

#     ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]
#     WAITERS = ["Ali", "Ahmed", "Sara", "Zain"]
#     # Color palette for menu item cards
#     CARD_COLORS = [ft.Colors.RED_200, ft.Colors.BLUE_200, ft.Colors.GREEN_200, ft.Colors.YELLOW_200, ft.Colors.PURPLE_200]

#     # Waiter and Order Type Dropdowns
#     waiter_dropdown = ft.Dropdown(
#         label="Select Waiter",
#         width=180,
#         options=[ft.dropdown.Option(w) for w in WAITERS],
#         value=selected_waiter,
#         on_change=lambda e: save_waiter(e.control.value),
#     )

#     order_type_dropdown = ft.Dropdown(
#         label="Order Type",
#         width=180,
#         options=[
#             ft.dropdown.Option("dine_in", "Dine-In"),
#             ft.dropdown.Option("takeaway", "Takeaway"),
#             ft.dropdown.Option("Delivery", "Delivery"),
#         ],
#         value=current_order_type,
#         on_change=lambda e: switch_order_type(e.control.value),
#     )

#     def save_waiter(waiter_name):
#         nonlocal selected_waiter
#         selected_waiter = waiter_name
#         page.client_storage.set("selected_waiter", waiter_name)
#         print(f"DEBUG: Saved waiter: {waiter_name}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"Waiter set to: {waiter_name}", color=ft.Colors.GREEN_600), open=True)
#         page.update()

#     def switch_order_type(order_type):
#         nonlocal current_order_type, current_order
#         current_order_type = order_type
#         page.client_storage.set("current_order_type", order_type)
#         current_order = ORDERS[current_order_type]
#         print(f"DEBUG: Switched to order type: {current_order_type}")
#         page.update()

#     def reset_order(e):
#         order_items.clear()
#         print("DEBUG: Reset order_items")
#         page.snack_bar = ft.SnackBar(ft.Text("Order reset!", color=ft.Colors.GREEN_600), open=True)
#         update_menu_container()
#         page.update()

#     def complete_order(e):
#         global is_completing
#         if is_completing:
#             print("DEBUG: Debounce: Complete button already processing")
#             return
#         if not order_items:
#             print("DEBUG: No items in order_items")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         if not selected_waiter:
#             print("DEBUG: No waiter selected")
#             page.snack_bar = ft.SnackBar(ft.Text("Please select a waiter!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return
#         show_order_details_dialog("complete")

#     def complete_order_with_details(order_id, order_details):
#         print(f"DEBUG: Completing order ID: {order_id}, Details: {order_details}")
#         if not order_details:
#             print("DEBUG: No order details provided")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
#             page.update()
#             return

#         # Clear order
#         order_items.clear()
#         update_menu_container()  # Refresh to reset quantities
#         try:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             db.add_order(order_id, current_order_type, order_details, date_time, selected_waiter)
#             print(f"DEBUG: Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}, Waiter={selected_waiter}")
#             status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Kitchen receipt status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             status = print_customer_bill(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Customer bill status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#             page.update()
#             page.snack_bar = ft.SnackBar(ft.Text(f"Order {order_id} completed!", color=ft.Colors.GREEN_600), open=True)
#             page.update()
#         except Exception as ex:
#             print(f"DEBUG: Error completing order: {str(ex)}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.RED_500), open=True)
#             page.update()

#     def show_order_details_dialog(mode):
#         print(f"DEBUG: Opening order details dialog for mode: {mode}, order_items: {order_items}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Confirm {current_order_type.replace('_', ' ').title()} {mode.title()}", size=16),
#             content=ft.Text("Proceed with this order?", size=14, color=ft.Colors.GREY_800),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_dialog(page, dialog)),
#                 ft.TextButton("OK", on_click=lambda e: validate_and_process(mode)),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Order details dialog opened for {mode}")

#         def validate_and_process(mode):
#             global is_completing
#             if mode == "complete" and is_completing:
#                 print("DEBUG: Debounce: Complete button already processing")
#                 return
#             if mode == "complete":
#                 is_completing = True

#             dialog.open = False
#             page.update()
#             print(f"DEBUG: Order details dialog closed")

#             order_id = get_next_order_id(db)
#             order_details = [
#                 {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
#                 for name, qty in order_items.items() if qty > 0
#             ]
#             print(f"DEBUG: Generated order details: {order_details}")

#             if not order_details:
#                 print("DEBUG: No valid order details generated")
#                 page.snack_bar = ft.SnackBar(ft.Text("No valid items in order!", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return

#             if mode == "receipt":
#                 status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Receipt print status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "bill":
#                 status = print_customer_bill(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Customer bill status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.RED_500 if "Error" in status else ft.Colors.GREEN_600), open=True)
#                 page.update()
#             elif mode == "complete":
#                 complete_order_with_details(order_id, order_details)
#                 is_completing = False

#     menu_title = ft.Text("Menu", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
#     menu_container = ft.GridView(
#         runs_count=2,  # 2 items per row
#         max_extent=180,  # Square card size
#         spacing=10,
#         padding=10,
#         auto_scroll=True,
#     )

#     reset_button = ft.ElevatedButton(
#         "\n",
#         icon=ft.Icons.RESTART_ALT,
#         color=ft.Colors.ORANGE_500,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=reset_order,
#     )
#     receipt_button = ft.ElevatedButton(
#         "QT",
#         icon=ft.Icons.PRINT,
#         color=ft.Colors.BLUE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("receipt"),
#     )
#     bill_button = ft.ElevatedButton(
#         "Bill",
#         icon=ft.Icons.RECEIPT,
#         color=ft.Colors.GREEN_600,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=lambda e: show_order_details_dialog("bill"),
#     )
#     complete_button = ft.ElevatedButton(
#         "Save",
#         icon=ft.Icons.DONE,
#         color=ft.Colors.PURPLE_500,
#         disabled=True,
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
#         on_click=complete_order,
#     )

#     def update_buttons():
#         has_items = len(order_items) > 0
#         receipt_button.disabled = not has_items
#         bill_button.disabled = not has_items
#         complete_button.disabled = not has_items
#         print(f"DEBUG: Updated buttons: enabled={has_items}, order_items={order_items}")
#         page.update()

#     def update_menu_container():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         print(f"DEBUG: Updating menu container with {len(MENU_ITEMS)} items")
#         menu_container.controls.clear()
#         for idx, item in enumerate(MENU_ITEMS):
#             quantity = order_items.get(item["name"], 0)
#             quantity_text = ft.Container(
#                 content=ft.Text(
#                     f"Qty: {quantity}" if quantity > 0 else "",
#                     size=12,
#                     color=ft.Colors.WHITE,
#                     weight=ft.FontWeight.BOLD,
#                     bgcolor=ft.Colors.RED_500 if quantity > 0 else ft.Colors.TRANSPARENT,
#                     visible=quantity > 0,
#                 ),
#                 padding=ft.padding.symmetric(horizontal=6, vertical=4),
#                 margin=ft.margin.only(top=8, right=8),
#                 border_radius=8,
#                 width=50,
#                 height=24,
#                 alignment=ft.alignment.center,
#             )
#             # Assign a unique color to each card
#             card_color = CARD_COLORS[idx % len(CARD_COLORS)]
#             name_container = ft.Container(
#                 content=ft.Text(
#                     item["name"],
#                     size=16,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK,
#                     text_align=ft.TextAlign.CENTER,
#                 ),
#                 bgcolor=card_color,
#                 padding=10,
#                 width=150,
#                 height=150,
#                 alignment=ft.alignment.center,
#             )
#             menu_container.controls.append(
#                 ft.Container(
#                     content=ft.Stack(
#                         [
#                             name_container,
#                             ft.Container(
#                                 content=quantity_text,
#                                 alignment=ft.alignment.top_right,
#                             ),
#                         ]
#                     ),
#                     width=150,
#                     height=150,
#                     border_radius=8,  # Square with slight rounding
#                     bgcolor=card_color,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                 )
#             )
#         update_buttons()
#         page.update()

#     update_menu_container()

#     display_value = ft.TextField(
#         value="0",
#         label="Quantity",
#         text_size=14,
#         text_align=ft.TextAlign.CENTER,
#         read_only=True,
#         color=ft.Colors.BLUE_GREY_900,
#         border_color=ft.Colors.AMBER_400,
#         focused_border_color=ft.Colors.AMBER_600,
#         width=150,
#         key="qty_display",
#     )

#     def update_display(e, digit):
#         current = display_value.value
#         if current == "0":
#             display_value.value = digit
#         else:
#             display_value.value = current + digit
#         print(f"DEBUG: Updated quantity display: {display_value.value}")
#         page.update()

#     def backspace_quantity(e):
#         current = display_value.value
#         if current == "0":
#             print("DEBUG: Backspace ignored: quantity is already 0")
#             return
#         display_value.value = current[:-1] or "0"
#         print(f"DEBUG: Backspace applied: {display_value.value}")
#         page.update()

#     def close_dialog(page, dialog):
#         dialog.open = False
#         display_value.value = "0"
#         print("DEBUG: Dialog closed")
#         page.update()

#     def add_quantity(page, dialog, item_name, qty):
#         try:
#             quantity = int(qty)
#             if quantity <= 0:
#                 print("DEBUG: Invalid quantity: must be greater than 0")
#                 page.snack_bar = ft.SnackBar(ft.Text("Quantity must be greater than 0", color=ft.Colors.RED_500), open=True)
#                 page.update()
#                 return
#             if item_name not in order_items:
#                 order_items[item_name] = 0
#             order_items[item_name] = quantity
#             print(f"DEBUG: Added {quantity} {item_name} to order_items: {order_items}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.GREEN_600), open=True)
#             update_menu_container()
#         except ValueError:
#             print("DEBUG: Invalid quantity: not a number")
#             page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid number", color=ft.Colors.RED_500), open=True)
#         close_dialog(page, dialog)

#     def show_quantity_dialog(page, item_name):
#         print(f"DEBUG: Opening quantity dialog for {item_name}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Select Quantity for {item_name}", color=ft.Colors.BROWN_800, size=16),
#             content=ft.Column(
#                 [
#                     ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("7", on_click=lambda e: update_display(e, "7"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("8", on_click=lambda e: update_display(e, "8"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("9", on_click=lambda e: update_display(e, "9"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("4", on_click=lambda e: update_display(e, "4"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("5", on_click=lambda e: update_display(e, "5"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("6", on_click=lambda e: update_display(e, "6"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("1", on_click=lambda e: update_display(e, "1"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("2", on_click=lambda e: update_display(e, "2"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("3", on_click=lambda e: update_display(e, "3"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     ),
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("0", on_click=lambda e: update_display(e, "0"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("\n", icon=ft.Icons.BACKSPACE, on_click=backspace_quantity, color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                     display_value,
#                     ft.Row(
#                         [
#                             ft.ElevatedButton("OK", on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value), color=ft.Colors.GREEN_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ft.ElevatedButton("Cancel", on_click=lambda e: close_dialog(page, dialog), color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=10,
#                 width=300,
#             ),
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Quantity dialog opened")

#     menu_content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Row(
#                     [waiter_dropdown, order_type_dropdown],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     spacing=10,
#                 ),
#                 ft.Container(
#                     content=menu_title,
#                     padding=8,
#                     bgcolor=ft.Colors.ORANGE_300,
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Container(
#                     content=menu_container,
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     margin=ft.margin.only(bottom=10),
#                 ),
#                 ft.Row(
#                     [reset_button, receipt_button, bill_button, complete_button],
#                     alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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

#     return menu_content



# import flet as ft
# import time
# from datetime import datetime
# import os
# from setting import check_permissions, print_kitchen_receipt, print_customer_bill

# MENU_ITEMS = []
# ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
# TOTAL_SALES = 0.0
# is_completing = False  # Debounce flag

# def get_next_order_id(db):
#     print("DEBUG: Generating next order ID")
#     if 'jnius' in globals():
#         order_id = f"{int(time.time()) % 99999:05d}"
#         print(f"DEBUG: Using timestamp-based order ID: {order_id}")
#         return order_id
#     order_id_file = "last_order_id.txt"
#     try:
#         if os.path.exists(order_id_file):
#             with open(order_id_file, "r") as f:
#                 last_id = int(f.read().strip() or 0)
#         else:
#             last_id = 0
#         next_id = (last_id % 99999) + 1
#         with open(order_id_file, "w") as f:
#             f.write(str(next_id))
#         print(f"DEBUG: Generated file-based order ID: {next_id:05d}")
#         return f"{next_id:05d}"
#     except Exception as ex:
#         print(f"DEBUG: Error generating order ID: {ex}")
#         return "00001"

# def menu_view(page: ft.Page, db: 'Database'):
#     page.title = "Restaurant Menu"
#     page.bgcolor = ft.Colors.GREY_100
#     page.padding = 10
#     page.scroll = ft.ScrollMode.AUTO

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()  # Expected: [{"name": str, "price": float, "category": str}, ...]
#     print(f"DEBUG: Loaded menu items: {MENU_ITEMS}")
#     current_order_type = page.client_storage.get("current_order_type") or "dine_in"
#     print(f"DEBUG: Initial order type: {current_order_type}")
#     current_order = ORDERS[current_order_type]
#     order_items = {}
#     selected_waiter = page.client_storage.get("selected_waiter") or None
#     print(f"DEBUG: Initial waiter: {selected_waiter}")

#     ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]
#     WAITERS = ["Ali", "Ahmed", "Sara", "Zain"]
#     COLOR_SCHEME = {
#         "primary": ft.Colors.BLUE_700,
#         "accent": ft.Colors.AMBER_600,
#         "background": ft.Colors.WHITE,
#         "text": ft.Colors.BLACK87,
#         "error": ft.Colors.RED_600,
#         "success": ft.Colors.GREEN_600,
#         "card_colors": [ft.Colors.BLUE_200, ft.Colors.GREEN_200, ft.Colors.YELLOW_200, ft.Colors.PURPLE_200, ft.Colors.RED_200]
#     }

#     # Group menu items by category
#     categories = sorted(set(item.get("category", "Uncategorized") for item in MENU_ITEMS))
#     print(f"DEBUG: Categories found: {categories}")

#     # Waiter and Order Type Dropdowns
#     waiter_dropdown = ft.Dropdown(
#         label="Select Waiter",
#         width=200,
#         options=[ft.dropdown.Option(w) for w in WAITERS],
#         value=selected_waiter,
#         border_color=COLOR_SCHEME["primary"],
#         focused_border_color=COLOR_SCHEME["accent"],
#         text_style=ft.TextStyle(color=COLOR_SCHEME["text"]),
#         bgcolor=COLOR_SCHEME["background"],
#         filled=True,
#         on_change=lambda e: save_waiter(e.control.value),
#     )

#     order_type_dropdown = ft.Dropdown(
#         label="Order Type",
#         width=200,
#         options=[
#             ft.dropdown.Option("dine_in", "Dine-In"),
#             ft.dropdown.Option("takeaway", "Takeaway"),
#             ft.dropdown.Option("Delivery", "Delivery"),
#         ],
#         value=current_order_type,
#         border_color=COLOR_SCHEME["primary"],
#         focused_border_color=COLOR_SCHEME["accent"],
#         text_style=ft.TextStyle(color=COLOR_SCHEME["text"]),
#         bgcolor=COLOR_SCHEME["background"],
#         filled=True,
#         on_change=lambda e: switch_order_type(e.control.value),
#     )

#     def save_waiter(waiter_name):
#         nonlocal selected_waiter
#         selected_waiter = waiter_name
#         page.client_storage.set("selected_waiter", waiter_name)
#         print(f"DEBUG: Saved waiter: {waiter_name}")
#         page.snack_bar = ft.SnackBar(ft.Text(f"Waiter set to: {waiter_name}", color=COLOR_SCHEME["success"]), open=True)
#         page.update()

#     def switch_order_type(order_type):
#         nonlocal current_order_type, current_order
#         current_order_type = order_type
#         page.client_storage.set("current_order_type", order_type)
#         current_order = ORDERS[current_order_type]
#         print(f"DEBUG: Switched to order type: {current_order_type}")
#         page.update()

#     def reset_order(e):
#         order_items.clear()
#         print("DEBUG: Reset order_items")
#         page.snack_bar = ft.SnackBar(ft.Text("Order reset!", color=COLOR_SCHEME["success"]), open=True)
#         update_menu_container()
#         page.update()

#     def complete_order(e):
#         global is_completing
#         if is_completing:
#             print("DEBUG: Debounce: Complete button already processing")
#             return
#         if not order_items:
#             print("DEBUG: No items in order_items")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=COLOR_SCHEME["error"]), open=True)
#             page.update()
#             return
#         if not selected_waiter:
#             print("DEBUG: No waiter selected")
#             page.snack_bar = ft.SnackBar(ft.Text("Please select a waiter!", color=COLOR_SCHEME["error"]), open=True)
#             page.update()
#             return
#         show_order_details_dialog("complete")

#     def complete_order_with_details(order_id, order_details):
#         print(f"DEBUG: Completing order ID: {order_id}, Details: {order_details}")
#         if not order_details:
#             print("DEBUG: No order details provided")
#             page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=COLOR_SCHEME["error"]), open=True)
#             page.update()
#             return

#         order_items.clear()
#         update_menu_container()
#         try:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             db.add_order(order_id, current_order_type, order_details, date_time, selected_waiter)
#             print(f"DEBUG: Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}, Waiter={selected_waiter}")
#             status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Kitchen receipt status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=COLOR_SCHEME["error"] if "Error" in status else COLOR_SCHEME["success"]), open=True)
#             page.update()
#             status = print_customer_bill(order_id, order_details, page, current_order_type)
#             print(f"DEBUG: Customer bill status: {status}")
#             page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=COLOR_SCHEME["error"] if "Error" in status else COLOR_SCHEME["success"]), open=True)
#             page.update()
#             page.snack_bar = ft.SnackBar(ft.Text(f"Order {order_id} completed!", color=COLOR_SCHEME["success"]), open=True)
#             page.update()
#         except Exception as ex:
#             print(f"DEBUG: Error completing order: {str(ex)}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Error completing order: {str(ex)}", color=COLOR_SCHEME["error"]), open=True)
#             page.update()

#     def show_order_details_dialog(mode):
#         print(f"DEBUG: Opening order details dialog for mode: {mode}, order_items: {order_items}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Confirm {current_order_type.replace('_', ' ').title()} {mode.title()}", size=18, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"]),
#             content=ft.Text("Proceed with this order?", size=16, color=COLOR_SCHEME["text"]),
#             actions=[
#                 ft.TextButton("Cancel", on_click=lambda e: close_dialog(page, dialog), style=ft.ButtonStyle(color=COLOR_SCHEME["error"])),
#                 ft.TextButton("OK", on_click=lambda e: validate_and_process(mode), style=ft.ButtonStyle(color=COLOR_SCHEME["success"])),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=COLOR_SCHEME["background"],
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Order details dialog opened for {mode}")

#         def validate_and_process(mode):
#             global is_completing
#             if mode == "complete" and is_completing:
#                 print("DEBUG: Debounce: Complete button already processing")
#                 return
#             if mode == "complete":
#                 is_completing = True

#             dialog.open = False
#             page.update()
#             print(f"DEBUG: Order details dialog closed")

#             order_id = get_next_order_id(db)
#             order_details = [
#                 {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
#                 for name, qty in order_items.items() if qty > 0
#             ]
#             print(f"DEBUG: Generated order details: {order_details}")

#             if not order_details:
#                 print("DEBUG: No valid order details generated")
#                 page.snack_bar = ft.SnackBar(ft.Text("No valid items in order!", color=COLOR_SCHEME["error"]), open=True)
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return

#             if mode == "receipt":
#                 status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Receipt print status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=COLOR_SCHEME["error"] if "Error" in status else COLOR_SCHEME["success"]), open=True)
#                 page.update()
#             elif mode == "bill":
#                 status = print_customer_bill(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Customer bill status: {status}")
#                 page.snack_bar = ft.SnackBar(ft.Text(status if "Error" in status else "Customer bill printed!", color=COLOR_SCHEME["error"] if "Error" in status else COLOR_SCHEME["success"]), open=True)
#                 page.update()
#             elif mode == "complete":
#                 complete_order_with_details(order_id, order_details)
#                 is_completing = False

#     menu_title = ft.Text("Restaurant Menu", size=24, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"])

#     # Create menu content (tabs if multiple categories, grid if single or empty)
#     menu_container = ft.Container(
#         content=ft.GridView(
#             runs_count=3,
#             max_extent=200,
#             spacing=10,
#             padding=10,
#             auto_scroll=True,
#         ),
#         padding=10,
#         bgcolor=COLOR_SCHEME["background"],
#         border_radius=8,
#         shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#     )

#     if len(categories) > 1:
#         menu_container = ft.Tabs(
#             selected_index=0,
#             animation_duration=300,
#             tabs=[
#                 ft.Tab(
#                     text=category,
#                     content=ft.Container(
#                         content=ft.GridView(
#                             runs_count=3,
#                             max_extent=200,
#                             spacing=10,
#                             padding=10,
#                             auto_scroll=True,
#                         ),
#                         padding=10,
#                         bgcolor=COLOR_SCHEME["background"],
#                         border_radius=8,
#                     ),
#                 )
#                 for category in categories
#             ],
#             expand=1,
#             tab_alignment=ft.TabAlignment.CENTER,
#             indicator_color=COLOR_SCHEME["accent"],
#             label_color=COLOR_SCHEME["primary"],
#             unselected_label_color=COLOR_SCHEME["text"],
#         )

#     reset_button = ft.ElevatedButton(
#         "Reset",
#         icon=ft.Icons.RESTART_ALT,
#         bgcolor=COLOR_SCHEME["accent"],
#         color=COLOR_SCHEME["text"],
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=15),
#         on_click=reset_order,
#     )
#     receipt_button = ft.ElevatedButton(
#         "Receipt",
#         icon=ft.Icons.PRINT,
#         bgcolor=COLOR_SCHEME["primary"],
#         color=COLOR_SCHEME["background"],
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=15),
#         disabled=True,
#         on_click=lambda e: show_order_details_dialog("receipt"),
#     )
#     bill_button = ft.ElevatedButton(
#         "Bill",
#         icon=ft.Icons.RECEIPT,
#         bgcolor=COLOR_SCHEME["success"],
#         color=COLOR_SCHEME["background"],
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=15),
#         disabled=True,
#         on_click=lambda e: show_order_details_dialog("bill"),
#     )
#     complete_button = ft.ElevatedButton(
#         "Complete",
#         icon=ft.Icons.DONE,
#         bgcolor=COLOR_SCHEME["primary"],
#         color=COLOR_SCHEME["background"],
#         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=15),
#         disabled=True,
#         on_click=complete_order,
#     )

#     def update_buttons():
#         has_items = len(order_items) > 0
#         receipt_button.disabled = not has_items
#         bill_button.disabled = not has_items
#         complete_button.disabled = not has_items
#         print(f"DEBUG: Updated buttons: enabled={has_items}, order_items={order_items}")
#         page.update()

#     def update_menu_container():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         print(f"DEBUG: Updating menu container with {len(MENU_ITEMS)} items")
#         categories = sorted(set(item.get("category", "Uncategorized") for item in MENU_ITEMS))

#         if not MENU_ITEMS:
#             menu_container.content.controls.clear()
#             menu_container.content.controls.append(
#                 ft.Text("No menu items available", size=16, color=COLOR_SCHEME["error"], text_align=ft.TextAlign.CENTER)
#             )
#         elif len(categories) <= 1:
#             menu_container.content.controls.clear()
#             for idx, item in enumerate(MENU_ITEMS):
#                 card_color = COLOR_SCHEME["card_colors"][idx % len(COLOR_SCHEME["card_colors"])]
#                 menu_container.content.controls.append(
#                     ft.Container(
#                         content=ft.Stack(
#                             [
#                                 ft.Container(
#                                     content=ft.Column(
#                                         [
#                                             ft.Text(
#                                                 item["name"],
#                                                 size=16,
#                                                 weight=ft.FontWeight.BOLD,
#                                                 color=COLOR_SCHEME["text"],
#                                                 text_align=ft.TextAlign.CENTER,
#                                             ),
#                                             ft.Text(
#                                                 f"${item['price']:.2f}",
#                                                 size=14,
#                                                 color=COLOR_SCHEME["text"],
#                                                 text_align=ft.TextAlign.CENTER,
#                                             ),
#                                             ft.Container(
#                                                 content=ft.Text(
#                                                     f"Qty: {order_items.get(item['name'], 0)}" if order_items.get(item['name'], 0) > 0 else "",
#                                                     size=12,
#                                                     color=ft.Colors.WHITE,
#                                                     weight=ft.FontWeight.BOLD,
#                                                     bgcolor=COLOR_SCHEME["error"] if order_items.get(item['name'], 0) > 0 else ft.Colors.TRANSPARENT,
#                                                     visible=order_items.get(item['name'], 0) > 0,
#                                                 ),
#                                                 padding=ft.padding.symmetric(horizontal=6, vertical=4),
#                                                 border_radius=8,
#                                                 alignment=ft.alignment.top_right,
#                                             ),
#                                         ],
#                                         alignment=ft.MainAxisAlignment.CENTER,
#                                         spacing=5,
#                                     ),
#                                     bgcolor=card_color,
#                                     padding=10,
#                                     border_radius=8,
#                                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                                 ),
#                             ],
#                         ),
#                         width=180,
#                         height=180,
#                         border_radius=8,
#                         on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                     )
#                 )
#         else:
#             menu_container.tabs = [
#                 ft.Tab(
#                     text=category,
#                     content=ft.Container(
#                         content=ft.GridView(
#                             runs_count=3,
#                             max_extent=200,
#                             spacing=10,
#                             padding=10,
#                             auto_scroll=True,
#                             controls=[
#                                 ft.Container(
#                                     content=ft.Stack(
#                                         [
#                                             ft.Container(
#                                                 content=ft.Column(
#                                                     [
#                                                         ft.Text(
#                                                             item["name"],
#                                                             size=16,
#                                                             weight=ft.FontWeight.BOLD,
#                                                             color=COLOR_SCHEME["text"],
#                                                             text_align=ft.TextAlign.CENTER,
#                                                         ),
#                                                         ft.Text(
#                                                             f"${item['price']:.2f}",
#                                                             size=14,
#                                                             color=COLOR_SCHEME["text"],
#                                                             text_align=ft.TextAlign.CENTER,
#                                                         ),
#                                                         ft.Container(
#                                                             content=ft.Text(
#                                                                 f"Qty: {order_items.get(item['name'], 0)}" if order_items.get(item['name'], 0) > 0 else "",
#                                                                 size=12,
#                                                                 color=ft.Colors.WHITE,
#                                                                 weight=ft.FontWeight.BOLD,
#                                                                 bgcolor=COLOR_SCHEME["error"] if order_items.get(item['name'], 0) > 0 else ft.Colors.TRANSPARENT,
#                                                                 visible=order_items.get(item['name'], 0) > 0,
#                                                             ),
#                                                             padding=ft.padding.symmetric(horizontal=6, vertical=4),
#                                                             border_radius=8,
#                                                             alignment=ft.alignment.top_right,
#                                                         ),
#                                                     ],
#                                                     alignment=ft.MainAxisAlignment.CENTER,
#                                                     spacing=5,
#                                                 ),
#                                                 bgcolor=COLOR_SCHEME["card_colors"][idx % len(COLOR_SCHEME["card_colors"])],
#                                                 padding=10,
#                                                 border_radius=8,
#                                                 shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                                             ),
#                                         ],
#                                     ),
#                                     width=180,
#                                     height=180,
#                                     border_radius=8,
#                                     on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                                 )
#                                 for idx, item in enumerate(MENU_ITEMS) if item.get("category", "Uncategorized") == category
#                             ],
#                         ),
#                         padding=10,
#                         bgcolor=COLOR_SCHEME["background"],
#                         border_radius=8,
#                     ),
#                 )
#                 for category in categories
#             ]
#         update_buttons()
#         page.update()

#     display_value = ft.TextField(
#         value="0",
#         label="Quantity",
#         text_size=16,
#         text_align=ft.TextAlign.CENTER,
#         read_only=True,
#         color=COLOR_SCHEME["text"],
#         border_color=COLOR_SCHEME["primary"],
#         focused_border_color=COLOR_SCHEME["accent"],
#         bgcolor=COLOR_SCHEME["background"],
#         filled=True,
#         width=150,
#         key="qty_display",
#     )

#     def update_display(e, digit):
#         current = display_value.value
#         if current == "0":
#             display_value.value = digit
#         else:
#             display_value.value = current + digit
#         print(f"DEBUG: Updated quantity display: {display_value.value}")
#         page.update()

#     def backspace_quantity(e):
#         current = display_value.value
#         if current == "0":
#             print("DEBUG: Backspace ignored: quantity is already 0")
#             return
#         display_value.value = current[:-1] or "0"
#         print(f"DEBUG: Backspace applied: {display_value.value}")
#         page.update()

#     def close_dialog(page, dialog):
#         dialog.open = False
#         display_value.value = "0"
#         print("DEBUG: Dialog closed")
#         page.update()

#     def add_quantity(page, dialog, item_name, qty):
#         try:
#             quantity = int(qty)
#             if quantity <= 0:
#                 print("DEBUG: Invalid quantity: must be greater than 0")
#                 page.snack_bar = ft.SnackBar(ft.Text("Quantity must be greater than 0", color=COLOR_SCHEME["error"]), open=True)
#                 page.update()
#                 return
#             if item_name not in order_items:
#                 order_items[item_name] = 0
#             order_items[item_name] = quantity
#             print(f"DEBUG: Added {quantity} {item_name} to order_items: {order_items}")
#             page.snack_bar = ft.SnackBar(ft.Text(f"Added {quantity} {item_name} to order", color=COLOR_SCHEME["success"]), open=True)
#             update_menu_container()
#         except ValueError:
#             print("DEBUG: Invalid quantity: not a number")
#             page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid number", color=COLOR_SCHEME["error"]), open=True)
#         close_dialog(page, dialog)

#     def show_quantity_dialog(page, item_name):
#         print(f"DEBUG: Opening quantity dialog for {item_name}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(f"Select Quantity for {item_name}", color=COLOR_SCHEME["text"], size=18, weight=ft.FontWeight.BOLD),
#             content=ft.Container(
#                 content=ft.Column(
#                     [
#                         ft.Text("Enter quantity:", size=16, color=COLOR_SCHEME["text"]),
#                         ft.Row(
#                             [
#                                 ft.ElevatedButton("7", on_click=lambda e: update_display(e, "7"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("8", on_click=lambda e: update_display(e, "8"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("9", on_click=lambda e: update_display(e, "9"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         ),
#                         ft.Row(
#                             [
#                                 ft.ElevatedButton("4", on_click=lambda e: update_display(e, "4"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("5", on_click=lambda e: update_display(e, "5"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("6", on_click=lambda e: update_display(e, "6"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         ),
#                         ft.Row(
#                             [
#                                 ft.ElevatedButton("1", on_click=lambda e: update_display(e, "1"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("2", on_click=lambda e: update_display(e, "2"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("3", on_click=lambda e: update_display(e, "3"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         ),
#                         ft.Row(
#                             [
#                                 ft.ElevatedButton("0", on_click=lambda e: update_display(e, "0"), bgcolor=COLOR_SCHEME["accent"], color=COLOR_SCHEME["text"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("", icon=ft.Icons.BACKSPACE, on_click=backspace_quantity, bgcolor=COLOR_SCHEME["error"], color=COLOR_SCHEME["background"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         ),
#                         display_value,
#                         ft.Row(
#                             [
#                                 ft.ElevatedButton("OK", on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value), bgcolor=COLOR_SCHEME["success"], color=COLOR_SCHEME["background"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                                 ft.ElevatedButton("Cancel", on_click=lambda e: close_dialog(page, dialog), bgcolor=COLOR_SCHEME["error"], color=COLOR_SCHEME["background"], style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         ),
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     spacing=10,
#                     scroll=ft.ScrollMode.AUTO,
#                 ),
#                 width=300,
#                 padding=10,
#                 bgcolor=COLOR_SCHEME["background"],
#                 border_radius=8,
#             ),
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=COLOR_SCHEME["background"],
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Quantity dialog opened")

#     # Initial population of menu
#     update_menu_container()

#     menu_content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Row(
#                     [waiter_dropdown, order_type_dropdown],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     spacing=10,
#                 ),
#                 ft.Container(
#                     content=menu_title,
#                     padding=10,
#                     bgcolor=COLOR_SCHEME["primary"],
#                     border_radius=8,
#                     margin=ft.margin.only(bottom=10),
#                     alignment=ft.alignment.center,
#                 ),
#                 menu_container,
#                 ft.Row(
#                     [reset_button, receipt_button, bill_button, complete_button],
#                     alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                     spacing=10,
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=10,
#             scroll=ft.ScrollMode.AUTO,
#         ),
#         width=min(page.width, 800),
#         alignment=ft.alignment.center,
#         padding=10,
#         bgcolor=COLOR_SCHEME["background"],
#         border_radius=8,
#         shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#     )

#     return menu_content


# import flet as ft
# import time
# from datetime import datetime
# import os
# from setting import check_permissions, print_kitchen_receipt, print_customer_bill

# MENU_ITEMS = []
# ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
# TOTAL_SALES = 0.0
# is_completing = False  # Debounce flag

# def get_next_order_id(db):
#     print("DEBUG: Generating next order ID")
#     if 'jnius' in globals():
#         order_id = f"{int(time.time()) % 99999:05d}"
#         print(f"DEBUG: Using timestamp-based order ID: {order_id}")
#         return order_id
#     order_id_file = "last_order_id.txt"
#     try:
#         if os.path.exists(order_id_file):
#             with open(order_id_file, "r") as f:
#                 last_id = int(f.read().strip() or 0)
#         else:
#             last_id = 0
#         next_id = (last_id % 99999) + 1
#         with open(order_id_file, "w") as f:
#             f.write(str(next_id))
#         print(f"DEBUG: Generated file-based order ID: {next_id:05d}")
#         return f"{next_id:05d}"
#     except Exception as ex:
#         print(f"DEBUG: Error generating order ID: {ex}")
#         return "00001"

# def menu_view(page: ft.Page, db: 'Database'):
#     page.title = "Menu"
#     page.bgcolor = ft.Colors.GREY_100
#     page.padding = 10
#     page.scroll = ft.ScrollMode.AUTO
#     page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

#     global MENU_ITEMS
#     MENU_ITEMS = db.get_menu()
#     print(f"DEBUG: Loaded menu items: {MENU_ITEMS}")
#     current_order_type = page.client_storage.get("current_order_type") or "dine_in"
#     print(f"DEBUG: Initial order type: {current_order_type}")
#     current_order = ORDERS[current_order_type]
#     order_items = {}
#     selected_waiter = page.client_storage.get("selected_waiter") or None
#     print(f"DEBUG: Initial waiter: {selected_waiter}")

#     ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]
#     WAITERS = ["Ali", "Ahmed", "Sara", "Zain"]

#     # Waiter and Order Type Dropdowns
#     waiter_dropdown = ft.Dropdown(
#         label="Select Waiter",
#         width=150,
#         options=[ft.dropdown.Option(w) for w in WAITERS],
#         value=selected_waiter,
#         text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
#         label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14, font_family="Roboto"),
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_600,
#         bgcolor=ft.Colors.WHITE,
#         content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#         on_change=lambda e: save_waiter(e.control.value),
#     )

#     order_type_dropdown = ft.Dropdown(
#         label="Order Type",
#         width=170,
#         options=[
#             ft.dropdown.Option("dine_in", "Dine-In"),
#             ft.dropdown.Option("takeaway", "Takeaway"),
#             ft.dropdown.Option("Delivery", "Delivery"),
#         ],
#         value=current_order_type,
#         text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
#         label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14, font_family="Roboto"),
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_600,
#         bgcolor=ft.Colors.WHITE,
#         content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
#         on_change=lambda e: switch_order_type(e.control.value),
#     )

#     def save_waiter(waiter_name):
#         nonlocal selected_waiter
#         selected_waiter = waiter_name
#         page.client_storage.set("selected_waiter", waiter_name)
#         print(f"DEBUG: Saved waiter: {waiter_name}")
#         page.snack_bar = ft.SnackBar(
#             ft.Text(f"Waiter set to: {waiter_name}", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
#             open=True,
#             duration=3000,
#         )
#         page.update()

#     def switch_order_type(order_type):
#         nonlocal current_order_type, current_order
#         current_order_type = order_type
#         page.client_storage.set("current_order_type", order_type)
#         current_order = ORDERS[current_order_type]
#         print(f"DEBUG: Switched to order type: {current_order_type}")
#         page.update()

#     def reset_order(e):
#         order_items.clear()
#         print("DEBUG: Reset order_items")
#         page.snack_bar = ft.SnackBar(
#             ft.Text("Order reset!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
#             open=True,
#             duration=3000,
#         )
#         update_menu_container()
#         page.update()

#     def complete_order(e):
#         global is_completing
#         if is_completing:
#             print("DEBUG: Debounce: Complete button already processing")
#             return
#         if not order_items:
#             print("DEBUG: No items in order_items")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("No items to complete!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return
#         if not selected_waiter:
#             print("DEBUG: No waiter selected")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("Please select a waiter!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return
#         show_order_details_dialog("complete")

#     def complete_order_with_details(order_id, order_details):
#         print(f"DEBUG: Completing order ID: {order_id}, Details: {order_details}")
#         if not order_details:
#             print("DEBUG: No order details provided")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("No items to complete!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#             return

#         order_items.clear()
#         update_menu_container()
#         try:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             db.add_order(order_id, current_order_type, order_details, date_time, selected_waiter)
#             print(f"DEBUG: Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}, Waiter={selected_waiter}")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Order {order_id} completed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()
#         except Exception as ex:
#             print(f"DEBUG: Error completing order: {str(ex)}")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             page.update()

#     def show_order_details_dialog(mode):
#         print(f"DEBUG: Opening order details dialog for mode: {mode}, order_items: {order_items}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Text(
#                 f"Confirm {current_order_type.replace('_', ' ').title()} {mode.title()}",
#                 size=16,
#                 weight=ft.FontWeight.BOLD,
#                 color=ft.Colors.GREY_800,
#                 font_family="Roboto",
#             ),
#             content=ft.Text(
#                 "Proceed with this order?",
#                 size=14,
#                 color=ft.Colors.GREY_800,
#                 font_family="Roboto",
#             ),
#             actions=[
#                 ft.TextButton(
#                     "Cancel",
#                     style=ft.ButtonStyle(color=ft.Colors.GREY_600, padding=10, shape=ft.RoundedRectangleBorder(radius=8)),
#                     on_click=lambda e: close_dialog(page, dialog),
#                 ),
#                 ft.ElevatedButton(
#                     "OK",
#                     icon=ft.Icons.CHECK,
#                     style=ft.ButtonStyle(
#                         color=ft.Colors.WHITE,
#                         bgcolor=ft.Colors.BLUE_600,
#                         padding=10,
#                         shape=ft.RoundedRectangleBorder(radius=8),
#                         elevation={"pressed": 2, "": 4},
#                     ),
#                     on_click=lambda e: validate_and_process(mode),
#                 ),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=ft.Colors.WHITE,
#             shape=ft.RoundedRectangleBorder(radius=10),
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Order details dialog opened for {mode}")

#         def validate_and_process(mode):
#             global is_completing
#             if mode == "complete" and is_completing:
#                 print("DEBUG: Debounce: Complete button already processing")
#                 return
#             if mode == "complete":
#                 is_completing = True

#             dialog.open = False
#             page.update()
#             print(f"DEBUG: Order details dialog closed")

#             order_id = get_next_order_id(db)
#             order_details = [
#                 {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
#                 for name, qty in order_items.items() if qty > 0
#             ]
#             print(f"DEBUG: Generated order details: {order_details}")

#             if not order_details:
#                 print("DEBUG: No valid order details generated")
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text("No valid items in order!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 if mode == "complete":
#                     is_completing = False
#                 return

#             if mode == "receipt":
#                 status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Receipt print status: {status}")
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600 if "Error" in status else ft.Colors.GREEN_600, font_family="Roboto"),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#             elif mode == "bill":
#                 status = print_customer_bill(order_id, order_details, page, current_order_type)
#                 print(f"DEBUG: Customer bill status: {status}")
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600 if "Error" in status else ft.Colors.GREEN_600, font_family="Roboto"),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#             elif mode == "complete":
#                 complete_order_with_details(order_id, order_details)
#                 is_completing = False

#     menu_title = ft.Text(
#         "Menu",
#         size=20,
#         weight=ft.FontWeight.BOLD,
#         color=ft.Colors.GREY_800,
#         font_family="Roboto",
#     )

#     menu_container = ft.GridView(
#         runs_count=2,
#         max_extent=170,
#         spacing=10,
#         padding=10,
#         auto_scroll=True,
#         expand=True,
#     )

  
#     reset_button = ft.IconButton(
#         icon=ft.Icons.RESTART_ALT,
#         icon_color=ft.Colors.RED_600,
#         tooltip="Reset Order",
#         on_click=reset_order,
#     )
   
#     receipt_button = ft.IconButton(
#         icon=ft.Icons.PRINT,
#         icon_color=ft.Colors.BLUE_600,
#         tooltip="Print Kitchen Receipt",
#         disabled=True,
#         on_click=lambda e: show_order_details_dialog("receipt"),

#     )
 
#     bill_button = ft.IconButton(
#         icon=ft.Icons.RECEIPT,
#         icon_color=ft.Colors.BLUE_600,
#         tooltip="Print Customer Bill",
#         disabled=True,
#         on_click=lambda e: show_order_details_dialog("bill"),

#     )
    
#     complete_button = ft.IconButton(
#         icon=ft.Icons.DONE,
#         icon_color=ft.Colors.GREEN_600,
#         tooltip="Complete Order",
#         disabled=True,
#         on_click=complete_order,
#     )

#     def update_buttons():
#         has_items = len(order_items) > 0
#         receipt_button.disabled = not has_items
#         bill_button.disabled = not has_items
#         complete_button.disabled = not has_items
#         print(f"DEBUG: Updated buttons: enabled={has_items}, order_items={order_items}")
#         page.update()

#     def update_menu_container():
#         global MENU_ITEMS
#         MENU_ITEMS = db.get_menu()
#         print(f"DEBUG: Updating menu container with {len(MENU_ITEMS)} items")
#         menu_container.controls.clear()
#         for idx, item in enumerate(MENU_ITEMS):
#             quantity = order_items.get(item["name"], 0)
#             quantity_text = ft.Container(
#                 content=ft.Text(
#                     f"Qty: {quantity}" if quantity > 0 else "",
#                     size=12,
#                     color=ft.Colors.WHITE,
#                     weight=ft.FontWeight.BOLD,
#                     bgcolor=ft.Colors.RED_600 if quantity > 0 else ft.Colors.TRANSPARENT,
#                     visible=quantity > 0,
#                     font_family="Roboto",
#                 ),
#                 padding=ft.padding.symmetric(horizontal=6, vertical=4),
#                 margin=ft.margin.only(top=8, right=8),
#                 border_radius=8,
#                 width=70,
#                 height=24,
#                 alignment=ft.alignment.center,
#             )
#             name_container = ft.Container(
#                 content=ft.Column(
#                     [
#                         ft.Text(
#                             item["name"],
#                             size=25,
#                             weight=ft.FontWeight.BOLD,
#                             color=ft.Colors.GREY_800,
#                             text_align=ft.TextAlign.CENTER,
#                             font_family="Roboto",
#                         ),
#                         ft.Text(
#                             f"Rs {item['price']:.2f}",
#                             size=14,
#                             color=ft.Colors.BLUE_600,
#                             text_align=ft.TextAlign.CENTER,
#                             font_family="Roboto",
#                         ),
#                     ],
#                     spacing=5,
#                     alignment=ft.MainAxisAlignment.CENTER,
#                 ),
#                 bgcolor=ft.Colors.GREY_200,
#                 padding=10,
#                 width=150,
#                 height=150,
#                 alignment=ft.alignment.center,
#                 clip_behavior=ft.ClipBehavior.HARD_EDGE,
#             )
#             menu_container.controls.append(
#                 ft.Container(
#                     content=ft.Stack(
#                         [
#                             name_container,
#                             ft.Container(
#                                 content=quantity_text,
#                                 alignment=ft.alignment.top_right,
#                             ),
#                         ]
#                     ),
#                     width=150,
#                     height=150,
#                     border_radius=8,
#                     bgcolor=ft.Colors.GREY_200,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
#                     on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
#                     clip_behavior=ft.ClipBehavior.HARD_EDGE,
#                 )
#             )
#         update_buttons()
#         page.update()

#     update_menu_container()

#     display_value = ft.TextField(
#         value="0",
#         label="Quantity",
#         text_size=14,
#         text_align=ft.TextAlign.CENTER,
#         read_only=True,
#         color=ft.Colors.GREY_800,
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_600,
#         bgcolor=ft.Colors.WHITE,
#         width=150,
#         key="qty_display",
#         text_style=ft.TextStyle(font_family="Roboto"),
#     )

#     def update_display(e, digit):
#         current = display_value.value
#         if current == "0":
#             display_value.value = digit
#         else:
#             display_value.value = current + digit
#         print(f"DEBUG: Updated quantity display: {display_value.value}")
#         page.update()

#     def backspace_quantity(e):
#         current = display_value.value
#         if current == "0":
#             print("DEBUG: Backspace ignored: quantity is already 0")
#             return
#         display_value.value = current[:-1] or "0"
#         print(f"DEBUG: Backspace applied: {display_value.value}")
#         page.update()

#     def close_dialog(page, dialog):
#         dialog.open = False
#         display_value.value = "0"
#         print("DEBUG: Dialog closed")
#         page.update()

#     def add_quantity(page, dialog, item_name, qty):
#         try:
#             quantity = int(qty)
#             if quantity <= 0:
#                 print("DEBUG: Invalid quantity: must be greater than 0")
#                 page.snack_bar = ft.SnackBar(
#                     ft.Text("Quantity must be greater than 0", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                     open=True,
#                     duration=3000,
#                 )
#                 page.update()
#                 return
#             if item_name not in order_items:
#                 order_items[item_name] = 0
#             order_items[item_name] = quantity
#             print(f"DEBUG: Added {quantity} {item_name} to order_items: {order_items}")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#             update_menu_container()
#         except ValueError:
#             print("DEBUG: Invalid quantity: not a number")
#             page.snack_bar = ft.SnackBar(
#                 ft.Text("Please enter a valid number", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
#                 open=True,
#                 duration=3000,
#             )
#         close_dialog(page, dialog)

#     def show_quantity_dialog(page, item_name):
#         print(f"DEBUG: Opening quantity dialog for {item_name}")
#         dialog = ft.AlertDialog(
#             modal=True,
#             # title=ft.Text(
#             #     f"Select Quantity for {item_name}",
#             #     size=16,
#             #     weight=ft.FontWeight.BOLD,
#             #     color=ft.Colors.GREY_800,
#             #     font_family="Roboto",
#             # ),
#             content=ft.Column(
#                 [
#                     ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
#                     ft.GridView(
#                         runs_count=3,
#                         max_extent=80,
#                         spacing=8,
#                         padding=8,
#                         controls=[
#                             ft.ElevatedButton(
#                                 str(i),
#                                 style=ft.ButtonStyle(
#                                     color=ft.Colors.GREY_800,
#                                     bgcolor=ft.Colors.WHITE,
#                                     padding=10,
#                                     shape=ft.RoundedRectangleBorder(radius=8),
#                                     elevation={"pressed": 2, "": 4},
#                                 ),
#                                 on_click=lambda e, d=str(i): update_display(e, d),
#                             ) for i in [7, 8, 9, 4, 5, 6, 1, 2, 3]
#                         ] + [
#                             ft.ElevatedButton(
#                                 "0",
#                                 style=ft.ButtonStyle(
#                                     color=ft.Colors.GREY_800,
#                                     bgcolor=ft.Colors.WHITE,
#                                     padding=10,
#                                     shape=ft.RoundedRectangleBorder(radius=8),
#                                     elevation={"pressed": 2, "": 4},
#                                 ),
#                                 on_click=lambda e: update_display(e, "0"),
#                             ),
#                             # ft.ElevatedButton(
#                             #     "",
#                             #     icon=ft.Icons.BACKSPACE,
#                             #     style=ft.ButtonStyle(
#                             #         color=ft.Colors.WHITE,
#                             #         bgcolor=ft.Colors.RED_600,
#                             #         padding=10,
#                             #         shape=ft.RoundedRectangleBorder(radius=8),
#                             #         elevation={"pressed": 2, "": 4},
#                             #     ),
#                             #     on_click=backspace_quantity,
#                             # ),

#                             ft.IconButton(
#                                 ft.Icons.BACKSPACE,
#                                 icon_color=ft.Colors.RED_600,
#                                 tooltip="Backspace",
#                                 on_click=backspace_quantity,

#                             )
#                         ],
#                     ),
#                     display_value,
#                     ft.Row(
#                         [
#                             ft.ElevatedButton(
#                                 "OK",
#                                 icon=ft.Icons.CHECK,
#                                 width=100,
#                                 height=50,
#                                 style=ft.ButtonStyle(
#                                     color=ft.Colors.WHITE,
#                                     bgcolor=ft.Colors.GREEN_600,
#                                     padding=10,
#                                     shape=ft.RoundedRectangleBorder(radius=8),
#                                     elevation={"pressed": 2, "": 4},
                                    
#                                 ),
#                                 on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value),
#                             ),
#                             ft.ElevatedButton(
#                                 "Cancel",
#                                 icon=ft.Icons.CLOSE,
#                                 width=100,
#                                 height=50,
#                                 style=ft.ButtonStyle(
#                                     color=ft.Colors.WHITE,
#                                     bgcolor=ft.Colors.RED_600,
#                                     padding=10,
#                                     shape=ft.RoundedRectangleBorder(radius=8),
#                                     elevation={"pressed": 2, "": 4},
#                                 ),
#                                 on_click=lambda e: close_dialog(page, dialog),
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         spacing=10,
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 spacing=12,
#                 width=300,
#                 height=550
#             ),
#             actions_alignment=ft.MainAxisAlignment.END,
#             bgcolor=ft.Colors.WHITE,
#             shape=ft.RoundedRectangleBorder(radius=10),
#         )
#         page.overlay.append(dialog)
#         dialog.open = True
#         page.update()
#         print(f"DEBUG: Quantity dialog opened")

#     menu_content = ft.Container(
#         content=ft.Column(
#             [
                
#                 ft.Container(
#                     content=ft.Row(
#                         [waiter_dropdown, order_type_dropdown],
#                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                         spacing=10,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(bottom=2),
#                     clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    
#                 ),
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             menu_title,
#                             menu_container,
#                         ],
#                         spacing=10,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(bottom=2),
#                     height=page.height - 250,
#                     clip_behavior=ft.ClipBehavior.HARD_EDGE,
#                 ),
#                 ft.Container(
#                     content=ft.Row(
#                         [reset_button, receipt_button, bill_button, complete_button],
#                         alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                         spacing=10,
#                     ),
#                     padding=12,
#                     bgcolor=ft.Colors.BLUE_100,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
#                     clip_behavior=ft.ClipBehavior.HARD_EDGE,
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.START,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=12,
#             scroll=ft.ScrollMode.AUTO,
#         ),
#         width=min(page.width, 400),
#         alignment=ft.alignment.center,
#         clip_behavior=ft.ClipBehavior.HARD_EDGE,
#     )

#     return menu_content



import flet as ft
import time
from datetime import datetime
import os
from setting import check_permissions, print_kitchen_receipt, print_customer_bill

MENU_ITEMS = []
ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
TOTAL_SALES = 0.0
is_completing = False  # Debounce flag

def get_next_order_id(db):
    print("DEBUG: Generating next order ID")
    if 'jnius' in globals():
        order_id = f"{int(time.time()) % 99999:05d}"
        print(f"DEBUG: Using timestamp-based order ID: {order_id}")
        return order_id
    order_id_file = "last_order_id.txt"
    try:
        if os.path.exists(order_id_file):
            with open(order_id_file, "r") as f:
                last_id = int(f.read().strip() or 0)
        else:
            last_id = 0
        next_id = (last_id % 99999) + 1
        with open(order_id_file, "w") as f:
            f.write(str(next_id))
        print(f"DEBUG: Generated file-based order ID: {next_id:05d}")
        return f"{next_id:05d}"
    except Exception as ex:
        print(f"DEBUG: Error generating order ID: {ex}")
        return "00001"

def menu_view(page: ft.Page, db: 'Database'):
    page.title = "Menu"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

    global MENU_ITEMS
    MENU_ITEMS = db.get_menu()
    print(f"DEBUG: Loaded menu items: {MENU_ITEMS}")
    current_order_type = page.client_storage.get("current_order_type") or "dine_in"
    print(f"DEBUG: Initial order type: {current_order_type}")
    current_order = ORDERS[current_order_type]
    order_items = {}
    selected_waiter = page.client_storage.get("selected_waiter") or None
    print(f"DEBUG: Initial waiter: {selected_waiter}")

    ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]
    # Fetch waiters from database
    waiters = db.get_all_waiters()
    print(f"DEBUG: Loaded waiters from database: {[w['name'] for w in waiters]}")

    # Waiter and Order Type Dropdowns
    waiter_dropdown = ft.Dropdown(
        label="Select Waiter",
        width=150,
        options=[ft.dropdown.Option(w["name"]) for w in waiters],
        value=selected_waiter if selected_waiter in [w["name"] for w in waiters] else None,
        text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
        label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14, font_family="Roboto"),
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.BLUE_600,
        bgcolor=ft.Colors.WHITE,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        on_change=lambda e: save_waiter(e.control.value),
    )

    order_type_dropdown = ft.Dropdown(
        label="Order Type",
        width=170,
        options=[
            ft.dropdown.Option("dine_in", "Dine-In"),
            ft.dropdown.Option("takeaway", "Takeaway"),
            ft.dropdown.Option("Delivery", "Delivery"),
        ],
        value=current_order_type,
        text_style=ft.TextStyle(size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
        label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14, font_family="Roboto"),
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.BLUE_600,
        bgcolor=ft.Colors.WHITE,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        on_change=lambda e: switch_order_type(e.control.value),
    )

    def save_waiter(waiter_name):
        nonlocal selected_waiter
        selected_waiter = waiter_name
        page.client_storage.set("selected_waiter", waiter_name)
        print(f"DEBUG: Saved waiter: {waiter_name}")
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Waiter set to: {waiter_name}", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
            open=True,
            duration=3000,
        )
        page.update()

    def switch_order_type(order_type):
        nonlocal current_order_type, current_order
        current_order_type = order_type
        page.client_storage.set("current_order_type", order_type)
        current_order = ORDERS[current_order_type]
        print(f"DEBUG: Switched to order type: {current_order_type}")
        page.update()

    def reset_order(e):
        order_items.clear()
        print("DEBUG: Reset order_items")
        page.snack_bar = ft.SnackBar(
            ft.Text("Order reset!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
            open=True,
            duration=3000,
        )
        update_menu_container()
        page.update()

    def complete_order(e):
        global is_completing
        if is_completing:
            print("DEBUG: Debounce: Complete button already processing")
            return
        if not order_items:
            print("DEBUG: No items in order_items")
            page.snack_bar = ft.SnackBar(
                ft.Text("No items to complete!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            page.update()
            return
        if not selected_waiter:
            print("DEBUG: No waiter selected")
            page.snack_bar = ft.SnackBar(
                ft.Text("Please select a waiter!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            page.update()
            return
        show_order_details_dialog("complete")

    def complete_order_with_details(order_id, order_details):
        print(f"DEBUG: Completing order ID: {order_id}, Details: {order_details}")
        if not order_details:
            print("DEBUG: No order details provided")
            page.snack_bar = ft.SnackBar(
                ft.Text("No items to complete!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            page.update()
            return

        order_items.clear()
        update_menu_container()
        try:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.add_order(order_id, current_order_type, order_details, date_time, selected_waiter)
            print(f"DEBUG: Saved order to database: Order ID={order_id}, Type={current_order_type}, Items={order_details}, Waiter={selected_waiter}")
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Order {order_id} completed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            page.update()
        except Exception as ex:
            print(f"DEBUG: Error completing order: {str(ex)}")
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            page.update()

    def show_order_details_dialog(mode):
        print(f"DEBUG: Opening order details dialog for mode: {mode}, order_items: {order_items}")
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                f"Confirm {current_order_type.replace('_', ' ').title()} {mode.title()}",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_800,
                font_family="Roboto",
            ),
            content=ft.Text(
                "Proceed with this order?",
                size=14,
                color=ft.Colors.GREY_800,
                font_family="Roboto",
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    style=ft.ButtonStyle(color=ft.Colors.GREY_600, padding=10, shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda e: close_dialog(page, dialog),
                ),
                ft.ElevatedButton(
                    "OK",
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_600,
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation={"pressed": 2, "": 4},
                    ),
                    on_click=lambda e: validate_and_process(mode),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        print(f"DEBUG: Order details dialog opened for {mode}")

        def validate_and_process(mode):
            global is_completing
            if mode == "complete" and is_completing:
                print("DEBUG: Debounce: Complete button already processing")
                return
            if mode == "complete":
                is_completing = True

            dialog.open = False
            page.update()
            print(f"DEBUG: Order details dialog closed")

            order_id = get_next_order_id(db)
            order_details = [
                {"name": name, "quantity": qty, "price": next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0), "total": qty * next((i["price"] for i in MENU_ITEMS if i["name"] == name), 0)}
                for name, qty in order_items.items() if qty > 0
            ]
            print(f"DEBUG: Generated order details: {order_details}")

            if not order_details:
                print("DEBUG: No valid order details generated")
                page.snack_bar = ft.SnackBar(
                    ft.Text("No valid items in order!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                    open=True,
                    duration=3000,
                )
                page.update()
                if mode == "complete":
                    is_completing = False
                return

            if mode == "receipt":
                status = print_kitchen_receipt(order_id, order_details, page, current_order_type)
                print(f"DEBUG: Receipt print status: {status}")
                page.snack_bar = ft.SnackBar(
                    ft.Text(status if "Error" in status else "Kitchen receipt printed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600 if "Error" in status else ft.Colors.GREEN_600, font_family="Roboto"),
                    open=True,
                    duration=3000,
                )
                page.update()
            elif mode == "bill":
                status = print_customer_bill(order_id, order_details, page, current_order_type)
                print(f"DEBUG: Customer bill status: {status}")
                page.snack_bar = ft.SnackBar(
                    ft.Text(status if "Error" in status else "Customer bill printed!", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600 if "Error" in status else ft.Colors.GREEN_600, font_family="Roboto"),
                    open=True,
                    duration=3000,
                )
                page.update()
            elif mode == "complete":
                complete_order_with_details(order_id, order_details)
                is_completing = False

    menu_title = ft.Text(
        "Menu",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREY_800,
        font_family="Roboto",
    )

    menu_container = ft.GridView(
        runs_count=2,
        max_extent=170,
        spacing=10,
        padding=10,
        auto_scroll=True,
        expand=True,
    )

    reset_button = ft.IconButton(
        icon=ft.Icons.RESTART_ALT,
        icon_color=ft.Colors.RED_600,
        tooltip="Reset Order",
        on_click=reset_order,
    )

    receipt_button = ft.IconButton(
        icon=ft.Icons.PRINT,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Print Kitchen Receipt",
        disabled=True,
        on_click=lambda e: show_order_details_dialog("receipt"),
    )

    bill_button = ft.IconButton(
        icon=ft.Icons.RECEIPT,
        icon_color=ft.Colors.BLUE_600,
        tooltip="Print Customer Bill",
        disabled=True,
        on_click=lambda e: show_order_details_dialog("bill"),
    )

    complete_button = ft.IconButton(
        icon=ft.Icons.DONE,
        icon_color=ft.Colors.GREEN_600,
        tooltip="Complete Order",
        disabled=True,
        on_click=complete_order,
    )

    def update_buttons():
        has_items = len(order_items) > 0
        receipt_button.disabled = not has_items
        bill_button.disabled = not has_items
        complete_button.disabled = not has_items
        print(f"DEBUG: Updated buttons: enabled={has_items}, order_items={order_items}")
        page.update()

    def update_menu_container():
        global MENU_ITEMS
        MENU_ITEMS = db.get_menu()
        print(f"DEBUG: Updating menu container with {len(MENU_ITEMS)} items")
        menu_container.controls.clear()
        for idx, item in enumerate(MENU_ITEMS):
            quantity = order_items.get(item["name"], 0)
            quantity_text = ft.Container(
                content=ft.Text(
                    f"Qty: {quantity}" if quantity > 0 else "",
                    size=12,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    bgcolor=ft.Colors.RED_600 if quantity > 0 else ft.Colors.TRANSPARENT,
                    visible=quantity > 0,
                    font_family="Roboto",
                ),
                padding=ft.padding.symmetric(horizontal=6, vertical=4),
                margin=ft.margin.only(top=8, right=8),
                border_radius=8,
                width=70,
                height=24,
                alignment=ft.alignment.center,
            )
            name_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            item["name"],
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                            text_align=ft.TextAlign.CENTER,
                            font_family="Roboto",
                        ),
                        ft.Text(
                            f"Rs {item['price']:.2f}",
                            size=14,
                            color=ft.Colors.BLUE_600,
                            text_align=ft.TextAlign.CENTER,
                            font_family="Roboto",
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=ft.Colors.GREY_200,
                padding=10,
                width=150,
                height=150,
                alignment=ft.alignment.center,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
            menu_container.controls.append(
                ft.Container(
                    content=ft.Stack(
                        [
                            name_container,
                            ft.Container(
                                content=quantity_text,
                                alignment=ft.alignment.top_right,
                            ),
                        ]
                    ),
                    width=150,
                    height=150,
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_200,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                )
            )
        update_buttons()
        page.update()

    update_menu_container()

    display_value = ft.TextField(
        value="0",
        label="Quantity",
        text_size=14,
        text_align=ft.TextAlign.CENTER,
        read_only=True,
        color=ft.Colors.GREY_800,
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.BLUE_600,
        bgcolor=ft.Colors.WHITE,
        width=150,
        key="qty_display",
        text_style=ft.TextStyle(font_family="Roboto"),
    )

    def update_display(e, digit):
        current = display_value.value
        if current == "0":
            display_value.value = digit
        else:
            display_value.value = current + digit
        print(f"DEBUG: Updated quantity display: {display_value.value}")
        page.update()

    def backspace_quantity(e):
        current = display_value.value
        if current == "0":
            print("DEBUG: Backspace ignored: quantity is already 0")
            return
        display_value.value = current[:-1] or "0"
        print(f"DEBUG: Backspace applied: {display_value.value}")
        page.update()

    def close_dialog(page, dialog):
        dialog.open = False
        display_value.value = "0"
        print("DEBUG: Dialog closed")
        page.update()

    def add_quantity(page, dialog, item_name, qty):
        try:
            quantity = int(qty)
            if quantity <= 0:
                print("DEBUG: Invalid quantity: must be greater than 0")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Quantity must be greater than 0", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                    open=True,
                    duration=3000,
                )
                page.update()
                return
            if item_name not in order_items:
                order_items[item_name] = 0
            order_items[item_name] = quantity
            print(f"DEBUG: Added {quantity} {item_name} to order_items: {order_items}")
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
            update_menu_container()
        except ValueError:
            print("DEBUG: Invalid quantity: not a number")
            page.snack_bar = ft.SnackBar(
                ft.Text("Please enter a valid number", color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600, font_family="Roboto"),
                open=True,
                duration=3000,
            )
        close_dialog(page, dialog)

    def show_quantity_dialog(page, item_name):
        print(f"DEBUG: Opening quantity dialog for {item_name}")
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800, font_family="Roboto"),
                    ft.GridView(
                        runs_count=3,
                        max_extent=80,
                        spacing=8,
                        padding=8,
                        controls=[
                            ft.ElevatedButton(
                                str(i),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.GREY_800,
                                    bgcolor=ft.Colors.WHITE,
                                    padding=10,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    elevation={"pressed": 2, "": 4},
                                ),
                                on_click=lambda e, d=str(i): update_display(e, d),
                            ) for i in [7, 8, 9, 4, 5, 6, 1, 2, 3]
                        ] + [
                            ft.ElevatedButton(
                                "0",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.GREY_800,
                                    bgcolor=ft.Colors.WHITE,
                                    padding=10,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    elevation={"pressed": 2, "": 4},
                                ),
                                on_click=lambda e: update_display(e, "0"),
                            ),
                            ft.IconButton(
                                ft.Icons.BACKSPACE,
                                icon_color=ft.Colors.RED_600,
                                tooltip="Backspace",
                                on_click=backspace_quantity,
                            )
                        ],
                    ),
                    display_value,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "OK",
                                icon=ft.Icons.CHECK,
                                width=100,
                                height=50,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREEN_600,
                                    padding=10,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    elevation={"pressed": 2, "": 4},
                                ),
                                on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value),
                            ),
                            ft.ElevatedButton(
                                "Cancel",
                                icon=ft.Icons.CLOSE,
                                width=100,
                                height=50,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED_600,
                                    padding=10,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    elevation={"pressed": 2, "": 4},
                                ),
                                on_click=lambda e: close_dialog(page, dialog),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
                width=300,
                height=550
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        print(f"DEBUG: Quantity dialog opened")

    menu_content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [waiter_dropdown, order_type_dropdown],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(bottom=2),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            menu_title,
                            menu_container,
                        ],
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(bottom=2),
                    height=page.height - 250,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Container(
                    content=ft.Row(
                        [reset_button, receipt_button, bill_button, complete_button],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.BLUE_100,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=min(page.width, 400),
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return menu_content