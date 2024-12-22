using MySql.Data.MySqlClient;
using System;

class OnlineCoursesApp
{
    static void Main(string[] args)
    {
        string connectionString = "Server=mysqlbds-lbsbds.f.aivencloud.com;Port=27913;Database=defaultdb;User ID=avnadmin;Password=AVNS_U_nGI5N9gKIDfCh1wrY;";

        using (MySqlConnection dbConnection = new MySqlConnection(connectionString))
        {
            try
            {
                dbConnection.Open();
                Console.WriteLine("Database connection established successfully!");

                bool exitProgram = false;
                while (!exitProgram)
                {
                    Console.WriteLine("\n--- Online Courses Menu ---");
                    Console.WriteLine("1. Show all tables");
                    Console.WriteLine("2. Display table data");
                    Console.WriteLine("3. Insert records into tables");
                    Console.WriteLine("4. Execute JOIN query");
                    Console.WriteLine("5. Execute filtering query");
                    Console.WriteLine("6. Execute aggregation query");
                    Console.WriteLine("7. Exit");

                    Console.Write("Select an option (1-7): ");
                    string userChoice = Console.ReadLine();

                    switch (userChoice)
                    {
                        case "1":
                            ShowAllTables(dbConnection);
                            break;
                        case "2":
                            DisplayTableData(dbConnection);
                            break;
                        case "3":
                            InsertRecords(dbConnection);
                            break;
                        case "4":
                            ExecuteJoinQuery(dbConnection);
                            break;
                        case "5":
                            ExecuteFilterQuery(dbConnection);
                            break;
                        case "6":
                            ExecuteAggregateQuery(dbConnection);
                            break;
                        case "7":
                            exitProgram = true;
                            Console.WriteLine("Exiting application.");
                            break;
                        default:
                            Console.WriteLine("Invalid selection. Please try again.");
                            break;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }

    static void ShowAllTables(MySqlConnection dbConnection)
    {
        string[] queries = {
            "SHOW TABLES;"
        };

        foreach (string query in queries)
        {
            ExecuteReaderQuery(dbConnection, query);
        }
    }

    static void DisplayTableData(MySqlConnection dbConnection)
    {
        string[] tableNames = { "categories", "instructors", "courses", "students", "enrollments" };

        foreach (string tableName in tableNames)
        {
            string query = $"SELECT * FROM {tableName};";
            Console.WriteLine($"\n--- {tableName} Table Data ---");
            ExecuteReaderQuery(dbConnection, query);
        }
    }

    static void InsertRecords(MySqlConnection dbConnection)
    {
        string categoriesQuery = "INSERT INTO categories (name, description) VALUES ('Test Category', 'Sample description.');";
        string instructorsQuery = "INSERT INTO instructors (first_name, last_name, email, bio) VALUES ('Test', 'Instructor', 'test@example.com', 'Bio information.');";
        string coursesQuery = "INSERT INTO courses (title, description, category_id, instructor_id) VALUES ('Test Course', 'Course description.', 1, 1);";
        string studentsQuery = "INSERT INTO students (first_name, last_name, email, registration_date) VALUES ('Test', 'Student', 'student@example.com', '2024-01-01');";
        string enrollmentsQuery = "INSERT INTO enrollments (student_id, course_id, enrollment_date, progress_percentage) VALUES (1, 1, '2024-01-02', 10);";

        ExecuteNonQuery(dbConnection, categoriesQuery);
        ExecuteNonQuery(dbConnection, instructorsQuery);
        ExecuteNonQuery(dbConnection, coursesQuery);
        ExecuteNonQuery(dbConnection, studentsQuery);
        ExecuteNonQuery(dbConnection, enrollmentsQuery);
    }

    static void ExecuteJoinQuery(MySqlConnection dbConnection)
    {
        string query = @"SELECT e.enrollment_id, s.first_name AS student_name, c.title AS course_title, e.progress_percentage
                          FROM enrollments e
                          JOIN students s ON e.student_id = s.student_id
                          JOIN courses c ON e.course_id = c.course_id;";
        ExecuteReaderQuery(dbConnection, query);
    }

    static void ExecuteFilterQuery(MySqlConnection dbConnection)
    {
        string query = "SELECT * FROM courses WHERE title LIKE '%Python%';";
        ExecuteReaderQuery(dbConnection, query);
    }

    static void ExecuteAggregateQuery(MySqlConnection dbConnection)
    {
        string query = "SELECT COUNT(*) AS TotalCourses, AVG(progress_percentage) AS AverageProgress FROM enrollments;";
        ExecuteReaderQuery(dbConnection, query);
    }

    static void ExecuteReaderQuery(MySqlConnection dbConnection, string query)
    {
        try
        {
            using (MySqlCommand command = new MySqlCommand(query, dbConnection))
            using (MySqlDataReader reader = command.ExecuteReader())
            {
                // Print headers (column names)
                for (int i = 0; i < reader.FieldCount; i++)
                {
                    Console.Write($"{reader.GetName(i),-20}");
                }
                Console.WriteLine();
                Console.WriteLine(new string('-', 80));  // Line separator

                // Print rows of data
                while (reader.Read())
                {
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        Console.Write($"{reader[i],-20}");
                    }
                    Console.WriteLine();
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error executing query: {ex.Message}");
        }
    }

    static void ExecuteNonQuery(MySqlConnection dbConnection, string query)
    {
        try
        {
            using (MySqlCommand command = new MySqlCommand(query, dbConnection))
            {
                int rowsAffected = command.ExecuteNonQuery();
                Console.WriteLine($"{rowsAffected} row(s) affected.");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error executing non-query: {ex.Message}");
        }
    }
}
