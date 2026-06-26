import re

class SafetyService:
    @staticmethod
    def sanitize_customer_reply(text: str, is_bangla: bool = False) -> str:
        """
        Scans and sanitizes the customer reply to guarantee compliance with all safety rules.
        """
        if not text:
            return ""

        # 1. Credentials Requests Checks (PIN/OTP/passwords/cards)
        # Avoid matching warning phrases like "do not share PIN" by using negative lookbehinds
        unsafe_creds = [
            r"share your otp", r"provide otp", r"send otp", r"share pin", r"provide pin",
            r"password", r"full card number", r"verification code", r"secret credential",
            r"ওটিপি দিন", r"পিন দিন", r"পাসওয়ার্ড দিন", r"ওটিপি চান", r"পিন বলুন",
            r"ওটিপি শেয়ার করুন", r"পিন শেয়ার করুন",
            r"\b(?:ask|provide|tell|send|enter|input|give)\b.*\b(?:pin|otp|password|passcode|card number)\b",
            r"(?<!not )(?<!never )share.*(?:pin|otp)",
            r"\b(?:পিন|ওটিপি|পাসওয়ার্ড|কার্ড নম্বর)\b.*\b(?:দিন|বলুন|পাঠান|শেয়ার করুন|চাই)\b"
        ]
        
        has_cred_violation = False
        text_lower = text.lower()
        for pattern in unsafe_creds:
            if re.search(pattern, text_lower):
                has_cred_violation = True
                break
                
        if has_cred_violation:
            # Overwrite with strict safety warning
            if is_bangla:
                text = "আমরা কখনোই আপনার পিন বা ওটিপি চাই না। অনুগ্রহ করে কারো সাথে এগুলো শেয়ার করবেন না।"
            else:
                text = "We will never ask for your PIN, OTP, or password. Please do not share these details with anyone."

        else:
            # 2. Refund / Reversal Confirmation Checks
            unsafe_promises = [
                r"we will refund", r"refund confirmed", r"reversal confirmed", r"we will reverse",
                r"account unblocked", r"money recovered", r"টাকা ফেরত দেওয়া হবে নিশ্চিত", r"রিফান্ড নিশ্চিত",
                r"\bwe\b.*\b(?:refund|reverse|unblock|recover|credit)\b",
                r"\b(?:refund|reversal|unblock|recovery)\b.*\b(?:will be|is|has been|confirmed|initiated|completed)\b",
                r"\bwill refund you\b",
                r"\bwill reverse the\b",
                r"টাকা ফেরত (?:দেওয়া হবে|দিচ্ছি|দেবো)",
                r"রিফান্ড করে (?:দেওয়া হবে|দেবো|দিচ্ছি)",
                r"অ্যাকাউন্ট আনব্লক (?:করা হবে|হবে)"
            ]
            
            has_promise_violation = False
            for pattern in unsafe_promises:
                if re.search(pattern, text_lower):
                    has_promise_violation = True
                    break
                    
            if has_promise_violation:
                # Override with safe policies
                if is_bangla:
                    text = "আপনার অভিযোগটি সফলভাবে নথিভুক্ত করা হয়েছে। যেকোনো যোগ্য পরিমাণ অফিশিয়াল চ্যানেলের মাধ্যমে ফেরত দেওয়া হবে। অনুগ্রহ করে কারো সাথে আপনার পিন বা ওটিপি শেয়ার করবেন না।"
                else:
                    text = "We have received your concern. any eligible amount will be returned through official channels. Please do not share your PIN or OTP with anyone."

            else:
                # 3. Directing to suspicious third parties (e.g. Unofficial links, Telegram, WhatsApp)
                unsafe_third_parties = [
                    r"\b(?:telegram|whatsapp|viber|imo|facebook|messenger)\b",
                    r"\b(?:হোয়াটসঅ্যাপ|টেলিগ্রাম|ভাইবার|ইমো|মেসেঞ্জার|ফেসবুক)\b",
                    r"https?://(?!bkash\.com|queuestorm\.com)\S+",
                    r"t\.me/\S+",
                    r"bit\.ly/\S+",
                    r"\bcontact.*(?:unofficial|third-party|support-desk|external-agent)\b"
                ]
                
                has_third_party_violation = False
                for pattern in unsafe_third_parties:
                    if re.search(pattern, text_lower):
                        has_third_party_violation = True
                        break
                        
                if has_third_party_violation:
                    if is_bangla:
                        text = "অনুগ্রহ করে কেবল আমাদের অফিশিয়াল সাপোর্ট চ্যানেলের মাধ্যমে যোগাযোগ করুন। যেকোনো অন্য লিংক বা যোগাযোগ মাধ্যম এড়িয়ে চলুন।"
                    else:
                        text = "Please only contact us through our official support channels. Do not click on external links or contact unofficial groups."

        # 4. Add missing safety disclaimers
        en_disclaimer = "Please do not share your PIN or OTP with anyone."
        bn_disclaimer = "অনুগ্রহ করে কারো সাথে আপনার পিন বা ওটিপি শেয়ার করবেন না।"
        
        if is_bangla:
            if bn_disclaimer not in text:
                text = f"{text.rstrip('. ')}. {bn_disclaimer}"
        else:
            if en_disclaimer not in text:
                text = f"{text.rstrip('. ')}. {en_disclaimer}"

        return text

    @staticmethod
    def sanitize_recommended_next_action(text: str) -> str:
        """
        Sanitizes internal next actions to prevent agents from promising unauthorized refunds.
        """
        if not text:
            return ""
            
        unsafe_directives = [
            r"\b(?:refund|reverse|unblock)\b.*\b(?:now|immediately|confirm|promise)\b",
            r"\b(?:initiate|process|complete)\b.*\b(?:refund|reversal)\b",
            r"refund confirmed", r"reversal confirmed"
        ]
        
        has_violation = False
        text_lower = text.lower()
        for pattern in unsafe_directives:
            if re.search(pattern, text_lower):
                has_violation = True
                break
                
        if has_violation:
            return "Verify transaction details and initiate the appropriate dispute workflow per company policy. Do not promise direct refunds."
            
        return text
