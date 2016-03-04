module Index where

import Users exposing (User, noah)
import Html exposing (..)
import Html.Attributes exposing (href)


viewWelcome : User -> Html
viewWelcome user =
    "Welcome to " ++ user.name ++ "'s page!"
        |> text

view : Html
view =
    div
        []
        [ a
            [ href "blog/index.html" ]
            [ text "Click me to go to the blog!"]
        , text " This is an example index page "
        , div [] [ viewWelcome noah ]
        ]


