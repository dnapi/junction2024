#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <regex>

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


int main() {
    // Open the file
    std::ifstream file("../ifc_examples_peikko/WoodenOffice.ifc");
    
    // Check if the file opened successfully
    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
        return 1;
    }

    std::string line;
    std::vector<std::string> lines;
    std::set<int> all_numbers;
    std::set<int> line_numbers;
    // Read the file line by line
    int total = 0;
    while (std::getline(file, line) && total < 5) {
        // Check if the first non-comment line has been skipped
        if (!line.empty() && line[0] != '#') {
            std::cout << "Skipped first non-comment line" << std::endl;
            continue;
        }
        lines.push_back(line);
        if (extractIFCEntity(line) == "IFCBEAM") {
            total++;
            //std::cout << "Found IFCBEAM" << std::endl;
            std::cout << line << std::endl;
            add_numbers(line, all_numbers, line_numbers);
        }
    }
    // Close the file
    file.close();
    std::cout << "Total lines found: " << total << std::endl;

    // Print the numbers
    std::cout << "All numbers: " << all_numbers.size() << std::endl;
    for (int num : all_numbers) {
       std::cout << num << " ";
    }
    std::cout << std::endl;
    std::cout << "line_numbers: " << line_numbers.size() << std::endl;
    for (int num : line_numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    std::cout << "lines: " << lines.size() << std::endl;
    
    while (all_numbers.size() > 0) {
        for (int i :  all_numbers) {
            std::cout << "i=" << i;
            add_numbers(lines[i - 1], all_numbers, line_numbers);
            all_numbers.erase(i);
            std::cout << "all_numbers: " << all_numbers.size() << std::endl;
            std::cout << "line_numbers: " << line_numbers.size() << std::endl;
        }
        std::cout << std::endl;
        break;
        //std::cout << *all_numbers.begin() << " ";
        //all_numbers.erase(all_numbers.begin());
    }

    // Print the numbers
    std::cout << "All numbers: " << all_numbers.size() << std::endl;
    for (int num : all_numbers) {
       std::cout << num << " ";
    }
    std::cout << std::endl;
    std::cout << "line_numbers: " << line_numbers.size() << std::endl;
    for (int num : line_numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
