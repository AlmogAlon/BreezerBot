#include <hiredis.h>
#include <iostream>

using namespace std;

redisContext *c = NULL;

void init_redis() {
    struct timeval timeout = { 1, 500000 };

    if (c == NULL) {
        c = redisConnectWithTimeout("127.0.0.1", 6379, timeout);
    }

    if (c == NULL || c->err) {
        if (c) {
            cout << "Connection error: " << c->errstr << endl;
            redisFree(c);
        } else {
            cout << "Connection error: can't allocate redis context" << endl;
        }
        exit(1);
    }

    redisReply *reply;
    reply = (redisReply *)redisCommand(c,"PING");
    freeReplyObject(reply);
}

void set_map_key(const char * map_name, const char* key_name, const char* key_value) {
    redisReply *reply;
    reply = (redisReply *)redisCommand(c, "HMSET %s %s %s", map_name, key_name, key_value);
    freeReplyObject(reply);
}