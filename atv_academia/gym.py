import flet as ft


# Paleta de cores do app
class Cores:
    FUNDO = "#0F0E17"
    SUPERFICIE = "#1A1826"
    SUPERFICIE_CLARA = "#242236"
    PRIMARIA = "#7F5AF0"
    PRIMARIA_ESCURA = "#5C3FC9"
    SUCESSO = "#2CB67D"
    PERIGO = "#EF4565"
    TEXTO = "#FFFFFE"
    TEXTO_SECUNDARIO = "#A7A9BE"


def main(page: ft.Page):
    page.title = "GymTrack"
    page.padding = 0
    page.bgcolor = Cores.FUNDO
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 480
    page.window.height = 850
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    # ---------- Estado ----------
    total = 0
    concluidos = 0

    # ---------- Campos de entrada ----------
    def campo_estilizado(label, largura, icone, tipo=None):
        return ft.TextField(
            label=label,
            width=largura,
            prefix_icon=icone,
            keyboard_type=tipo,
            border_radius=12,
            filled=True,
            bgcolor=Cores.SUPERFICIE_CLARA,
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=Cores.PRIMARIA,
            label_style=ft.TextStyle(color=Cores.TEXTO_SECUNDARIO),
            text_style=ft.TextStyle(color=Cores.TEXTO),
            cursor_color=Cores.PRIMARIA,
        )

    nome = campo_estilizado("Nome do exercício", 250, ft.Icons.FITNESS_CENTER)
    series = campo_estilizado("Séries", 110, ft.Icons.REPEAT, ft.KeyboardType.NUMBER)
    repeticoes = campo_estilizado("Repetições", 130, ft.Icons.NUMBERS, ft.KeyboardType.NUMBER)

    lista_exercicios = ft.Column(spacing=12)

    # ---------- Cabeçalho de progresso ----------
    texto_progresso = ft.Text(
        "0 de 0 concluídos",
        size=13,
        color=Cores.TEXTO_SECUNDARIO,
    )

    barra_progresso = ft.ProgressBar(
        value=0,
        width=None,
        height=10,
        border_radius=10,
        color=Cores.SUCESSO,
        bgcolor=Cores.SUPERFICIE_CLARA,
    )

    estado_vazio = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.SPORTS_GYMNASTICS, size=60, color=Cores.TEXTO_SECUNDARIO),
                ft.Text(
                    "Nenhum exercício ainda",
                    size=16,
                    color=Cores.TEXTO_SECUNDARIO,
                    weight=ft.FontWeight.W_600,
                ),
                ft.Text(
                    "Adicione seu primeiro exercício acima 👆",
                    size=12,
                    color=Cores.TEXTO_SECUNDARIO,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        alignment=ft.Alignment.CENTER,
        padding=30,
    )

    # ---------- Funções ----------
    def atualizar_contador():
        texto_progresso.value = f"{concluidos} de {total} concluídos"
        barra_progresso.value = (concluidos / total) if total > 0 else 0
        estado_vazio.visible = total == 0
        page.update()

    def concluir(e):
        nonlocal concluidos

        botao = e.control
        card = botao.data["card"]
        badge = botao.data["badge"]
        titulo_texto = botao.data["titulo"]

        if botao.data["feito"]:
            return  # já concluído, ignora novos cliques

        botao.data["feito"] = True
        botao.text = "Concluído"
        botao.icon = ft.Icons.CHECK_CIRCLE
        botao.bgcolor = Cores.SUCESSO
        botao.disabled = True

        card.bgcolor = "#17251F"
        card.border = ft.Border.all(1, Cores.SUCESSO)
        titulo_texto.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
        badge.visible = True

        concluidos += 1
        atualizar_contador()

    def excluir(e):
        nonlocal total, concluidos

        card = e.control.data["card"]
        if e.control.data["feito"]:
            concluidos -= 1

        card.animate_opacity = 250
        lista_exercicios.controls.remove(card)
        total -= 1

        atualizar_contador()

    def campos_invalidos():
        return nome.value.strip() == "" or series.value.strip() == "" or repeticoes.value.strip() == ""

    def mostrar_aviso(mensagem, icone, cor):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Row(
                    [ft.Icon(icone, color=ft.Colors.WHITE), ft.Text(mensagem, color=ft.Colors.WHITE)]
                ),
                bgcolor=cor,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )

    def adicionar(e):
        nonlocal total

        if campos_invalidos():
            mostrar_aviso("Preencha todos os campos!", ft.Icons.WARNING_ROUNDED, Cores.PERIGO)
            return

        titulo_texto = ft.Text(
            nome.value,
            size=17,
            weight=ft.FontWeight.BOLD,
            color=Cores.TEXTO,
        )

        badge_concluido = ft.Icon(
            ft.Icons.CHECK_CIRCLE, color=Cores.SUCESSO, size=18, visible=False
        )

        botao_concluir = ft.ElevatedButton(
            "Concluir",
            icon=ft.Icons.CHECK,
            bgcolor=Cores.PRIMARIA,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=concluir,
            data={"feito": False},
        )

        botao_excluir = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=Cores.PERIGO,
            tooltip="Remover",
            on_click=excluir,
        )

        card = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.FITNESS_CENTER, color=Cores.PRIMARIA, size=22),
                        bgcolor=Cores.SUPERFICIE_CLARA,
                        border_radius=50,
                        padding=10,
                    ),
                    ft.Column(
                        [
                            ft.Row([titulo_texto, badge_concluido], spacing=6),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.REPEAT, size=14, color=Cores.TEXTO_SECUNDARIO),
                                    ft.Text(
                                        f"{series.value} séries  ×  {repeticoes.value} repetições",
                                        size=13,
                                        color=Cores.TEXTO_SECUNDARIO,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        expand=True,
                        spacing=4,
                    ),
                    ft.Column([botao_concluir, botao_excluir], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            border_radius=16,
            bgcolor=Cores.SUPERFICIE,
            border=ft.Border.all(1, "#2E2C42"),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            animate_opacity=300,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.25, "#000000"),
                offset=ft.Offset(0, 4),
            ),
        )

        botao_concluir.data.update({"card": card, "badge": badge_concluido, "titulo": titulo_texto})
        botao_excluir.data = {"card": card, "feito": False}
  
        botao_concluir.data["feito_ref"] = botao_excluir.data

        def concluir_sincronizado(e, be=botao_excluir):
            concluir(e)
            be.data["feito"] = True

        botao_concluir.on_click = concluir_sincronizado

        lista_exercicios.controls.append(card)

        total += 1
        nome.value = ""
        series.value = ""
        repeticoes.value = ""
        nome.focus()

        atualizar_contador()

    cabecalho = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SPORTS_GYMNASTICS, color=ft.Colors.WHITE, size=34),
                        ft.Column(
                            [
                                ft.Text("GymTrack", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text(
                                    "Organize e acompanhe seus treinos 💪",
                                    size=13,
                                    color=ft.Colors.with_opacity(0.85, "#FFFFFF"),
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=12,
                ),
            ]
        ),
        padding=ft.Padding.only(left=24, right=24, top=30, bottom=24),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[Cores.PRIMARIA_ESCURA, Cores.PRIMARIA],
        ),
        border_radius=ft.BorderRadius.only(bottom_left=28, bottom_right=28),
    )

    cartao_formulario = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=Cores.PRIMARIA), ft.Text(
                        "Novo exercício", size=18, weight=ft.FontWeight.BOLD, color=Cores.TEXTO
                    )],
                    spacing=8,
                ),
                ft.Row([nome], wrap=True),
                ft.Row([series, repeticoes], spacing=12, wrap=True),
                ft.ElevatedButton(
                    "Adicionar exercício",
                    icon=ft.Icons.ADD,
                    bgcolor=Cores.PRIMARIA,
                    color=ft.Colors.WHITE,
                    height=48,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    ),
                    on_click=adicionar,
                    width=400,
                ),
            ],
            spacing=14,
        ),
        padding=20,
        margin=ft.Margin.only(left=20, right=20, top=-20),
        bgcolor=Cores.SUPERFICIE,
        border_radius=18,
        shadow=ft.BoxShadow(
            blur_radius=16,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 6),
        ),
    )

    cartao_progresso = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [ft.Icon(ft.Icons.TRACK_CHANGES, color=Cores.SUCESSO, size=18), ft.Text(
                                "Progresso do treino", size=14, weight=ft.FontWeight.W_600, color=Cores.TEXTO
                            )],
                            spacing=6,
                        ),
                        texto_progresso,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                barra_progresso,
            ],
            spacing=10,
        ),
        padding=18,
        margin=ft.Margin.symmetric(horizontal=20, vertical=16),
        bgcolor=Cores.SUPERFICIE,
        border_radius=16,
        border=ft.Border.all(1, "#2E2C42"),
    )

    page.add(
        cabecalho,
        cartao_formulario,
        cartao_progresso,
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Seus exercícios", size=16, weight=ft.FontWeight.BOLD, color=Cores.TEXTO),
                    estado_vazio,
                    lista_exercicios,
                ],
                spacing=12,
            ),
            padding=ft.Padding.only(left=20, right=20, bottom=30),
        ),
    )

    atualizar_contador()


ft.run(main)