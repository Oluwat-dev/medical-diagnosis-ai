import streamlit as st
from models.medical_models import MedicalSymptomAnalyzer
from utils.visualization_streamlit import MedicalVisualization
import pandas as pd
from datetime import datetime, timedelta

def show_symptom_checker_page():
    """Display the symptom checker page"""
    
    st.title("🩺 AI Symptom Checker")
    st.markdown("""
    Analyze your symptoms using our AI-powered symptom checker. This tool provides preliminary 
    health insights based on the symptoms you report.
    """)
    
    # Medical disclaimer for symptom checking
    st.error("""
    ⚠️ **SYMPTOM CHECKER DISCLAIMER**
    
    This symptom checker is for informational purposes only and should not replace professional medical advice.
    - **NOT a substitute for medical consultation**
    - **Emergency symptoms**: Call emergency services immediately
    - **Serious concerns**: Contact your healthcare provider
    - **Always seek professional medical advice** for proper diagnosis and treatment
    """)
    
    # Initialize components
    symptom_analyzer = MedicalSymptomAnalyzer()
    visualizer = MedicalVisualization()
    
    # Emergency symptoms warning
    st.error("""
    🚨 **SEEK IMMEDIATE EMERGENCY CARE IF YOU HAVE:**
    - Chest pain or pressure
    - Difficulty breathing or shortness of breath
    - Sudden severe headache
    - Loss of consciousness
    - Severe abdominal pain
    - High fever (over 103°F/39.4°C)
    - Signs of stroke (face drooping, arm weakness, speech difficulty)
    - Severe allergic reaction
    """)
    
    # Main symptom checker interface
    st.header("📝 Symptom Assessment")
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Quick Check", "Detailed Assessment", "Symptom History"])
    
    with tab1:
        show_quick_symptom_check(symptom_analyzer, visualizer)
    
    with tab2:
        show_detailed_assessment(symptom_analyzer, visualizer)
    
    with tab3:
        show_symptom_history()

