import os
import re
from pathlib import Path

class DatasetNormalizer:
    """
    Normalizes multiple agricultural datasets into a consistent format for RAG systems.
    """
    
    def __init__(self, input_dir="./data/cleaned_text", output_dir="./data/updated_cleaned_text"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def normalize_all(self):
        """Process all datasets"""
        print("=" * 70)
        print("DATASET NORMALIZATION FOR RAG SYSTEM")
        print("=" * 70)
        
        # Process each dataset
        self.normalize_call_query()
        self.normalize_crop_calendar()
        self.normalize_crop_production()
        self.normalize_crop_yield()
        self.normalize_faq()
        self.normalize_fertilizer_prediction()
        self.normalize_pest_solution()
        self.normalize_pesticide_remedy_1()
        self.normalize_pesticide_remedy_2()
        
        print("\n" + "=" * 70)
        print("✓ ALL DATASETS NORMALIZED SUCCESSFULLY!")
        print(f"✓ Output directory: {self.output_dir.absolute()}")
        print("=" * 70)
    
    def normalize_call_query(self):
        """Normalize Call_Query.txt"""
        input_file = self.input_dir / "Call_Query.txt"
        output_file = self.output_dir / "Call_Query_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
                
            lines = entry.split('\n')
            question = ""
            answer = ""
            
            for line in lines:
                if line.startswith('Question:'):
                    question = line.replace('Question:', '').strip()
                elif line.startswith('Answers:') or line.startswith('Answer:'):
                    answer = line.replace('Answers:', '').replace('Answer:', '').strip()
            
            if question and answer:
                # Capitalize first letter if needed
                if answer and not answer[0].isupper():
                    answer = answer[0].upper() + answer[1:]
                
                normalized_entry = f"""[DATASET: call_query]
[TYPE: general_knowledge]
Query: {question}
Answer: {answer}
Details: Category=Agricultural Knowledge"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_crop_calendar(self):
        """Normalize crop_calender.txt"""
        input_file = self.input_dir / "crop_calender.txt"
        output_file = self.output_dir / "crop_calender_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            state = data.get('State', '')
            crop = data.get('Crop Name', '')
            sowing = data.get('Sowing Period', '')
            harvesting = data.get('Harvesting Period', '')
            
            if state and crop:
                query = f"When to sow and harvest {crop} in {state}?"
                answer = f"In {state}, {crop} should be sown during {sowing} and harvested during {harvesting}."
                details = f"State={state} | Crop={crop} | Sowing={sowing} | Harvesting={harvesting}"
                
                normalized_entry = f"""[DATASET: crop_calendar]
[TYPE: seasonal_information]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_crop_production(self):
        """Normalize crop_production.txt"""
        input_file = self.input_dir / "crop_production.txt"
        output_file = self.output_dir / "crop_production_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            state = data.get('State', '')
            district = data.get('District', '')
            year = data.get('Year', '')
            season = data.get('Season', '')
            crop = data.get('Crop', '')
            area = data.get('Area cultivated', data.get('Area', ''))
            production = data.get('Total production', data.get('Production', ''))
            
            if state and crop:
                query = f"What was the {crop} production in {district} district, {state} during {season} {year}?"
                answer = f"In {district} district of {state} during the {season} season of {year}, {crop} was cultivated on {area} with a total production of {production}."
                details = f"State={state} | District={district} | Year={year} | Season={season} | Crop={crop} | Area={area} | Production={production}"
                
                normalized_entry = f"""[DATASET: crop_production]
[TYPE: statistical_data]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_crop_yield(self):
        """Normalize crop_yield.txt"""
        input_file = self.input_dir / "crop_yield.txt"
        output_file = self.output_dir / "crop_yield_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            crop = data.get('Crop', '')
            year = data.get('Crop Year', '')
            season = data.get('Season', '')
            state = data.get('State', '')
            area = data.get('Area', '')
            production = data.get('Production', '')
            rainfall = data.get('Annual Rainfall', '')
            fertilizer = data.get('Fertilizer', '')
            pesticide = data.get('Pesticide', '')
            yield_val = data.get('Yield', '')
            
            if crop and state:
                query = f"What was the yield of {crop} in {state} during {season} {year}?"
                answer = f"In {state} during {season} {year}, {crop} had a yield of {yield_val} with production of {production} tonnes from {area} hectares area."
                details = f"Crop={crop} | Year={year} | Season={season} | State={state} | Area={area} | Production={production} | Rainfall={rainfall} | Fertilizer={fertilizer} | Pesticide={pesticide} | Yield={yield_val}"
                
                normalized_entry = f"""[DATASET: crop_yield]
[TYPE: analytical_data]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_faq(self):
        """Normalize faq_dataset.txt"""
        input_file = self.input_dir / "faq_dataset.txt"
        output_file = self.output_dir / "faq_dataset_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            lines = entry.split('\n')
            question = ""
            answer = ""
            
            for line in lines:
                if line.startswith('Questions:') or line.startswith('Question:'):
                    question = line.replace('Questions:', '').replace('Question:', '').strip()
                elif line.startswith('Answers:') or line.startswith('Answer:'):
                    answer = line.replace('Answers:', '').replace('Answer:', '').strip()
            
            if question and answer:
                # Convert to title case for question
                question_formatted = question.capitalize()
                if not question_formatted.endswith('?'):
                    question_formatted += '?'
                
                # Capitalize answer
                answer_formatted = answer.capitalize() if answer else answer
                
                normalized_entry = f"""[DATASET: faq]
[TYPE: expert_advice]
Query: {question_formatted}
Answer: {answer_formatted}
Details: Category=Expert Agricultural Advice"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_fertilizer_prediction(self):
        """Normalize fertilizer prediction.txt"""
        input_file = self.input_dir / "fertilizer prediction.txt"
        output_file = self.output_dir / "fertilizer_prediction_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            temp = data.get('Temparature', data.get('Temperature', ''))
            humidity = data.get('Humidity', '')
            moisture = data.get('Moisture', '')
            soil = data.get('Soil Type', '')
            crop = data.get('Crop Type', '')
            n = data.get('Nitrogen', '')
            k = data.get('Potassium', '')
            p = data.get('Phosphorous', '')
            fertilizer = data.get('Fertilizer Name', '')
            
            if crop and fertilizer:
                query = f"What fertilizer is recommended for {crop} in {soil} soil with temperature {temp}°C, humidity {humidity}%, moisture {moisture}%, nitrogen {n}, potassium {k}, phosphorous {p}?"
                answer = f"{fertilizer} fertilizer is recommended for {crop} grown in {soil} soil under these conditions."
                details = f"Temperature={temp} | Humidity={humidity} | Moisture={moisture} | SoilType={soil} | Crop={crop} | N={n} | K={k} | P={p} | Fertilizer={fertilizer}"
                
                normalized_entry = f"""[DATASET: fertilizer_recommendation]
[TYPE: prescriptive_data]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_pest_solution(self):
        """Normalize pest&solution.txt"""
        input_file = self.input_dir / "pest&solution.txt"
        output_file = self.output_dir / "pest_solution_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            pest = data.get('Pest Name', '')
            pesticides = data.get('Most Commonly Used Pesticides', '')
            
            if pest and pesticides:
                query = f"What pesticides are commonly used for {pest}?"
                answer = f"The most commonly used pesticides for {pest} are {pesticides}."
                details = f"Pest={pest} | Pesticides={pesticides}"
                
                normalized_entry = f"""[DATASET: pest_control]
[TYPE: pest_management]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_pesticide_remedy_1(self):
        """Normalize pesticide_remedy_1.txt"""
        input_file = self.input_dir / "pesticide_remedy_1.txt"
        output_file = self.output_dir / "pesticide_remedy_1_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            crop = data.get('Crop', '')
            disease = data.get('Disease Or Pest', data.get('Disease', ''))
            agent = data.get('Agent', '')
            treatment = data.get('Recommended Treatment', '')
            dosage = data.get('Dosage', '')
            duration = data.get('Duration', '')
            precautions = data.get('Precautions', '')
            
            if crop and disease:
                query = f"How to treat {disease} in {crop}?"
                answer = f"For {disease} in {crop}"
                if agent:
                    answer += f" caused by {agent}"
                answer += f", use {treatment}"
                if dosage:
                    answer += f" at {dosage} dosage"
                if duration:
                    answer += f". Apply every {duration}"
                if precautions:
                    answer += f". {precautions}"
                
                details = f"Crop={crop} | Disease={disease}"
                if agent:
                    details += f" | Agent={agent}"
                if treatment:
                    details += f" | Treatment={treatment}"
                if dosage:
                    details += f" | Dosage={dosage}"
                if duration:
                    details += f" | Duration={duration}"
                if precautions:
                    details += f" | Precautions={precautions}"
                
                normalized_entry = f"""[DATASET: pesticide_remedy]
[TYPE: treatment_protocol]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")
    
    def normalize_pesticide_remedy_2(self):
        """Normalize pesticide_remedy_2.txt"""
        input_file = self.input_dir / "pesticide_remedy_2.txt"
        output_file = self.output_dir / "pesticide_remedy_2_normalized.txt"
        
        if not input_file.exists():
            print(f"⚠ Skipping {input_file.name} - file not found")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.strip().split('---')
        normalized = []
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            data = {}
            for line in entry.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            crop = data.get('Crop', '')
            disease = data.get('Disease Or Pest', data.get('Disease', ''))
            agent = data.get('Agent', '')
            pathogen = data.get('Pathogen Type', '')
            treatment = data.get('Recommended Treatment', '')
            treatment_type = data.get('Treatment Type', '')
            active = data.get('Active Ingredient', '')
            dosage = data.get('Dosage', '')
            interval = data.get('Application Interval Days', '')
            stage = data.get('Stage Applicable', '')
            organic = data.get('Organic Option', '')
            precautions = data.get('Precautions', '')
            region = data.get('Region Applicability', '')
            
            if crop and disease:
                query = f"How to treat {disease} in {crop}?"
                answer = f"{disease} in {crop}"
                if agent:
                    answer += f" caused by {agent}"
                if pathogen:
                    answer += f" ({pathogen})"
                answer += f": {treatment}"
                if active:
                    answer += f" including {active}"
                if dosage:
                    answer += f" at {dosage}"
                if interval:
                    answer += f" every {interval} days"
                if organic:
                    answer += f". Organic options: {organic}"
                if precautions:
                    answer += f". {precautions}"
                
                details_parts = [
                    f"Crop={crop}",
                    f"Disease={disease}"
                ]
                if agent:
                    details_parts.append(f"Agent={agent}")
                if pathogen:
                    details_parts.append(f"PathogenType={pathogen}")
                if treatment:
                    details_parts.append(f"Treatment={treatment}")
                if treatment_type:
                    details_parts.append(f"TreatmentType={treatment_type}")
                if active:
                    details_parts.append(f"ActiveIngredient={active}")
                if dosage:
                    details_parts.append(f"Dosage={dosage}")
                if interval:
                    details_parts.append(f"Interval={interval} days")
                if stage:
                    details_parts.append(f"Stage={stage}")
                if organic:
                    details_parts.append(f"OrganicOption={organic}")
                if precautions:
                    details_parts.append(f"Precautions={precautions}")
                if region:
                    details_parts.append(f"Region={region}")
                
                details = " | ".join(details_parts)
                
                normalized_entry = f"""[DATASET: pesticide_remedy_detailed]
[TYPE: treatment_protocol]
Query: {query}
Answer: {answer}
Details: {details}"""
                normalized.append(normalized_entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n---\n'.join(normalized))
        
        print(f"✓ Normalized {len(normalized)} entries: {input_file.name} → {output_file.name}")


def main():
    """Main execution function"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  AGRICULTURAL DATASET NORMALIZER FOR RAG SYSTEMS".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Create normalizer instance
    normalizer = DatasetNormalizer(
        input_dir="./backend/data/cleaned_text",  # Change this to your input directory
        output_dir="./backend/data/updated_cleaned_text"  # Change this to your output directory
    )
    
    # Normalize all datasets
    normalizer.normalize_all()
    
    print("\n📋 NEXT STEPS:")
    print("   1. Review the normalized files in the output directory")
    print("   2. Update your RAG pipeline to use the normalized data")
    print("   3. Use '---' as your chunk separator")
    print("   4. Test with queries from different datasets")
    print("\n💡 TIP: Each normalized entry follows the format:")
    print("   [DATASET: name]")
    print("   [TYPE: category]")
    print("   Query: question")
    print("   Answer: response")
    print("   Details: key=value | key=value")
    print("\n")


if __name__ == "__main__":
    main()