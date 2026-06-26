from app.services.safety_service import SafetyService

def test_safety_filter_credential_requests():
    unsafe_reply_en = "Please share your PIN so we can verify your account."
    safe_reply_en = SafetyService.sanitize_customer_reply(unsafe_reply_en, is_bangla=False)
    assert "never ask for your PIN" in safe_reply_en
    assert "Please do not share your PIN or OTP with anyone" in safe_reply_en

    unsafe_reply_bn = "আপনার ওটিপি দিন ভেরিফাই করার জন্য।"
    safe_reply_bn = SafetyService.sanitize_customer_reply(unsafe_reply_bn, is_bangla=True)
    assert "পিন" in safe_reply_bn and "ওটিপি" in safe_reply_bn and "না" in safe_reply_bn

def test_safety_filter_refund_promises():
    unsafe_promise = "We will refund your money within 2 hours."
    safe_promise = SafetyService.sanitize_customer_reply(unsafe_promise, is_bangla=False)
    assert "any eligible amount will be returned through official channels" in safe_promise
    assert "will refund" not in safe_promise

    unsafe_promise_bn = "আমরা আপনাকে ৫০০ টাকা রিফান্ড করে দেবো।"
    safe_promise_bn = SafetyService.sanitize_customer_reply(unsafe_promise_bn, is_bangla=True)
    assert "অফিশিয়াল চ্যানেলের মাধ্যমে ফেরত" in safe_promise_bn
    assert "রিফান্ড করে দেবো" not in safe_promise_bn

def test_safety_filter_next_action():
    unsafe_action = "Refund the customer immediately."
    safe_action = SafetyService.sanitize_recommended_next_action(unsafe_action)
    assert "Do not promise direct refunds" in safe_action

def test_safety_filter_suspicious_third_parties():
    unsafe_reply_en = "Please join our Telegram group at t.me/scam to resolve this."
    safe_reply_en = SafetyService.sanitize_customer_reply(unsafe_reply_en, is_bangla=False)
    assert "official support channels" in safe_reply_en
    assert "Telegram" not in safe_reply_en

    unsafe_reply_bn = "দয়া করে আমাদের হোয়াটসঅ্যাপ গ্রুপে জয়েন করুন সাহায্যের জন্য।"
    safe_reply_bn = SafetyService.sanitize_customer_reply(unsafe_reply_bn, is_bangla=True)
    assert "অফিশিয়াল সাপোর্ট চ্যানেলের" in safe_reply_bn
    assert "হোয়াটসঅ্যাপ" not in safe_reply_bn
