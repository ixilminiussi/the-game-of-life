#include <definitions.h>
#include <state.c>
#include <properties.c>

void main()
{
    //@@//
    if (!SUPSTATE(failed))
    {
        if (MSG(ping))
        {
            SUPSTATE(startTime) = std::chrono::steady_clock::now();
        }
        else
        {
            fprintf(SUPSTATE(resultFile), "%d,%d,%d,%d\n", MSG(x), MSG(y), MSG(generation), MSG(alive));
            if (MSG(generation) == GRAPHPROPERTIES(end))
            {
                // std::chrono::duration<float> duration;
                // duration = std::chrono::steady_clock::now() - SUPSTATE(startTime);

                SUPSTATE(finishedCells)
                ++;
                // fprintf(SUPSTATE(resultFile), "%d,%d,%d,%d,%d\n", MSG(x), MSG(y), MSG(generation), MSG(alive), std::chrono::duration_cast<std::chrono::milliseconds>(duration).count());
                if (SUPSTATE(finishedCells) >= GRAPHPROPERTIES(cellCount))
                {
                    Super::stop_application();
                }
            }
        }
    }
    //@@//
}