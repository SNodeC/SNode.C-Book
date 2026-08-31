#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>
#include <SemanticLog.h>

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
            snode::semantic::appLog().error() << "MariaDB state error " << state.error << ": "
                       << state.errorMessage;
        } else if (state.connected) {
            snode::semantic::appLog().trace() << "MariaDB connected";
        } else {
            snode::semantic::appLog().trace() << "MariaDB disconnected";
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      snode::semantic::appLog().trace() << "insert affected rows: " << rows;
                  },
                  [](const std::string& error, unsigned int number) {
                      snode::semantic::appLog().error() << "affectedRows error " << number << ": "
                                 << error;
                  });
          },
          [](const std::string& error, unsigned int number) {
              snode::semantic::appLog().error() << "insert error " << number << ": " << error;
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  snode::semantic::appLog().trace() << "measurement: " << row[0] << " = " << row[1];
              } else {
                  snode::semantic::appLog().trace() << "measurement query complete";
              }
          },
          [](const std::string& error, unsigned int number) {
              snode::semantic::appLog().error() << "query error " << number << ": " << error;
          });

    return core::SNodeC::start();
}
