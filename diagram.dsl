# DEFINITIONS

[a] := "Off State"                   # Inside rectangle
(b) := "On State"                    # Inside rounded rectangle
/c/ := "Transition State"            # Inside Parallelogram


# Rules

# Horizontal layout
a -> b -> c
"new state" -> b  # This affects the layout since it introduces branch


# Vertical layout
a |> b |> c
"another state" |> a
"state" |> c
