#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    DEVICESTATE(neighbourUpdates[MSG(generation) % 2])
    ++;
    DEVICESTATE(liveNeighbours[MSG(generation) % 2]) += MSG(alive);
    //@@//
}