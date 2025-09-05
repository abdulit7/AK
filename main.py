# # import flet as ft
# # from dashboard import dashboard_view
# # from expense import expense_view
# # from sale import sale_view
# # from menu import menu_view
# # from product import product_view
# # from order import order_view
# # from setting import settings_view
# # from database import Database

# # # Initialize database
# # db = Database()
# # MENU_ITEMS = db.get_menu()
# # EXPENSES = {"Rent": 5000, "Water": 500, "Fuel": 500, "Other": 400}
# # ORDERS = {"dine_in": {}, "takeaway": {}, "online": {}}
# # TOTAL_SALES = 0.0
# # TOTAL_EXPENSES = sum(EXPENSES.values())
# # NET_PROFIT = 0.0

# # def main(page: ft.Page):
# #     page.title = "AKBER TIKKA"
# #     page.vertical_alignment = ft.MainAxisAlignment.START
# #     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
# #     page.padding = ft.padding.only(top=30)  # Add top padding for Android status bar
# #     page.bgcolor = ft.Colors.ORANGE_100
# #     page.scroll = ft.ScrollMode.AUTO
# #     # Set mobile dimensions
# #     page.window.width = 370
# #     page.window.height = 640
# #     page.window.resizable = True

# #     # Top AppBar
# #     page.appbar = ft.AppBar(
# #         title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD),
# #         center_title=True,
# #         bgcolor=ft.Colors.ORANGE_400,
# #         actions=[
# #             ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard")),
# #             ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda e: page.go("/settings")),
# #         ],
# #     )
# #     print("AppBar initialized with title 'AKBER TIKKA'")

# #     # Bottom AppBar
# #     def on_fab_click(e):
# #         page.go("/products")
# #         page.update()

# #     page.floating_action_button = ft.FloatingActionButton(
# #         icon=ft.Icons.ADD,
# #         on_click=on_fab_click,
# #         bgcolor=ft.Colors.GREEN_600,
# #         mini=True,
# #     )
# #     page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

# #     page.bottom_appbar = ft.BottomAppBar(
# #         bgcolor=ft.Colors.BLUE_700,
# #         shape=ft.NotchShape.CIRCULAR,
# #         height=60,
# #         content=ft.Row(
# #             controls=[
# #                 ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.WHITE, tooltip="Menu", on_click=lambda e: page.go("/menu")),
# #                 ft.Container(expand=True),
# #                 ft.IconButton(ft.Icons.MONETIZATION_ON, icon_color=ft.Colors.WHITE, tooltip="Expenses", on_click=lambda e: page.go("/expense")),
# #                 ft.IconButton(ft.Icons.SHOW_CHART, icon_color=ft.Colors.WHITE, tooltip="Sales", on_click=lambda e: page.go("/sale")),
# #             ],
# #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             spacing=10,
# #         ),
# #     )
# #     print("BottomAppBar initialized with Menu, Expenses, Sales buttons")

# #     # Route map
# #     def get_route_map(page):
# #         return {
# #             "/dashboard": lambda: dashboard_view(page, db),
# #             "/expense": lambda: expense_view(page, db),
# #             "/sale": lambda: sale_view(page, db),
# #             "/menu": lambda: menu_view(page, db),
# #             "/products": lambda: product_view(page, db),
# #             "/order": lambda: order_view(page, db),
# #             "/orders": lambda: order_view(page, db),
# #             "/settings": lambda: settings_view(page, db),
# #             "/": lambda: dashboard_view(page, db),
# #         }

# #     def route_change(e: ft.RouteChangeEvent):
# #         print(f"Navigating to route: {e.route}")
# #         route = e.route

# #         # Clear overlays to prevent dialog stacking
# #         if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
# #             page.overlay.clear()
# #         page.snack_bar = None

# #         # Handle invalid or root route
# #         route_map = get_route_map(page)
# #         content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=ft.Colors.RED_600))

# #         # Build content
# #         content = content_builder()
# #         view_width = min(page.width, 360)

