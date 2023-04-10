""" domible/src/domible/starterDocuments/barebones.py

the following is what I get using emmit 
(in vscode,  in a .html file, type !<tab> as the first characters in the file):

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

</body>
</html>

barebones.py will return a reference to a domible.elements.roots.Html object
which will render the above HTML when evaluated
"""

from domible.elements import Html, Head, Meta, Title, Body


def barebones(title: str = "Domible Default Title") -> Html:
    return Html([
        Head([
            Meta(charset="UTF-8"),
            Meta(**{"http-equiv":"X-UA-Compatible"}, content="IE=edge"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title(title),
        ]),
        Body()
    ])


# end of file 