### The calculator performs arithmetic operations and persists the last 10 calculations to an XML history file.
```
Code Under Test
Interfaces
// Pure calculation contract — no I/O
public interface ICalculator
{
    double Add(double a, double b);
    double Subtract(double a, double b);
    double Multiply(double a, double b);
    double Divide(double a, double b);
}

// History persistence contract — abstracts XML I/O
public interface IHistoryRepository
{
    IReadOnlyList<CalculationRecord> Load();
    void Save(IReadOnlyList<CalculationRecord> records);
}

// Orchestrator — combines calculation + history
public interface ICalculatorService
{
    double Calculate(string operation, double a, double b);
    IReadOnlyList<CalculationRecord> GetHistory();
    void ClearHistory();
}
Models
public record CalculationRecord(
    string Operation,      // "Add", "Subtract", "Multiply", "Divide"
    double Operand1,
    double Operand2,
    double Result,
    DateTime Timestamp);
Concrete Implementations
// Pure math — no dependencies
public class Calculator : ICalculator { ... }

// Reads/writes XML file — real I/O
public class XmlHistoryRepository : IHistoryRepository
{
    private readonly string _filePath;
    public XmlHistoryRepository(string filePath) => _filePath = filePath;
    // Serializes/deserializes List<CalculationRecord> to XML
    // Keeps only the last 10 entries on Save()
}

// Orchestrates calculation + history persistence
public class CalculatorService : ICalculatorService
{
    private readonly ICalculator _calculator;
    private readonly IHistoryRepository _history;
    // Calculate() → compute result → append to history → save → return result
    // GetHistory() → load from repository
    // ClearHistory() → save empty list
}
XML History Format
<?xml version="1.0" encoding="utf-8"?>
<CalculationHistory>
  <Entry>
    <Operation>Add</Operation>
    <Operand1>10</Operand1>
    <Operand2>5</Operand2>
    <Result>15</Result>
    <Timestamp>2026-04-01T09:30:00Z</Timestamp>
  </Entry>
  <!-- ... up to 10 entries, oldest dropped first -->
</CalculationHistory>
```
