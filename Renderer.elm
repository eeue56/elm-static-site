
module Renderer where
import Native.Renderer
import Index
import Users
import Blog.Index


port index : String
port index =
    Index.view
        |> Native.Renderer.toHtml


port users : String
port users =
    Users.view
        |> Native.Renderer.toHtml


port blogindex : String
port blogindex =
    Blog.Index.view
        |> Native.Renderer.toHtml

