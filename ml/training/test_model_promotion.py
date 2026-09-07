import os
import shutil
import joblib

import automatic_retraining


TEST_DIR = r"E:\SmartPulse\ml\models\promotion_test"

TEST_MODEL_DIR = os.path.join(
    TEST_DIR,
    "retrained_model"
)

TEST_BACKUP_DIR = os.path.join(
    TEST_DIR,
    "model_backup"
)

os.makedirs(
    TEST_MODEL_DIR,
    exist_ok=True
)

os.makedirs(
    TEST_BACKUP_DIR,
    exist_ok=True
)


original_current_model_path = (
    automatic_retraining.CURRENT_MODEL_PATH
)

original_current_scaler_path = (
    automatic_retraining.CURRENT_SCALER_PATH
)

original_backup_dir = (
    automatic_retraining.BACKUP_MODEL_DIR
)


test_current_model_path = os.path.join(
    TEST_DIR,
    "current_model.pkl"
)

test_current_scaler_path = os.path.join(
    TEST_DIR,
    "current_scaler.pkl"
)


test_new_model_path = os.path.join(
    TEST_MODEL_DIR,
    "failure_prediction_model.pkl"
)

test_new_scaler_path = os.path.join(
    TEST_MODEL_DIR,
    "feature_scaler.pkl"
)


test_backup_model_path = os.path.join(
    TEST_BACKUP_DIR,
    "failure_prediction_model_backup.pkl"
)

test_backup_scaler_path = os.path.join(
    TEST_BACKUP_DIR,
    "feature_scaler_backup.pkl"
)


print("=" * 80)
print("SMARTPULSE MODEL PROMOTION SAFETY TEST")
print("=" * 80)


print("\nSTEP 1 - Creating temporary test environment")
print("-" * 80)

shutil.copy2(
    original_current_model_path,
    test_current_model_path
)

shutil.copy2(
    original_current_scaler_path,
    test_current_scaler_path
)

shutil.copy2(
    original_current_model_path,
    test_new_model_path
)

shutil.copy2(
    original_current_scaler_path,
    test_new_scaler_path
)

automatic_retraining.CURRENT_MODEL_PATH = (
    test_current_model_path
)

automatic_retraining.CURRENT_SCALER_PATH = (
    test_current_scaler_path
)

automatic_retraining.BACKUP_MODEL_DIR = (
    TEST_BACKUP_DIR
)


print("Temporary model created.")
print("Temporary scaler created.")


print("\nSTEP 2 - Testing backup and promotion")
print("-" * 80)

backup_model, backup_scaler = (
    automatic_retraining.promote_new_model(
        test_new_model_path,
        test_new_scaler_path
    )
)


print("\nSTEP 3 - Verifying backup files")
print("-" * 80)

if not os.path.exists(backup_model):
    raise RuntimeError(
        "TEST FAILED: Backup model was not created."
    )

if not os.path.exists(backup_scaler):
    raise RuntimeError(
        "TEST FAILED: Backup scaler was not created."
    )

print("Backup model exists.")
print("Backup scaler exists.")


print("\nSTEP 4 - Verifying promoted files")
print("-" * 80)

if not os.path.exists(test_current_model_path):
    raise RuntimeError(
        "TEST FAILED: Promoted model does not exist."
    )

if not os.path.exists(test_current_scaler_path):
    raise RuntimeError(
        "TEST FAILED: Promoted scaler does not exist."
    )

joblib.load(
    test_current_model_path
)

joblib.load(
    test_current_scaler_path
)

print("Promoted model can be loaded.")
print("Promoted scaler can be loaded.")


print("\nSTEP 5 - Restoring original configuration")
print("-" * 80)

automatic_retraining.CURRENT_MODEL_PATH = (
    original_current_model_path
)

automatic_retraining.CURRENT_SCALER_PATH = (
    original_current_scaler_path
)

automatic_retraining.BACKUP_MODEL_DIR = (
    original_backup_dir
)


print("Original configuration restored.")


print("\nSTEP 6 - Cleaning temporary test files")
print("-" * 80)

shutil.rmtree(
    TEST_DIR,
    ignore_errors=True
)

print("Temporary test directory removed.")


print("\n" + "=" * 80)
print("MODEL PROMOTION SAFETY TEST PASSED")
print("=" * 80)