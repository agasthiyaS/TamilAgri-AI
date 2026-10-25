// TamilAgri AI - Unified Multilingual Translation System (English & Tamil)

export const LOCATIONS = {
  Thanjavur: { en: 'Thanjavur (Delta Hub)', ta: 'தஞ்சாவூர் (டெல்டா மையம்)' },
  Madurai: { en: 'Madurai (Southern)', ta: 'மதுரை (தென் மண்டலம்)' },
  Tiruchirappalli: { en: 'Tiruchirappalli', ta: 'திருச்சிராப்பள்ளி' },
  Thiruvarur: { en: 'Thiruvarur', ta: 'திருவாரூர்' },
  Nagapattinam: { en: 'Nagapattinam', ta: 'நாகப்பட்டினம்' },
  Coimbatore: { en: 'Coimbatore', ta: 'கோயம்புத்தூர்' },
  Cuddalore: { en: 'Cuddalore', ta: 'கடலூர்' },
  Salem: { en: 'Salem', ta: 'சேலம்' },
  Tirunelveli: { en: 'Tirunelveli', ta: 'திருநெல்வேலி' },
  Villupuram: { en: 'Villupuram', ta: 'விழுப்புரம்' },
};

export const GROWTH_STAGES = {
  Nursery: { en: 'Nursery (Seedling emergence)', ta: 'நாற்றங்கால் பருவம்' },
  Tillering: { en: 'Tillering (Vegetative branching)', ta: 'தூர் கட்டும் பருவம்' },
  Flowering: { en: 'Flowering (Anthesis & Pollination)', ta: 'பூக்கும் பருவம்' },
  'Grain filling': { en: 'Grain filling (Milk & Dough stage)', ta: 'பால் பிடிக்கும் / மணி முதிரும் பருவம்' },
  Harvest: { en: 'Harvest (Ripening & Threshing)', ta: 'அறுவடைப் பருவம்' },
};

export const HAZARDS = {
  'Heavy Rainfall': { en: 'Heavy Rainfall', ta: 'கனமழை' },
  'Extreme Heat': { en: 'Extreme Heat', ta: 'கடும் வெப்பம்' },
};

export const WEATHER_CONDITIONS = {
  'Clear Sky': { en: 'Clear Sky', ta: 'தெளிவான வானம்' },
  'Partly Cloudy': { en: 'Partly Cloudy', ta: 'பகுதி மேகமூட்டம்' },
  'Cloudy': { en: 'Cloudy', ta: 'மேகமூட்டம்' },
  'Light Rain': { en: 'Light Rain', ta: 'லேசான மழை' },
  'Light Showers': { en: 'Light Showers', ta: 'லேசான தூறல்' },
  'Moderate Rain': { en: 'Moderate Rain', ta: 'மிதமான மழை' },
  'Heavy Rain': { en: 'Heavy Rain', ta: 'கனமழை' },
  'Heavy Rainfall Alert': { en: 'Heavy Rainfall Alert', ta: 'கனமழை எச்சரிக்கை' },
  'Hot & Humid': { en: 'Hot & Humid', ta: 'வெப்பம் & ஈரப்பதம்' },
  'Extreme Heat Warning': { en: 'Extreme Heat Warning', ta: 'கடும் வெப்ப எச்சரிக்கை' },
  'Scattered Thunderstorms': { en: 'Scattered Thunderstorms', ta: 'இடியுடன் கூடிய மழை' },
};

export const STATUSES = {
  SIMULATED: { en: 'SIMULATED (Demo)', ta: 'மாதிரி (Demo)' },
  DELIVERED: { en: 'DELIVERED', ta: 'அனுப்பப்பட்டது' },
  FAILED: { en: 'FAILED', ta: 'தோல்வி' },
};

export function translateLocation(loc, lang = 'ta') {
  if (!loc) return '';
  const item = LOCATIONS[loc];
  return item ? (lang === 'ta' ? item.ta : item.en) : loc;
}

export function translateGrowthStage(stage, lang = 'ta') {
  if (!stage) return '';
  const item = GROWTH_STAGES[stage];
  return item ? (lang === 'ta' ? item.ta : item.en) : stage;
}

