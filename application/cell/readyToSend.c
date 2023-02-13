#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    if (DEVICESTATE(begin))
    {
        RTS(sender);
        return 0;
    }
    if (DEVICESTATE(buffer))
    {
        RTSSUP();
        return 0;
    }
    if (DEVICESTATE(generation) < GRAPHPROPERTIES(end) && (DEVICESTATE(neighbourUpdates[DEVICESTATE(generation) % 2]) >= 8))
    {
        RTS(sender);
    }
    //@@//
}