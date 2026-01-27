import difflib
import pandas as pd
import joblib
import re
import os

# --- Get the correct path to your model ---
current_dir = os.path.dirname(os.path.abspath(__file__))  # folder of this script
model_path = os.path.join(current_dir, 'disease_model.pkl')

# Load the model (joblib is sufficient if saved with joblib)
loaded_model = joblib.load(model_path)

# Load CSV
csv_path = os.path.join(current_dir, "sih_new.csv")
df = pd.read_csv(csv_path)
all_symptoms = df.columns[:-1].tolist()

# Symptom mapping (keep as you had it)
symptom_mapping = {
    'high_fever': ['high fever', 'hot', 'temperature'],
    'loss_of_appetite': ['loss of appetite', 'not hungry', 'no appetite', 'no food', 'skip meals'],
    'abdominal_pain': ['abdominal pain', 'stomach', 'tummy', 'belly', 'cramps'],
    'yellowish_skin': ['yellowish skin', 'yellow skin', 'yellowish', 'pale'],
    'yellowing_of_eyes': ['yellowing of eyes', 'yellow eyes', 'jaundice', 'eyes yellow'],
    'skin_rash': ['skin rash', 'rash', 'spots', 'bumps', 'itchy'],
    'chest_pain': ['chest pain', 'chest', 'chest hurt', 'tight chest', 'pressure'],
    'sweating': ['sweating', 'sweat', 'sweaty', 'hot sweat'],
    'itching': ['itching', 'itch', 'itchy', 'scratch'],
    'dark_urine': ['dark urine', 'dark pee', 'brown pee', 'urine dark'],
    'diarrhoea': ['diarrhoea', 'diarrhea', 'loose stool', 'runny stool'],
    'irritability': ['irritability', 'grumpy', 'moody', 'snappy', 'irritated'],
    'excessive_hunger': ['excessive hunger', 'very hungry', 'always hungry', 'eat a lot'],
    'lethargy': ['lethargy'],
    'weight_loss': ['weight loss', 'losing weight', 'thin', 'slim'],
    'breathlessness': ['breathlessness', 'breathless', 'panting', 'short breath'],
    'phlegm': ['phlegm', 'mucus', 'spit', 'thick spit','running nose',"runny nose"],
    'mild_fever': ['mild fever', 'low fever','fever', 'slight fever', 'warm'],
    'swelled_lymph_nodes': ['swelled lymph nodes', 'lumps', 'swollen neck', 'glands'],
    'blurred_and_distorted_vision': ['blurred and distorted vision', 'blurred', 'fuzzy', 'double vision'],
    'loss_of_balance': ['loss of balance', 'unsteady', 'wobbly', 'off balance','no balance','cant balance'],
    'dizziness': ['dizziness', 'dizzy', 'lightheaded', 'spinning','spin'],
    'abnormal_menstruation': ['abnormal menstruation', 'irregular', 'period problem', 'cycle'],
    'depression': ['depression', 'sad', 'down', 'low mood'],
    'red_spots_over_body': ['red spots over body', 'red spots', 'spots'],
    'fast_heart_rate': ['fast heart rate', 'fast heart', 'racing', 'palpitations'],
    'muscle_weakness': ['muscle weakness', 'weak muscles', 'muscle weak', 'low strength'],
    'family_history': ['family history', 'family sick', 'genetic', 'runs in family'],
    'obesity': ['obesity', 'overweight', 'fat', 'heavy'],
    'neck_pain': ['neck pain', 'neck hurt', 'stiff neck'],
    'constipation': ['constipation', 'constipated', 'hard stool', 'not pooping','hard stool','hard poop','cant poop'],
    'stiff_neck': ['stiff neck', 'neck stiff', 'neck tight','neck pain','neck stiffness','stiffness in neck',],
    'restlessness': ['restlessness', 'restless', 'fidgety', 'uneasy'],
    'mood_swings': ['mood swings', 'moody', 'up down', 'mood changes'],
    'painful_walking': ['painful walking', 'pain walk', 'walking hurt', 'legs hurt'],
    'swelling_joints': ['swelling joints', 'swollen joints', 'puffy joints', 'joints hurt'],
    'back_pain': ['back pain', 'back hurt', 'aching back','back ache'],
    'sneezing': ['sneezing', 'sneeze', 'ahchoo'],
    'acidity': ['acidity', 'acid', 'heartburn', 'burning'],
    'stomach_pain': ['stomach pain', 'stomach', 'belly', 'tummy', 'cramps'],
    'indigestion': ['indigestion', 'upset stomach', 'stomach upset'],
    'burning_micturition': ['burning micturition', 'burn pee', 'pain pee', 'burn while peeing','burning sensation while peeing','pain while peeing','hurts to pee'],
    'swollen_extremeties': ['swollen extremeties', 'swollen hands', 'swollen feet', 'puffy hands', 'puffy feet'],
    'increased_appetite': ['increased appetite', 'hungry more', 'eat more', 'more appetite','hungry'],
    'slurred_speech': ['slurred speech', 'slurry talk', 'talk funny', 'speech unclear'],
    'enlarged_thyroid': ['enlarged thyroid', 'swollen neck', 'thyroid bump', 'neck swelling',"neck is swelled",'neck is swelling'],
    'polyuria': ['polyuria', 'pee more', 'frequent urination', 'urinate often'],
    'brittle_nails': ['brittle nails', 'weak nails', 'nails break', 'nails chip'],
    'loss_of_smell': ['loss of smell', 'cannot smell', 'no smell', 'smell gone'],
    'coma': ['coma', 'unconscious', 'not awake', 'passed out'],
    'congestion': ['congestion', 'blocked nose', 'nose stuffed', 'nasal blocked',"stffy nose"],
    'runny_nose': ['runny nose', 'nose running', 'dripping nose', 'snotty','running nose'],
    'sinus_pressure': ['sinus pressure', 'face pressure', 'head pressure', 'sinus ache'],
    'redness_of_eyes': ['red eyes', 'bloodshot', 'eyes red', 'eye irritation','redness of eyes'],
    'throat_irritation': ['throat irritation', 'sore throat', 'throat hurts', 'scratchy throat','pain in throat','throat pain',],
    'palpitations': ['palpitations', 'fast heart', 'racing heart', 'heart flutter','fast heartbeat','high hearbeat'],
    'stomach_bleeding': ['stomach bleeding', 'vomiting blood', 'bleeding gut', 'stomach bleed','blood in vomiting',"blood in vomit"],
    'receiving_unsterile_injections': ['unsterile injections', 'dirty shots', 'unsafe injections'],
    'rusty_sputum': ['rusty sputum', 'blood spit', 'brown phlegm'],
    'receiving_blood_transfusion': ['blood transfusion', 'blood given', 'transfusion'],
    'blood_in_sputum': ['blood in spit', 'bloody phlegm', 'coughing blood'],
    'pain_behind_the_eyes': ['eye pain', 'behind eyes hurt', 'eye ache'],
    'inflammatory_nails': ['inflamed nails', 'red nails', 'swollen nails'],
    'silver_like_dusting': ['silver dust nails', 'shiny nails', 'dusty nails'],
    'small_dents_in_nails': ['dented nails', 'nail dents', 'pitted nails'],
    'visual_disturbances': ['vision problems', 'blurred vision', 'see blurry', 'vision unclear'],
    'blister': ['blister', 'skin bubble', 'fluid bump', 'skin bump'],
    'toxic_look_(typhos)': ['toxic look', 'sick look', 'very ill', 'looks bad'],
    'internal_itching': ['internal itch', 'inside itch', 'deep itch'],
    'red_sore_around_nose': ['red sore nose', 'nose sore', 'nose red', 'pimple nose'],
    'skin_peeling': ['skin peeling', 'flaky skin', 'peeling'],
    'history_of_alcohol_consumption': ['alcohol history', 'drink history', 'drinks often', 'alcohol use'],
    'prominent_veins_on_calf': ['veins on calf', 'veiny legs', 'visible veins'],
    'altered_sensorium': ['confused', 'not aware', 'disoriented', 'mixed up'],
    'fluid_overload.1': ['fluid overload', 'swelling', 'puffy', 'water retention'],
    'belly_pain': ['belly pain', 'stomach ache', 'tummy pain', 'cramps'],
    'lack_of_concentration': ['cannot focus', 'distracted', 'hard to focus', 'mind wanders'],
    'distention_of_abdomen': ['bloated', 'swollen belly', 'belly swollen', 'stomach bloated'],
    'continuous_feel_of_urine': ['need to pee', 'urinate often', 'frequent pee', 'always pee'],
    'mucoid_sputum': ['mucus spit', 'thick spit', 'phlegm', 'gunky spit'],
    'passage_of_gases': ['gas', 'farting', 'flatulence', 'passing gas'],
    'bruising': ['bruises', 'black marks', 'skin marks', 'spots'],
    'yellow_crust_ooze': ['yellow crust', 'ooze', 'yellow scab', 'crusty'],
    'swollen_legs': ['swollen legs', 'puffy legs', 'legs puff', 'leg swelling'],
    'cold_hands_and_feets': ['cold hands', 'cold feet', 'cold extremities', 'hands cold', 'feet cold'],
    'irregular_sugar_level': ['high sugar', 'low sugar', 'sugar level', 'blood sugar'],
    'chills_shivering': ['chills', 'shivering', 'cold shake', 'goosebumps'],
    'cough_sore_throat': ['cough', 'sore throat', 'throat pain', 'cough throat'],
    'nausea_vomiting': ['nausea', 'vomiting', 'feel like vomit', 'throw up'],
    'fatigue_malaise': ['fatigue', 'tired', 'weak', 'exhausted','lethargic','lethargy'],
    'headache_migraine': ['headache', 'migraine', 'head hurts', 'head pain'],
    'muscle_joint_pain': ['muscle pain', 'joint pain', 'body ache', 'aching muscles'],
}

# --- Functions ---
def get_matched_symptoms(user_input):
    user_input = user_input.lower()
    matched = []
    words = re.sub(r"[^\w\s]", "", user_input).strip().split()

    for symptom, variations in symptom_mapping.items():
        for variation in variations:
            if variation in user_input:
                matched.append(symptom)
                break
            else:
                close = difflib.get_close_matches(variation, words, n=1, cutoff=0.75)
                if close:
                    matched.append(symptom)
                    break
    return matched

def create_input_vector(matched, all_symptoms):
    input_data = {symptom: 0 for symptom in all_symptoms}
    for symptom in matched:
        if symptom in input_data:
            input_data[symptom] = 1
    return pd.DataFrame([input_data])

# --- Main Flow ---
text = input("What symptoms are you experiencing? ")

matched_symptoms = get_matched_symptoms(text)
print("Matched Symptoms:", matched_symptoms)

X_input = create_input_vector(matched_symptoms, all_symptoms)

prediction = loaded_model.predict(X_input)
print(f"You may have {prediction[0]}")
