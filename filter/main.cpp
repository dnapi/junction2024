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
    //std::string filename = "../ifc_examples_peikko/WoodenOffice.ifc";
    std::string filename = "../ifc_examples_peikko/DummyModel.ifc";
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
    //all_numbers = {397904, 1210184, 397891, 1210184, 397911, 1210184, 397917, 1210184, 631399, 1219531, 631356, 1219531, 631313, 1219531, 631442, 1219531, 631728, 1219676, 631771, 1219676, 631814, 1219676, 631685, 1219676, 632057, 1220158, 632186, 1220158, 632100, 1220158, 632143, 1220158, 747648, 790556, 747777, 790556, 747691, 790556, 747734, 790556, 389415, 1216050, 389406, 1216050, 389424, 1216050, 389430, 1216050, 439179, 1202053, 439045, 1202053, 439093, 1202053, 439136, 1202053, 1057275, 1210749, 1057232, 1210749, 1057189, 1210749, 1057318, 1210749, 1060262, 1217397, 1060219, 1217397, 1060133, 1217397, 1060176, 1217397, 560318, 1200473, 560274, 1200473, 560230, 1200473, 560362, 1200473, 389072, 1216644, 389064, 1216644, 389049, 1216644, 389078, 1216644, 1062773, 1177976, 1062717, 1177976, 1062661, 1177976, 1062829, 1177976, 1057671, 1214357, 1057714, 1214357, 1057530, 1180566, 1057362, 1180566, 1057418, 1180566, 1057474, 1180566, 671760, 84942, 1056526, 1209470, 1056397, 1209470, 1056440, 1209470, 1056483, 1209470, 747949, 790729, 747863, 790729, 747820, 790729, 747906, 790729, 355820, 1205906, 355949, 1205906, 355906, 1205906, 355863, 1205906, 900493, 1207019, 900450, 1207019, 900536, 1207019, 900579, 1207019, 630325, 1215533, 630281, 1215533, 770849, 1213288, 770855, 1213288, 770861, 1213288, 770867, 1213288, 355576, 1205610, 355108, 1205610, 355532, 1205610, 355488, 1205610, 1059286, 1177816, 1059118, 1177816, 1059174, 1177816, 1059230, 1177816, 559850, 1199638, 559894, 1199638, 559938, 1199638, 559806, 1199638, 900822, 1206416, 900865, 1206416, 900908, 1206416, 900951, 1206416, 747992, 791257, 748035, 791257, 748078, 791257, 748121, 791257, 1057585, 1214357, 1057628, 1214357, 1062002, 1178130, 1062058, 1178130, 1061890, 1178130, 1061946, 1178130, 1058382, 1177662, 1058438, 1177662, 1058494, 1177662, 1058326, 1177662, 1061606, 1178207, 1061550, 1178207, 1061662, 1178207, 1061494, 1178207, 1061266, 1178284, 1061098, 1178284, 1061210, 1178284, 1061154, 1178284, 1058834, 1177739, 1058722, 1177739, 1058778, 1177739, 1058890, 1177739, 1059737, 1212772, 1059866, 1212772, 900207, 1207232, 900164, 1207232, 900075, 1207232, 900121, 1207232, 813370, 1197817, 813327, 1197817, 813284, 1197817, 813241, 1197817, 560649, 1203138, 560692, 1203138, 560735, 1203138, 560606, 1203138, 1059031, 1211666, 1058988, 1211666, 1059074, 1211666, 1058945, 1211666, 1060078, 1178371, 1060022, 1178371, 1059966, 1178371, 1059910, 1178371, 632558, 1223056, 632515, 1223056, 632429, 1223056, 632472, 1223056, 400264, 1207990, 400255, 1207990, 400272, 1207990, 400278, 1207990, 390627, 1198284, 390680, 1198284, 390727, 1198284, 390772, 1198284, 1062574, 1218657, 1062488, 1218657, 1062617, 1218657, 1062531, 1218657, 1059341, 1212268, 1059384, 1212268, 1059470, 1212268, 1059427, 1212268, 1060362, 1177893, 1060418, 1177893, 1060474, 1177893, 1060306, 1177893, 1055428, 1126700, 1055540, 1126700, 1055484, 1126700, 1055365, 1126700, 1062884, 1218850, 1062927, 1218850, 1062970, 1218850, 1063013, 1218850, 1062335, 1178053, 1062433, 1178053, 1062279, 1178053, 1062384, 1178053, 438801, 1211666, 438795, 1211666, 438813, 1211666, 438807, 1211666, 671664, 84942, 747456, 788156, 747604, 788156, 747560, 788156, 747516, 788156, 1057986, 1180620, 1057930, 1180620, 1058042, 1180620, 1058098, 1180620, 1058196, 1216644, 672107, 1120592, 1057757, 1216050, 1057800, 1216050, 1057843, 1216050, 1057886, 1216050, 698605, 1180718, 698493, 1180718, 698549, 1180718, 698427, 1180718, 1061846, 1217691, 1061803, 1217691, 1061760, 1217691, 1061717, 1217691, 672064, 1120592, 672021, 1120592, 671978, 1120592, 1061054, 1214889, 1061011, 1214889, 1060968, 1214889, 1060870, 1179472, 1060702, 1179472, 1060758, 1179472, 1060814, 1179472, 1060925, 1214889, 84942, 1180835, 812998, 1197595, 812955, 1197595, 812912, 1197595, 812862, 1197595, 480349, 1204986, 480306, 1204986, 480263, 1204986, 480220, 1204986, 1058282, 1216644, 1058239, 1216644, 630984, 1219334, 630941, 1219334, 631070, 1219334, 631027, 1219334, 1056793, 1210184, 1056836, 1210184, 1056879, 1210184, 1056922, 1210184, 1058153, 1216644, 1062156, 1218158, 1062113, 1218158, 1062199, 1218158, 1062242, 1218158, 1058678, 1211184, 1058635, 1211184, 1058592, 1211184, 1058549, 1211184, 630193, 1215533, 630237, 1215533, 630612, 1198516, 630569, 1198516, 630698, 1198516, 630655, 1198516, 1061407, 1217544, 1061364, 1217544, 1061450, 1217544, 1061321, 1217544, 1056130, 1213288, 1056087, 1213288, 1056044, 1213288, 1055997, 1213288, 1055595, 1217203, 1055729, 1217203, 1055686, 1217203, 1055643, 1217203, 1059780, 1212772, 1059570, 1177606, 1059514, 1177606, 1059626, 1177606, 1059682, 1177606, 1059823, 1212772, 752695, 84942, 752587, 84942, 1060658, 1215077, 1060615, 1215077, 1060572, 1215077, 1060529, 
    //    1215077};
    all_numbers = {152, 1272, 106, 1322, 311, 2830, 329, 2800, 217, 1354, 197, 1330, 227, 2830, 247, 2800, 278, 1272, 258, 1322, 286, 1330, 302,
        1354};
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
        // if (extractIFCEntity(line) == "IFCBEAM") {
        //     total++;
        //     add_numbers(line, all_numbers, line_numbers);
        // }
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
