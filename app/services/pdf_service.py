from io import BytesIO

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    PageBreak
)

from reportlab.lib import colors

from app.services.card_service import CardService


class PDFService:

    @classmethod
    def create_card_table(
        cls,
        card_data
    ):

        card = card_data["numbers"]

        card_id = card_data["id"]

        data = [

            [
                f"CARTELA #{card_id}",
                "",
                "",
                "",
                ""
            ],

            ["B", "I", "N", "G", "O"]
        ]

        for row in range(5):

            row_data = []

            for column in range(5):

                row_data.append(
                    card[column][row]
                )

            data.append(row_data)

        table = Table(
            data,
            colWidths=45,
            rowHeights=35
        )

        table.setStyle(
            TableStyle([

                (
                    "SPAN",
                    (0, 0),
                    (4, 0)
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (4, 0),
                    colors.black
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (4, 0),
                    colors.white
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (4, 0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (4, 0),
                    12
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    colors.darkred
                ),

                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, 1),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (-1, 1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    14
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BOTTOMPADDING",
                    (0, 1),
                    (-1, 1),
                    10
                ),

                (
                    "BACKGROUND",
                    (2, 4),
                    (2, 4),
                    colors.gold
                )
            ])
        )

        return table

    @classmethod
    def generate_cards_pdf(
        cls,
        quantity: int
    ):

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        elements = []

        cards = CardService.generate_unique_cards(
            quantity
        )

        for page_start in range(0, quantity, 4):

            current_cards = cards[
                page_start:page_start + 4
            ]

            card_tables = []

            for card in current_cards:

                card_tables.append(
                    cls.create_card_table(card)
                )

            rows = []

            for i in range(0, len(card_tables), 2):

                left = card_tables[i]

                right = (
                    card_tables[i + 1]
                    if i + 1 < len(card_tables)
                    else Spacer(1, 1)
                )

                rows.append([left, right])

            page_table = Table(
                rows,
                colWidths=[260, 260],
                rowHeights=[260] * len(rows)
            )

            page_table.setStyle(
                TableStyle([

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    )
                ])
            )

            elements.append(page_table)

            if page_start + 4 < quantity:

                elements.append(
                    PageBreak()
                )

        document.build(elements)

        buffer.seek(0)

        return buffer