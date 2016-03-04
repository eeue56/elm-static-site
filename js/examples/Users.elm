module Users where

type alias User =
    { name: String
    , location: String
    , age: Int
    }

noah : User
noah =
    { name = "Noah"
    , location = "Wales"
    , age = 23
    }

dave : User
dave =
    { name = "Dave"
    , location = "Scotland"
    , age = 33
    }

users =
    [ noah
    , dave
    ]