# #         # Create view without embedding AppBar/BottomAppBar in controls
# #         page.views.clear()
# #         page.views.append(
# #             ft.View(
# #                 route=route,
# #                 controls=[
# #                     ft.Container(
# #                         content=content,
# #                         width=view_width,
# #                         alignment=ft.alignment.center,
# #                         padding=ft.padding.symmetric(horizontal=10),
# #                     )
# #                 ],
# #                 scroll=ft.ScrollMode.AUTO,
# #                 appbar=page.appbar,
# #                 floating_action_button=page.floating_action_button,
# #                 bottom_appbar=page.bottom_appbar,
# #             )
# #         )
# #         print(f"View stack size: {len(page.views)}")
# #         print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
# #         print(f"BottomAppBar status: {'visible' if page.bottom_appbar else 'not visible'}")
# #         try:
# #             page.update()
# #         except Exception as e:
# #             print(f"Error updating page: {e}")
# #             page.snack_bar = ft.SnackBar(content=ft.Text(f"Render error: {e}"), open=True)
# #             page.update()

# #     def view_pop(e):
# #         if len(page.views) > 1:
# #             page.views.pop()
# #             page.go(page.views[-1].route)
# #         else:
# #             page.go("/dashboard")  # Default to dashboard
# #         print(f"View stack after pop: {len(page.views)}")
# #         page.update()

# #     # Set routing handlers
# #     page.on_route_change = route_change
# #     page.on_view_pop = view_pop
# #     page.go("/dashboard")  # Start at dashboard
# #     print("Initial route set to /dashboard")

# # ft.app(target=main, assets_dir="assets")


# # import flet as ft
# # from dashboard import dashboard_view
# # from expense import expense_view
# # from sale import sale_view
# # from menu import menu_view
# # from product import product_view
# # from order import order_view
# # from setting import settings_view
# # from database import Database

# # # Initialize database
# # db = Database()
# # MENU_ITEMS = db.get_menu()
# # EXPENSES = {"Rent": 5000, "Water": 500, "Fuel": 500, "Other": 400}
# # ORDERS = {"dine_in": {}, "takeaway": {}, "online": {}}
# # TOTAL_SALES = 0.0
# # TOTAL_EXPENSES = sum(EXPENSES.values())
# # NET_PROFIT = 0.0

# # def main(page: ft.Page):
# #     page.title = "AKBER TIKKA"
# #     page.vertical_alignment = ft.MainAxisAlignment.START
# #     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
# #     page.padding = ft.padding.only(top=30)  # Add top padding for Android status bar
# #     page.bgcolor = ft.Colors.ORANGE_100
# #     page.scroll = ft.ScrollMode.AUTO
# #     # Set mobile dimensions
# #     page.window.width = 370
# #     page.window.height = 640
# #     page.window.resizable = True

# #     # Top AppBar with Close button
# #     def close_app(e):
# #         print("DEBUG: Closing app")
# #         page.window.close()

# #     page.appbar = ft.AppBar(
# #         title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD),
# #         center_title=True,
# #         bgcolor=ft.Colors.ORANGE_400,
# #         actions=[
# #             ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard"), icon_color=ft.Colors.TEAL),
# #             ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda e: page.go("/settings"), icon_color=ft.Colors.BLUE),
# #             ft.IconButton(ft.Icons.POWER_SETTINGS_NEW, tooltip="Close App", on_click=close_app, icon_color=ft.Colors.RED_600),
# #         ],
# #     )
# #     print("AppBar initialized with title 'AKBER TIKKA' and Close button")

# #     # Bottom AppBar
# #     # def on_fab_click(e):
# #     #     page.go("/products")
# #     #     page.update()

# #     # page.floating_action_button = ft.FloatingActionButton(
# #     #     icon=ft.Icons.ADD,
# #     #     on_click=on_fab_click,
# #     #     bgcolor=ft.Colors.GREEN_600,
# #     #     mini=True,
# #     # )
# #     # page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

