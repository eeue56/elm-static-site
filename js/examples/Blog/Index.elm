module Blog.Index where

import Users exposing (User, users)
import Html exposing (..)
import String


viewBloggerInfo : User -> Html
viewBloggerInfo user =
    let
        words =
            String.join ""
                [ user.name
                , " is currently in "
                , user.location
                , " and is "
                , toString user.age
                , " years old!"
                ]
    in
        div
            []
            [ text words]

view =
    div
        []
        (List.map viewBloggerInfo users)
