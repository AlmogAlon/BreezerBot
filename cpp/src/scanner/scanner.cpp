#include <tins/tins.h>
#include <iostream>
#include <set>
#include <string>
#include <utils/redis_tools.h>
#include <mutex>
#include <thread>
#include <chrono>
#include <sys/time.h>


using namespace std;
using namespace Tins;

long long current_timestamp() {
    struct timeval te; 
    gettimeofday(&te, NULL); // get current time
    long long milliseconds = te.tv_sec*1000LL + te.tv_usec/1000; // calculate milliseconds
    // printf("milliseconds: %lld\n", milliseconds);
    return milliseconds;
}

class SingleNetwork {
private:
    double rssi_sum;
    int count;
    long long timestamp;

public:
    SingleNetwork() : rssi_sum(0), count(0) {}

    void add_rssi(double rssi) {
        rssi_sum += rssi;
        count ++;
        timestamp = current_timestamp();
    }

    long long get_timestamp() {
        return timestamp;
    }

    double get_rssi() {
        if (count == 0) {
            return -100;
        }
        return rssi_sum / count;
    }

    int get_count() {
        return count;
    }

    void reset() {
        rssi_sum = 0;
        count = 0;
    }
};

class BeaconSniffer {
public:
    void run(const string& iface);

    void start_dump_thread();
    void run_dump_thread();
private:
    mutex data_mutex;
    thread dump_thread;

    typedef Dot11::address_type address_type;
    typedef map<std::string, SingleNetwork> data_type;
 
    bool callback(PDU& pdu);
     
    data_type data;
};

void BeaconSniffer::run_dump_thread() {
    cout << "run_query_thread" << endl;
    while(true) {
        data_mutex.lock();
        data_type::iterator it;
        for ( it = data.begin(); it != data.end(); it++ )
        {
            if (it->second.get_count() != 0) {
                char tmp[100];
                snprintf(tmp, 100, "%lf,%lld", it->second.get_rssi(), it->second.get_timestamp());
                set_map_key("scanner", it->first.c_str(), tmp);
                it->second.reset();
            }
        }
        data_mutex.unlock();
        this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
    cout << "Stopping run_query_thread" << endl;
}

void dump_thread_func(BeaconSniffer* handler) {
    handler->run_dump_thread();
}

void BeaconSniffer::start_dump_thread() {
    dump_thread = thread(dump_thread_func, this);
}

void BeaconSniffer::run(const std::string& iface) {
    SnifferConfiguration config;
    config.set_promisc_mode(true);
    config.set_filter("type mgt subtype beacon");
    config.set_rfmon(true);
    Sniffer sniffer(iface, config);
    sniffer.sniff_loop(make_sniffer_handler(this, &BeaconSniffer::callback));
}
 
bool BeaconSniffer::callback(PDU& pdu) {
    const Dot11Beacon& beacon = pdu.rfind_pdu<Dot11Beacon>();
    const RadioTap* tap = pdu.find_pdu<RadioTap>();
    if ((!beacon.from_ds() && !beacon.to_ds()) && (tap != NULL)) {
        try {
            double rssi = tap->dbm_signal();

            string addr = beacon.addr2().to_string();
            string ssid = beacon.ssid();

            string key = addr + "-" + ssid;

            data_mutex.lock();
            data_type::iterator it = data.find(key);
            if (it == data.end()) {
                data[key] = SingleNetwork();
            } 

            data[key].add_rssi(rssi);
            data_mutex.unlock();
        } catch (runtime_error&) {
            // No ssid, just ignore it.
        }
    }
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: " <<* argv << " <interface>" << endl;
        return 1;
    }

    init_redis();
    string interface = argv[1];
    BeaconSniffer sniffer;
    sniffer.start_dump_thread();
    sniffer.run(interface);
}