# #     page.bottom_appbar = ft.BottomAppBar(
# #         bgcolor=ft.Colors.BLUE_700,
# #         shape=ft.NotchShape.CIRCULAR,
# #         height=60,
# #         content=ft.Row(
# #             controls=[
# #                 ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.WHITE, tooltip="Menu", on_click=lambda e: page.go("/menu")),
# #                 ft.Container(expand=True),
# #                 ft.IconButton(ft.Icons.MONETIZATION_ON, icon_color=ft.Colors.WHITE, tooltip="Expenses", on_click=lambda e: page.go("/expense")),
# #                 ft.IconButton(ft.Icons.SHOW_CHART, icon_color=ft.Colors.WHITE, tooltip="Sales", on_click=lambda e: page.go("/sale")),
# #             ],
# #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             spacing=10,
# #         ),
# #     )
# #     print("BottomAppBar initialized with Menu, Expenses, Sales buttons")

# #     # Route map
# #     def get_route_map(page):
# #         return {
# #             "/dashboard": lambda: dashboard_view(page, db),
# #             "/expense": lambda: expense_view(page, db),
# #             "/sale": lambda: sale_view(page, db),
# #             "/menu": lambda: menu_view(page, db),
# #             "/products": lambda: product_view(page, db),
# #             "/order": lambda: order_view(page, db),
# #             "/orders": lambda: order_view(page, db),
# #             "/settings": lambda: settings_view(page, db),
# #             "/": lambda: dashboard_view(page, db),
# #         }

# #     def route_change(e: ft.RouteChangeEvent):
# #         print(f"Navigating to route: {e.route}")
# #         route = e.route

# #         # Clear overlays to prevent dialog stacking
# #         if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
# #             page.overlay.clear()
# #         page.snack_bar = None

# #         # Handle invalid or root route
# #         route_map = get_route_map(page)
# #         content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=ft.Colors.RED_600))

# #         # Build content
# #         content = content_builder()
# #         view_width = min(page.width, 360)

# #         # Create view without embedding AppBar/BottomAppBar in controls
# #         page.views.clear()
# #         page.views.append(
# #             ft.View(
# #                 route=route,
# #                 controls=[
# #                     ft.Container(
# #                         content=content,
# #                         width=view_width,
# #                         alignment=ft.alignment.center,
# #                         padding=ft.padding.symmetric(horizontal=10),
# #                     )
# #                 ],
# #                 scroll=ft.ScrollMode.AUTO,
# #                 appbar=page.appbar,
# #                 # floating_action_button=page.floating_action_button,
# #                 bottom_appbar=page.bottom_appbar,
# #             )
# #         )
# #         print(f"View stack size: {len(page.views)}")
# #         print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
# #         print(f"BottomAppBar status: {'visible' if page.bottom_appbar else 'not visible'}")
# #         try:
# #             page.update()
# #         except Exception as e:
# #             print(f"Error updating page: {e}")
# #             page.snack_bar = ft.SnackBar(content=ft.Text(f"Render error: {e}"), open=True)
# #             page.update()

# #     def view_pop(e):
# #         if len(page.views) > 1:
# #             page.views.pop()
# #             page.go(page.views[-1].route)
# #             print(f"View stack after pop: {len(page.views)}, Navigated to: {page.views[-1].route}")
# #         else:
# #             print("DEBUG: No more views to pop, closing app")
# #             page.window.close()
# #         page.update()

# #     # Set routing handlers
# #     page.on_route_change = route_change
# #     page.on_view_pop = view_pop
# #     page.go("/dashboard")  # Start at dashboard
# #     print("Initial route set to /dashboard")

# # ft.app(target=main, assets_dir="assets")



# # import asyncio
# # import flet as ft
# # from dashboard import dashboard_view
# # from expense import expense_view
# # from sale import sale_view
# # from menu import menu_view
# # from product import product_view
# # from order import order_view
# # from setting import settings_view
# # from database import Database

# # # Initialize database
# # db = Database()
# # ORDERS = {"dine_in": {}, "takeaway": {}, "online": {}}
# # TOTAL_SALES = 0.0
# # EXPENSES = {"Rent": 5000, "Water": 500, "Fuel": 500, "Other": 400}
# # TOTAL_EXPENSES = sum(EXPENSES.values())
# # NET_PROFIT = 0.0

