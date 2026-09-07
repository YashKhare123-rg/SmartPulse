from retraining_service import run_retraining


password = input("Enter MySQL password: ")

result = run_retraining(
    test_mode=True,
    db_password=password
)

print("=" * 80)
print("RETRAINING SERVICE TEST")
print("=" * 80)

print(f"Success     : {result['success']}")
print(f"Return Code : {result['return_code']}")

print("\nOUTPUT")
print("-" * 80)
print(result["output"])

if result["error"]:

    print("\nERROR")
    print("-" * 80)
    print(result["error"])