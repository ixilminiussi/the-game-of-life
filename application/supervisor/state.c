#include <definitions.h>
#include <code.c>
//@@//
uint8_t failed = false;
uint32_t finishedCells = 0;

std::chrono::steady_clock::time_point startTime;

FILE *resultFile;
//@@//

inline uint8_t SUPSTATE(val) {
    return val;
}

inline uint32_t SUPSTATE(val) {
    return val;
}