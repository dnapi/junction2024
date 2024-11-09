#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <regex>
#include <filesystem>

namespace fs = std::filesystem;

// void add_numbers(std::string input, std::set<int>& numbers, std::vector<int>& line_numbers) {
//     std::regex pattern("#(\\d+)"); // Regex to match numbers after #

//     // Use regex iterator to find all matches
//     auto matches_begin = std::sregex_iterator(input.begin(), input.end(), pattern);
//     auto matches_end = std::sregex_iterator();

//     int count = 0;
//     for (std::sregex_iterator i = matches_begin; i != matches_end; ++i) {
//         std::smatch match = *i;
//         int num = std::stoi(match.str(1));// Extract the number and convert to int
//         if (count > 0)
//             numbers.insert(num);
//         else
//             line_numbers.push_back(num);
//         count++;
//     }
    
// }



void add_numbers(const std::string& input, std::set<int>& numbers, std::set<int>& line_numbers) {
    size_t pos = 0;
    int count = 0;

    // Loop through the string to find all occurrences of '#'
    while ((pos = input.find('#', pos)) != std::string::npos) {
        size_t start = pos + 1;
        size_t end = start;

        // Extract digits following the '#'
        while (end < input.size() && std::isdigit(input[end])) {
            ++end;
        }

        if (start < end) {
            int num = std::stoi(input.substr(start, end - start)); // Convert substring to int
            if (count > 0) {
                numbers.insert(num); // Add to set if not the first number
            } else {
                line_numbers.insert(num); // Add first number to vector
            }
            count++;
        }

        pos = end; // Move position forward for next search
    }
}


// std::vector<int> extractNumbers(const std::string& input) {
//     std::vector<int> numbers;
//     size_t pos = 0;

//     // Loop through the string to find all occurrences of '#'
//     while ((pos = input.find('#', pos)) != std::string::npos) {
//         size_t start = pos + 1;
//         size_t end = start;

//         // Find the end of the number (until a non-digit character is found)
//         while (end < input.size() && std::isdigit(input[end])) {
//             ++end;
//         }

//         // Convert the number substring to an integer and add to the vector
//         if (start < end) {
//             numbers.push_back(std::stoi(input.substr(start, end - start)));
//         }

//         // Move the position forward
//         pos = end;
//     }

//     return numbers;
// }

// std::string extractIFCEntity(const std::string& input) {
//     std::regex pattern("#\\d+=\\s*(\\w+)\\("); // Regex to match the entity name
//     std::smatch match;

//     if (std::regex_search(input, match, pattern)) {
//         return match.str(1); // Return the matched entity name
//     }

//     return ""; // Return an empty string if no match is found
// }


std::string extractIFCEntity(const std::string& input) {
    // Find the position of the first space and the first '('
    size_t start = input.find(' ') + 1;
    size_t end = input.find('(');

    // Ensure both characters are found and return the substring
    if (start != std::string::npos && end != std::string::npos && start < end) {
        return input.substr(start, end - start);
    }

    return ""; // Return an empty string if the format is incorrect
}

void saveToFile(const std::set<int> numbers, int position_data, const std::vector<std::string>& header, const std::vector<std::string>& lines, const std::string& filename) {
    // Open the file in write mode
    std::ofstream outfile(filename);

    // Check if the file was opened successfully
    if (!outfile.is_open()) {
        std::cerr << "Failed to open file " << filename << std::endl;
        return;
    }

    // Write each string in the vector to the file
    for (int i = 0; i < position_data; i++) {
        outfile << header[i] << std::endl;  // Write the line followed by a newline
    }

    for (int i : numbers) {
        outfile << lines[i - 1] << std::endl;  // Write the line followed by a newline
    }

    for (int i = position_data; i < header.size(); i++) {
        outfile << header[i] << std::endl;  // Write the line followed by a newline
    }
    // Close the file
    outfile.close();
}


int main() {
    // Open the file
    std::string filename = "../ifc_examples_peikko/WoodenOffice.ifc";
    std::ifstream file(filename);
    
    // Check if the file opened successfully
    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
        return 1;
    }

    std::string line;
    std::vector<std::string> lines;
    std::vector<std::string> header;
    std::set<int> all_numbers;
    std::set<int> line_numbers;
    // Read the file line by line
    int total = 0;
    int postion_data = 0;
    bool tail = false;
    while (std::getline(file, line)) { // && total < 50000000
        // Taking header
        if (!line.empty() && line[0] != '#') {
            header.push_back(line);
            if (!tail) {
                postion_data++;
            }
            continue;
        }
        tail = true;
        lines.push_back(line);
        if (extractIFCEntity(line) == "IFCBEAM") {
            total++;
            add_numbers(line, all_numbers, line_numbers);
        }
    }
    // Close the file
    file.close();
    
    while (!all_numbers.empty()) {
        std::set<int> to_remove;  // Set to store numbers to be removed after iteration

        for (int i : all_numbers) {
            add_numbers(lines[i - 1], all_numbers, line_numbers);
            // Mark the number for removal
            to_remove.insert(i);
        }

        // Now remove all the numbers from the set
        for (int i : to_remove) {
            all_numbers.erase(i);
        }
    }

    std::cout << "Total number of found IFCBEAM: " << line_numbers.size() << std::endl;

    saveToFile(line_numbers, postion_data, header, lines, "ifc_beam_only.ifc");

    std::cout << "File with extacted size to ifc_beam_only.ifc\n";


    try {
        std::string file1 = filename;
        std::string file2 = "ifc_beam_only.ifc";
        auto size1 = fs::file_size(file1);
        auto size2 = fs::file_size(file2);

         // Convert size from bytes to megabytes (MB)
        double size1MB = static_cast<double>(size1) / (1024 * 1024);
        double size2MB = static_cast<double>(size2) / (1024 * 1024);

        std::cout << "Size of original file " << ": " << static_cast<int>(size1MB) << " MB\n";
        std::cout << "Size of extracted file" << ": " << static_cast<int>(size2MB) << " MB\n";
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << '\n';
    }


    return 0;
}
