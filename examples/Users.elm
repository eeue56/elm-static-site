module Users where

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
