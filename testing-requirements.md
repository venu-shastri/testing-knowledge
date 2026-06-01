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
```

### python
```
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
import xml.etree.ElementTree as ET
import os


# =========================
# Models
# =========================

@dataclass(frozen=True)
class CalculationRecord:
    operation: str
    operand1: float
    operand2: float
    result: float
    timestamp: datetime


# =========================
# Interfaces
# =========================

class ICalculator(ABC):

    @abstractmethod
    def add(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def subtract(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def multiply(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def divide(self, a: float, b: float) -> float:
        pass


class IHistoryRepository(ABC):

    @abstractmethod
    def load(self) -> List[CalculationRecord]:
        pass

    @abstractmethod
    def save(self, records: List[CalculationRecord]) -> None:
        pass


class ICalculatorService(ABC):

    @abstractmethod
    def calculate(self, operation: str, a: float, b: float) -> float:
        pass

    @abstractmethod
    def get_history(self) -> List[CalculationRecord]:
        pass

    @abstractmethod
    def clear_history(self) -> None:
        pass


# =========================
# Calculator
# =========================

class Calculator(ICalculator):

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b


# =========================
# XML Repository
# =========================

class XmlHistoryRepository(IHistoryRepository):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def load(self) -> List[CalculationRecord]:

        if not os.path.exists(self._file_path):
            return []

        tree = ET.parse(self._file_path)
        root = tree.getroot()

        records = []

        for entry in root.findall("Entry"):
            records.append(
                CalculationRecord(
                    operation=entry.findtext("Operation"),
                    operand1=float(entry.findtext("Operand1")),
                    operand2=float(entry.findtext("Operand2")),
                    result=float(entry.findtext("Result")),
                    timestamp=datetime.fromisoformat(
                        entry.findtext("Timestamp").replace("Z", "+00:00")
                    )
                )
            )

        return records

    def save(self, records: List[CalculationRecord]) -> None:

        records = records[-10:]  # keep last 10

        root = ET.Element("CalculationHistory")

        for record in records:
            entry = ET.SubElement(root, "Entry")

            ET.SubElement(entry, "Operation").text = record.operation
            ET.SubElement(entry, "Operand1").text = str(record.operand1)
            ET.SubElement(entry, "Operand2").text = str(record.operand2)
            ET.SubElement(entry, "Result").text = str(record.result)
            ET.SubElement(entry, "Timestamp").text = (
                record.timestamp.astimezone(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )

        tree = ET.ElementTree(root)
        tree.write(
            self._file_path,
            encoding="utf-8",
            xml_declaration=True
        )


# =========================
# Calculator Service
# =========================

class CalculatorService(ICalculatorService):

    def __init__(
        self,
        calculator: ICalculator,
        history_repository: IHistoryRepository
    ):
        self._calculator = calculator
        self._history = history_repository

    def calculate(self, operation: str, a: float, b: float) -> float:

        operation_map = {
            "Add": self._calculator.add,
            "Subtract": self._calculator.subtract,
            "Multiply": self._calculator.multiply,
            "Divide": self._calculator.divide,
        }

        if operation not in operation_map:
            raise ValueError(f"Unsupported operation: {operation}")

        result = operation_map[operation](a, b)

        history = list(self._history.load())

        history.append(
            CalculationRecord(
                operation=operation,
                operand1=a,
                operand2=b,
                result=result,
                timestamp=datetime.now(timezone.utc)
            )
        )

        self._history.save(history)

        return result

    def get_history(self) -> List[CalculationRecord]:
        return self._history.load()

    def clear_history(self) -> None:
        self._history.save([])


# =========================
# Example Usage
# =========================

if __name__ == "__main__":

    calculator = Calculator()
    repository = XmlHistoryRepository("history.xml")

    service = CalculatorService(
        calculator=calculator,
        history_repository=repository
    )

    print(service.calculate("Add", 10, 5))
    print(service.calculate("Multiply", 3, 4))

    for record in service.get_history():
        print(record)
```

</CalculationHistory>
```
