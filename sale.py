

# # import flet as ft
# # import datetime

# # def sale_view(page: ft.Page, db: 'Database'):
# #     page.title = "Sales"
# #     page.bgcolor = ft.Colors.BLACK
# #     page.padding = 0

# #     # DatePicker for date selection
# #     selected_date = datetime.datetime.now()

# #     def update_sales_by_date(e):
# #         nonlocal selected_date
# #         selected_date = e.control.value
# #         date_picker.open = False
# #         update_sales_display()
# #         page.update()

# #     date_picker = ft.DatePicker(
# #         first_date=datetime.datetime(year=2000, month=1, day=1),
# #         last_date=datetime.datetime(year=2050, month=12, day=31),
# #         value=selected_date,
# #         on_change=update_sales_by_date,
# #         on_dismiss=lambda e: page.update()
# #     )

# #     def show_date_picker(e):
# #         page.dialog = date_picker
# #         date_picker.open = True
# #         page.overlay.append(date_picker)
# #         page.update()

# #     date_picker_button = ft.ElevatedButton(
# #         content=ft.Row(
# #             [
# #                 ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700, size=20),
# #                 ft.Text("Pick Date", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
# #             ],
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             spacing=8,
# #         ),
# #         style=ft.ButtonStyle(
# #             shape=ft.RoundedRectangleBorder(radius=10),
# #             bgcolor=ft.Colors.WHITE,
# #             padding=10,
# #             elevation={"pressed": 2, "": 6},
# #         ),
# #         on_click=show_date_picker,
# #         opacity=1.0,
# #         on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
# #     )

# #     # Display sales
# #     sales_list = ft.ListView(
# #         spacing=10,
# #         padding=10,
# #         auto_scroll=True,
# #     )

# #     def update_sales_display():
# #         sales_list.controls.clear()
# #         orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
# #         if orders:
# #             total_sales = sum(order["total"] for order in orders)
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     f"Sales on {selected_date.strftime('%Y-%m-%d')}:",
# #                     size=16,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.BLACK87,
# #                 )
# #             )
# #             for order in orders:
# #                 items = db.get_order_items(order["order_id"])
# #                 items_display = ft.Container(
# #                     content=ft.Column(
# #                         [
# #                             ft.Text("Order Items", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
# #                             ft.ListView(
# #                                 controls=[
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"{item['item_name']} x {item['quantity']}",
# #                                                 size=10,
# #                                                 color=ft.Colors.BLACK87,
# #                                                 max_lines=1,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{item['total']:.2f}",
# #                                                 size=10,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                                 color=ft.Colors.GREEN_700,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ) for item in items
# #                                 ],
# #                                 spacing=5,
# #                                 padding=5,
# #                                 auto_scroll=True,
# #                             ),
# #                         ],
# #                         spacing=5,
# #                     ),
# #                     bgcolor=ft.Colors.WHITE,
# #                     padding=5,
# #                     border_radius=8,
# #                     shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
# #                     margin=ft.margin.only(left=5, right=5, top=5),
# #                     width=340,
# #                     visible=False,
# #                 )

# #                 def toggle_details(e):
# #                     items_display.visible = not items_display.visible
# #                     page.update()

# #                 sales_list.controls.append(
# #                     ft.GestureDetector(
# #                         content=ft.Container(
# #                             content=ft.Column(
# #                                 [
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"Order ID: {order['order_id'][:8]}... | {order['order_type'].replace('_', ' ').title()} | {order['order_date']}",
# #                                                 size=12,
# #                                                 weight=ft.FontWeight.W_500,
# #                                                 color=ft.Colors.BLACK87,
# #                                                 max_lines=1,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{order['total']:.2f}",
# #                                                 size=12,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                                 color=ft.Colors.GREEN_700,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ),
# #                                     ft.Text(
# #                                         f"Table: {order['table_number'] or 'N/A'} | Name: {order['customer_name'] or 'N/A'} | Number: {order['customer_number'] or 'N/A'}",
# #                                         size=10,
# #                                         color=ft.Colors.BLACK54,
# #                                         max_lines=1,
# #                                     ),
# #                                     items_display,
# #                                 ],
# #                                 spacing=5,
# #                             ),
# #                             bgcolor=ft.Colors.WHITE,
# #                             padding=10,
# #                             border_radius=8,
# #                             shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
# #                             width=340,
# #                         ),
# #                         on_tap=toggle_details,
# #                         on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
# #                     )
# #                 )
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     f"Total Sales: Rs{total_sales:.2f}",
# #                     size=14,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.BLACK87,
# #                     text_align=ft.TextAlign.RIGHT,
# #                 )
# #             )
# #         else:
# #             sales_list.controls.append(
# #                 ft.Container(
# #                     content=ft.Text(
# #                         "No sales for this date",
# #                         size=14,
# #                         color=ft.Colors.BLACK54,
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     padding=10,
# #                     width=340,
# #                 )
# #             )
# #         page.update()

# #     # Initial display
# #     update_sales_display()

# #     # Gradient background
# #     background = ft.Container(
# #         gradient=ft.LinearGradient(
# #             begin=ft.Alignment(-1, -1),
# #             end=ft.Alignment(1, 1),
# #             colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
# #         ),
# #         expand=True,
# #     )