def show_quick_symptom_check(symptom_analyzer: MedicalSymptomAnalyzer, visualizer: MedicalVisualization):
    """Quick symptom check interface"""
    
    st.subheader("🚀 Quick Symptom Check")
    st.markdown("Select your current symptoms for a rapid preliminary assessment.")
    
    # Common symptoms organized by category
    symptom_categories = {
        "General Symptoms": [
            "fever", "fatigue", "headache", "dizziness", "nausea", "vomiting"
        ],
        "Respiratory": [
            "cough", "shortness_of_breath", "chest_pain", "sore_throat", "runny_nose"
        ],
        "Gastrointestinal": [
            "stomach_pain", "diarrhea", "constipation", "loss_of_appetite", "heartburn"
        ],
        "Musculoskeletal": [
            "muscle_pain", "joint_pain", "back_pain", "neck_pain", "stiffness"
        ],
        "Skin": [
            "rash", "itching", "dry_skin", "bruising", "swelling"
        ],
        "Other": [
            "sleep_problems", "mood_changes", "vision_changes", "hearing_problems"
        ]
    }
    
    selected_symptoms = []
    
    # Create columns for symptom categories
    cols = st.columns(2)
    
    for i, (category, symptoms) in enumerate(symptom_categories.items()):
        with cols[i % 2]:
            st.write(f"**{category}:**")
            for symptom in symptoms:
                if st.checkbox(symptom.replace('_', ' ').title(), key=f"quick_{symptom}"):
                    selected_symptoms.append(symptom)
    
    # Duration and severity
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.selectbox(
            "How long have you had these symptoms?",
            ["Less than 1 day", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"],
            key="quick_duration"
        )
    
    with col2:
        overall_severity = st.selectbox(
            "Overall severity",
            ["Mild", "Moderate", "Severe"],
            key="quick_severity"
        )
    
    # Analyze symptoms
    if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
        if selected_symptoms:
            with st.spinner("Analyzing symptoms..."):
                analysis_result = symptom_analyzer.analyze_symptoms(selected_symptoms)
                
                if 'error' not in analysis_result:
                    display_symptom_analysis_results(analysis_result, visualizer, duration, overall_severity)
                else:
                    st.error(analysis_result['error'])
        else:
            st.warning("Please select at least one symptom to analyze.")

def show_detailed_assessment(symptom_analyzer: MedicalSymptomAnalyzer, visualizer: MedicalVisualization):
    """Detailed symptom assessment interface"""
    
    st.subheader("🔍 Detailed Health Assessment")
    st.markdown("Provide comprehensive information for a more thorough analysis.")
    
    # Patient demographics
    st.write("**Personal Information:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], key="detailed_gender")
    
    with col3:
        weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    
    # Current symptoms with details
    st.write("**Current Symptoms:**")
    
    # Primary complaint
    primary_complaint = st.text_area(
        "Describe your main concern:",
        placeholder="E.g., I have been experiencing chest pain for 2 days..."
    )
    
    # Symptom checklist with severity
    st.write("**Symptom Severity (0 = None, 10 = Severe):**")
    
    detailed_symptoms = {
        "fever": "Fever/elevated temperature",
        "headache": "Headache",
        "cough": "Cough",
        "shortness_of_breath": "Shortness of breath",
        "chest_pain": "Chest pain",
        "stomach_pain": "Abdominal/stomach pain",
        "nausea": "Nausea",
        "vomiting": "Vomiting",
        "diarrhea": "Diarrhea",
        "fatigue": "Fatigue/tiredness",
        "dizziness": "Dizziness",
        "rash": "Skin rash"
    }
    
    symptom_scores = {}
    selected_detailed_symptoms = []
    
    for symptom_key, symptom_label in detailed_symptoms.items():
        score = st.slider(symptom_label, 0, 10, 0, key=f"detailed_{symptom_key}")
        symptom_scores[symptom_key] = score
        if score > 0:
            selected_detailed_symptoms.append(symptom_key)
    
    # Medical history
    st.write("**Medical History:**")
    col1, col2 = st.columns(2)
    
    with col1:
        chronic_conditions = st.multiselect(
            "Chronic conditions",
            ["Diabetes", "Hypertension", "Heart Disease", "Asthma", "COPD", 
             "Arthritis", "Depression", "Anxiety", "Other"]
        )
        
        current_medications = st.text_area(
            "Current medications",
            placeholder="List current medications..."
        )
    
    with col2:
        allergies = st.text_area(
            "Known allergies",
            placeholder="Food, drug, environmental allergies..."
        )
        
        recent_travel = st.checkbox("Recent travel (within 2 weeks)")
        recent_exposure = st.checkbox("Known exposure to illness")
    
    # Analyze detailed symptoms
    if st.button("🔍 Perform Detailed Analysis", type="primary", use_container_width=True):
        if selected_detailed_symptoms:
            with st.spinner("Performing comprehensive analysis..."):
                analysis_result = symptom_analyzer.analyze_symptoms(selected_detailed_symptoms)
                
                if 'error' not in analysis_result:
                    display_detailed_analysis_results(
                        analysis_result, visualizer, symptom_scores, 
                        age, gender, chronic_conditions, primary_complaint
                    )
                else:
                    st.error(analysis_result['error'])
        else:
            st.warning("Please indicate severity for at least one symptom.")

def show_symptom_history():
    """Symptom tracking and history interface"""
    
    st.subheader("📊 Symptom History & Tracking")
    st.markdown("Track your symptoms over time to identify patterns and trends.")
    
    # Initialize session state for symptom history
    if 'symptom_history' not in st.session_state:
        st.session_state.symptom_history = []
    
    # Add new symptom entry
    st.write("**Log New Symptoms:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        log_date = st.date_input("Date", datetime.now())
        log_time = st.time_input("Time", datetime.now().time())
    
    with col2:
        log_symptoms = st.multiselect(
            "Symptoms experienced",
            ["fever", "headache", "cough", "fatigue", "nausea", "stomach_pain", 
             "dizziness", "chest_pain", "shortness_of_breath", "rash"]
        )
    
    log_severity = st.selectbox("Overall severity", ["Mild", "Moderate", "Severe"], key="log_severity")
    log_notes = st.text_area("Additional notes", placeholder="Any additional observations...")
    
    if st.button("📝 Log Symptoms", use_container_width=True):
        if log_symptoms:
            entry = {
                'date': log_date,
                'time': log_time,
                'symptoms': log_symptoms,
                'severity': log_severity,
                'notes': log_notes
            }
            st.session_state.symptom_history.append(entry)
            st.success("Symptoms logged successfully!")
        else:
            st.warning("Please select at least one symptom to log.")
    
    # Display symptom history
    if st.session_state.symptom_history:
        st.write("**Your Symptom History:**")
        
        # Convert to DataFrame for better display
        history_data = []
        for entry in st.session_state.symptom_history:
            history_data.append({
                'Date': entry['date'],
                'Time': entry['time'],
                'Symptoms': ', '.join(entry['symptoms']),
                'Severity': entry['severity'],
                'Notes': entry['notes'][:50] + '...' if len(entry['notes']) > 50 else entry['notes']
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Symptom frequency analysis
        st.write("**Symptom Frequency Analysis:**")
        all_symptoms = []
        for entry in st.session_state.symptom_history:
            all_symptoms.extend(entry['symptoms'])
        
        if all_symptoms:
            symptom_counts = pd.Series(all_symptoms).value_counts()
            st.bar_chart(symptom_counts)
        
        # Clear history button
        if st.button("🗑️ Clear History", help="This will remove all logged symptoms"):
            st.session_state.symptom_history = []
            st.success("Symptom history cleared!")
            st.rerun()
    
    else:
        st.info("No symptom history recorded yet. Start logging your symptoms above.")

def display_symptom_analysis_results(analysis_result: dict, visualizer: MedicalVisualization, 
                                   duration: str, severity: str):
    """Display results from symptom analysis"""
    
    st.header("📊 Analysis Results")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Symptoms Analyzed", analysis_result['total_symptoms'])
    
    with col2:
        st.metric("Matched Symptoms", analysis_result['matched_symptoms'])
    
    with col3:
        severity_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        st.metric("Severity Level", 
                 f"{severity_color.get(analysis_result['severity'], '⚪')} {analysis_result['severity'].upper()}")
    
    # Possible conditions
    if analysis_result['possible_conditions']:
        st.subheader("🔍 Possible Conditions")
        visualizer.plot_symptom_analysis(analysis_result)
        
        # Show top conditions in text format
        st.write("**Most likely conditions based on symptoms:**")
        for i, (condition, score) in enumerate(analysis_result['possible_conditions'][:5], 1):
            st.write(f"{i}. **{condition}** (Symptom match score: {score})")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    recommendations = analysis_result.get('recommendations', [])
    
    for rec in recommendations:
        if rec.startswith("🚨"):
            st.error(rec)
        elif rec.startswith("📋") or rec.startswith("🔄"):
            st.warning(rec)
        else:
            st.info(rec)
    
    # Duration and severity context
    st.subheader("📋 Assessment Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Symptom Duration:** {duration}")
        if "More than 2 weeks" in duration:
            st.warning("Chronic symptoms require medical evaluation")
        elif "Less than 1 day" in duration:
            st.info("Acute symptoms - monitor for changes")
    
    with col2:
        st.write(f"**Reported Severity:** {severity}")
        if severity == "Severe":
            st.error("Severe symptoms require prompt medical attention")
        elif severity == "Moderate":
            st.warning("Moderate symptoms should be monitored closely")

def display_detailed_analysis_results(analysis_result: dict, visualizer: MedicalVisualization,
                                    symptom_scores: dict, age: int, gender: str, 
                                    chronic_conditions: list, primary_complaint: str):
    """Display results from detailed symptom analysis"""
    
    st.header("📊 Comprehensive Analysis Results")
    
    # Patient summary
    st.subheader("👤 Patient Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Age:** {age} years")
        st.write(f"**Gender:** {gender}")
    
    with col2:
        active_symptoms = sum(1 for score in symptom_scores.values() if score > 0)
        high_severity = sum(1 for score in symptom_scores.values() if score >= 7)
        st.write(f"**Active Symptoms:** {active_symptoms}")
        st.write(f"**High Severity:** {high_severity}")
    
    with col3:
        st.write(f"**Chronic Conditions:** {len(chronic_conditions)}")
        if chronic_conditions:
            st.write(f"- {', '.join(chronic_conditions[:2])}")
    
    # Primary complaint
    if primary_complaint:
        st.subheader("📝 Chief Complaint")
        st.write(f'"{primary_complaint}"')
    
    # Symptom severity visualization
    st.subheader("📈 Symptom Severity Profile")
    
    # Filter out zero scores for visualization
    active_symptom_scores = {k: v for k, v in symptom_scores.items() if v > 0}
    
    if active_symptom_scores:
        # Create severity chart
        symptoms = list(active_symptom_scores.keys())
        scores = list(active_symptom_scores.values())
        
        df_symptoms = pd.DataFrame({
            'Symptom': [s.replace('_', ' ').title() for s in symptoms],
            'Severity': scores
        })
        
        st.bar_chart(df_symptoms.set_index('Symptom'))
    
    # Standard analysis results
    display_symptom_analysis_results(analysis_result, visualizer, "Detailed Assessment", "Variable")
    
    # Risk factors based on patient profile
    st.subheader("⚠️ Risk Factor Analysis")
    
    risk_factors = []
    
    if age >= 65:
        risk_factors.append("Advanced age increases risk for various conditions")
    
    if chronic_conditions:
        risk_factors.append(f"Pre-existing conditions: {', '.join(chronic_conditions)}")
    
    high_severity_symptoms = [k for k, v in symptom_scores.items() if v >= 8]
    if high_severity_symptoms:
        risk_factors.append(f"High severity symptoms present: {', '.join(high_severity_symptoms)}")
    
    if risk_factors:
        for factor in risk_factors:
            st.warning(f"⚠️ {factor}")
    else:
        st.success("✅ No major risk factors identified")
    
    # Personalized recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    personalized_recs = []
    
    if age >= 65:
        personalized_recs.append("Consider more frequent health check-ups due to age")
    
    if chronic_conditions:
        personalized_recs.append("Ensure chronic conditions are well-managed")
        personalized_recs.append("Consider how symptoms may relate to existing conditions")
    
    max_severity = max(symptom_scores.values()) if symptom_scores.values() else 0
    if max_severity >= 8:
        personalized_recs.append("High severity symptoms warrant prompt medical evaluation")
    
    if not personalized_recs:
        personalized_recs.append("Continue monitoring symptoms and maintain healthy lifestyle")
    
    for rec in personalized_recs:
        st.info(f"💡 {rec}")