# # def main(page: ft.Page):
# #     page.title = "AKBER TIKKA"
# #     page.vertical_alignment = ft.MainAxisAlignment.START
# #     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
# #     page.padding = ft.padding.only(top=30)
# #     page.bgcolor = ft.Colors.GREY_100
# #     page.scroll = ft.ScrollMode.AUTO
# #     page.window.width = 370
# #     page.window.height = 640
# #     page.window.resizable = True

# #     COLOR_SCHEME = {
# #         "primary": ft.Colors.BLUE_700,
# #         "accent": ft.Colors.AMBER_600,
# #         "background": ft.Colors.WHITE,
# #         "text": ft.Colors.BLACK87,
# #         "error": ft.Colors.RED_600,
# #         "success": ft.Colors.GREEN_600
# #     }

# #     # Top AppBar with Close button
# #     def close_app(e):
# #         print("DEBUG: Closing app")
# #         page.window.close()

# #     page.appbar = ft.AppBar(
# #         title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"]),
# #         center_title=True,
# #         bgcolor=COLOR_SCHEME["primary"],
# #         actions=[
# #             ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard"), icon_color=COLOR_SCHEME["accent"]),
# #             ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda e: page.go("/settings"), icon_color=COLOR_SCHEME["accent"]),
# #             ft.IconButton(ft.Icons.POWER_SETTINGS_NEW, tooltip="Close App", on_click=close_app, icon_color=COLOR_SCHEME["error"]),
# #         ],
# #     )
# #     print("AppBar initialized with title 'AKBER TIKKA' and Close button")

# #     # Floating Action Button
# #     def on_fab_click(e):
# #         page.go("/products")
# #         page.update()

# #     page.floating_action_button = ft.FloatingActionButton(
# #         icon=ft.Icons.ADD,
# #         on_click=on_fab_click,
# #         bgcolor=COLOR_SCHEME["success"],
# #         mini=True,
# #     )
# #     page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

# #     # Bottom AppBar
# #     page.bottom_appbar = ft.BottomAppBar(
# #         bgcolor=COLOR_SCHEME["primary"],
# #         shape=ft.NotchShape.CIRCULAR,
# #         height=60,
# #         content=ft.Row(
# #             controls=[
# #                 ft.IconButton(ft.Icons.MENU, icon_color=COLOR_SCHEME["background"], tooltip="Menu", on_click=lambda e: page.go("/menu")),
# #                 ft.Container(expand=True),
# #                 ft.IconButton(ft.Icons.MONETIZATION_ON, icon_color=COLOR_SCHEME["background"], tooltip="Expenses", on_click=lambda e: page.go("/expense")),
# #                 ft.IconButton(ft.Icons.SHOW_CHART, icon_color=COLOR_SCHEME["background"], tooltip="Sales", on_click=lambda e: page.go("/sale")),
# #             ],
# #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #             spacing=10,
# #         ),
# #     )
# #     print("BottomAppBar initialized with Menu, Expenses, Sales buttons")

# #     # Route map
# #     def get_route_map(page):
# #         return {
# #             "/dashboard": lambda: dashboard_view(page, db),
# #             "/expense": lambda: expense_view(page, db),
# #             "/sale": lambda: sale_view(page, db),
# #             "/menu": lambda: menu_view(page, db),
# #             "/products": lambda: product_view(page, db),
# #             "/order": lambda: order_view(page, db),
# #             "/orders": lambda: order_view(page, db),
# #             "/settings": lambda: settings_view(page, db),
# #             "/": lambda: dashboard_view(page, db),
# #         }

# #     def route_change(e: ft.RouteChangeEvent):
# #         print(f"Navigating to route: {e.route}")
# #         route = e.route

# #         # Clear overlays to prevent dialog stacking
# #         if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
# #             page.overlay.clear()
# #         page.snack_bar = None

# #         # Handle invalid or root route
# #         route_map = get_route_map(page)
# #         content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=COLOR_SCHEME["error"]))

# #         # Build content
# #         content = content_builder()
# #         view_width = min(page.width, 360)

