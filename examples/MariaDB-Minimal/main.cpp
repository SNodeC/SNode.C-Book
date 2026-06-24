#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>
#include <log/Logger.h>

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
            LOG(ERROR) << "MariaDB state error " << state.error << ": "
                       << state.errorMessage;
        } else if (state.connected) {
            VLOG(1) << "MariaDB connected";
        } else {
            VLOG(1) << "MariaDB disconnected";
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      VLOG(1) << "insert affected rows: " << rows;
                  },
                  [](const std::string& error, unsigned int number) {
                      LOG(ERROR) << "affectedRows error " << number << ": "
                                 << error;
                  });
          },
          [](const std::string& error, unsigned int number) {
              LOG(ERROR) << "insert error " << number << ": " << error;
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  VLOG(1) << "measurement: " << row[0] << " = " << row[1];
              } else {
                  VLOG(1) << "measurement query complete";
              }
          },
          [](const std::string& error, unsigned int number) {
              LOG(ERROR) << "query error " << number << ": " << error;
          });

    return core::SNodeC::start();
}
