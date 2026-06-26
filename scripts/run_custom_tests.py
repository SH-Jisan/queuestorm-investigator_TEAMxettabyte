import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_custom_cases():
    test_cases = [
        {
            "id": "CUSTOM-01",
            "language_group": "English",
            "label": "Wrong Transfer (Consistent)",
            "payload": {
                "ticket_id": "TKT-ENG-01",
                "complaint": "I made a mistake and sent 3000 taka to 01712345678 instead of my friend's number today. Please refund.",
                "language": "en",
                "channel": "in_app_chat",
                "user_type": "customer",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-WT-99",
                        "timestamp": "2026-06-26T14:30:00Z",
                        "type": "transfer",
                        "amount": 3000,
                        "counterparty": "+8801712345678",
                        "status": "completed"
                    }
                ]
            }
        },
        {
            "id": "CUSTOM-02",
            "language_group": "Bangla",
            "label": "Payment Failed (Consistent)",
            "payload": {
                "ticket_id": "TKT-BN-02",
                "complaint": "আমার মোবাইল রিচার্জ ব্যর্থ হয়েছে কিন্তু অ্যাকাউন্ট থেকে ৫০০ টাকা কেটে নেওয়া হয়েছে। সাহায্য করুন।",
                "language": "bn",
                "channel": "in_app_chat",
                "user_type": "customer",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-PF-44",
                        "timestamp": "2026-06-26T15:20:00Z",
                        "type": "payment",
                        "amount": 500,
                        "counterparty": "MERCHANT-RECHARGE",
                        "status": "failed"
                    }
                ]
            }
        },
        {
            "id": "CUSTOM-03",
            "language_group": "Banglish",
            "label": "Duplicate Payment (Consistent)",
            "payload": {
                "ticket_id": "TKT-BGL-03",
                "complaint": "amar double payment hoye gese, 1500 taka duibar kete nise merchant account e. please return korben.",
                "language": "en",
                "channel": "in_app_chat",
                "user_type": "customer",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-DUP-01",
                        "timestamp": "2026-06-26T10:00:00Z",
                        "type": "payment",
                        "amount": 1500,
                        "counterparty": "MERCHANT-SHOP",
                        "status": "completed"
                    },
                    {
                        "transaction_id": "TXN-DUP-02",
                        "timestamp": "2026-06-26T10:03:00Z",
                        "type": "payment",
                        "amount": 1500,
                        "counterparty": "MERCHANT-SHOP",
                        "status": "completed"
                    }
                ]
            }
        },
        {
            "id": "CUSTOM-04",
            "language_group": "Safety / Phishing (English)",
            "label": "Phishing Attempt / OTP request warning",
            "payload": {
                "ticket_id": "TKT-SAFE-04",
                "complaint": "Someone called me claiming to be from customer support and asked for my PIN and OTP. They said my account is blocked.",
                "language": "en",
                "channel": "in_app_chat",
                "user_type": "customer",
                "transaction_history": []
            }
        }
    ]

    print("=" * 80)
    print("RUNNING 4 CUSTOM TEST SCENARIOS (English, Bangla, Banglish, Safety)")
    print("=" * 80)

    for case in test_cases:
        print(f"\n[+] ID: {case['id']} | Language: {case['language_group']} | Scenario: {case['label']}")
        print(f"    - Complaint Text: \"{case['payload']['complaint']}\"")
        
        response = client.post("/analyze-ticket", json=case['payload'])
        if response.status_code != 200:
            print(f"    [-] Request failed with status code {response.status_code}: {response.text}")
            continue

        res = response.json()
        print(f"    [Expected & Actual Output Summary]")
        print(f"      * relevant_transaction_id : {res['relevant_transaction_id']}")
        print(f"      * evidence_verdict        : {res['evidence_verdict']}")
        print(f"      * case_type               : {res['case_type']}")
        print(f"      * department              : {res['department']}")
        print(f"      * severity                : {res['severity']}")
        print(f"      * human_review_required   : {res['human_review_required']}")
        print(f"      * agent_summary           : {res['agent_summary']}")
        print(f"      * recommended_next_action : {res['recommended_next_action']}")
        print(f"      * customer_reply          : {res['customer_reply']}")
        print("-" * 80)

if __name__ == "__main__":
    run_custom_cases()
