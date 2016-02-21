module Users where

import Html exposing (text)

view = text ""


type alias User =
    { name: String
    , location: String
    , age: Int
    }

noah : User
noah =
    { name = "Noah"
    , location = "N/A"
    , age = 23
    }