# #         # Create view
# #         page.views.clear()
# #         page.views.append(
# #             ft.View(
# #                 route=route,
# #                 controls=[
# #                     ft.Container(
# #                         content=content,
# #                         width=view_width,
# #                         alignment=ft.alignment.center,
# #                         padding=ft.padding.symmetric(horizontal=10),
# #                     )
# #                 ],
# #                 scroll=ft.ScrollMode.AUTO,
# #                 appbar=page.appbar,
# #                 floating_action_button=page.floating_action_button,
# #                 bottom_appbar=page.bottom_appbar,
# #             )
# #         )
# #         print(f"View stack size: {len(page.views)}")
# #         print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
# #         print(f"BottomAppBar status: {'visible' if page.bottom_appbar else 'not visible'}")
# #         try:
# #             page.update()
# #         except Exception as e:
# #             print(f"Error updating page: {e}")
# #             page.snack_bar = ft.SnackBar(content=ft.Text(f"Render error: {e}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]), open=True)
# #             page.update()

# #     def view_pop(e):
# #         if len(page.views) > 1:
# #             page.views.pop()
# #             page.go(page.views[-1].route)
# #             print(f"View stack after pop: {len(page.views)}, Navigated to: {page.views[-1].route}")
# #         else:
# #             print("DEBUG: No more views to pop, closing app")
# #             page.window.close()
# #         page.update()

# #     # Set routing handlers
# #     page.on_route_change = route_change
# #     page.on_view_pop = view_pop
# #     page.go("/dashboard")
# #     print("Initial route set to /dashboard")

# # if __name__ == "__main__":
# #     loop = asyncio.new_event_loop()
# #     asyncio.set_event_loop(loop)
# #     ft.app(target=main, assets_dir="assets")
# #     loop.close()



# import asyncio
# import flet as ft
# from dashboard import dashboard_view
# from expense import expense_view
# from sale import sale_view
# from menu import menu_view
# from product import product_view
# from order import order_view
# from setting import settings_view
# from database import Database
# from employee import employee_view

# # Initialize database
# db = Database()
# ORDERS = {"dine_in": {}, "takeaway": {}, "online": {}}
# TOTAL_SALES = 0.0
# EXPENSES = {"Rent": 5000, "Water": 500, "Fuel": 500, "Other": 400}
# TOTAL_EXPENSES = sum(EXPENSES.values())
# NET_PROFIT = 0.0

# def main(page: ft.Page):
#     page.title = "AKBER TIKKA"
#     page.vertical_alignment = ft.MainAxisAlignment.START
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.padding = ft.padding.only(top=30)
#     page.bgcolor = ft.Colors.GREY_100
#     page.scroll = ft.ScrollMode.AUTO
#     page.window.width = 400
#     page.window.height = 660
#     page.window.resizable = True

#     COLOR_SCHEME = {
#         "primary": ft.Colors.BLUE_700,
#         "accent": ft.Colors.AMBER_600,
#         "background": ft.Colors.WHITE,
#         "text": ft.Colors.BLACK87,
#         "error": ft.Colors.RED_600,
#         "success": ft.Colors.GREEN_600
#     }

#     # Top AppBar with Close button
#     def close_app(e):
#         print("DEBUG: Closing app")
#         page.window.close()

#     page.appbar = ft.AppBar(
#         title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"]),
#         center_title=True,
#         bgcolor=COLOR_SCHEME["primary"],
#         actions=[
#             ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard"), icon_color=COLOR_SCHEME["accent"]),
#             ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda e: page.go("/settings"), icon_color=COLOR_SCHEME["accent"]),
#             ft.IconButton(ft.Icons.POWER_SETTINGS_NEW, tooltip="Close App", on_click=close_app, icon_color=COLOR_SCHEME["error"]),
#         ],
#     )
#     print("AppBar initialized with title 'AKBER TIKKA' and Close button")

#     # Floating Action Button
#     # def on_fab_click(e):
#     #     page.go("/products")
#     #     page.update()

#     # page.floating_action_button = ft.FloatingActionButton(
#     #     icon=ft.Icons.ADD,
#     #     on_click=on_fab_click,
#     #     bgcolor=COLOR_SCHEME["success"],
#     #     mini=True,
#     # )
#     # page.floating_action_button_location = ft.FloatingActionButtonLocation.END_FLOAT

