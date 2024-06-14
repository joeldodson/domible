""" domible/src/domible/starterDocuments/barebones.py """

from domible.elements import Html, Head, Meta, Title, Body


def basic_head_empty_body(title: str = "Domible Default Title", lang: str = "en") -> Html:
    """
    barebones creates an Html object with the minimal recommended elements:
    DOCTYPE, head with two meta elements and a tile, and a body with nothing
    """

    return Html(
        lang=lang,
        contents=[
            Head(
                [
                    Meta(charset="UTF-8"),
                    Meta(**{"http-equiv": "X-UA-Compatible"}, content="IE=edge"),
                    Meta(
                        name="viewport", content="width=device-width, initial-scale=1.0"
                    ),
                    Title(title),
                ]
            ),
            Body(),
        ],
    )


# end of file
