#include <hiredis.h>

void init_redis();
void set_map_key(const char * map_name, const char* key_name, const char* key_value);