# --------------------------
# FORM FIELD MAPS
# --------------------------

NY_DL_FIELD_MAP = {
    "lastName": "FULL LAST NAME",
    "firstName": "FULL FIRST NAME",
    "middleName": "FULL MIDDLE NAME",
    "suffix": "SUFFIX",
    "dateOfBirthMonth": "DATE OF BIRTH Month",
    "dateOfBirthDay": "DATE OF BIRTH Day",
    "dateOfBirthYear": "DATE OF BIRTH Year",
    "sex": "SEX",
    "eyeColor": "EYE COLOR",
    "hairColor": "HAIR COLOR",
    "height": "Feet",
    "weight": "WEIGHT",
    "dlIdNumber": "ID Identification NUMBER ON NEW YORK STATE DRIVER LICENSE LEARNER PERMIT or NONDRIVER ID Identification CARD",
    "dlStateCountry": "Out of State License ID Identification No Number",
    "idPurpose": "PURPOSE FOR APPLICATION",
    "dateOfExpiration": "Date of Expiration",
    "ssn": "SOCIAL SECURITY NUMBER SSN",
    "signatureForNoSSN": "If you have never been issued a Social Security Number",
    "signatureDateForNoSSN": "Signature Date for No SSN",
    "liveAddress": "ADDRESS WHERE YOU LIVE REQUIRED IF DIFFERENT FROM ADDRESS FOR MAIL",
    "applicantSignature": "PLEASE PRINT NAME",
    "applicantSignatureDate": "Date",
    "registerToVote": "If you are not registered to vote where you live now would you like to apply to register",
    "donateLifeRegistry": "Would you like to be added to the Donate Life Registry",
    "veteranStatus": "Check this box if you would like to have Veteran printed on the front",
}

CA_DL_FIELD_MAP = {
    "dlIdNumber": "Driver LicenseORID Card Number",
    "dlStateCountry": "StateORCountry",
    "ssn": "DOCUMENT#",
    "firstName": "TextField",
    "middleName": "Middle Name",
    "lastName": "Last Name",
    "suffix": "Suffx(Jr , Sr , III)",
    "mailingAddress": "TextField_1",
    "liveAddress": "TextField_2",
    "hairColor": "HairColor",
    "eyeColor": "TextField_3",
    "height": "TextField_4",
    "weight": "TextField_5",
    "signatureForNoSSN": "Mother’s/Guardian’sSignatureCOX",
    "signatureDateForNoSSN": "Date",
    "questionBDate": "indicate date and reason below",
    "questionBReason": "TextField_6",
    "questionCDetails": "briefy explain",
    "registerToVote": ("toanewcounty—Completetheattached voterform.", "Yes"),
    "motherSignature": "Mother’s/Guardian’sSignatureCOX",
    "motherSignatureDate": "Date",
    "fatherSignature": "Father’s/Guardian’s SignatureX",
    "fatherSignatureDate": "Date_1",
    "applicantSignature": "Text1",
    "applicantSignatureDate": "Date_2",
    "applicantPhoneArea": "Daytime Phone Number()",
    "applicantPhoneNumber": "Text2",
    "idPurpose": "ID CARD",

    # ✅ Checkbox mappings
    "eat": ("CheckBox_22", "Yes"),
    "neat": ("CheckBox_23", "Yes"),
    "peat": ("CheckBox_24", "Yes"),
    "cret": ("CheckBox_25", "Yes"),
}





PASSPORT_FIELD_MAP = {
    "firstName": "Given Name",
    "lastName": "Surname",
    "middleName": "Middle Name",
    "dob": "Date of Birth",
    "sex": "Sex",
    "placeOfBirth": "Place of Birth",
    "passportNumber": "Passport Number",
    "issueDate": "Date of Issue",
    "expiryDate": "Date of Expiry",
    "ssn": "Social Security Number",
    "mailingAddress": "Mailing Address",
    "applicantSignature": "Applicant Signature",
    "applicantSignatureDate": "Signature Date",
}


