# DEFINITIONS

a := "Off State"                   # Inside rectangle
b := "On State"                    # Inside rounded rectangle
c := "Transition State"            # Inside Parallelogram


# Rules

# Horizontal layout
#(a) -> [b] -> /c/
["next state"] -> [c] -> ["pandey"]  # This affects the layout since it introduces branch

#("new state") -> /b/  # This affects the layout since it introduces branch
#
#/"curr state"/ -> /"man"/
#
#
## Vertical layout
#(a) -> (b) <- [c]
#["another state"] -> ("bibek")
