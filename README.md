# ITT_Learn_and_Code

**ITT_Learn_and_Code** is a structured learning and development repository built to help developers understand real-world software concepts through simple, clear, and practical examples.  
The goal is to make complex topics easier by demonstrating them with hands-on code, best practices, and explanation-driven learning.

---

## 📝 Assignment: Clean Code Refactoring — Data Processing System

### Problem Statement

We have a data processing system that reads data from files, validates it, transforms it, and outputs results in various formats. The system works correctly but violates multiple clean code principles. The task is to identify these violations and refactor the code to address the design gaps.

### Original Code (C#)

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace CleanCodeAssignments.Comprehensive
{
    public class DataProcessor
    {
        public string inputFilePath;
        public string outputFilePath;
        public int recordsProcessed;
        public int errorCount;
        public List<string> errorMessages;

        public bool validateData = true;
        public bool transformData = true;

        public Dictionary<string, int> statistics;
        public string logFilePath = "processing.log";

        private List<string> rawData;
        public string dateFormat = "yyyy-MM-dd";
        private List<Dictionary<string, object>> parsedRecords;
        public int batchSize = 100;
        private StringBuilder logBuffer;

        public DataProcessor(string inputFile, string outputFile)
        {
            inputFilePath = inputFile;
            outputFilePath = outputFile;
            recordsProcessed = 0;
            errorCount = 0;
            errorMessages = new List<string>();
            rawData = new List<string>();
            parsedRecords = new List<Dictionary<string, object>>();
            statistics = new Dictionary<string, int>();
            logBuffer = new StringBuilder();

            if (!File.Exists(inputFile))
            {
                File.Create(inputFile).Close();
            }

            Log("DataProcessor initialized");
        }

        public void ProcessData()
        {
            Log("Starting data processing");

            try
            {
                Log($"Reading input file: {inputFilePath}");
                rawData = new List<string>(File.ReadAllLines(inputFilePath));
                Log($"Read {rawData.Count} lines");

                Log("Parsing data...");
                foreach (var line in rawData)
                {
                    if (string.IsNullOrWhiteSpace(line)) continue;

                    var parts = line.Split(',');
                    if (parts.Length >= 3)
                    {
                        var record = new Dictionary<string, object>
                        {
                            { "id", parts[0].Trim() },
                            { "name", parts[1].Trim() },
                            { "value", parts[2].Trim() }
                        };

                        if (parts.Length >= 4)
                        {
                            record["date"] = parts[3].Trim();
                        }

                        parsedRecords.Add(record);
                    }
                    else
                    {
                        errorCount++;
                        errorMessages.Add($"Invalid line format: {line}");
                        Log($"ERROR: Invalid line format: {line}");
                    }
                }

                Log($"Parsed {parsedRecords.Count} records");

                if (validateData)
                {
                    Log("Validating data...");
                    var validRecords = new List<Dictionary<string, object>>();

                    foreach (var record in parsedRecords)
                    {
                        bool isValid = true;

                        if (!record.ContainsKey("id") || string.IsNullOrEmpty(record["id"].ToString()))
                        {
                            isValid = false;
                            errorMessages.Add($"Record missing ID");
                        }

                        if (!record.ContainsKey("name") || string.IsNullOrEmpty(record["name"].ToString()))
                        {
                            isValid = false;
                            errorMessages.Add($"Record {record.GetValueOrDefault("id")} missing name");
                        }

                        if (record.ContainsKey("value"))
                        {
                            if (!double.TryParse(record["value"].ToString(), out _))
                            {
                                isValid = false;
                                errorMessages.Add($"Record {record.GetValueOrDefault("id")} has invalid value");
                            }
                        }

                        if (isValid)
                        {
                            validRecords.Add(record);
                        }
                        else
                        {
                            errorCount++;
                        }
                    }

                    parsedRecords = validRecords;
                    Log($"Validation complete. {parsedRecords.Count} valid records");
                }

                if (transformData)
                {
                    Log("Transforming data...");

                    foreach (var record in parsedRecords)
                    {
                        if (record.ContainsKey("name"))
                        {
                            record["name"] = record["name"].ToString().ToUpper();
                        }

                        if (record.ContainsKey("date"))
                        {
                            if (DateTime.TryParse(record["date"].ToString(), out DateTime date))
                            {
                                record["date"] = date.ToString(dateFormat);
                            }
                        }

                        if (record.ContainsKey("value"))
                        {
                            double value = double.Parse(record["value"].ToString());
                            record["doubled_value"] = value * 2;
                            record["squared_value"] = value * value;
                        }
                    }

                    Log("Transformation complete");
                }

                Log("Calculating statistics...");
                statistics["total_records"] = parsedRecords.Count;
                statistics["error_count"] = errorCount;

                double totalValue = 0;
                foreach (var record in parsedRecords)
                {
                    if (record.ContainsKey("value"))
                    {
                        totalValue += double.Parse(record["value"].ToString());
                    }
                }
                statistics["total_value"] = (int)totalValue;
                statistics["average_value"] = parsedRecords.Count > 0
                    ? (int)(totalValue / parsedRecords.Count) : 0;

                Log($"Statistics calculated: {statistics.Count} metrics");

                Log($"Writing output to: {outputFilePath}");
                var outputLines = new List<string>();
                outputLines.Add("ID,NAME,VALUE,DATE,DOUBLED_VALUE,SQUARED_VALUE");

                foreach (var record in parsedRecords)
                {
                    var line = $"{record.GetValueOrDefault("id")}," +
                              $"{record.GetValueOrDefault("name")}," +
                              $"{record.GetValueOrDefault("value")}," +
                              $"{record.GetValueOrDefault("date")}," +
                              $"{record.GetValueOrDefault("doubled_value")}," +
                              $"{record.GetValueOrDefault("squared_value")}";
                    outputLines.Add(line);
                }

                File.WriteAllLines(outputFilePath, outputLines);
                recordsProcessed = parsedRecords.Count;

                Log($"Output written. {recordsProcessed} records processed");

                File.WriteAllText(logFilePath, logBuffer.ToString());

                Console.WriteLine("Processing complete!");
                Console.WriteLine($"Records processed: {recordsProcessed}");
                Console.WriteLine($"Errors: {errorCount}");
            }
            catch (Exception ex)
            {
                errorCount++;
                errorMessages.Add($"Fatal error: {ex.Message}");
                Log($"FATAL ERROR: {ex.Message}");
                Console.WriteLine($"Processing failed: {ex.Message}");
            }
        }

        private void Log(string message)
        {
            string timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            logBuffer.AppendLine($"[{timestamp}] {message}");
        }

        public void DisplayStatistics()
        {
            Console.WriteLine("\n=== Processing Statistics ===");
            foreach (var stat in statistics)
            {
                Console.WriteLine($"{stat.Key}: {stat.Value}");
            }

            if (errorMessages.Count > 0)
            {
                Console.WriteLine("\n=== Errors ===");
                foreach (var error in errorMessages)
                {
                    Console.WriteLine($"- {error}");
                }
            }
        }

        public void ExportToJson(string jsonFilePath) { /* ... */ }
        public void ExportToXml(string xmlFilePath) { /* ... */ }
        public void ExportByFormat(string filePath, string format) { /* ... */ }
        public List<Dictionary<string, object>> FilterByValue(double minValue) { /* ... */ }
        public void UpdateConfiguration(string dateFormatNew, int batchSizeNew,
            bool validate, bool transform) { /* ... */ }
        public static void GenerateSampleData(string filePath, int recordCount) { /* ... */ }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
            DataProcessor.GenerateSampleData("input.csv", 50);

            var processor = new DataProcessor("input.csv", "output.csv");
            processor.validateData = true;
            processor.transformData = true;
            processor.dateFormat = "MM/dd/yyyy";
            processor.batchSize = 50;

            processor.ProcessData();
            processor.DisplayStatistics();

            processor.ExportToJson("output.json");
            processor.ExportToXml("output.xml");

            var filtered = processor.FilterByValue(100);
            Console.WriteLine($"\nFiltered records: {filtered.Count}");

            processor.errorMessages.Add("Manually added error"); // violation!
        }
    }
}
```

### Clean Code Violations Identified

| #   | Violation                                 | Description                                                                                                                                                                     |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Single Responsibility Principle (SRP)** | `DataProcessor` handles reading, parsing, validation, transformation, statistics, exporting, logging, and console output — all in one class.                                    |
| 2   | **Encapsulation**                         | Public fields (`inputFilePath`, `errorCount`, `errorMessages`, `statistics`, etc.) expose internal state and allow external mutation (e.g. `processor.errorMessages.Add(...)`). |
| 3   | **God Method**                            | `ProcessData()` is a monolithic method doing everything: file I/O, parsing, validation, transformation, statistics, output writing, and logging.                                |
| 4   | **Open/Closed Principle (OCP)**           | `ExportByFormat()` uses a switch statement on format strings. Adding a new format requires modifying the class.                                                                 |
| 5   | **Magic Strings / Primitive Obsession**   | Records are stored as `Dictionary<string, object>` instead of a proper domain model — keys like `"id"`, `"name"`, `"value"` are scattered as magic strings.                     |
| 6   | **Side Effects in Constructor**           | The constructor creates the input file if it doesn't exist — an unexpected side effect for a data processor.                                                                    |
| 7   | **Tight Coupling**                        | Direct `File.ReadAllLines`, `File.WriteAllLines`, `Console.WriteLine` calls everywhere make the class impossible to test in isolation.                                          |
| 8   | **Configuration Coupling**                | Configuration fields (`dateFormat`, `batchSize`, `validateData`, `transformData`) are mixed into the processor class as mutable public fields.                                  |

---

### Refactored Solution (Python)

The refactored version applies clean code principles by decomposing the monolithic class into focused, single-responsibility components.

#### Project Structure

```
data_processing_system/
├── config/
│   └── processor_config.py          # ProcessorConfig — immutable configuration
├── core/
│   ├── services/
│   │   └── data_processing_service.py  # DataProcessingService — orchestrator
│   └── transformation/
│       └── record_transformer.py     # RecordTransformer — field transforms
├── domain/
│   ├── record.py                     # Record — typed domain model
│   └── processing_statistics.py      # ProcessingStatistics — statistics model
├── statistics/
│   └── statistics_calculator.py      # StatisticsCalculator — computes metrics
└── utils/
    ├── exporters/
    │   ├── exporter.py               # Exporter (ABC) — abstract interface
    │   ├── csv_exporter.py           # CsvExporter
    │   ├── json_exporter.py          # JsonExporter
    │   └── xml_exporter.py           # XmlExporter
    ├── filtering/
    │   └── value_filter.py           # ValueFilter — filters records by value
    ├── io/
    │   ├── file_reader.py            # FileReader — reads input files
    │   ├── file_writer.py            # FileWriter — writes output files
    │   └── sample_data_generator.py  # SampleDataGenerator — test data
    └── logging/
        └── logger.py                 # Logger — file-based logging
