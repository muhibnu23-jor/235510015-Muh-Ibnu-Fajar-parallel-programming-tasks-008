from dask_ml.datasets import make_classification
from dask_ml.model_selection import train_test_split
from dask_ml.linear_model import LogisticRegression
from dask.distributed import Client
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    client = Client(processes=False)

    print("Generating dataset...")
    X, y = make_classification(
        n_samples=20000,
        n_features=20,
        chunks=2000
    )

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3
    )

    print("Training Logistic Regression...")
    model = LogisticRegression(solver="lbfgs")
    model.fit(X_train, y_train)

    print("Predicting...")
    y_pred = model.predict(X_test)

    y_test = y_test.compute()
    y_pred = y_pred.compute()

    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
