#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    if (!DEVICESTATE(begin))
    {
        uint8_t previousGeneration = DEVICESTATE(generation) % 2;

        DEVICESTATE(generation)
        ++;

        // rules of the game
        if (DEVICESTATE(alive) && (DEVICESTATE(liveNeighbours[previousGeneration]) == 2 || DEVICESTATE(liveNeighbours[previousGeneration]) == 3))
            DEVICESTATE(alive) = 1;
        else if (!DEVICESTATE(alive) && DEVICESTATE(liveNeighbours[previousGeneration]) == 3)
            DEVICESTATE(alive) = 1;
        else
            DEVICESTATE(alive) = 0;

        DEVICESTATE(liveNeighbours[previousGeneration]) = 0;
        DEVICESTATE(neighbourUpdates[previousGeneration]) = 0;
    }
    else
    {
        DEVICESTATE(begin) = 0;
    }

    if (DEVICESTATE(generation) == DEVICESTATE(cycle) || DEVICESTATE(generation) == GRAPHPROPERTIES(end))
    {
        DEVICESTATE(btimer) = tinselCycleCount() - DEVICESTATE(start);
        DEVICESTATE(balive) = DEVICESTATE(alive);
        DEVICESTATE(bgeneration) = DEVICESTATE(generation);
        DEVICESTATE(cycle) += GRAPHPROPERTIES(cycles);
        DEVICESTATE(buffer) = DEVICESTATE(alive) || DEVICESTATE(generation) == GRAPHPROPERTIES(end); // send if we're alive or if we're on the last generation
        //DEVICESTATE(buffer) = 1;
    }

    MSG(alive) = DEVICESTATE(alive);
    MSG(generation) = DEVICESTATE(generation);
    //@@//
}