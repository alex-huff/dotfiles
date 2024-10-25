def focused_container_tabbed_ancestor:
    def _focused_container_tabbed_ancestor(
        current_tabbed_ancestor
    ):
        if .focused
        then
            current_tabbed_ancestor
        else
            (
                if .layout == "tabbed" and (
                    $closest_ancestor or current_tabbed_ancestor == null
                )
                then
                    .
                else
                    current_tabbed_ancestor
                end
            ) as $current_tabbed_ancestor |
                first(
                    (.nodes[], .floating_nodes[]) |
                        _focused_container_tabbed_ancestor(
                            $current_tabbed_ancestor
                        )
                )
        end
    ;
    _focused_container_tabbed_ancestor(null)
;

def last_focused_leaf:
    .focus[0] as $last_focused_child_id |
        if $last_focused_child_id == null
        then
            .
        else
            first(
                (.nodes[], .floating_nodes[]) |
                    select(.id == $last_focused_child_id) |
                    last_focused_leaf
            )
        end
;

focused_container_tabbed_ancestor |
    .nodes[$n] |
    last_focused_leaf.id // "__focused__"
