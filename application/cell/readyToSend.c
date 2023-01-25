#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    if (DEVICESTATE(begin))
    {
        RTS(neighbourSend);
        return 0;
    }
    if (DEVICESTATE(buffer))
    {
        RTS(aggregatorSend);
        return 0;
    }
    if (DEVICESTATE(generation) < GRAPHPROPERTIES(end) && (DEVICESTATE(neighbourUpdates[DEVICESTATE(generation) % 2]) >= 8))
    {
        RTS(neighbourSend);
    }
    //@@//
}