```

#### How Violations Were Fixed

| Violation               | Fix                                                                                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**                 | Split into `FileReader`, `RecordParser`, `RecordValidator`, `RecordTransformer`, `StatisticsCalculator`, `Exporter` subclasses, `ValueFilter`, `Logger`, and `DataProcessingService` (orchestrator). |
| **Encapsulation**       | `Record` is a proper domain object with typed attributes. No public mutable state is exposed.                                                                                                        |
| **God Method**          | `DataProcessingService.process()` delegates to injected collaborators — each step is a single method call.                                                                                           |
| **OCP**                 | `Exporter` is an abstract base class. New formats are added by creating a new subclass — no switch statements.                                                                                       |
| **Primitive Obsession** | `Dictionary<string, object>` replaced with a `Record` class and `ProcessorConfig` class.                                                                                                             |
| **Side Effects**        | Constructor does no file I/O. `SampleDataGenerator` is a separate utility.                                                                                                                           |
| **Tight Coupling**      | Dependencies are injected into `DataProcessingService` via constructor — easy to test with mocks.                                                                                                    |
| **Configuration**       | `ProcessorConfig` is a dedicated configuration class, passed as a dependency.                                                                                                                        |

#### Running the Refactored Code

```bash
python main.py
```

---

## 🚀 What This Repository Offers

- **Real-world coding examples**
- **Clean and scalable code patterns**
- **Step-by-step explanations for clarity**
- **AI, ML, DevOps, and backend code samples**
- **Debugging guides and architecture notes**
- **Best practices for Python, APIs, Docker, and more**

---

## 📘 Purpose

This repository is created to:

- Provide a single place to **learn and build together**
- Break down difficult concepts into **easy-to-understand examples**
- Help new and experienced developers practice **real industry-level coding standards**

---

## 🧩 Who Is This For?

- Students
- Beginners in coding
- Developers practicing for interviews
- Engineers exploring new technologies
- Anyone who wants to learn by doing

---

## 🤝 Contribution

Contributions are welcome!  
Feel free to submit pull requests, open issues, or suggest new topics to cover.

---

## ⭐ Support

If you find this helpful, give the repository a **star** — it helps others discover it and supports future updates.

---

### **Learn. Build. Improve. Repeat.**

**ITT_Learn_and_Code**
