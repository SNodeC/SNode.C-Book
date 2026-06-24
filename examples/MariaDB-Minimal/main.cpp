#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>

#include <iostream>
#include <mysql.h>
#include <string>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const database::mariadb::MariaDBConnectionDetails details = {
        .connectionName = "measurements-db",
        .hostname = "localhost",
        .username = "snodec",
        .password = "<password>",
        .database = "snodec",
        .port = 3306,
        .socket = "",
        .flags = 0,
    };

    database::mariadb::MariaDBClient db(details, [](const database::mariadb::MariaDBState& state) {
        if (state.error != 0) {
            std::cerr << "MariaDB state error " << state.error << ": "
                      << state.errorMessage << "\n";
        } else if (state.connected) {
            std::cout << "MariaDB connected\n";
        } else {
            std::cout << "MariaDB disconnected\n";
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      std::cout << "insert affected rows: " << rows << "\n";
                  },
                  [](const std::string& error, unsigned int number) {
                      std::cerr << "affectedRows error " << number << ": "
                                << error << "\n";
                  });
          },
          [](const std::string& error, unsigned int number) {
              std::cerr << "insert error " << number << ": " << error << "\n";
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  std::cout << "measurement: " << row[0] << " = " << row[1] << "\n";
              } else {
                  std::cout << "measurement query complete\n";
              }
          },
          [](const std::string& error, unsigned int number) {
              std::cerr << "query error " << number << ": " << error << "\n";
          });

    return core::SNodeC::start();
}
