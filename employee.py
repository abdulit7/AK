import flet as ft

def employee_view(page: ft.Page, db: 'Database'):
    COLOR_SCHEME = {
        "primary": ft.Colors.BLUE_700,
        "accent": ft.Colors.AMBER_600,
        "background": ft.Colors.WHITE,
        "text": ft.Colors.BLACK87,
        "error": ft.Colors.RED_600,
        "success": ft.Colors.GREEN_600
    }

    def show_snack_bar(message, success=True):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, size=14, color=COLOR_SCHEME["background"], font_family="Roboto", weight=ft.FontWeight.W_500),
            bgcolor=COLOR_SCHEME["success" if success else "error"],
            padding=12,
            margin=ft.margin.only(bottom=80),
            open=True,
            duration=3000,
        )
        page.update()

    # User Management
    def open_add_user_dialog(e):
        username_field = ft.TextField(label="Username", width=200, text_style=ft.TextStyle(font_family="Roboto"))
        password_field = ft.TextField(label="Password", password=True, width=200, text_style=ft.TextStyle(font_family="Roboto"))
        role_field = ft.Dropdown(
            label="Role",
            options=[ft.dropdown.Option("Admin"), ft.dropdown.Option("User")],
            width=200,
            text_style=ft.TextStyle(font_family="Roboto"),
        )

        def add_user(e):
            try:
                db.add_user(username_field.value, password_field.value, role_field.value)
                show_snack_bar(f"User {username_field.value} added")
                refresh_users()
                page.overlay.clear()
            except Exception as ex:
                show_snack_bar(str(ex), False)
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add User", font_family="Roboto"),
            content=ft.Column([username_field, password_field, role_field], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.overlay.clear()),
                ft.ElevatedButton("Add", on_click=add_user, style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"])),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def open_edit_user_dialog(user):
        username_field = ft.TextField(label="Username", value=user["username"], width=200, text_style=ft.TextStyle(font_family="Roboto"))
        password_field = ft.TextField(label="Password", value=user["password"], password=True, width=200, text_style=ft.TextStyle(font_family="Roboto"))
        role_field = ft.Dropdown(
            label="Role",
            value=user["role"],
            options=[ft.dropdown.Option("Admin"), ft.dropdown.Option("User")],
            width=200,
            text_style=ft.TextStyle(font_family="Roboto"),
        )

        def edit_user(e):
            try:
                db.update_user(user["id"], username_field.value, password_field.value, role_field.value)
                show_snack_bar(f"User {username_field.value} updated")
                refresh_users()
                page.overlay.clear()
            except Exception as ex:
                show_snack_bar(str(ex), False)
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit User", font_family="Roboto"),
            content=ft.Column([username_field, password_field, role_field], spacing=10, tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.overlay.clear()),
                ft.ElevatedButton("Update", on_click=edit_user, style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"])),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def delete_user(user_id, username):
        try:
            db.delete_user(user_id)
            show_snack_bar(f"User {username} deleted")
            refresh_users()
        except Exception as ex:
            show_snack_bar(str(ex), False)
        page.update()

    def refresh_users():
        users = db.get_all_users()
        user_rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(user["username"], font_family="Roboto")),
                ft.DataCell(ft.Text(user["role"], font_family="Roboto")),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=COLOR_SCHEME["primary"], on_click=lambda e, u=user: open_edit_user_dialog(u)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=COLOR_SCHEME["error"], on_click=lambda e, u=user: delete_user(u["id"], u["username"])),
                ])),
            ]) for user in users
        ]
        user_table.rows = user_rows
        page.update()

    user_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name", font_family="Roboto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Role", font_family="Roboto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Action", font_family="Roboto", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_300),
        heading_row_color=ft.Colors.GREY_200,
    )

    # Waiter Management
    def open_add_waiter_dialog(e):
        name_field = ft.TextField(label="Waiter Name", width=200, text_style=ft.TextStyle(font_family="Roboto"))

        def add_waiter(e):
            try:
                db.add_waiter(name_field.value)
                show_snack_bar(f"Waiter {name_field.value} added")
                refresh_waiters()
                page.overlay.clear()
            except Exception as ex:
                show_snack_bar(str(ex), False)
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Waiter", font_family="Roboto"),
            content=name_field,
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.overlay.clear()),
                ft.ElevatedButton("Add", on_click=add_waiter, style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"])),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def open_edit_waiter_dialog(waiter):
        name_field = ft.TextField(label="Waiter Name", value=waiter["name"], width=200, text_style=ft.TextStyle(font_family="Roboto"))

        def edit_waiter(e):
            try:
                db.update_waiter(waiter["id"], name_field.value)
                show_snack_bar(f"Waiter {name_field.value} updated")
                refresh_waiters()
                page.overlay.clear()
            except Exception as ex:
                show_snack_bar(str(ex), False)
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Waiter", font_family="Roboto"),
            content=name_field,
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.overlay.clear()),
                ft.ElevatedButton("Update", on_click=edit_waiter, style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"])),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def delete_waiter(waiter_id, name):
        try:
            db.delete_waiter(waiter_id)
            show_snack_bar(f"Waiter {name} deleted")
            refresh_waiters()
        except Exception as ex:
            show_snack_bar(str(ex), False)
        page.update()

    def refresh_waiters():
        waiters = db.get_all_waiters()
        waiter_rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(waiter["name"], font_family="Roboto")),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=COLOR_SCHEME["primary"], on_click=lambda e, w=waiter: open_edit_waiter_dialog(w)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=COLOR_SCHEME["error"], on_click=lambda e, w=waiter: delete_waiter(w["id"], w["name"])),
                ])),
            ]) for waiter in waiters
        ]
        waiter_table.rows = waiter_rows
        page.update()

    waiter_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Waiter Name", font_family="Roboto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Actions", font_family="Roboto", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_300),
        heading_row_color=ft.Colors.GREY_200,
    )

    # Initialize tables
    refresh_users()
    refresh_waiters()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Employee Management", size=20, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"], font_family="Roboto"),
                ft.Text("Users", size=16, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"], font_family="Roboto"),
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.ADD), ft.Text("Add User")]),
                    style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"]),
                    on_click=open_add_user_dialog,
                ),
                user_table,
                ft.Text("Waiters", size=16, weight=ft.FontWeight.BOLD, color=COLOR_SCHEME["text"], font_family="Roboto"),
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.ADD), ft.Text("Add Waiter")]),
                    style=ft.ButtonStyle(bgcolor=COLOR_SCHEME["primary"], color=COLOR_SCHEME["background"]),
                    on_click=open_add_waiter_dialog,
                ),
                waiter_table,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=COLOR_SCHEME["background"],
        padding=10,
        border_radius=8,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.GREY_300),
    )