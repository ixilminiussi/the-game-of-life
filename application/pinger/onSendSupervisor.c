#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    MSG(ping) = 1;
    MSG(alive) = 0;
    MSG(generation) = 0;
    MSG(x) = 0;
    MSG(y) = 0;

    DEVICESTATE(send) = 0;
    //@@//
}