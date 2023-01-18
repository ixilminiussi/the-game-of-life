#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    if (DEVICESTATE(send))
    {
        RTSSUP();
    }
    //@@//
}