#     # Route map
#     def get_route_map(page):
#         return {
#             "/dashboard": lambda: dashboard_view(page, db),
#             "/expense": lambda: expense_view(page, db),
#             "/sale": lambda: sale_view(page, db),
#             "/menu": lambda: menu_view(page, db),
#             "/products": lambda: product_view(page, db),
#             "/order": lambda: order_view(page, db),
#             "/orders": lambda: order_view(page, db),
#             "/settings": lambda: settings_view(page, db),
#             "/employees": lambda: employee_view(page, db),
#             "/": lambda: dashboard_view(page, db),
#         }

#     def route_change(e: ft.RouteChangeEvent):
#         print(f"Navigating to route: {e.route}")
#         route = e.route

#         # Clear overlays to prevent dialog stacking
#         if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
#             page.overlay.clear()
#         page.snack_bar = None

#         # Handle invalid or root route
#         route_map = get_route_map(page)
#         content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=COLOR_SCHEME["error"]))

#         # Build content
#         content = content_builder()
#         view_width = min(page.width, 390)

#         # Create view
#         page.views.clear()
#         page.views.append(
#             ft.View(
#                 route=route,
#                 controls=[
#                     ft.Container(
#                         content=content,
#                         width=view_width,
#                         alignment=ft.alignment.center,
#                         padding=ft.padding.symmetric(horizontal=10),
#                     )
#                 ],
#                 scroll=ft.ScrollMode.AUTO,
#                 appbar=page.appbar,
               
#             )
#         )
#         print(f"View stack size: {len(page.views)}")
#         print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
#         try:
#             page.update()
#         except Exception as e:
#             print(f"Error updating page: {e}")
#             page.snack_bar = ft.SnackBar(content=ft.Text(f"Render error: {e}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]), open=True)
#             page.update()

#     def view_pop(e):
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)
#             print(f"View stack after pop: {len(page.views)}, Navigated to: {page.views[-1].route}")
#         else:
#             print("DEBUG: No more views to pop, closing app")
#             page.window.close()
#         page.update()

#     # Set routing handlers
#     page.on_route_change = route_change
#     page.on_view_pop = view_pop
#     page.go("/dashboard")
#     print("Initial route set to /dashboard")

# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     ft.app(target=main, assets_dir="assets")
#     loop.close()



import asyncio
import flet as ft
from dashboard import dashboard_view
from expense import expense_view
from sale import sale_view
from menu import menu_view
from product import product_view
from setting import settings_view
from employee import employee_view
from login import login_view
from database import Database

# Initialize database
db = Database()

