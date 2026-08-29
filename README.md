# Phishing Website Detection Using Machine Learning

A machine learning project focused on detecting **phishing websites** from structured website and URL-related features.

The project covers the full machine learning workflow, from dataset inspection and preprocessing to model comparison, feature engineering, hyperparameter tuning, feature selection, and deployment concepts.

## Project Goal

Phishing websites attempt to impersonate legitimate services in order to steal sensitive information such as usernames, passwords, and financial data.

The goal of this project is to build a supervised machine learning system that classifies websites as:

- **Phishing (`-1`)**
- **Legitimate (`1`)**

## Dataset

The project uses a phishing website dataset obtained from Kaggle.

- **11,054 website samples**
- **30 original website features**
- Numerical feature values encoded mainly as `-1`, `0`, and `1`
- Target column: `class`
- Identifier column `Index` was removed before model training

Examples of original features include URL length, HTTPS usage, subdomains, anchor URL behavior, website traffic, page rank, server form handler behavior, links in script tags, and domain-related indicators.

## Feature Engineering

Three additional features were created from the original website characteristics:

- **Suspicion Score**: counts the number of `-1` values
- **Safe Score**: counts the number of `1` values
- **Neutral Score**: counts the number of `0` values

The target column and the `Index` identifier are excluded from these calculations to prevent leakage.

## Machine Learning Models

Five models were evaluated:

- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Isolation Forest

The models were evaluated using accuracy, precision, recall, F1-score, and confusion matrices.

## Model Comparison

| Model | Weighted F1 Score |
|---|---:|
| Logistic Regression | 0.9403 |
| Random Forest | **0.9737** |
| SVM | 0.9629 |
| KNN | 0.9448 |
| Isolation Forest | 0.4774 |

**Random Forest achieved the strongest baseline performance.**

## Hyperparameter Tuning

Random Forest was optimized using `RandomizedSearchCV`.

After tuning:

- **Accuracy:** approximately `0.9747`
- **Weighted F1-score:** approximately `0.9746`

The tuned model produced the following confusion matrix using the class order `[-1, 1]`:

```text
[[ 942,  37],
 [  19, 1213]]
```

This means the final model correctly classified the large majority of both phishing and legitimate websites.

## Feature Selection

Feature importance from the tuned Random Forest model was used to select the **15 most important features**.

The reduced model achieved:

- **Weighted F1-score:** approximately `0.9692`

This shows that the model can retain strong predictive performance while using fewer input features.

## Repository Structure

```text
Phishing-Website-Detection-ML/
│
├── data/
│   ├── phishing.csv
│   └── phishing_processed.csv
│
├── notebook/
│   └── Phishing_Website_Detection_Final.ipynb
│
├── results/
│   ├── FINAL_RESULTS.txt
│   ├── model_comparison.csv
│   ├── model_comparison.png
│   ├── tuned_random_forest_metrics.csv
│   ├── tuned_rf_confusion_matrix.png
│   ├── best_random_forest_parameters.json
│   ├── feature_importance.csv
│   ├── feature_importance_top15.png
│   ├── feature_selection_metrics.csv
│   └── selected_top15_features.txt
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Google Colab

## Installation

Clone the repository:

```bash
git clone <YOUR-REPOSITORY-URL>
cd Phishing-Website-Detection-ML
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Running the Project

Open:

```text
notebook/Phishing_Website_Detection_Final.ipynb
```

Run the notebook from top to bottom.

The notebook performs the complete pipeline:

1. Loads and inspects the dataset
2. Removes the identifier column
3. Creates engineered features
4. Explicitly defines `class` as the target
5. Performs an 80/20 train-test split
6. Trains and evaluates multiple models
7. Tunes Random Forest
8. Calculates feature importance
9. Retrains the model using the top 15 features
10. Reports final evaluation results

## Key Findings

- Random Forest was the best-performing baseline model.
- Hyperparameter tuning slightly improved performance further.
- SVM also performed strongly.
- Feature selection reduced dimensionality while preserving most of the model's performance.
- Isolation Forest performed significantly worse because this task is primarily a supervised binary classification problem rather than a pure anomaly-detection problem.

## Real-World Deployment Concept

A trained phishing detection model could be integrated into:

- **Browser extensions** to analyze websites before users visit them
- **Email security systems** to inspect suspicious links
- **SIEM or IDS workflows** to enrich alerts with phishing predictions
- **Web APIs** that return phishing risk predictions to other applications

A production deployment would require a real-time feature extraction pipeline capable of generating the same features used during model training.

## Limitations

- Performance depends on the characteristics and age of the training dataset.
- Real phishing techniques evolve over time.
- The current project uses predefined structured features rather than analyzing raw webpage content directly.
- The model is currently evaluated offline and is not deployed in a live production environment.

## Future Work

Possible improvements include:

- Training on newer and more diverse phishing datasets
- Testing additional ensemble and boosting algorithms
- Adding URL lexical and domain intelligence features
- Building a real-time prediction API
- Integrating the model with a browser extension or SOC monitoring workflow
- Monitoring model performance over time to detect concept drift

## Conclusion

This project demonstrates how machine learning can be applied to phishing detection through a complete and reproducible workflow.

The final tuned Random Forest achieved a **weighted F1-score of approximately 0.9746**, while feature selection showed that strong performance can still be maintained with a smaller set of high-value features.

The project connects machine learning experimentation with a practical cybersecurity use case and realistic deployment concepts.
