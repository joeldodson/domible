""" domible/src/domible/starterDocuments/barebones.py """ 

from domible.elements import Html, Head, Meta, Title, Body


def basicHeadEmptyBody(title: str = "Domible Default Title") -> Html:
    """
    barebones creates an Html object with the minimal recommended elements:
    DOCTYPE, head with two meta elements and a tile, and a body with nothing
    """

    return Html(
        [
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
        ]
    )


# end of file