export function translateHazard(hazard, lang = 'ta') {
  if (!hazard) return '';
  const item = HAZARDS[hazard];
  return item ? (lang === 'ta' ? item.ta : item.en) : hazard;
}

export function translateWeatherCondition(condition, lang = 'ta') {
  if (!condition) return '';
  const item = WEATHER_CONDITIONS[condition];
  return item ? (lang === 'ta' ? item.ta : item.en) : condition;
}

export function translateStatus(status, lang = 'ta') {
  if (!status) return '';
  const item = STATUSES[status];
  return item ? (lang === 'ta' ? item.ta : item.en) : status;
}

export function translateCrop(crop, lang = 'ta') {
  if (crop === 'Paddy' || crop === 'Paddy (Rice)') {
    return lang === 'ta' ? 'நெல் பயிர்' : 'Paddy (Rice)';
  }
  return crop;
}

export const translations = {
  en: {
    // Brand & Navigation
    projectTitle: "TamilAgri AI",
    projectSubtitle: "Crop-Specific Climate Risk & Multilingual SMS Early Warning",
    navDashboard: "Dashboard",
    navRiskAnalysis: "Climate Risk Analysis",
    navRegistration: "Farmer Registration",
    navAlertHistory: "Alert History",
    navSettings: "Settings & Info",
    demoMode: "DEMO MODE",
    liveMode: "LIVE MODE",
    demoPillTooltip: "Running in zero-cost Demo Mode without real SMS charges",
    
    // Dashboard Stats & Badges
    statFarmers: "Registered Farmers",
    statFarmersBadge: "Active in SQLite",
    statHighRisk: "High Risk Conditions",
    statHighRiskBadge: "Flowering Submergence Hazard",
    statAlertsSent: "Alerts Dispatched",
    statAlertsBadge: "Simulated + Logged",
    statActiveCrop: "Monitored Crop",
    statCropBadge: "5 Growth Stages Configured",
    paddyCrop: "Paddy (Rice)",
    recentAlerts: "Recent Warning Dispatches",
    weatherOverview: "Agricultural Weather Snapshot",
    quickRiskAssessment: "Quick Risk Assessment",
    noAlertsYet: "No alerts generated yet. Trigger an alert from the Climate Risk Analysis page.",
    noFarmersYet: "No farmers registered yet.",
    viewAllFarmers: "View All Farmers",
    viewAllAlerts: "View Full Audit History",

    // Weather Risk Monitoring
    runWeatherMonitoring: "Run Weather Monitoring",
    monitoringInProgress: "Monitoring Weather & Risks...",
    monitoringComplete: "Weather risk-monitoring cycle completed successfully.",
    monitoringConflict: "Another monitoring cycle is already in progress. Please wait for it to complete.",
    monitoringError: "Failed to execute weather monitoring. Please check the backend connection.",
    monitoringCardTitle: "Automatic Weather Risk Monitoring",
    monitoringCardSubtitle: "Periodically evaluate forecasts for registered farmers, apply crop growth stage thresholds, and trigger multilingual warnings.",
    monitoringSummaryTitle: "Weather Risk Monitoring Summary",
    summaryFarmersChecked: "Farmers Checked",
    summaryRisksDetected: "Risks Detected",
    summaryAlertsSimulated: "Simulated SMS Alerts",
    summaryAlertsSent: "Genuinely Sent Alerts",
    summaryDuplicatesSuppressed: "Duplicate Alerts Suppressed",
    summaryFailures: "Failures",
    demoOnlyBadge: "Demo only — not delivered",
    lastRunAt: "Last Monitored",
    liveDispatchesSubtext: "Live gateway dispatches",
    guardActiveSubtext: "24-hour guard active",
    viewAllDispatches: "View All Dispatches",
    
    // Risk Analysis Page
    riskTitle: "Crop-Specific Climate Risk Evaluator",
    riskSubtitle: "Evaluate upcoming weather hazards against Paddy phenological growth stages using verified rule models.",
    selectLocation: "Select Location / District",
    selectStage: "Current Growth Stage",
    fetchAndAnalyze: "Fetch Forecast & Analyze Risk",
    analyzing: "Evaluating Rules...",
    overallRiskLevel: "Overall Risk Level",
    overallRiskLevelFor: "Overall Risk Level for",
    riskAssessmentTitle: "Risk Assessment",
    hazardBreakdown: "Hazard Evaluations",
    recommendedPrecautions: "Recommended Agricultural Precautions",
    forecastWindow: "Forecast Window",
    forecastSource: "Data Source",
    triggerWarningAlert: "Send SMS Warning to Farmers",
    disclaimerTitle: "Demo Model & Verification Notice",
    disclaimerText: "Thresholds are prototype demonstration rules. Agricultural practices must be verified with official TNAU advisories.",
    districtPlaceholder: "Or enter any Tamil Nadu district/taluk name...",
    cropThresholdNote: "Crop: Paddy (Oryza sativa) • Evaluated against rain & heat thresholds",
    registeredInArea: "registered in area",
    thresholdLabel: "Threshold:",
    reasonLabel: "Risk Explanation:",
    precautionLabel: "Precautionary Guidance:",
    advisoryBannerTitle: "TamilAgri AI Climate Advisory (Language Intelligence)",
    
    // Growth Stages
    stageNursery: "Nursery",
    stageTillering: "Tillering",
    stageFlowering: "Flowering",
    stageGrainFilling: "Grain filling",
    stageHarvest: "Harvest",
    
    // Hazards & Levels
    hazardRain: "Heavy Rainfall",
    hazardHeat: "Extreme Heat",
    hazardRainCard: "Heavy Rainfall Hazard",
    hazardHeatCard: "Extreme Heat Hazard",
    riskLow: "Low Risk",
    riskMedium: "Medium Risk",
    riskHigh: "High Risk",
    
    // Farmer Registration
    regTitle: "Farmer Registration",
    regSubtitle: "Enroll farmers to receive timely automated SMS weather warnings in their preferred language.",
    farmerName: "Farmer Full Name",
    mobileNumber: "Mobile Number (10 digits)",
    locationDistrict: "Location / Village / District",
    cropType: "Crop Type",
    growthStage: "Current Growth Stage",
    prefLang: "Preferred SMS Language",
    registerBtn: "Register Farmer",
    registering: "Registering...",
    farmerListTitle: "Enrolled Farmers Directory",
    deleteConfirm: "Are you sure you want to remove this farmer profile?",
    phoneValidationHelp: "Must be a 10-digit Indian mobile number (e.g., 9876543210).",
    farmerRegisteredSuccess: "Farmer registered successfully!",
    farmerLoadError: "Could not load farmers list.",
    farmerDeleteSuccess: "Farmer profile deleted.",
    farmerDeleteError: "Failed to remove farmer profile.",
    selectVillagePlaceholder: "Or specify village/taluk (e.g. Kumbakonam, Thanjavur)",
    namePlaceholder: "e.g., K. Selvakumar",
    loadingFarmers: "Loading farmers...",
    
    // Alert History
    historyTitle: "Alert & Warning Audit History",
    historySubtitle: "Chronological log of simulated and delivered SMS notifications with duplicate suppression.",
    colFarmer: "Farmer",
    colPhone: "Mobile",
    colLocation: "Location",
    colHazard: "Hazard",
    colRisk: "Risk Level",
    colCrop: "Crop",
    colLang: "Lang",
    colStatus: "Status",
    colSentAt: "Timestamp",
    colActions: "Actions",
    filterHazard: "All Hazards",
    filterRisk: "All Risks",
    filterStatus: "All Statuses",
    viewMessageBtn: "View SMS",
    refreshLogsBtn: "Refresh Logs",
    filterLabel: "Filters:",
    resetBtn: "Reset",
    loadingLogs: "Loading alert logs...",
    smsPayloadTitle: "SMS Payload Details",
    recipientLabel: "Recipient:",
    gatewayLabel: "Gateway:",
    
    // Settings
    settingsTitle: "System Configuration & Integration Status",
    settingsSubtitle: "Overview of adapter providers, credentials status, and agronomic rule bases.",
    systemHealth: "System Health Status",
    operatingMode: "Operating Mode",
    zeroCostSimEnv: "Zero-cost simulation environment",
    weatherProvider: "Weather Provider Adapter",
    smsProvider: "SMS Gateway Adapter",
    activeAdapterLabel: "Active adapter:",
    statusReady: "Ready",
    statusSimulated: "Simulated",
    statusConnected: "Connected",
    dbStorageLabel: "Database Storage",
    sqliteLocalFile: "SQLite (Local file tamilagri.db)",
    displayLanguageLabel: "Dashboard Display Language / மொழி",
    demoExplanation: "Demo Mode Operation",
    demoExplanationText: "TamilAgri AI is currently executing in Demo Mode. Weather forecasts are generated from representative Tamil Nadu district agromet datasets, and SMS messages are safely logged and stored without incurring carrier fees.",
    tnauVerificationHeader: "Agricultural Rule Verification Status",
    tnauVerificationText: "Initial rules for Paddy growth stages are based on agronomic thresholds for rainfall submergence, pollen wash, and heat-induced spikelet sterility. Integration with TNAU AAS API is ready via modular adapters.",
    configuredThresholdsLabel: "Configured Rule Thresholds (backend/app/rules/crop_rules.py):",
    thresholdNursery: "Heavy Rain > 50mm/day (submergence risk) | Heat > 38°C (seedling scorch)",
    thresholdTillering: "Heavy Rain > 65mm/day (tiller inhibition) | Heat > 39°C (transpiration stress)",
    thresholdFlowering: "Heavy Rain > 40mm/day (pollen wash) | Heat > 36°C (spikelet sterility)",
    thresholdGrainFilling: "Heavy Rain > 50mm/day (crop lodging) | Heat > 38°C (forced maturity & chalkiness)",
    thresholdHarvest: "Rain > 15mm/day (grain sprouting & machinery stall) | Heat > 40°C (grain sun-cracking)",
    apiDocsHeader: "FastAPI Interactive API Documentation",
    openSwagger: "Open Swagger UI (/docs)",
    
    // Common Actions & Modal
    cancel: "Cancel",
    confirmSend: "Confirm & Dispatch SMS",
    sending: "Sending...",
    close: "Close",
    successMsg: "Action completed successfully!",
    errorMsg: "An error occurred. Please check the backend connection.",
    forceResendLabel: "Force re-send (override 24h duplicate suppression)",
    chooseFarmerOption: "-- Choose registered farmer --",
    customMessageLabel: "Optional Custom Message Override (Leave blank for automated bilingual template)",
    customMessagePlaceholderTa: "தானியங்கி தமிழ் மாதிரி செய்தி பயன்படுத்தப்படும்...",
    customMessagePlaceholderEn: "Automatic English SMS template will be formatted...",
    tamilSmsPreviewTitle: "Tamil SMS Preview (தமிழ் முன்னறிவிப்பு)",
    englishSmsPreviewTitle: "English SMS Preview",
    generatingPreview: "Generating template preview...",
    demoGatewayNotice: "Simulated dispatch will be logged in the database without carrier SMS charges.",
    dispatchToast: "Alert dispatched to {name}! Status: [{status}] via {provider} adapter.",

    // Footer
    footerTitle: "TamilAgri AI — AI-Powered Crop-Specific Climate Risk Analysis & SMS Early Warning System.",
    footerSubtitle: "Designed for Hackathons • Tamil Nadu Agricultural University (TNAU) Agronomy Rules Demonstration • Clean Architecture",
  },
  
  ta: {
    // Brand & Navigation
    projectTitle: "தமிழ் அக்ரி AI",
    projectSubtitle: "பயிர் சார்ந்த காலநிலை இடர் பகுப்பாய்வு & பன்மொழி SMS முன்னெச்சரிக்கை",
    navDashboard: "முகப்பு பலகை",
    navRiskAnalysis: "காலநிலை இடர் பகுப்பாய்வு",
    navRegistration: "விவசாயிகள் பதிவு",
    navAlertHistory: "எச்சரிக்கை வரலாறு",
    navSettings: "அமைப்புகள் & தகவல்",
    demoMode: "மாதிரி முறை (DEMO)",
    liveMode: "நேரலை முறை (LIVE)",
    demoPillTooltip: "கட்டணமில்லா மாதிரி முறையில் இயங்குகிறது (SMS கட்டணமில்லை)",
    
    // Dashboard Stats & Badges
    statFarmers: "பதிவுசெய்த விவசாயிகள்",
    statFarmersBadge: "SQLite தரவுத்தளத்தில் உள்ளது",
    statHighRisk: "அதிக ஆபத்து நிலைமைகள்",
    statHighRiskBadge: "பூக்கும் பருவ நீரில் மூழ்குதல் இடர்",
    statAlertsSent: "அனுப்பப்பட்ட எச்சரிக்கைகள்",
    statAlertsBadge: "மாதிரி + பதிவு செய்யப்பட்டது",
    statActiveCrop: "கண்காணிக்கப்படும் பயிர்",
    statCropBadge: "5 வளர்ச்சிப் பருவங்கள் அமைக்கப்பட்டுள்ளன",
    paddyCrop: "நெல் பயிர்",
    recentAlerts: "சமீபத்திய எச்சரிக்கை தகவல்கள்",
    weatherOverview: "வேளாண் வானிலை நிலவரம்",
    quickRiskAssessment: "விரைவு இடர் மதிப்பீடு",
    noAlertsYet: "இதுவரை எச்சரிக்கைகள் எதுவும் அனுப்பப்படவில்லை. இடர் பகுப்பாய்வு பக்கத்தில் எச்சரிக்கையை அனுப்பலாம்.",
    noFarmersYet: "விவசாயிகள் யாரும் இன்னும் பதிவு செய்யப்படவில்லை.",
    viewAllFarmers: "அனைத்து விவசாயிகளையும் காண்க",
    viewAllAlerts: "முழு வரலாற்றுப் பதிவை காண்க",

    // Weather Risk Monitoring
    runWeatherMonitoring: "வானிலை இடர் கண்காணிப்பை இயக்கு",
    monitoringInProgress: "வானிலை & இடர்கள் கண்காணிக்கப்படுகிறது...",
    monitoringComplete: "வானிலை இடர் கண்காணிப்பு வெற்றிகரமாக முடிந்தது.",
    monitoringConflict: "மற்றொரு கண்காணிப்பு சுழற்சி தற்போது இயங்குகிறது. சிறிது நேரம் காத்திருக்கவும்.",
    monitoringError: "வானிலை கண்காணிப்பை இயக்க முடியவில்லை. சேவையக இணைப்பை சரிபார்க்கவும்.",
    monitoringCardTitle: "தானியங்கி வானிலை இடர் கண்காணிப்பு",
    monitoringCardSubtitle: "பதிவுசெய்த விவசாயிகளின் இருப்பிட வானிலையை ஆய்வு செய்து, பயிர் வளர்ச்சி நிலைக்கு ஏற்ப SMS எச்சரிக்கைகளை உருவாக்குகிறது.",
    monitoringSummaryTitle: "வானிலை இடர் கண்காணிப்பு சுருக்கம்",
    summaryFarmersChecked: "ஆய்வு செய்யப்பட்ட விவசாயிகள்",
    summaryRisksDetected: "கண்டறியப்பட்ட இடர்கள்",
    summaryAlertsSimulated: "மாதிரி SMS எச்சரிக்கைகள்",
    summaryAlertsSent: "உண்மையாக அனுப்பப்பட்டவை",
    summaryDuplicatesSuppressed: "தடுக்கப்பட்ட நகல் எச்சரிக்கைகள்",
    summaryFailures: "தோல்விகள்",
    demoOnlyBadge: "மாதிரி மட்டுமே — அனுப்பப்படவில்லை",
    lastRunAt: "கடைசியாக கண்காணிக்கப்பட்டது",
    liveDispatchesSubtext: "நேரலை வாயில் வழியே அனுப்பப்பட்டவை",
    guardActiveSubtext: "24 மணிநேர பாதுகாப்பு செயலில் உள்ளது",
    viewAllDispatches: "அனைத்து பதிவுகளையும் காண்க",
    
    // Risk Analysis Page
    riskTitle: "பயிர் சார்ந்த காலநிலை இடர் மதிப்பீட்டாளர்",
    riskSubtitle: "நெற்பயிரின் வெவ்வேறு வளர்ச்சிப் பருவங்களில் வரவிருக்கும் வானிலை இடர்களை சரிபார்க்கப்பட்ட விதிகளின்படி பகுப்பாய்வு செய்க.",
    selectLocation: "பகுதி / மாவட்டம் தேர்வு செய்க",
    selectStage: "தற்போதைய பயிர் வளர்ச்சிப் பருவம்",
    fetchAndAnalyze: "வானிலை பெற்று இடரை பகுப்பாய்",
    analyzing: "விதிகள் மதிப்பீடு செய்யப்படுகிறது...",
    overallRiskLevel: "ஒட்டுமொத்த ஆபத்து நிலை",
    overallRiskLevelFor: "ஒட்டுமொத்த ஆபத்து நிலை -",
    riskAssessmentTitle: "இடர் மதிப்பீடு",
    hazardBreakdown: "வானிலை இடர் விவரங்கள்",
    recommendedPrecautions: "பரிந்துரைக்கப்படும் வேளாண் முன்னெச்சரிக்கைகள்",
    forecastWindow: "வானிலை முன்னறிவிப்பு காலம்",
    forecastSource: "தரவு மூலம்",
    triggerWarningAlert: "விவசாயிகளுக்கு SMS எச்சரிக்கை அனுப்பு",
    disclaimerTitle: "மாதிரி முறை & சரிபார்ப்பு அறிவிப்பு",
    disclaimerText: "இந்த வரம்புகள் மாதிரி விளக்கத்திற்காக அமைக்கப்பட்டவை. வேளாண் பணிகளுக்கு முன் தமிழ்நாடு வேளாண் பல்கலைக்கழகத்தின் (TNAU) ஆலோசனைகளைப் பெறவும்.",
    districtPlaceholder: "அல்லது ஏதேனும் தமிழ்நாடு மாவட்டம் / வட்டம் பெயரை உள்ளிடவும்...",
    cropThresholdNote: "பயிர்: நெல் (Oryza sativa) • மழை மற்றும் வெப்ப வரம்புகளுக்கு ஏற்ப மதிப்பிடப்பட்டது",
    registeredInArea: "இப்பகுதியில் பதிவு செய்யப்பட்டவர்கள்",
    thresholdLabel: "வரம்பு:",
    reasonLabel: "காரணம்:",
    precautionLabel: "பரிந்துரைக்கப்படும் முன்னெச்சரிக்கை:",
    advisoryBannerTitle: "தமிழ் அக்ரி AI வேளாண் ஆலோசனை (Language Intelligence)",
    
    // Growth Stages
    stageNursery: "நாற்றங்கால் பருவம்",
    stageTillering: "தூர் கட்டும் பருவம்",
    stageFlowering: "பூக்கும் பருவம்",
    stageGrainFilling: "பால் பிடிக்கும் / மணி முதிரும் பருவம்",
    stageHarvest: "அறுவடைப் பருவம்",
    
    // Hazards & Levels
    hazardRain: "கனமழை",
    hazardHeat: "கடும் வெப்பம்",
    hazardRainCard: "கனமழை இடர்பாடு",
    hazardHeatCard: "கடும் வெப்ப இடர்பாடு",
    riskLow: "குறைந்த ஆபத்து",
    riskMedium: "மிதமான ஆபத்து",
    riskHigh: "அதிக ஆபத்து",
    
    // Farmer Registration
    regTitle: "விவசாயிகள் பதிவு படிவம்",
    regSubtitle: "வானிலை முன்னெச்சரிக்கை SMS செய்திகளை உடனுக்குடன் பெற விவசாயிகளைப் பதிவு செய்க.",
    farmerName: "விவசாயியின் முழுப் பெயர்",
    mobileNumber: "கைபேசி எண் (10 இலக்கங்கள்)",
    locationDistrict: "இருப்பிடம் / கிராமம் / மாவட்டம்",
    cropType: "பயிர் வகை",
    growthStage: "தற்போதைய பயிர் பருவம்",
    prefLang: "விருப்பமான SMS மொழி",
    registerBtn: "விவசாயியைப் பதிவு செய்",
    registering: "பதிவு செய்யப்படுகிறது...",
    farmerListTitle: "பதிவுசெய்த விவசாயிகள் பட்டியல்",
    deleteConfirm: "இந்த விவசாயி சுயவிவரத்தை நீக்க விரும்புகிறீர்களா?",
    phoneValidationHelp: "சரியான 10 இலக்க இந்திய மொபைல் எண்ணை உள்ளிடவும் (எ.கா: 9876543210).",
    farmerRegisteredSuccess: "விவசாயி வெற்றிகரமாகப் பதிவு செய்யப்பட்டார்!",
    farmerLoadError: "விவசாயிகள் பட்டியலை ஏற்ற முடியவில்லை.",
    farmerDeleteSuccess: "விவசாயி சுயவிவரம் நீக்கப்பட்டது.",
    farmerDeleteError: "விவசாயி சுயவிவரத்தை நீக்க முடியவில்லை.",
    selectVillagePlaceholder: "அல்லது கிராமம்/வட்டம் உள்ளிடவும் (எ.கா: கும்பகோணம், தஞ்சாவூர்)",
    namePlaceholder: "எ.கா: கே. செல்வக்குமார்",
    loadingFarmers: "விவசாயிகள் விவரங்கள் ஏற்றப்படுகிறது...",
    
    // Alert History
    historyTitle: "எச்சரிக்கை மற்றும் SMS வரலாற்றுப் பதிவு",
    historySubtitle: "அனுப்பப்பட்ட அனைத்து மாதிரி மற்றும் நேரலை SMS எச்சரிக்கைகளின் முழுப் பதிவேடு.",
    colFarmer: "விவசாயி",
    colPhone: "கைபேசி எண்",
    colLocation: "இருப்பிடம்",
    colHazard: "இடர்பாடு",
    colRisk: "ஆபத்து நிலை",
    colCrop: "பயிர்",
    colLang: "மொழி",
    colStatus: "நிலை",
    colSentAt: "நேரம்",
    colActions: "நடவடிக்கைகள்",
    filterHazard: "அனைத்து இடர்பாடுகள்",
    filterRisk: "அனைத்து நிலைகள்",
    filterStatus: "அனைத்து நிலவரங்கள்",
    viewMessageBtn: "SMS பார்க்க",
    refreshLogsBtn: "பதிவுகளை புதுப்பி",
    filterLabel: "வடிகட்டிகள்:",
    resetBtn: "மீட்டமை",
    loadingLogs: "எச்சரிக்கை பதிவுகள் ஏற்றப்படுகிறது...",
    smsPayloadTitle: "SMS செய்தி விவரங்கள்",
    recipientLabel: "பெறுநர்:",
    gatewayLabel: "செய்தி வாயில்:",
    
    // Settings
    settingsTitle: "கணினி அமைப்புகள் & இணைப்பு நிலவரம்",
    settingsSubtitle: "வானிலை மற்றும் SMS இணைப்பிகள், பாதுகாப்பு நிலவரங்கள் மற்றும் வேளாண் விதிகள்.",
    systemHealth: "கணினி இயக்க நிலை",
    operatingMode: "இயக்க முறை",
    zeroCostSimEnv: "கட்டணமில்லா மாதிரி சூழல்",
    weatherProvider: "வானிலை தகவல் இணைப்பி",
    smsProvider: "SMS தகவல் வாயில் இணைப்பி",
    activeAdapterLabel: "செயலில் உள்ள இணைப்பி:",
    statusReady: "தயார்",
    statusSimulated: "மாதிரி முறை",
    statusConnected: "இணைக்கப்பட்டுள்ளது",
    dbStorageLabel: "தரவுத்தள சேமிப்பு",
    sqliteLocalFile: "SQLite (உள்ளூர் கோப்பு tamilagri.db)",
    displayLanguageLabel: "முகப்பு மொழி / Display Language",
    demoExplanation: "மாதிரி முறை செயல்பாடு",
    demoExplanationText: "தமிழ் அக்ரி AI தற்போது மாதிரி முறையில் இயங்குகிறது. தமிழ்நாடு மாவட்ட வானிலை முன்மாதிரிகள் பயன்படுத்தப்படுகின்றன மற்றும் கட்டணமின்றி பாதுகாப்பாக SMS பரிசோதிக்கப்படுகிறது.",
    tnauVerificationHeader: "வேளாண் விதிகள் சரிபார்ப்பு நிலை",
    tnauVerificationText: "நெற்பயிரின் நாற்றங்கால், பூக்கும் பருவம் மற்றும் அறுவடை பருவத்திற்கான விதிகள் மாதிரி நிலையில் உள்ளன. தமிழ்நாடு வேளாண் பல்கலைக்கழக (TNAU) தரவுகளுடன் இணைக்க வழிவகை செய்யப்பட்டுள்ளது.",
    configuredThresholdsLabel: "அமைக்கப்பட்ட விதி வரம்புகள் (backend/app/rules/crop_rules.py):",
    thresholdNursery: "கனமழை > 50மிமீ/நாள் (நீரில் மூழ்குதல் இடர்) | கடும் வெப்பம் > 38°C (நாற்று கருகல்)",
    thresholdTillering: "கனமழை > 65மிமீ/நாள் (தூர்கட்டுதல் பாதிப்பு) | கடும் வெப்பம் > 39°C (நீரிழப்பு அழுத்தம்)",
    thresholdFlowering: "கனமழை > 40மிமீ/நாள் (மகரந்தம் அடித்து செல்லப்படுதல்) | கடும் வெப்பம் > 36°C (மணிக்கருவுறாமை / பதர் ஆகுதல்)",
    thresholdGrainFilling: "கனமழை > 50மிமீ/நாள் (பயிர் சாய்வு) | கடும் வெப்பம் > 38°C (முதிர்ச்சி துரிதமாதல் & மாவுத்தன்மை குறைவு)",
    thresholdHarvest: "மழை > 15மிமீ/நாள் (தானியம் முளைத்தல் & அறுவடை இயந்திர பாதிப்பு) | கடும் வெப்பம் > 40°C (தானிய வெடிப்பு)",
    apiDocsHeader: "FastAPI செயல்முறை ஆவணங்கள்",
    openSwagger: "Swagger UI ஆவணத்தைத் திற (/docs)",
    
    // Common Actions & Modal
    cancel: "ரத்து செய்",
    confirmSend: "உறுதி செய்து SMS அனுப்பு",
    sending: "அனுப்பப்படுகிறது...",
    close: "மூடு",
    successMsg: "வெற்றிகரமாக முடிக்கப்பட்டது!",
    errorMsg: "பிழை ஏற்பட்டது. பின்தள சேவையைச் சரிபார்க்கவும்.",
    forceResendLabel: "கட்டாயமாக மீண்டும் அனுப்பு (24 மணிநேர கட்டுப்பாட்டைத் தவிர்)",
    chooseFarmerOption: "-- பதிவு செய்த விவசாயியைத் தேர்ந்தெடுக்கவும் --",
    customMessageLabel: "விருப்பப்படியான தனிப்பயன் செய்தி (மாதிரி செய்திக்கு காலியாக விடவும்)",
    customMessagePlaceholderTa: "தானியங்கி தமிழ் மாதிரி செய்தி பயன்படுத்தப்படும்...",
    customMessagePlaceholderEn: "Automatic English SMS template will be formatted...",
    tamilSmsPreviewTitle: "தமிழ் SMS முன்னோட்டம் (Tamil SMS Preview)",
    englishSmsPreviewTitle: "ஆங்கில SMS முன்னோட்டம் (English SMS Preview)",
    generatingPreview: "செய்தி முன்னோட்டம் உருவாக்கப்படுகிறது...",
    demoGatewayNotice: "மாதிரி முறையில் அனுப்பப்படும் செய்தி கட்டணமின்றி தரவுத்தளத்தில் பாதுகாப்பாக சேமிக்கப்படும்.",
    dispatchToast: "{name} விவசாயிக்கு SMS அனுப்பப்பட்டது! நிலை: [{status}] (இணைப்பி: {provider})",

    // Footer
    footerTitle: "தமிழ் அக்ரி AI — பயிர் சார்ந்த காலநிலை இடர் பகுப்பாய்வு & SMS முன்னெச்சரிக்கை அமைப்பு.",
    footerSubtitle: "ஹேக்கத்தான் மாதிரி வடிவமைப்பு • தமிழ்நாடு வேளாண் பல்கலைக்கழக (TNAU) விதிகள் விளக்கம் • தூய கட்டமைப்பு",
  }
};