# #     # Main content container
# #     sales_content = ft.Container(
# #         content=ft.Column(
# #             [
# #                 ft.Container(
# #                     content=ft.Text(
# #                         "Sales by Date",
# #                         size=24,
# #                         weight=ft.FontWeight.BOLD,
# #                         color=ft.Colors.WHITE,
# #                         font_family="Roboto",
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     shadow=ft.BoxShadow(
# #                         blur_radius=8,
# #                         spread_radius=1,
# #                         color=ft.Colors.BLACK26,
# #                     ),
# #                     padding=8,
# #                 ),
# #                 date_picker_button,
# #                 ft.Container(
# #                     content=sales_list,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     padding=10,
# #                     shadow=ft.BoxShadow(
# #                         blur_radius=15,
# #                         spread_radius=3,
# #                         color=ft.Colors.BLACK26,
# #                     ),
# #                     margin=ft.margin.symmetric(horizontal=10, vertical=20),
# #                     height=400,
# #                     width=340,
# #                 ),
# #                 # ft.ElevatedButton(
# #                 #     content=ft.Row(
# #                 #         [
# #                 #             ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_700, size=20),
# #                 #             ft.Text("Back to Dashboard", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
# #                 #         ],
# #                 #         alignment=ft.MainAxisAlignment.CENTER,
# #                 #         spacing=8,
# #                 #     ),
# #                 #     style=ft.ButtonStyle(
# #                 #         shape=ft.RoundedRectangleBorder(radius=10),
# #                 #         bgcolor=ft.Colors.WHITE,
# #                 #         padding=10,
# #                 #         elevation={"pressed": 2, "": 6},
# #                 #     ),
# #                 #     on_click=lambda e: page.go("/dashboard"),
# #                 #     opacity=1.0,
# #                 #     on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
# #                 # ),
# #             ],
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=10,
# #         ),
# #         width=min(page.width, 360),
# #         alignment=ft.alignment.center,
# #     )

# #     # Stack the gradient background and content
# #     return ft.Stack(
# #         [
# #             background,
# #             sales_content,
# #         ],
# #         expand=True,
# #     )


# # import flet as ft
# # import datetime

# # def sale_view(page: ft.Page, db: 'Database'):
# #     page.title = "Sales"
# #     page.bgcolor = ft.Colors.BLACK
# #     page.padding = 0

# #     # DatePicker for date selection
# #     selected_date = datetime.datetime.now()

# #     def update_sales_by_date(e):
# #         nonlocal selected_date
# #         selected_date = e.control.value
# #         date_picker.open = False
# #         update_sales_display()
# #         page.update()

# #     date_picker = ft.DatePicker(
# #         first_date=datetime.datetime(year=2000, month=1, day=1),
# #         last_date=datetime.datetime(year=2050, month=12, day=31),
# #         value=selected_date,
# #         on_change=update_sales_by_date,
# #         on_dismiss=lambda e: page.update()
# #     )

# #     def show_date_picker(e):
# #         page.dialog = date_picker
# #         date_picker.open = True
# #         page.overlay.append(date_picker)
# #         page.update()

# #     date_picker_button = ft.ElevatedButton(
# #         content=ft.Row(
# #             [
# #                 ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700, size=20),
# #                 ft.Text("Pick Date", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
# #             ],
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             spacing=8,
# #         ),
# #         style=ft.ButtonStyle(
# #             shape=ft.RoundedRectangleBorder(radius=10),
# #             bgcolor=ft.Colors.WHITE,
# #             padding=10,
# #             elevation={"pressed": 2, "": 6},
# #         ),
# #         on_click=show_date_picker,
# #         opacity=1.0,
# #         on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
# #     )

# #     # Waiter Dropdown
# #     WAITERS = ["All", "Ali", "Ahmed", "Sara", "Zain"]  # Include "All" for overall sales
# #     selected_waiter = page.client_storage.get("selected_waiter") or "All"

# #     waiter_dropdown = ft.Dropdown(
# #         label="Select Waiter",
# #         width=180,
# #         options=[ft.dropdown.Option(w) for w in WAITERS],
# #         value=selected_waiter,
# #         on_change=lambda e: update_waiter(e.control.value),
# #     )

# #     def update_waiter(waiter_name):
# #         nonlocal selected_waiter
# #         selected_waiter = waiter_name
# #         page.client_storage.set("selected_waiter", waiter_name)
# #         print(f"DEBUG: Selected waiter: {waiter_name}")
# #         update_sales_display()
# #         page.update()

# #     # Display sales
# #     sales_list = ft.ListView(
# #         spacing=10,
# #         padding=10,
# #         auto_scroll=True,
# #     )

# #     def update_sales_display():
# #         sales_list.controls.clear()
# #         orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
# #         if not orders:
# #             sales_list.controls.append(
# #                 ft.Container(
# #                     content=ft.Text(
# #                         f"No sales for {selected_date.strftime('%Y-%m-%d')}",
# #                         size=14,
# #                         color=ft.Colors.BLACK54,
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     padding=10,
# #                     width=340,
# #                 )
# #             )
# #             page.update()
# #             return

# #         # Filter orders by selected waiter
# #         if selected_waiter != "All":
# #             orders = [order for order in orders if order.get("waiter") == selected_waiter]
        
# #         total_sales = sum(order["total"] for order in orders)
# #         total_quantity = 0
        
# #         if orders:
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     f"Sales on {selected_date.strftime('%Y-%m-%d')} {'for ' + selected_waiter if selected_waiter != 'All' else ''}:",
# #                     size=16,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.BLACK87,
# #                 )
# #             )
# #             for order in orders:
# #                 items = db.get_order_items(order["order_id"])
# #                 total_quantity += sum(item["quantity"] for item in items)
# #                 items_display = ft.Container(
# #                     content=ft.Column(
# #                         [
# #                             ft.Text("Order Items", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
# #                             ft.ListView(
# #                                 controls=[
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"{item['item_name']} x {item['quantity']}",
# #                                                 size=10,
# #                                                 color=ft.Colors.BLACK87,
# #                                                 max_lines=1,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{item['total']:.2f}",
# #                                                 size=10,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                                 color=ft.Colors.GREEN_700,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ) for item in items
# #                                 ],
# #                                 spacing=5,
# #                                 padding=5,
# #                                 auto_scroll=True,
# #                             ),
# #                         ],
# #                         spacing=5,
# #                     ),
# #                     bgcolor=ft.Colors.WHITE,
# #                     padding=5,
# #                     border_radius=8,
# #                     shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
# #                     margin=ft.margin.only(left=5, right=5, top=5),
# #                     width=340,
# #                     visible=False,
# #                 )

# #                 def toggle_details(e):
# #                     items_display.visible = not items_display.visible
# #                     page.update()

# #                 sales_list.controls.append(
# #                     ft.GestureDetector(
# #                         content=ft.Container(
# #                             content=ft.Column(
# #                                 [
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"Order ID: {order['order_id'][:8]}... | {order['order_type'].replace('_', ' ').title()} | {order['order_date']}",
# #                                                 size=12,
# #                                                 weight=ft.FontWeight.W_500,
# #                                                 color=ft.Colors.BLACK87,
# #                                                 max_lines=1,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{order['total']:.2f}",
# #                                                 size=12,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                                 color=ft.Colors.GREEN_700,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ),
# #                                     ft.Text(
# #                                         f"Waiter: {order.get('waiter', 'N/A')}",
# #                                         size=10,
# #                                         color=ft.Colors.BLACK54,
# #                                         max_lines=1,
# #                                     ),
# #                                     items_display,
# #                                 ],
# #                                 spacing=5,
# #                             ),
# #                             bgcolor=ft.Colors.WHITE,
# #                             padding=10,
# #                             border_radius=8,
# #                             shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
# #                             width=340,
# #                         ),
# #                         on_tap=toggle_details,
# #                         on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
# #                     )
# #                 )
            
# #             # Display total sales and quantity for selected waiter
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     f"Total Sales {'for ' + selected_waiter if selected_waiter != 'All' else ''}: Rs{total_sales:.2f}",
# #                     size=14,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.BLACK87,
# #                     text_align=ft.TextAlign.RIGHT,
# #                 )
# #             )
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     f"Total Quantity {'for ' + selected_waiter if selected_waiter != 'All' else ''}: {total_quantity}",
# #                     size=14,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.BLACK87,
# #                     text_align=ft.TextAlign.RIGHT,
# #                 )
# #             )
            
# #             # Display overall sales and quantity if waiter is "All"
# #             if selected_waiter == "All":
# #                 all_orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
# #                 overall_sales = sum(order["total"] for order in all_orders)
# #                 overall_quantity = sum(sum(item["quantity"] for item in db.get_order_items(order["order_id"])) for order in all_orders)
# #                 sales_list.controls.append(
# #                     ft.Text(
# #                         f"Overall Sales: Rs{overall_sales:.2f}",
# #                         size=14,
# #                         weight=ft.FontWeight.BOLD,
# #                         color=ft.Colors.BLUE_700,
# #                         text_align=ft.TextAlign.RIGHT,
# #                     )
# #                 )
# #                 sales_list.controls.append(
# #                     ft.Text(
# #                         f"Overall Quantity: {overall_quantity}",
# #                         size=14,
# #                         weight=ft.FontWeight.BOLD,
# #                         color=ft.Colors.BLUE_700,
# #                         text_align=ft.TextAlign.RIGHT,
# #                     )
# #                 )
# #         else:
# #             sales_list.controls.append(
# #                 ft.Container(
# #                     content=ft.Text(
# #                         f"No sales for {selected_date.strftime('%Y-%m-%d')} {'for ' + selected_waiter if selected_waiter != 'All' else ''}",
# #                         size=14,
# #                         color=ft.Colors.BLACK54,
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     padding=10,
# #                     width=340,
# #                 )
# #             )
# #         page.update()

# #     # Initial display
# #     update_sales_display()

# #     # Gradient background
# #     background = ft.Container(
# #         gradient=ft.LinearGradient(
# #             begin=ft.Alignment(-1, -1),
# #             end=ft.Alignment(1, 1),
# #             colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
# #         ),
# #         expand=True,
# #     )

# #     # Main content container
# #     sales_content = ft.Container(
# #         content=ft.Column(
# #             [
# #                 ft.Container(
# #                     content=ft.Text(
# #                         "Sales by Date",
# #                         size=24,
# #                         weight=ft.FontWeight.BOLD,
# #                         color=ft.Colors.WHITE,
# #                         font_family="Roboto",
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     shadow=ft.BoxShadow(
# #                         blur_radius=8,
# #                         spread_radius=1,
# #                         color=ft.Colors.BLACK26,
# #                     ),
# #                     padding=8,
# #                 ),
# #                 ft.Row(
# #                     [date_picker_button, waiter_dropdown],
# #                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                     spacing=10,
# #                 ),
# #                 ft.Container(
# #                     content=sales_list,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     padding=10,
# #                     shadow=ft.BoxShadow(
# #                         blur_radius=15,
# #                         spread_radius=3,
# #                         color=ft.Colors.BLACK26,
# #                     ),
# #                     margin=ft.margin.symmetric(horizontal=10, vertical=20),
# #                     height=400,
# #                     width=340,
# #                 ),
# #             ],
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=10,
# #         ),
# #         width=min(page.width, 360),
# #         alignment=ft.alignment.center,
# #     )

# #     # Stack the gradient background and content
# #     return ft.Stack(
# #         [
# #             background,
# #             sales_content,
# #         ],
# #         expand=True,
# #     )



# # import flet as ft
# # import datetime

# # def sale_view(page: ft.Page, db: 'Database'):
# #     page.title = "Sales Dashboard"
# #     page.bgcolor = ft.Colors.GREY_100
# #     page.padding = 10
# #     page.scroll = ft.ScrollMode.AUTO

# #     # DatePicker for date selection
# #     selected_date = datetime.datetime.now()

# #     def update_sales_by_date(e):
# #         nonlocal selected_date
# #         selected_date = e.control.value
# #         date_picker.open = False
# #         update_sales_display()
# #         page.update()

# #     date_picker = ft.DatePicker(
# #         first_date=datetime.datetime(year=2000, month=1, day=1),
# #         last_date=datetime.datetime(year=2050, month=12, day=31),
# #         value=selected_date,
# #         on_change=update_sales_by_date,
# #         on_dismiss=lambda e: page.update(),
# #         #bgcolor=ft.Colors.WHITE,
# #         #content_padding=10,
# #     )

# #     def show_date_picker(e):
# #         page.dialog = date_picker
# #         date_picker.open = True
# #         page.overlay.append(date_picker)
# #         page.update()

# #     date_picker_button = ft.ElevatedButton(
# #         content=ft.Row(
# #             [
# #                 ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.BLUE_600, size=18),
# #                 ft.Text(
# #                     selected_date.strftime("%Y-%m-%d"),
# #                     color=ft.Colors.BLUE_600,
# #                     weight=ft.FontWeight.W_500,
# #                     size=14,
# #                 ),
# #             ],
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             spacing=8,
# #         ),
# #         style=ft.ButtonStyle(
# #             shape=ft.RoundedRectangleBorder(radius=8),
# #             bgcolor=ft.Colors.WHITE,
# #             padding=ft.padding.symmetric(horizontal=16, vertical=12),
# #             elevation={"pressed": 2, "": 4},
# #         ),
# #         on_click=show_date_picker,
# #         opacity=1.0,
# #         on_hover=lambda e: setattr(e.control, 'opacity', 0.9 if e.data == "true" else 1.0) or e.control.update(),
# #     )

# #     # Waiter Dropdown
# #     WAITERS = ["All", "Ali", "Ahmed", "Sara", "Zain"]
# #     selected_waiter = page.client_storage.get("selected_waiter") or "All"

# #     waiter_dropdown = ft.Dropdown(
# #         label="Select Waiter",
# #         width=200,
# #         options=[ft.dropdown.Option(w) for w in WAITERS],
# #         value=selected_waiter,
# #         text_size=14,
# #         label_style=ft.TextStyle(color=ft.Colors.GREY_700, size=14),
# #         content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
# #         bgcolor=ft.Colors.WHITE,
# #         border_color=ft.Colors.GREY_300,
# #         focused_border_color=ft.Colors.BLUE_600,
# #         on_change=lambda e: update_waiter(e.control.value),
# #     )

# #     def update_waiter(waiter_name):
# #         nonlocal selected_waiter
# #         selected_waiter = waiter_name
# #         page.client_storage.set("selected_waiter", waiter_name)
# #         print(f"DEBUG: Selected waiter: {waiter_name}")
# #         page.snack_bar = ft.SnackBar(
# #             ft.Text(f"Viewing sales for {waiter_name}", color=ft.Colors.GREEN_600),
# #             open=True,
# #         )
# #         update_sales_display()
# #         page.update()

# #     # Sales List
# #     sales_list = ft.ListView(
# #         spacing=12,
# #         padding=10,
# #         auto_scroll=True,
# #         expand=True,
# #     )

# #     def update_sales_display():
# #         sales_list.controls.clear()
# #         orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
# #         if not orders:
# #             sales_list.controls.append(
# #                 ft.Container(
# #                     content=ft.Text(
# #                         f"No sales for {selected_date.strftime('%Y-%m-%d')}",
# #                         size=16,
# #                         color=ft.Colors.GREY_600,
# #                         text_align=ft.TextAlign.CENTER,
# #                         weight=ft.FontWeight.W_500,
# #                     ),
# #                     padding=20,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
# #                     width=340,
# #                 )
# #             )
# #             page.update()
# #             return

# #         # Filter orders by selected waiter
# #         if selected_waiter != "All":
# #             orders = [order for order in orders if order.get("waiter") == selected_waiter]

# #         total_sales = sum(order["total"] for order in orders)
# #         total_quantity = 0
# #         product_quantities = {}

# #         # Summary card for totals
# #         summary_controls = [
# #             ft.Text(
# #                 f"Sales Summary {'for ' + selected_waiter if selected_waiter != 'All' else ''} - {selected_date.strftime('%Y-%m-%d')}",
# #                 size=16,
# #                 weight=ft.FontWeight.BOLD,
# #                 color=ft.Colors.GREY_800,
# #             ),
# #             ft.Divider(height=1, color=ft.Colors.GREY_300),
# #             ft.Row(
# #                 [
# #                     ft.Text("Total Sales:", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
# #                     ft.Text(f"Rs{total_sales:.2f}", size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
# #                 ],
# #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             ),
# #             # ft.Row(
# #             #     [
# #             #         ft.Text("Total Quantity:", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
# #             #         ft.Text(f"{total_quantity}", size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
# #             #     ],
# #             #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             # ),
# #         ]

# #         # Orders section
# #         if orders:
# #             sales_list.controls.append(
# #                 ft.Text(
# #                     "Orders",
# #                     size=16,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.GREY_800,
# #                 )
# #             )
# #             for order in orders:
# #                 items = db.get_order_items(order["order_id"])
# #                 for item in items:
# #                     total_quantity += item["quantity"]
# #                     item_name = item["item_name"]
# #                     product_quantities[item_name] = product_quantities.get(item_name, 0) + item["quantity"]

# #                 items_display = ft.Container(
# #                     content=ft.Column(
# #                         [
# #                             ft.Text(
# #                                 "Items",
# #                                 size=12,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.GREY_800,
# #                             ),
# #                             ft.ListView(
# #                                 controls=[
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"{item['item_name']} x {item['quantity']}",
# #                                                 size=12,
# #                                                 color=ft.Colors.GREY_700,
# #                                                 weight=ft.FontWeight.W_500,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{item['total']:.2f}",
# #                                                 size=12,
# #                                                 color=ft.Colors.GREEN_700,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ) for item in items
# #                                 ],
# #                                 spacing=8,
# #                                 padding=8,
# #                                 auto_scroll=True,
# #                             ),
# #                         ],
# #                         spacing=8,
# #                     ),
# #                     bgcolor=ft.Colors.GREY_50,
# #                     padding=10,
# #                     border_radius=8,
# #                     margin=ft.margin.only(left=8, right=8, top=4),
# #                     width=324,
# #                     visible=False,
# #                 )

# #                 def toggle_details(e):
# #                     items_display.visible = not items_display.visible
# #                     page.update()

# #                 sales_list.controls.append(
# #                     ft.GestureDetector(
# #                         content=ft.Container(
# #                             content=ft.Column(
# #                                 [
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"Order {order['order_id'][:8]} | {order['order_type'].replace('_', ' ').title()}",
# #                                                 size=14,
# #                                                 weight=ft.FontWeight.W_500,
# #                                                 color=ft.Colors.GREY_800,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"Rs{order['total']:.2f}",
# #                                                 size=14,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                                 color=ft.Colors.GREEN_700,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ),
# #                                     ft.Text(
# #                                         f"Waiter: {order.get('waiter', 'N/A')} | {order['order_date']}",
# #                                         size=12,
# #                                         color=ft.Colors.GREY_600,
# #                                         weight=ft.FontWeight.W_400,
# #                                     ),
# #                                     items_display,
# #                                 ],
# #                                 spacing=8,
# #                             ),
# #                             bgcolor=ft.Colors.WHITE,
# #                             padding=12,
# #                             border_radius=10,
# #                             shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
# #                             width=340,
# #                             animate_opacity=True,
# #                             opacity=1.0,
# #                         ),
# #                         on_tap=toggle_details,
# #                         on_hover=lambda e: setattr(e.control.content, 'opacity', 0.95 if e.data == "true" else 1.0) or e.control.content.update(),
# #                     )
# #                 )

# #             # Update summary with actual total_quantity
# #             # summary_controls[2] = ft.Row(
# #             #     [
# #             #         ft.Text("Total Quantity:", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
# #             #         ft.Text(f"{total_quantity}", size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
# #             #     ],
# #             #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             # )

# #             # Product quantities
# #             summary_controls.extend([
# #                 ft.Text(
# #                     f"Product Quantities {'for ' + selected_waiter if selected_waiter != 'All' else ''}",
# #                     size=14,
# #                     weight=ft.FontWeight.BOLD,
# #                     color=ft.Colors.GREY_800,
# #                 ),
# #                 ft.ListView(
# #                     controls=[
# #                         ft.Row(
# #                             [
# #                                 ft.Text(
# #                                     f"{item_name}",
# #                                     size=12,
# #                                     color=ft.Colors.GREY_700,
# #                                     weight=ft.FontWeight.W_500,
# #                                 ),
# #                                 ft.Text(
# #                                     f"{qty}",
# #                                     size=12,
# #                                     color=ft.Colors.BLUE_600,
# #                                     weight=ft.FontWeight.BOLD,
# #                                 ),
# #                             ],
# #                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                         ) for item_name, qty in sorted(product_quantities.items())
# #                     ],
# #                     spacing=8,
# #                     padding=8,
# #                     auto_scroll=True,
# #                 ),
# #             ])

# #         # Add summary card at the top
# #         sales_list.controls.insert(
# #             0,
# #             ft.Container(
# #                 content=ft.Column(
# #                     summary_controls,
# #                     spacing=10,
# #                 ),
# #                 bgcolor=ft.Colors.WHITE,
# #                 padding=12,
# #                 border_radius=10,
# #                 shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
# #                 width=340,
# #                 margin=ft.margin.only(bottom=12),
# #             )
# #         )

# #         # Overall totals for "All" waiters
# #         if selected_waiter == "All":
# #             all_orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
# #             overall_sales = sum(order["total"] for order in all_orders)
# #             overall_quantity = sum(sum(item["quantity"] for item in db.get_order_items(order["order_id"])) for order in all_orders)
# #             overall_product_quantities = {}
# #             for order in all_orders:
# #                 items = db.get_order_items(order["order_id"])
# #                 for item in items:
# #                     item_name = item["item_name"]
# #                     overall_product_quantities[item_name] = overall_product_quantities.get(item_name, 0) + item["quantity"]

# #             sales_list.controls.append(
# #                 ft.Container(
# #                     content=ft.Column(
# #                         [
# #                             ft.Text(
# #                                 "Overall Summary",
# #                                 size=16,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.GREY_800,
# #                             ),
# #                             ft.Divider(height=1, color=ft.Colors.GREY_300),
# #                             ft.Row(
# #                                 [
# #                                     ft.Text("Overall Sales:", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
# #                                     ft.Text(f"Rs{overall_sales:.2f}", size=14, color=ft.Colors.BLUE_600, weight=ft.FontWeight.BOLD),
# #                                 ],
# #                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                             ),
# #                             # ft.Row(
# #                             #     [
# #                             #         ft.Text("Overall Quantity:", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
# #                             #         ft.Text(f"{overall_quantity}", size=14, color=ft.Colors.BLUE_600, weight=ft.FontWeight.BOLD),
# #                             #     ],
# #                             #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                             # ),
# #                             ft.Text(
# #                                 "Overall Product Quantities",
# #                                 size=14,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.GREY_800,
# #                             ),
# #                             ft.ListView(
# #                                 controls=[
# #                                     ft.Row(
# #                                         [
# #                                             ft.Text(
# #                                                 f"{item_name}",
# #                                                 size=12,
# #                                                 color=ft.Colors.GREY_700,
# #                                                 weight=ft.FontWeight.W_500,
# #                                             ),
# #                                             ft.Text(
# #                                                 f"{qty}",
# #                                                 size=12,
# #                                                 color=ft.Colors.BLUE_600,
# #                                                 weight=ft.FontWeight.BOLD,
# #                                             ),
# #                                         ],
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                     ) for item_name, qty in sorted(overall_product_quantities.items())
# #                                 ],
# #                                 spacing=8,
# #                                 padding=8,
# #                                 auto_scroll=True,
# #                             ),
# #                         ],
# #                         spacing=10,
# #                     ),
# #                     bgcolor=ft.Colors.WHITE,
# #                     padding=12,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
# #                     width=340,
# #                     margin=ft.margin.only(top=12),
# #                 )
# #             )

# #         page.update()

# #     # Initial display
# #     update_sales_display()

# #     # Main content
# #     sales_content = ft.Container(
# #         content=ft.Column(
# #             [
# #                 ft.Container(
# #                     content=ft.Text(
# #                         "Sales Dashboard",
# #                         size=24,
# #                         weight=ft.FontWeight.BOLD,
# #                         color=ft.Colors.GREY_800,
# #                         font_family="Roboto",
# #                         text_align=ft.TextAlign.CENTER,
# #                     ),
# #                     padding=12,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
# #                     margin=ft.margin.only(bottom=12),
# #                 ),
# #                 ft.Row(
# #                     [date_picker_button, waiter_dropdown],
# #                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                     spacing=12,
# #                 ),
# #                 ft.Container(
# #                     content=sales_list,
# #                     bgcolor=ft.Colors.GREY_50,
# #                     border_radius=10,
# #                     padding=12,
# #                     shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_300),
# #                     margin=ft.margin.only(top=12),
# #                     width=360,
# #                     height=page.height - 200,
# #                 ),
# #             ],
# #             alignment=ft.MainAxisAlignment.START,
# #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=12,
# #         ),
# #         width=min(page.width, 360),
# #         alignment=ft.alignment.center,
# #     )

# #     return sales_content



# import flet as ft
# import datetime

# def sale_view(page: ft.Page, db: 'Database'):
#     page.title = "Sales Dashboard"
#     page.bgcolor = ft.Colors.GREY_100
#     page.padding = 0  # Full-screen layout
#     page.scroll = ft.ScrollMode.AUTO
#     page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

#     # DatePicker for date selection
#     selected_date = datetime.datetime.now()

#     def update_sales_by_date(e):
#         nonlocal selected_date
#         selected_date = e.control.value
#         date_picker.open = False
#         update_sales_display()
#         page.update()

#     date_picker = ft.DatePicker(
#         first_date=datetime.datetime(year=2000, month=1, day=1),
#         last_date=datetime.datetime(year=2050, month=12, day=31),
#         value=selected_date,
#         on_change=update_sales_by_date,
#         on_dismiss=lambda e: page.update(),
#     )

#     def show_date_picker(e):
#         page.dialog = date_picker
#         date_picker.open = True
#         page.overlay.append(date_picker)
#         page.update()

#     date_picker_button = ft.ElevatedButton(
#         content=ft.Row(
#             [
#                 ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.BLUE_700, size=20),
#                 ft.Text(
#                     selected_date.strftime("%Y-%m-%d"),
#                     color=ft.Colors.BLUE_700,
#                     weight=ft.FontWeight.W_500,
#                     size=12,
#                     font_family="Roboto",
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             spacing=8,
#         ),
#         style=ft.ButtonStyle(
#             shape=ft.RoundedRectangleBorder(radius=8),
#             bgcolor=ft.Colors.WHITE,
#             padding=ft.padding.symmetric(horizontal=16, vertical=12),
#             elevation={"pressed": 2, "": 4},
#             animation_duration=200,
#             text_style=ft.TextStyle(size=16, font_family="Roboto", weight=ft.FontWeight.W_500),
#         ),
#         width=120,
#         on_click=show_date_picker,
#         opacity=1.0,
#         on_hover=lambda e: setattr(e.control, 'opacity', 0.9 if e.data == "true" else 1.0) or e.control.update(),
#     )

#     # Waiter Dropdown
#     WAITERS = ["All", "Ali", "Ahmed", "Sara", "Zain"]
#     selected_waiter = page.client_storage.get("selected_waiter") or "All"

#     waiter_dropdown = ft.Dropdown(
#         label="Select Waiter",
#         width=150,
#         options=[ft.dropdown.Option(w) for w in WAITERS],
#         value=selected_waiter,
#         text_style=ft.TextStyle(size=16, color=ft.Colors.BLACK, font_family="Roboto", weight=ft.FontWeight.W_500),
#         label_style=ft.TextStyle(color=ft.Colors.GREY_600, size=14, font_family="Roboto"),
#         content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
#         bgcolor=ft.Colors.WHITE,
#         border_color=ft.Colors.GREY_300,
#         focused_border_color=ft.Colors.BLUE_700,
#         filled=True,
#         border_radius=8,
#         on_change=lambda e: update_waiter(e.control.value),
#     )

#     def update_waiter(waiter_name):
#         nonlocal selected_waiter
#         selected_waiter = waiter_name
#         page.client_storage.set("selected_waiter", waiter_name)
#         print(f"DEBUG: Selected waiter: {waiter_name}")
#         page.snack_bar = ft.SnackBar(
#             content=ft.Text(f"Viewing sales for {waiter_name}", size=14, color=ft.Colors.WHITE, font_family="Roboto", weight=ft.FontWeight.W_500),
#             bgcolor=ft.Colors.GREEN_700,
#             padding=12,
#             margin=ft.margin.only(bottom=80),
#             open=True,
#             duration=3000,
#         )
#         update_sales_display()
#         page.update()

#     # Sales List
#     sales_list = ft.ListView(
#         spacing=12,
#         padding=16,
#         auto_scroll=True,
#     )

#     def update_sales_display():
#         sales_list.controls.clear()
#         orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
#         if not orders:
#             sales_list.controls.append(
#                 ft.Container(
#                     content=ft.Text(
#                         f"No sales for {selected_date.strftime('%Y-%m-%d')}",
#                         size=16,
#                         color=ft.Colors.GREY_600,
#                         text_align=ft.TextAlign.CENTER,
#                         weight=ft.FontWeight.W_500,
#                         font_family="Roboto",
#                     ),
#                     padding=20,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
#                 )
#             )
#             page.update()
#             return

#         # Filter orders by selected waiter
#         if selected_waiter != "All":
#             orders = [order for order in orders if order.get("waiter") == selected_waiter]

#         total_sales = sum(order["total"] for order in orders)
#         total_quantity = 0
#         product_quantities = {}

#         # Summary card for totals
#         summary_controls = [
#             ft.Text(
#                 f"Sales Summary {'for ' + selected_waiter if selected_waiter != 'All' else ''} - {selected_date.strftime('%Y-%m-%d')}",
#                 size=18,
#                 weight=ft.FontWeight.BOLD,
#                 color=ft.Colors.BLACK,
#                 font_family="Roboto",
#             ),
#             ft.Divider(height=1, color=ft.Colors.GREY_300),
#             ft.Row(
#                 [
#                     ft.Text("Total Sales:", size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500, font_family="Roboto"),
#                     ft.Text(f"Rs{total_sales:.2f}", size=16, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD, font_family="Roboto"),
#                 ],
#                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#             ),
#         ]

#         # Orders section
#         if orders:
#             sales_list.controls.append(
#                 ft.Text(
#                     "Orders",
#                     size=18,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK,
#                     font_family="Roboto",
#                 )
#             )
#             for order in orders:
#                 items = db.get_order_items(order["order_id"])
#                 for item in items:
#                     total_quantity += item["quantity"]
#                     item_name = item["item_name"]
#                     product_quantities[item_name] = product_quantities.get(item_name, 0) + item["quantity"]

#                 items_display = ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text(
#                                 "Items",
#                                 size=14,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.GREY_800,
#                                 font_family="Roboto",
#                             ),
#                             ft.ListView(
#                                 controls=[
#                                     ft.Row(
#                                         [
#                                             ft.Text(
#                                                 f"{item['item_name']} x {item['quantity']}",
#                                                 size=14,
#                                                 color=ft.Colors.GREY_700,
#                                                 weight=ft.FontWeight.W_500,
#                                                 font_family="Roboto",
#                                             ),
#                                             ft.Text(
#                                                 f"Rs{item['total']:.2f}",
#                                                 size=14,
#                                                 color=ft.Colors.GREEN_700,
#                                                 weight=ft.FontWeight.BOLD,
#                                                 font_family="Roboto",
#                                             ),
#                                         ],
#                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                     ) for item in items
#                                 ],
#                                 spacing=8,
#                                 padding=8,
#                                 auto_scroll=True,
#                             ),
#                         ],
#                         spacing=8,
#                     ),
#                     bgcolor=ft.Colors.GREY_50,
#                     padding=10,
#                     border_radius=8,
#                     margin=ft.margin.only(left=8, right=8, top=4),
#                     visible=False,
#                 )

#                 def toggle_details(e):
#                     items_display.visible = not items_display.visible
#                     page.update()

#                 sales_list.controls.append(
#                     ft.GestureDetector(
#                         content=ft.Container(
#                             content=ft.Column(
#                                 [
#                                     ft.Row(
#                                         [
#                                             ft.Text(
#                                                 f"Order {order['order_id'][:8]} | {order['order_type'].replace('_', ' ').title()}",
#                                                 size=16,
#                                                 weight=ft.FontWeight.W_500,
#                                                 color=ft.Colors.BLACK,
#                                                 font_family="Roboto",
#                                             ),
#                                             ft.Text(
#                                                 f"Rs{order['total']:.2f}",
#                                                 size=16,
#                                                 weight=ft.FontWeight.BOLD,
#                                                 color=ft.Colors.GREEN_700,
#                                                 font_family="Roboto",
#                                             ),
#                                         ],
#                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                     ),
#                                     ft.Text(
#                                         f"Waiter: {order.get('waiter', 'N/A')} | {order['order_date']}",
#                                         size=14,
#                                         color=ft.Colors.GREY_600,
#                                         weight=ft.FontWeight.W_400,
#                                         font_family="Roboto",
#                                     ),
#                                     items_display,
#                                 ],
#                                 spacing=8,
#                             ),
#                             bgcolor=ft.Colors.WHITE,
#                             padding=12,
#                             border_radius=10,
#                             shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
#                             animate_opacity=True,
#                             opacity=1.0,
#                         ),
#                         on_tap=toggle_details,
#                         on_hover=lambda e: setattr(e.control.content, 'opacity', 0.95 if e.data == "true" else 1.0) or e.control.content.update(),
#                     )
#                 )

#             # Product quantities
#             summary_controls.extend([
#                 ft.Text(
#                     f"Product Quantities {'for ' + selected_waiter if selected_waiter != 'All' else ''}",
#                     size=16,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK,
#                     font_family="Roboto",
#                 ),
#                 ft.ListView(
#                     controls=[
#                         ft.Row(
#                             [
#                                 ft.Text(
#                                     f"{item_name}",
#                                     size=14,
#                                     color=ft.Colors.GREY_700,
#                                     weight=ft.FontWeight.W_500,
#                                     font_family="Roboto",
#                                 ),
#                                 ft.Text(
#                                     f"{qty}",
#                                     size=14,
#                                     color=ft.Colors.BLUE_700,
#                                     weight=ft.FontWeight.BOLD,
#                                     font_family="Roboto",
#                                 ),
#                             ],
#                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                         ) for item_name, qty in sorted(product_quantities.items())
#                     ],
#                     spacing=8,
#                     padding=8,
#                     auto_scroll=True,
#                 ),
#             ])

#         # Add summary card at the top
#         sales_list.controls.insert(
#             0,
#             ft.Container(
#                 content=ft.Column(
#                     summary_controls,
#                     spacing=10,
#                 ),
#                 bgcolor=ft.Colors.WHITE,
#                 padding=12,
#                 border_radius=10,
#                 shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
#                 margin=ft.margin.only(bottom=12),
#             )
#         )

#         # Overall totals for "All" waiters
#         if selected_waiter == "All":
#             all_orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
#             overall_sales = sum(order["total"] for order in all_orders)
#             overall_quantity = sum(sum(item["quantity"] for item in db.get_order_items(order["order_id"])) for order in all_orders)
#             overall_product_quantities = {}
#             for order in all_orders:
#                 items = db.get_order_items(order["order_id"])
#                 for item in items:
#                     item_name = item["item_name"]
#                     overall_product_quantities[item_name] = overall_product_quantities.get(item_name, 0) + item["quantity"]

#             sales_list.controls.append(
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text(
#                                 "Overall Summary",
#                                 size=18,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.BLACK,
#                                 font_family="Roboto",
#                             ),
#                             ft.Divider(height=1, color=ft.Colors.GREY_300),
#                             ft.Row(
#                                 [
#                                     ft.Text("Overall Sales:", size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500, font_family="Roboto"),
#                                     ft.Text(f"Rs{overall_sales:.2f}", size=16, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, font_family="Roboto"),
#                                 ],
#                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                             ),
#                             ft.Text(
#                                 "Overall Product Quantities",
#                                 size=16,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.BLACK,
#                                 font_family="Roboto",
#                             ),
#                             ft.ListView(
#                                 controls=[
#                                     ft.Row(
#                                         [
#                                             ft.Text(
#                                                 f"{item_name}",
#                                                 size=14,
#                                                 color=ft.Colors.GREY_700,
#                                                 weight=ft.FontWeight.W_500,
#                                                 font_family="Roboto",
#                                             ),
#                                             ft.Text(
#                                                 f"{qty}",
#                                                 size=14,
#                                                 color=ft.Colors.BLUE_700,
#                                                 weight=ft.FontWeight.BOLD,
#                                                 font_family="Roboto",
#                                             ),
#                                         ],
#                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                     ) for item_name, qty in sorted(overall_product_quantities.items())
#                                 ],
#                                 spacing=8,
#                                 padding=8,
#                                 auto_scroll=True,
#                             ),
#                         ],
#                         spacing=10,
#                     ),
#                     bgcolor=ft.Colors.WHITE,
#                     padding=12,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
#                     margin=ft.margin.only(top=12),
#                 )
#             )

#         page.update()

#     # Initial display
#     update_sales_display()

#     # Main content
#     sales_content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Text(
#                     "Sales Dashboard",
#                     size=24,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK,
#                     font_family="Roboto",
#                     text_align=ft.TextAlign.CENTER,
#                 ),
#                 ft.Row(
#                     [date_picker_button, waiter_dropdown],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     spacing=12,
#                 ),
#                 sales_list,
#             ],
#             alignment=ft.MainAxisAlignment.START,
#             horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
#             spacing=16,
#             scroll=ft.ScrollMode.AUTO,
#         ),
#         width=page.width,
#         height=page.height,
#         bgcolor=ft.Colors.WHITE,
#         padding=ft.padding.symmetric(horizontal=16, vertical=16),
#         border_radius=12,
#         shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.GREY_300),
#         clip_behavior=ft.ClipBehavior.HARD_EDGE,
#     )

#     return sales_content



import flet as ft
import datetime

def sale_view(page: ft.Page, db: 'Database'):
    page.title = "Sales Dashboard"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 0  # Full-screen layout
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

    # DatePicker for date selection
    selected_date = datetime.datetime.now()

    def update_sales_by_date(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_picker.open = False
        update_sales_display()
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2000, month=1, day=1),
        last_date=datetime.datetime(year=2050, month=12, day=31),
        value=selected_date,
        on_change=update_sales_by_date,
        on_dismiss=lambda e: page.update(),
    )

    def show_date_picker(e):
        page.dialog = date_picker
        date_picker.open = True
        page.overlay.append(date_picker)
        page.update()

    date_picker_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.BLUE_700, size=20),
                ft.Text(
                    selected_date.strftime("%Y-%m-%d"),
                    color=ft.Colors.BLUE_700,
                    weight=ft.FontWeight.W_500,
                    size=12,
                    font_family="Roboto",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            elevation={"pressed": 2, "": 4},
            animation_duration=200,
            text_style=ft.TextStyle(size=16, font_family="Roboto", weight=ft.FontWeight.W_500),
        ),
        width=120,
        on_click=show_date_picker,
        opacity=1.0,
        on_hover=lambda e: setattr(e.control, 'opacity', 0.9 if e.data == "true" else 1.0) or e.control.update(),
    )

    # Waiter Dropdown
    waiters = [{"name": "All"}] + db.get_all_waiters()
    print(f"DEBUG: Loaded waiters from database: {[w['name'] for w in waiters]}")
    selected_waiter = page.client_storage.get("selected_waiter") or "All"

    waiter_dropdown = ft.Dropdown(
        label="Select Waiter",
        width=150,
        options=[ft.dropdown.Option(w["name"]) for w in waiters],
        value=selected_waiter if selected_waiter in [w["name"] for w in waiters] else "All",
        text_style=ft.TextStyle(size=16, color=ft.Colors.BLACK, font_family="Roboto", weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=ft.Colors.GREY_600, size=14, font_family="Roboto"),
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.BLUE_700,
        filled=True,
        border_radius=8,
        on_change=lambda e: update_waiter(e.control.value),
    )

    def update_waiter(waiter_name):
        nonlocal selected_waiter
        selected_waiter = waiter_name
        page.client_storage.set("selected_waiter", waiter_name)
        print(f"DEBUG: Selected waiter: {waiter_name}")
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Viewing sales for {waiter_name}", size=14, color=ft.Colors.WHITE, font_family="Roboto", weight=ft.FontWeight.W_500),
            bgcolor=ft.Colors.GREEN_700,
            padding=12,
            margin=ft.margin.only(bottom=80),
            open=True,
            duration=3000,
        )
        update_sales_display()
        page.update()

    # Sales List
    sales_list = ft.ListView(
        spacing=12,
        padding=16,
        auto_scroll=True,
    )

    def update_sales_display():
        sales_list.controls.clear()
        orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
        if not orders:
            sales_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"No sales for {selected_date.strftime('%Y-%m-%d')}",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500,
                        font_family="Roboto",
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
                )
            )
            page.update()
            return

        # Filter orders by selected waiter
        if selected_waiter != "All":
            orders = [order for order in orders if order.get("waiter") == selected_waiter]

        total_sales = sum(order["total"] for order in orders)
        total_quantity = 0
        product_quantities = {}

        # Summary card for totals
        summary_controls = [
            ft.Text(
                f"Sales Summary {'for ' + selected_waiter if selected_waiter != 'All' else ''} - {selected_date.strftime('%Y-%m-%d')}",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
                font_family="Roboto",
            ),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Row(
                [
                    ft.Text("Total Sales:", size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500, font_family="Roboto"),
                    ft.Text(f"Rs{total_sales:.2f}", size=16, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD, font_family="Roboto"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]

        # Orders section
        if orders:
            sales_list.controls.append(
                ft.Text(
                    "Orders",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    font_family="Roboto",
                )
            )
            for order in orders:
                items = db.get_order_items(order["order_id"])
                for item in items:
                    total_quantity += item["quantity"]
                    item_name = item["item_name"]
                    product_quantities[item_name] = product_quantities.get(item_name, 0) + item["quantity"]

                items_display = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Items",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                                font_family="Roboto",
                            ),
                            ft.ListView(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"{item['item_name']} x {item['quantity']}",
                                                size=14,
                                                color=ft.Colors.GREY_700,
                                                weight=ft.FontWeight.W_500,
                                                font_family="Roboto",
                                            ),
                                            ft.Text(
                                                f"Rs{item['total']:.2f}",
                                                size=14,
                                                color=ft.Colors.GREEN_700,
                                                weight=ft.FontWeight.BOLD,
                                                font_family="Roboto",
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ) for item in items
                                ],
                                spacing=8,
                                padding=8,
                                auto_scroll=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.GREY_50,
                    padding=10,
                    border_radius=8,
                    margin=ft.margin.only(left=8, right=8, top=4),
                    visible=False,
                )

                def toggle_details(e):
                    items_display.visible = not items_display.visible
                    page.update()

                sales_list.controls.append(
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"Order {order['order_id'][:8]} | {order['order_type'].replace('_', ' ').title()}",
                                                size=16,
                                                weight=ft.FontWeight.W_500,
                                                color=ft.Colors.BLACK,
                                                font_family="Roboto",
                                            ),
                                            ft.Text(
                                                f"Rs{order['total']:.2f}",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREEN_700,
                                                font_family="Roboto",
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Text(
                                        f"Waiter: {order.get('waiter', 'N/A')} | {order['order_date']}",
                                        size=14,
                                        color=ft.Colors.GREY_600,
                                        weight=ft.FontWeight.W_400,
                                        font_family="Roboto",
                                    ),
                                    items_display,
                                ],
                                spacing=8,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=12,
                            border_radius=10,
                            shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
                            animate_opacity=True,
                            opacity=1.0,
                        ),
                        on_tap=toggle_details,
                        on_hover=lambda e: setattr(e.control.content, 'opacity', 0.95 if e.data == "true" else 1.0) or e.control.content.update(),
                    )
                )

            # Product quantities
            summary_controls.extend([
                ft.Text(
                    f"Product Quantities {'for ' + selected_waiter if selected_waiter != 'All' else ''}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    font_family="Roboto",
                ),
                ft.ListView(
                    controls=[
                        ft.Row(
                            [
                                ft.Text(
                                    f"{item_name}",
                                    size=14,
                                    color=ft.Colors.GREY_700,
                                    weight=ft.FontWeight.W_500,
                                    font_family="Roboto",
                                ),
                                ft.Text(
                                    f"{qty}",
                                    size=14,
                                    color=ft.Colors.BLUE_700,
                                    weight=ft.FontWeight.BOLD,
                                    font_family="Roboto",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ) for item_name, qty in sorted(product_quantities.items())
                    ],
                    spacing=8,
                    padding=8,
                    auto_scroll=True,
                ),
            ])

        # Add summary card at the top
        sales_list.controls.insert(
            0,
            ft.Container(
                content=ft.Column(
                    summary_controls,
                    spacing=10,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=12,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
                margin=ft.margin.only(bottom=12),
            )
        )

        # Overall totals for "All" waiters
        if selected_waiter == "All":
            all_orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
            overall_sales = sum(order["total"] for order in all_orders)
            overall_quantity = sum(sum(item["quantity"] for item in db.get_order_items(order["order_id"])) for order in all_orders)
            overall_product_quantities = {}
            for order in all_orders:
                items = db.get_order_items(order["order_id"])
                for item in items:
                    item_name = item["item_name"]
                    overall_product_quantities[item_name] = overall_product_quantities.get(item_name, 0) + item["quantity"]

            sales_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Overall Summary",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                                font_family="Roboto",
                            ),
                            ft.Divider(height=1, color=ft.Colors.GREY_300),
                            ft.Row(
                                [
                                    ft.Text("Overall Sales:", size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500, font_family="Roboto"),
                                    ft.Text(f"Rs{overall_sales:.2f}", size=16, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, font_family="Roboto"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                "Overall Product Quantities",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                                font_family="Roboto",
                            ),
                            ft.ListView(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"{item_name}",
                                                size=14,
                                                color=ft.Colors.GREY_700,
                                                weight=ft.FontWeight.W_500,
                                                font_family="Roboto",
                                            ),
                                            ft.Text(
                                                f"{qty}",
                                                size=14,
                                                color=ft.Colors.BLUE_700,
                                                weight=ft.FontWeight.BOLD,
                                                font_family="Roboto",
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ) for item_name, qty in sorted(overall_product_quantities.items())
                                ],
                                spacing=8,
                                padding=8,
                                auto_scroll=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    padding=12,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.GREY_300),
                    margin=ft.margin.only(top=12),
                )
            )

        page.update()

    # Initial display
    update_sales_display()

    # Main content
    sales_content = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Sales Dashboard",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    font_family="Roboto",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    [date_picker_button, waiter_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
                sales_list,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=page.width,
        height=page.height,
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.GREY_300),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return sales_content