def main(page: ft.Page):
    page.title = "AKBER TIKKA"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=30)
    page.bgcolor = ft.Colors.GREY_100
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 370
    page.window.height = 640
    page.window.resizable = True
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

    COLOR_SCHEME = {
        "primary": ft.Colors.BLUE_700,
        "accent": ft.Colors.AMBER_600,
        "background": ft.Colors.WHITE,
        "text": ft.Colors.BLACK87,
        "error": ft.Colors.RED_600,
        "success": ft.Colors.GREEN_600
    }

    # Top AppBar with Close button
    def close_app(e):
        print("DEBUG: Closing app")
        page.window.close()

    page.appbar = ft.AppBar(
        title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"], font_family="Roboto"),
        center_title=True,
        bgcolor=COLOR_SCHEME["primary"],
        actions=[
            ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard"), icon_color=COLOR_SCHEME["accent"]),
            ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda e: page.go("/settings"), icon_color=COLOR_SCHEME["accent"]),
            ft.IconButton(ft.Icons.PEOPLE, tooltip="Employees", on_click=lambda e: page.go("/employees"), icon_color=COLOR_SCHEME["accent"]),
            ft.IconButton(ft.Icons.POWER_SETTINGS_NEW, tooltip="Close App", on_click=close_app, icon_color=COLOR_SCHEME["error"]),
        ],
    )

    # # Floating Action Button
    # def on_fab_click(e):
    #     page.go("/products")
    #     page.update()

    # page.floating_action_button = ft.FloatingActionButton(
    #     icon=ft.Icons.ADD,
    #     on_click=on_fab_click,
    #     bgcolor=COLOR_SCHEME["success"],
    #     mini=True,
    # )
    # page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    # Bottom AppBar
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=COLOR_SCHEME["primary"],
        shape=ft.NotchShape.CIRCULAR,
        height=60,
        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.MENU, icon_color=COLOR_SCHEME["background"], tooltip="Menu", on_click=lambda e: page.go("/menu")),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.MONETIZATION_ON, icon_color=COLOR_SCHEME["background"], tooltip="Expenses", on_click=lambda e: page.go("/expense")),
                ft.IconButton(ft.Icons.SHOW_CHART, icon_color=COLOR_SCHEME["background"], tooltip="Sales", on_click=lambda e: page.go("/sale")),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
    )

    # Route map
    def get_route_map(page):
        return {
            "/dashboard": lambda: dashboard_view(page, db),
            "/expense": lambda: expense_view(page, db),
            "/sale": lambda: sale_view(page, db),
            "/menu": lambda: menu_view(page, db),
            "/products": lambda: product_view(page, db),
            "/order": lambda: order_view(page, db),
            "/orders": lambda: order_view(page, db),
            "/settings": lambda: settings_view(page, db),
            "/employees": lambda: employee_view(page, db),
            "/login": lambda: login_view(page, db),
            "/": lambda: login_view(page, db),
        }

    def route_change(e: ft.RouteChangeEvent):
        print(f"Navigating to route: {e.route}")
        route = e.route

        # Clear overlays to prevent dialog stacking
        if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
            page.overlay.clear()
        page.snack_bar = None

        # Check if user is logged in
        current_user = page.client_storage.get("current_user")
        if not current_user and route != "/login":
            page.go("/login")
            return

        # Define allowed routes based on role
        user_role = db.get_user_role(current_user) if current_user else None
        allowed_routes = {
            "Admin": ["/dashboard", "/expense", "/sale", "/menu", "/products", "/order", "/orders", "/settings", "/employees", "/login"],
            "User": ["/menu", "/settings", "/login"],
        }

        # Restrict access for non-allowed routes
        if user_role and route not in allowed_routes.get(user_role, []):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Access Denied!", size=14, color=COLOR_SCHEME["background"], font_family="Roboto", weight=ft.FontWeight.W_500),
                bgcolor=COLOR_SCHEME["error"],
                padding=12,
                margin=ft.margin.only(bottom=80),
                open=True,
                duration=3000,
            )
            page.go("/menu")
            return

        # Handle invalid or root route
        route_map = get_route_map(page)
        content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=COLOR_SCHEME["error"]))

        # Build content
        content = content_builder()
        view_width = min(page.width, 360)

        # Create view
        page.views.clear()
        page.views.append(
            ft.View(
                route=route,
                controls=[
                    ft.Container(
                        content=content,
                        width=view_width,
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(horizontal=10),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                appbar=page.appbar if route != "/login" else None,
                floating_action_button=page.floating_action_button if route != "/login" else None,
                bottom_appbar=page.bottom_appbar if route != "/login" else None,
            )
        )
        print(f"View stack size: {len(page.views)}")
        print(f"AppBar status: {'visible' if page.appbar and route != '/login' else 'not visible'}")
        print(f"BottomAppBar status: {'visible' if page.bottom_appbar and route != '/login' else 'not visible'}")
        try:
            page.update()
        except Exception as e:
            print(f"Error updating page: {e}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Render error: {e}", color=COLOR_SCHEME["background"], bgcolor=COLOR_SCHEME["error"]),
                open=True,
                padding=12,
                margin=ft.margin.only(bottom=80),
            )
            page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
            print(f"View stack after pop: {len(page.views)}, Navigated to: {page.views[-1].route}")
        else:
            print("DEBUG: No more views to pop, closing app")
            page.window.close()
        page.update()

    # Set routing handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")
    print("Initial route set to /login")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ft.app(target=main, assets_dir="assets")

    loop.close()
