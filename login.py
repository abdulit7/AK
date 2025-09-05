import flet as ft

def login_view(page: ft.Page, db: 'Database'):
    page.title = "Login"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 0
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

    COLOR_SCHEME = {
        "primary": ft.Colors.BLUE_700,
        "accent": ft.Colors.AMBER_600,
        "background": ft.Colors.WHITE,
        "text": ft.Colors.BLACK87,
        "error": ft.Colors.RED_600,
        "success": ft.Colors.GREEN_600
    }

    username_field = ft.TextField(
        label="Username",
        width=300,
        text_style=ft.TextStyle(size=16, color=COLOR_SCHEME["text"], font_family="Roboto", weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(size=14, color=ft.Colors.GREY_600, font_family="Roboto"),
        border_color=ft.Colors.GREY_300,
        focused_border_color=COLOR_SCHEME["primary"],
        filled=True,
        border_radius=8,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        text_style=ft.TextStyle(size=16, color=COLOR_SCHEME["text"], font_family="Roboto", weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(size=14, color=ft.Colors.GREY_600, font_family="Roboto"),
        border_color=ft.Colors.GREY_300,
        focused_border_color=COLOR_SCHEME["primary"],
        filled=True,
        border_radius=8,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )

    def login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()
        user = db.authenticate_user(username, password)
        if user:
            page.client_storage.set("current_user", username)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Welcome, {username}!", size=14, color=COLOR_SCHEME["background"], font_family="Roboto", weight=ft.FontWeight.W_500),
                bgcolor=COLOR_SCHEME["success"],
                padding=12,
                margin=ft.margin.only(bottom=80),
                open=True,
                duration=3000,
            )
            page.go("/dashboard" if user["role"] == "Admin" else "/menu")
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid credentials!", size=14, color=COLOR_SCHEME["background"], font_family="Roboto", weight=ft.FontWeight.W_500),
                bgcolor=COLOR_SCHEME["error"],
                padding=12,
                margin=ft.margin.only(bottom=80),
                open=True,
                duration=3000,
            )
        page.update()

    login_content = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Login",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_SCHEME["text"],
                    font_family="Roboto",
                    text_align=ft.TextAlign.CENTER,
                ),
                username_field,
                password_field,
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGIN, color=COLOR_SCHEME["primary"], size=20),
                            ft.Text("Login", color=COLOR_SCHEME["primary"], weight=ft.FontWeight.BOLD, size=16, font_family="Roboto"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=COLOR_SCHEME["background"],
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        elevation={"pressed": 2, "": 4},
                    ),
                    width=240,
                    on_click=login,
                    opacity=1.0,
                    on_hover=lambda e: setattr(e.control, 'opacity', 0.9 if e.data == "true" else 1.0) or e.control.update(),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=page.width,
        bgcolor=COLOR_SCHEME["background"],
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.GREY_300),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return login_content