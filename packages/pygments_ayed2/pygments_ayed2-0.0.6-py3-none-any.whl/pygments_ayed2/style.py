from pygments.style import Style
from pygments.token import Name, Punctuation, Token


class Ayed2Style(Style):
    name = "ayed2"

    background_color = "#262220"
    highlight_color = "#424032"

    line_number_color = "#4e4e4e"
    line_number_special_color = "#8f9494"

    styles = {
        Token.Keyword.Type:     'ansibrightblue',
        Token.String:           'ansibrightblue',
        Token.Number:           'ansibrightcyan',
        Token.Operator:         'ansibrightred',
        Token.Keyword:          'ansibrightgreen',
        Token.Name:             'ansiwhite',
        Token.Punctuation:      'ansicyan',
        Punctuation.Assignment: 'ansibrightyellow',
        Name.NamedLiteral:      'ansimagenta',
        Name.Builtin:           'ansibrightmagenta',
    }