PASSPORT_DS11_FIELD_MAP = {
    # Applicant Info
    "first_name": "Applicant First Name",
    "middle_name": "Applicant Middle Name",
    "last_name": "Applicant Last Name",
    "dob_day": "Applicant DOB D",
    "dob_month": "Applicant DOB M",
    "dob_year": "Applicant DOB Y",
    "dob_full": "Applicant DOB 2",
    "place_of_birth": "Applicant Place of Birth",
    "ssn_1": "Applicant SSN 1",
    "ssn_2": "Applicant SSN 2",
    "ssn_3": "Applicant SSN 3",
    "email": "Applicant Email",
    "phone_1": "Applicant Phone 1",
    "phone_2": "Applicant Phone 2",
    "phone_3": "Applicant Phone 3",
    "extra_contact": "Applicant Additional Contact Phone Numbers",

    # Address
    "address_street": "Applicant Address Street",
    "address_city": "Applicant Address City",
    "address_state": "Applicant Address State",
    "address_zip": "Applicant Address Zip Code",
    "address_country": "Applicant Address Country",
    "address_line2": "Address Line 2",

    # Permanent Address
    "perm_street": "Permanent Address Street",
    "perm_apartment": "Permanent Address Apartment/Unit",
    "perm_city": "Permanent Address City",
    "perm_state": "Permanent Address State",
    "perm_zip": "Permanent Address Zip Code",

    # Passport/Book/Card status
    "book_lost": "Book Status Lost",
    "book_stolen": "Book Status Stolen",
    "book_possession": "Book Status Possession",
    "book_submitting": "Book Status Submitting",
    "card_lost": "Card Status Lost",
    "card_stolen": "Card Status Stolen",
    "card_possession": "Card Status Possession",
    "card_submitting": "Card Status Submitting",
    "lost_circumstances": "Circumstances of lost/stolen book/card",

    # Travel
    "travel_departure": "Travel Departure Date",
    "travel_return": "Travel Return Date",
    "countries_to_visit": "Countries to be visited",

    # Physical description
    "gender": "Gender",
    "height": "Height",
    "eye_color": "Eye Color",
    "hair_color": "Hair Color",

    # Marital Status
    "ever_married": "Ever Married",
    "divorced": "Divorced",
    "marriage_date": "Date of Marriage (mm/dd/yyyy)",
    "widow_divorce_date": "Widow/Divorce Date (mm/dd/yyyy)",
    "current_spouse_name": "Full Name of Current Spouse or Most Recent Spouse (Last, first, Middle)",
    "current_spouse_dob": "Current Spouse Date of Birth",
    "current_spouse_birthplace": "Current Spouse Place of Birth",
    "spouse_us_citizen": "Spouse US Citizen",

    # Parents
    "parent1_last_name": "Parent 1 Last Name",
    "parent1_first_middle": "Parent 1 FM Name",
    "parent1_dob": "Parent 1 DOB",
    "parent1_birthplace": "Parent 1 Place of Birth",
    "parent1_gender": "Parent 1 Gender",
    "parent1_us_citizen": "Parent 1 US Citizen",

    "parent2_last_name": "Parent 2 Last Name",
    "parent2_first_middle": "Parent 2 FM Name",
    "parent2_dob": "Parent 2 DOB",
    "parent2_birthplace": "Parent 2 Place of Birth",
    "parent2_gender": "Parent 2 Gender",
    "parent2_us_citizen": "Parent 2 US Citizen",

    # Emergency Contact
    "emergency_name": "Emergency Contact Name",
    "emergency_phone": "Emergency Contact Phone",
    "emergency_address": "Emergency Contact Address",
    "emergency_apartment": "Emergency Contact Apartment/Unit",
    "emergency_city": "Emergency Contact City",
    "emergency_state": "Emergency Contact State",
    "emergency_zip": "Emergency Contact Zip Code",
    "emergency_relationship": "Relationship to Applicant",

    # Work / School
    "occupation": "Occupation",
    "employer_or_school": "Employer or School",

    # Other names used
    "other_name_1": "List all other name you have used",
    "other_name_2": "List all other names you have used",

    # Passport selection
    "regular_or_large_book": "Regular or Large Book",
    "selection": "Selection",
    "ever_applied": "Ever Applied or Issued",

    # Misc
    "name_on_passport_card": "Name as printed on your most recent passport card",
    "name_on_passport_book": "Your name as printed on your most recent U.S. passport book and/or passport card",
    "applicant2_name": "Name of Applicant 2",
}


PASSPORT_DS11_OPTIONS = {

    # Passport selection
    "Selection": "selection",                 # Options: Book, Card, Both
    "Regular or Large Book": "regular_or_large_book",  # Options: Regular, Large

    # Physical description
    "Gender": "gender",                        # Options: M, F

    # Parents
    "Parent 1 Gender": "parent1_gender",      # Options: M, F
    "Parent 1 US Citizen": "parent1_us_citizen",  # Options: Yes, No
    "Parent 2 Gender": "parent2_gender",      # Options: M, F
    "Parent 2 US Citizen": "parent2_us_citizen",  # Options: Yes, No

    # Marital status
    "Ever Married": "ever_married",           # Options: Yes, No
    "Spouse US Citizen": "spouse_us_citizen", # Options: Yes, No
    "Divorced": "divorced",                   # Options: Yes, No

    # Additional numbers
    "Additional #": "Additional #",           # Options: Home, Work, Cell, Other

    # Passport / Card history
    "Ever Applied or Issued": "ever_applied",        # Options: Yes, No
    "Book Status Submitting": "book_status_submitting",  # Options: Submitting
    "Book Status Stolen": "book_status_stolen",          # Options: Stolen
    "Book Status Lost": "book_status_lost",            # Options: Lost
    "Book Status Possession": "book_status_possession",  # Options: Possession
    "Card Status Submitting": "card_status_submitting",  # Options: Submitting
    "Card Status Stolen": "card_status_stolen",          # Options: Stolen
    "Card Status Lost": "card_status_lost",              # Options: Lost
    "Card Status Possession": "card_status_possession"   # Options: Possession


}


# Central registry
FORM_MAPS = {
    "PASSPORT_DS11": {
        "text": PASSPORT_DS11_FIELD_MAP,
        "choice": PASSPORT_DS11_OPTIONS
    },
    "NY_DL": {
        "text": NY_DL_FIELD_MAP,
        "choice": {}  # add later if needed
    },
    "CA_DL": {
        "text": CA_DL_FIELD_MAP,
        "choice": {}
    },
    "PASSPORT": {
        "text": PASSPORT_FIELD_MAP,
        "choice": {}
    }
}
