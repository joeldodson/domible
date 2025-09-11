#!/usr/bin/env python
""" 
code to test Details and Summary 
"""

from domible.elements import Div, Paragraph, UnorderedList, ListItem, Details, Summary, Heading 
from domible.tools import open_html_fragment_in_browser
from domible.builders import (
    default_toggle_details_button, 
    default_expand_details_button,
    default_collapse_details_button,
)

title = "Testing Details, Summary, and Associated Buttons"

song = {
    "Title": "One of My Turns",
    "Album": "The Wall",
    "Artist": "Pink Floyd",
    "Written by": "Roger Waters",
    "Produced by": "Roger Waters, David Gilmour, Bob Ezrin",
}
lyrics = [
"Day after day, love turns grey ",
"Like the skin of a dying man",
"And night after night, we pretend it's all right",
"But I have grown older and you have grown colder",
"And nothing is very much fun anymore",
"And I can feel one of my turns coming on",
"I feel cold as a razor blade, tight as a tourniquet",
"Dry as a funeral drum",
"Run to the bedroom, in the suitcase on the left you'll find my favourite axe",
"Don't look so frightened, this is just a passing phase one of my bad days",
"Would you like to watch TV? Or get between the sheets?",
"Or contemplate the silent freeway?",
"Would you like something to eat?",
"Would you like to learn to fly?",
"Would you, would you like to see me try?",
"Oh! Oh, no",
"Would you like to call the cops?",
"Do you think it's time I stopped?",
"Why are you running away?",
]

song_html= UnorderedList(
    [ListItem(f"{k}: {v}") for k,v in song.items()]
)

lyrics_html = [Paragraph(line) for line in lyrics]

html_fragment = Div(
    [
        Heading(1, title),
        default_expand_details_button(),
        default_collapse_details_button(),
        default_toggle_details_button(),
        Details(
            Summary(Heading(2, "A Treat from The Wall")),
            [
                Details(Summary("Song Metadata"), song_html),
                Details(Summary("Lyrics"), lyrics_html),
            ],
        ),
    ]
)

open_html_fragment_in_browser(html_fragment, title)


"""
in case I want to add another song...

I've got a little black book with my poems in
Got a bag with a toothbrush and a comb in
When I'm a good dog
They sometimes throw me the bone in
I got elastic bands keepin' my shoes on
Got those swollen hand blues
I got thirteen channels of shit on the TV to choose from
I've got electric light
And I've got second sight
I got amazing powers of observation
And that is how I know, when I try to get through
On the telephone to you, there'll be nobody home
I've got the obligatory Hendrix perm and the inevitable pinhole burns
Now all down the front of my favorite satin shirt
I've got nicotine stains on my fingers, I've got a silver spoon on a chain
Got a grand piano to prop up my mortal remains
I've got wild staring eyes
And I've got a strong urge to fly, but I got nowhere to fly to
♪
Ooh, babe when I pick up the phone there is still nobody home
I've got a pair of Gohills boots and I got fading roots
"""
