#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    DEVICESTATE(alive) = DEVICEPROPERTIES(alive);
    if (!GRAPHPROPERTIES(includeStart))
        DEVICESTATE(cycle) += GRAPHPROPERTIES(cycles);
    //@@//
}