#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#include <mysql.h>
#include <string>

#endif

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
            // Report state.errorMessage and state.error.
        } else if (state.connected) {
            // Database connection is available.
        } else {
            // Database connection is currently unavailable.
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      static_cast<void>(rows);
                  },
                  [](const std::string& error, unsigned int number) {
                      static_cast<void>(error);
                      static_cast<void>(number);
                  });
          },
          [](const std::string& error, unsigned int number) {
              static_cast<void>(error);
              static_cast<void>(number);
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  // row[0] is sensor, row[1] is value.
              } else {
                  // No more rows for this result.
              }
          },
          [](const std::string& error, unsigned int number) {
              static_cast<void>(error);
              static_cast<void>(number);
          });

    return core::SNodeC::start();
}
