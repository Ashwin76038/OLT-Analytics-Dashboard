# SQL engine and executed checks

The project author confirms using **MySQL** for the original project. MySQL is the author's SQL tool; this review has not executed the original queries in a MySQL instance.

The additional public audit scripts use Python and an in-memory **SQLite** database to independently reconcile counts, denominators and listed amounts. Their passing results establish those checks in SQLite, not MySQL execution or Power BI DAX validation.

The existing `sql/powerbi_star_schema.sql` is a **SQL Server reference DDL** artifact. Its `dbo` qualification, bracketed names and casts should not be represented as tested MySQL syntax. It is retained as an existing reference; this review does not claim to have reproduced the author's MySQL workflow.

For interview descriptions: “I used MySQL in the project. Additional Python/SQLite checks reconcile the public tables; native MySQL and Power BI execution checks are separately pending.”
