#include <definitions.h>
#include <sharedCode.c>
//@@//
uint32_t cellCount;
uint32_t end;
uint32_t cycles;
uint8_t includeStart;
//@@//

inline uint8_t DEVICEPROPERTIES(val)
{
    return val;
}

inline uint32_t DEVICEPROPERTIES(val)
{
    return val;
}