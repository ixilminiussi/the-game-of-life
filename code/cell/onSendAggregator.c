#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    MSG(alive) = DEVICESTATE(balive);
    MSG(generation) = DEVICESTATE(bgeneration);
    MSG(x) = DEVICEPROPERTIES(x);
    MSG(y) = DEVICEPROPERTIES(y);
    MSG(ping) = 0;
    DEVICESTATE(buffer) = 0;

    if (DEVICESTATE(generation) == GRAPHPROPERTIES(end))
    {
        DEVICESTATE(generation)
        ++;
    }
    //@@//
}