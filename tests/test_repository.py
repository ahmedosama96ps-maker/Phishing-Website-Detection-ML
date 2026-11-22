"""Dataset, notebook syntax, and quick model-fit smoke checks.

These intentionally do not validate the archived reported model accuracy.
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

    def test_small_training_smoke(self):
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import f1_score

        data = pd.read_csv(ROOT / "data" / "phishing.csv")
        x = data.drop(columns=["Index", "class"])
        y = data["class"]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, stratify=y, random_state=42
        )
        model = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
        model.fit(x_train.iloc[:500], y_train.iloc[:500])
        pred = model.predict(x_test.iloc[:50])
        self.assertEqual(len(pred), 50)
        self.assertGreaterEqual(f1_score(y_test.iloc[:50], pred, average="weighted"), 0.0)

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
