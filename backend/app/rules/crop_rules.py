"""
Configurable Agricultural Climate Risk Rules for TamilAgri AI.

DISCLAIMER & DEMO NOTICE:
-------------------------
The thresholds, hazard triggers, and recommendations defined below are DEMO rules
designed for hackathon demonstration purposes.
They do NOT guarantee crop damage or predict exact yield loss.

TODO: All agronomic thresholds below MUST be verified with official advisories from:
1. Tamil Nadu Agricultural University (TNAU) - Agronomy / Agromet Advisory Service (AAS)
2. India Meteorological Department (IMD) - District Agromet Units (DAMUs)
3. Department of Agriculture, Government of Tamil Nadu
"""

IS_DEMO_RULESET = True

# TODO: Verify Paddy (Oryza sativa) growth stage climate thresholds with TNAU Rice Expert System
PADDY_RISK_RULES = {
    "Nursery": {
        "Heavy Rainfall": {
            "high": {
                # TODO: Verify rainfall threshold with TNAU (Demo threshold: >50mm daily)
                "threshold_rainfall_mm": 50.0,
                "reason_en": "Heavy rain exceeds 50mm. Risk of seedling submergence, seed displacement, and root rot in nursery beds.",
                "reason_ta": "மழை 50மி.மீ-க்கு மேல் பதிவாக வாய்ப்புள்ளது. நாற்றங்கால் நீரில் மூழ்கி அழுகும் அல்லது நாற்றுகள் அடித்துச் செல்லப்படும் அபாயம் உள்ளது.",
                "precaution_en": "Immediately open field drainage channels to avoid standing water higher than seedling height. Cover young nursery beds if possible.",
                "precaution_ta": "நாற்றங்காலில் தேங்கும் உபரி நீரை உடனடியாக வடிகால் வழியாக வெளியேற்றவும். நாற்று மூழ்காமல் 2 செ.மீ அளவில் தண்ணீர் பராமரிக்கவும்."
            },
            "medium": {
                # TODO: Verify rainfall threshold with TNAU (Demo threshold: 25-50mm)
                "threshold_rainfall_mm": 25.0,
                "reason_en": "Moderate to heavy rain (25-50mm) may cause water saturation in nursery beds.",
                "reason_ta": "மிதமான முதல் கனமழை (25-50மி.மீ) காரணமாக நாற்றங்காலில் நீர் தேங்க வாய்ப்புள்ளது.",
                "precaution_en": "Ensure unobstructed drainage bunds. Avoid applying nitrogen fertilizers right before rainfall.",
                "precaution_ta": "வடிகால் வாய்க்கால்களை தூர்வாரி வைக்கவும். மழைக்கு முன் தழைச்சத்து (யூரியா) உரம் இடுவதை தவிர்க்கவும்."
            },
            "low": {
                "reason_en": "Rainfall conditions are within normal nursery limits.",
                "reason_ta": "மழைப்பொழிவு நாற்றங்கால் பருவத்திற்கு பாதுகாப்பான அளவிலேயே உள்ளது.",
                "precaution_en": "Maintain normal thin water layer (2-3 cm) in nursery beds.",
                "precaution_ta": "நாற்றங்காலில் வழக்கமான 2-3 செ.மீ அளவு நீர்மட்டத்தை பராமரிக்கவும்."
            }
        },
        "Extreme Heat": {
            "high": {
                # TODO: Verify maximum temperature threshold with TNAU (Demo threshold: >38°C)
                "threshold_temp_c": 38.0,
                "reason_en": "Forecast maximum temperature exceeds 38°C. Risk of seedling leaf scorch, moisture depletion, and stunted root emergence.",
                "reason_ta": "வெப்பநிலை 38°C-க்கு மேல் பதிவாக வாய்ப்புள்ளது. நாற்று இலைகள் கருகும் மற்றும் ஈரப்பதம் விரைவாக வறண்டு போகும் அபாயம் உள்ளது.",
                "precaution_en": "Irrigate nursery during late evening or early morning. Keep standing water of 2-3 cm to cool root zone.",
                "precaution_ta": "அதிகாலையிலோ அல்லது மாலையிலோ நீர்பாசனம் செய்யவும். வேர்ப் பகுதியை குளிர்விக்க 2-3 செ.மீ நீர் தேக்கி வைக்கவும்."
            },
            "medium": {
                # TODO: Verify maximum temperature threshold with TNAU (Demo threshold: 35-38°C)
                "threshold_temp_c": 35.0,
                "reason_en": "Daytime temperatures are warm (35-38°C), causing elevated transpiration in young seedlings.",
                "reason_ta": "பகல் வெப்பநிலை (35-38°C) நாற்றுகளின் நீராவிப்போக்கை அதிகரிக்கும்.",
                "precaution_en": "Ensure frequent light watering. Avoid dry soil crusting.",
                "precaution_ta": "மண் வெடிக்காமல் இருக்க தொடர்ச்சியாக மிதமான நீர் பாய்ச்சவும்."
            },
            "low": {
                "reason_en": "Temperature is optimal for nursery growth.",
                "reason_ta": "வெப்பநிலை நாற்று வளர்ச்சிக்கு உகந்த அளவில் உள்ளது.",
                "precaution_en": "Follow standard water management.",
                "precaution_ta": "வழக்கமான பாசன முறையைத் தொடரவும்."
            }
        }
    },
    "Tillering": {
        "Heavy Rainfall": {
            "high": {
                # TODO: Verify threshold with TNAU Rice agronomists (Demo threshold: >65mm)
                "threshold_rainfall_mm": 65.0,
                "reason_en": "Heavy precipitation (>65mm) can submerge tillers, suppress effective tillering, and leach applied fertilizers.",
                "reason_ta": "கனமழை 65மி.மீ-க்கு மேல் பதிவாக வாய்ப்புள்ளது. தூர் கட்டும் பருவத்தில் பயிர் மூழ்கி தூர் எண்ணிக்கை குறையும், இட்ட உரங்கள் அடித்துச் செல்லப்படும்.",
                "precaution_en": "Facilitate rapid field de-watering. Postpone top-dressing fertilizers until heavy rains cease.",
                "precaution_ta": "வயலில் தேங்கும் தண்ணீரை உடனடியாக வடிக்கவும். மழை முடியும் வரை மேலுரம் இடுவதைத் தள்ளிவைக்கவும்."
            },
            "medium": {
                "threshold_rainfall_mm": 35.0,
                "reason_en": "Rainfall between 35-65mm may lead to temporary water stagnation in low-lying paddy patches.",
                "reason_ta": "35-65மி.மீ மழைப்பொழிவால் பள்ளமான நிலப்பரப்பில் தற்காலிக நீர் தேக்கம் ஏற்படலாம்.",
                "precaution_en": "Inspect bunds and clear excess water drains. Monitor for early leaf blast symptoms.",
                "precaution_ta": "வரப்புகளை பலப்படுத்தி வடிகால் வசதி செய்யவும். இலைக்கருகல் நோய் அறிகுறிகள் உள்ளதா என கண்காணிக்கவும்."
            },
            "low": {
                "reason_en": "Favorable rainfall for vegetative tillering stage.",
                "reason_ta": "தூர் கட்டும் பருவத்திற்கு சாதகமான மழைப்பொழிவு.",
                "precaution_en": "Maintain 3-5 cm shallow standing water.",
                "precaution_ta": "வயலில் 3-5 செ.மீ அளவு நீர் இருக்குமாறு பார்த்துக்கொள்ளவும்."
            }
        },
        "Extreme Heat": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >39°C)
                "threshold_temp_c": 39.0,
                "reason_en": "High heat (>39°C) reduces tiller initiation and causes physiological water stress.",
                "reason_ta": "கடும் வெப்பம் (39°C மேல்) தூர் வெடிப்பதை குறைக்கும் மற்றும் பயிரில் நீர்ச்சத்து பற்றாக்குறையை ஏற்படுத்தும்.",
                "precaution_en": "Maintain 5 cm standing water layer to buffer heat. Avoid spraying agrochemicals in peak noon hours.",
                "precaution_ta": "சூட்டைத் தணிக்க வயலில் 5 செ.மீ நீர் தேக்கி வைக்கவும். உச்சி வெயிலில் பூச்சி மருந்து தெளிப்பதைத் தவிர்க்கவும்."
            },
            "medium": {
                "threshold_temp_c": 36.0,
                "reason_en": "Elevated temperatures (36-39°C) accelerate soil water evaporation.",
                "reason_ta": "அதிகரித்த வெப்பநிலை (36-39°C) மண்ணில் உள்ள நீரை விரைவாக ஆவியாக்கும்.",
                "precaution_en": "Adopt alternate wetting and drying carefully; do not allow hairline cracks to widen.",
                "precaution_ta": "காய்ச்சலும் பாய்ச்சலுமாக நீர் பாய்ச்சவும்; நிலம் அதிகளவில் வெடிக்க விடக்கூடாது."
            },
            "low": {
                "reason_en": "Temperatures are within healthy limits for tillering.",
                "reason_ta": "வெப்பநிலை தூர் வளர்ச்சிக்கு இயல்பான அளவிலேயே உள்ளது.",
                "precaution_en": "Continue routine irrigation.",
                "precaution_ta": "வழக்கமான பாசனத்தை தொடரவும்."
            }
        }
    },
    "Flowering": {
        "Heavy Rainfall": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >40mm - critical stage!)
                "threshold_rainfall_mm": 40.0,
                "reason_en": "Flowering is the most sensitive stage. Heavy rainfall (>40mm) washes away pollen grains, leading to empty (chaffy) grains.",
                "reason_ta": "பூக்கும் பருவம் மிகவும் நுட்பமானது. கனமழை (40மி.மீ மேல்) மகரந்த தூள்களை அடித்துச் சென்று பதர் நெல் உருவாக வழிவகுக்கும்.",
                "precaution_en": "Ensure swift water disposal. Postpone any pesticide/fungicide sprays to prevent flower drop.",
                "precaution_ta": "வயலில் தேங்கும் நீரை வடிக்கவும். பூக்கள் கொட்டுவதைத் தவிர்க்க எந்தவித ரசாயன மருந்துகளையும் இப்போது தெளிக்க வேண்டாம்."
            },
            "medium": {
                "threshold_rainfall_mm": 20.0,
                "reason_en": "Rainfall (20-40mm) during morning anthesis (flowering hours 9am-12pm) can hinder pollination.",
                "reason_ta": "காலை 9 முதல் 12 மணி வரையிலான பூக்கும் நேரத்தில் மழை பெய்தால் மகரந்தச்சேர்க்கை பாதிக்கப்படலாம்.",
                "precaution_en": "Avoid walking through flowering crop or disturbing panicles during morning hours.",
                "precaution_ta": "காலை வேளையில் வயலுக்குள் சென்று பூத்த கதிர்களை அசைப்பதைத் தவிர்க்கவும்."
            },
            "low": {
                "reason_en": "Favorable dry conditions for panicle pollination.",
                "reason_ta": "மகரந்தச் சேர்க்கைக்கு உகந்த தட்பவெப்ப நிலை.",
                "precaution_en": "Maintain 4-5 cm water until flowering completes.",
                "precaution_ta": "பூக்கும் பருவம் முடியும் வரை வயலில் 4-5 செ.மீ நீர் தொடர்ந்து இருக்குமாறு செய்யவும்."
            }
        },
        "Extreme Heat": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >36°C causes spikelet sterility)
                "threshold_temp_c": 36.0,
                "reason_en": "Temperatures above 36°C during anthesis induce spikelet sterility (anther indehiscence), severely reducing grain set.",
                "reason_ta": "பூக்கும் தருணத்தில் 36°C-க்கு மேல் வெப்பம் நிலவினால் மலட்டுத்தன்மை ஏற்பட்டு கதிர்கள் பதராகும் அபாயம் அதிகம்.",
                "precaution_en": "Maintain continuous 5-7 cm standing water to lower microclimate temperature. Irrigate during evening.",
                "precaution_ta": "பயிர் சூழல் வெப்பத்தை குறைக்க வயலில் 5-7 செ.மீ நீர் தேக்கி வைக்கவும். மாலையில் குளிர்ந்த நீர் பாய்ச்சவும்."
            },
            "medium": {
                "threshold_temp_c": 34.0,
                "reason_en": "Temperatures between 34-36°C may cause mild pollen desiccation.",
                "reason_ta": "வெப்பநிலை 34-36°C வரை இருந்தால் மகரந்தத் துகள்கள் உலர்ந்து போகும் வாய்ப்புள்ளது.",
                "precaution_en": "Keep soil thoroughly saturated. Do not let crop suffer water deficit.",
                "precaution_ta": "மண்ணை எப்போதும் ஈரப்பதமாக வைத்திருக்கவும். பயிருக்கு நீர்த்தட்டுப்பாடு ஏற்படாமல் பார்த்துக் கொள்ளவும்."
            },
            "low": {
                "reason_en": "Temperatures are optimal for successful rice flowering.",
                "reason_ta": "பூக்கும் பருவத்திற்கு வெப்பநிலை சாதகமாக உள்ளது.",
                "precaution_en": "Maintain routine standing water.",
                "precaution_ta": "வழக்கமான நீர்மட்டத்தை பராமரிக்கவும்."
            }
        }
    },
    "Grain filling": {
        "Heavy Rainfall": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >50mm)
                "threshold_rainfall_mm": 50.0,
                "reason_en": "Heavy rains (>50mm) combined with grain weight increase risks of crop lodging and panicle blast.",
                "reason_ta": "கனமழையினால் (50மி.மீ மேல்) கதிர் பாரம் தாங்காமல் பயிர் சாய்ந்து அழுகும் மற்றும் குலைநோய் தாக்கும் அபாயம் உள்ளது.",
                "precaution_en": "Drain standing water immediately. Check field perimeter bunds to prevent external runoff intrusion.",
                "precaution_ta": "வயலில் தேங்கும் நீரை உடனே வெளியேற்றவும். வெளிநீர் உள்ளே வராதவாறு வரப்புகளை உயர்த்தவும்."
            },
            "medium": {
                "threshold_rainfall_mm": 25.0,
                "reason_en": "Moderate rain (25-50mm) may foster fungal growth in dense canopies.",
                "reason_ta": "25-50மி.மீ மழையானது பயிர்களிடையே பூஞ்சான தொற்று பரவ சாதகமாகலாம்.",
                "precaution_en": "Monitor ears for sheath rot or discoloration. Clear field corners for air circulation.",
                "precaution_ta": "கதிர்களில் பூஞ்சான அறிகுறிகள் உள்ளதா என கண்காணிக்கவும். நல்ல காற்றோட்டம் இருக்குமாறு பராமரிக்கவும்."
            },
            "low": {
                "reason_en": "Safe conditions for milk and dough grain development.",
                "reason_ta": "பால் பிடிக்கும் மற்றும் மணி முதிரும் தருணத்திற்கு சாதகமான சூழல்.",
                "precaution_en": "Maintain moist soil with intermittent shallow irrigation.",
                "precaution_ta": "மண் காயாமல் மிதமான ஈரம் இருக்குமாறு இடைவெளி விட்டு நீர் பாய்ச்சவும்."
            }
        },
        "Extreme Heat": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >38°C)
                "threshold_temp_c": 38.0,
                "reason_en": "High heat (>38°C) shortens grain-filling duration, leading to chalky, shriveled, or broken rice grains.",
                "reason_ta": "அதிக வெப்பம் (38°C மேல்) மணிகள் முதிர்வதை அவசரப்படுத்தி, சுருங்கிய மற்றும் உடைந்த அரிசி உருவாக காரணமாகும்.",
                "precaution_en": "Provide frequent light irrigation during early morning or late night to cool the soil.",
                "precaution_ta": "மண்ணைக் குளிர்விக்க அதிகாலையிலோ அல்லது இரவிலோ மிதமான நீர்ப்பாசனம் செய்யவும்."
            },
            "medium": {
                "threshold_temp_c": 35.0,
                "reason_en": "Warm temperatures (35-38°C) speed up grain drying prematurely.",
                "reason_ta": "35-38°C வெப்பநிலை தானியங்கள் முன்கூட்டியே காய்ந்துபோக வழிவகுக்கும்.",
                "precaution_en": "Do not drain water completely until 10-14 days before harvest.",
                "precaution_ta": "அறுவடைக்கு 10-14 நாட்களுக்கு முன்பு வரை வயலை முழுமையாக காயவிட வேண்டாம்."
            },
            "low": {
                "reason_en": "Favorable temperature for solid grain weight development.",
                "reason_ta": "நெல் மணிகள் திரட்சியாக வளர சாதகமான வெப்பநிலை.",
                "precaution_en": "Maintain standard soil moisture.",
                "precaution_ta": "சாதாரண ஈரப்பதத்தை பராமரிக்கவும்."
            }
        }
    },
    "Harvest": {
        "Heavy Rainfall": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >15mm - harvest is very sensitive to any rain)
                "threshold_rainfall_mm": 15.0,
                "reason_en": "Rainfall (>15mm) at harvest causes grain discoloration, in-panicle viviparous germination, and stalls machinery.",
                "reason_ta": "அறுவடையின் போது மழை (15மி.மீ மேல்) பெய்தால் கதிரிலேயே நெல் முளைத்துவிடும் மற்றும் இயந்திரங்கள் வயலில் இறங்க முடியாது.",
                "precaution_en": "Expedite harvest immediately if crop is ready before rains, or postpone combining until field dries. Shift harvested paddy to covered shelter.",
                "precaution_ta": "பயிர் முதிர்ந்திருந்தால் உடனே அறுவடை செய்யவும் அல்லது மழை நிற்கும் வரை ஒத்திவைக்கவும். அறுவடை செய்த நெல்லை தார்பாய் போட்டு மூடவும்."
            },
            "medium": {
                "threshold_rainfall_mm": 5.0,
                "reason_en": "Light showers (5-15mm) increase harvested grain moisture above safe storage levels.",
                "reason_ta": "லேசான மழை (5-15மி.மீ) நெல்லின் ஈரப்பதத்தை அதிகரித்து சேமிப்புக் காலத்தில் கெட்டுப்போக வழிவகுக்கும்.",
                "precaution_en": "Dry harvested grains to below 14% moisture immediately using dryers or clean tarpaulins.",
                "precaution_ta": "அறுவடை செய்த நெல்லை உடனடியாக தார்பாயில் பரப்பி 14% ஈரப்பதத்திற்குள் காயவைக்கவும்."
            },
            "low": {
                "reason_en": "Dry weather provides ideal harvesting conditions.",
                "reason_ta": "அறுவடை பணிக்கு மிகவும் சாதகமான வறண்ட வானிலை.",
                "precaution_en": "Proceed with routine harvesting and grain sun-drying.",
                "precaution_ta": "வழக்கமான அறுவடை மற்றும் நெல் உலர்த்தும் பணிகளை மேற்கொள்ளலாம்."
            }
        },
        "Extreme Heat": {
            "high": {
                # TODO: Verify threshold with TNAU (Demo threshold: >40°C)
                "threshold_temp_c": 40.0,
                "reason_en": "Extreme heat (>40°C) causes rapid sun-cracking of mature grains and severe heat exhaustion risk for farm workers.",
                "reason_ta": "கடும் வெயில் (40°C மேல்) முதிர்ந்த நெல்லில் கீறல்களை உண்டாக்கி அரவை திறனை குறைக்கும்; தொழிலாளர்களுக்கு வெப்ப பக்கவாதம் ஏற்படலாம்.",
                "precaution_en": "Operate harvesters in early morning (6 AM - 10 AM) or late afternoon. Keep hydration points in field.",
                "precaution_ta": "காலை 6 முதல் 10 மணி வரை அல்லது மாலை வேளையில் அறுவடை செய்யவும். தொழிலாளர்களுக்கு குடிநீர் வசதி செய்யவும்."
            },
            "medium": {
                "threshold_temp_c": 37.0,
                "reason_en": "Warm temperatures (37-40°C) may overheat stored bags if piled wet in open sun.",
                "reason_ta": "37-40°C வெயிலில் நெல் மூட்டைகளை நேரடியாக திறந்தவெளியில் அடுக்கி வைத்தால் வெப்பம் கூடும்.",
                "precaution_en": "Store bagged grain in aerated, shaded sheds.",
                "precaution_ta": "நெல் மூட்டைகளை நல்ல நிழலான மற்றும் காற்றோட்டமான கிடங்குகளில் சேமிக்கவும்."
            },
            "low": {
                "reason_en": "Moderate temperatures suitable for harvesting operations.",
                "reason_ta": "அறுவடை செய்வதற்கு உகந்த மிதமான தட்பவெப்ப நிலை.",
                "precaution_en": "Standard harvest schedule can be followed.",
                "precaution_ta": "வழக்கமான அறுவடை நேர அட்டவணையைப் பின்பற்றலாம்."
            }
        }
    }
}
