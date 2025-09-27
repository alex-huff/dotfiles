def focused_container_target_ancestor:
    def _focused_container_target_ancestor(
        current_target_ancestor
    ):
        if .focused
        then
            current_target_ancestor
        else
            (
                .layout == $target_layout
                and .type != "root"
                and (.nodes | length) > 1
                and ($closest_ancestor or current_target_ancestor[0] == null)
            ) as $is_valid_ancestor |
            first(
                . as $node |
                ([.nodes, false], [.floating_nodes, true]) |
                .[0] as $children |
                .[1] as $is_floating_child |
                range($children | length) |
                . as $index |
                $children[.] |
                _focused_container_target_ancestor(
                    if $is_floating_child
                    then
                        [null, null]
                    elif $is_valid_ancestor
                    then
                        [$node, $index]
                    else
                        current_target_ancestor
                    end
                )
            )
        end
    ;
    _focused_container_target_ancestor([null, null])
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

focused_container_target_ancestor as $target |
$target[0] |
.nodes[
    if $relative
    then
        ($target[1] + $n) as $absolute_index |
        if $absolute_index >= 0 then $absolute_index else 0 end
    else
        $n
    end
] |
last_focused_leaf.id // "__focused__"
