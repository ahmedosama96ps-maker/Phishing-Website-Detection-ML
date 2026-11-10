"""Static checks for the published notebook and CSV dataset.

This intentionally does not claim to verify model accuracy. Run the notebook for that.
"""
import ast
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NotebookRepositoryChecks(unittest.TestCase):
    def test_dataset_schema_and_labels(self):
        with (ROOT / "data" / "phishing.csv").open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            self.assertIn("class", reader.fieldnames)
            self.assertIn("Index", reader.fieldnames)
            self.assertEqual(len(reader.fieldnames), 32)
            n = 0
            labels = set()
            for row in reader:
                n += 1
                labels.add(row["class"])
        self.assertEqual(n, 11054)
        self.assertEqual(labels, {"-1", "1"})

    def test_all_code_cells_parse(self):
        notebook = json.loads((ROOT / "notebook" / "Phishing_Website_Detection_Final.ipynb").read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
        self.assertGreaterEqual(len(code_cells), 8)
        for index, cell in enumerate(code_cells):
            with self.subTest(index=index):
                ast.parse("".join(cell["source"]))

    def test_actual_training_not_placeholder(self):
        notebook = json.loads((ROOT / "notebook" / "Phishing_Website_Detection_Final.ipynb").read_text(encoding="utf-8"))
        source = "\n".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
        for required in ("cross_validate(", "tuner.fit(", "best_rf.predict(", "reduced_rf.fit(", "unsupervised_model.fit("):
            self.assertIn(required, source)


if __name__ == "__main__":
    unittest.main()
