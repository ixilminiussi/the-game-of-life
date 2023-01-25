#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    DEVICESTATE(alive) = DEVICEPROPERTIES(alive);
    DEVICESTATE(start) = tinselCycleCount();
    if (!GRAPHPROPERTIES(includeStart))
        DEVICESTATE(cycle) += GRAPHPROPERTIES(cycles);
    //@@//
}