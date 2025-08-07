# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Physical Therapy Extraction Example."""
import textwrap
import langextract as lx

# The input text is a concatenation of a discharge summary, PT notes, and an
# imaging report for a patient who underwent hip surgery.
input_text = textwrap.dedent("""\
    <document filename="Discharge_Summary.txt">
    Patient: John Doe, 78-year-old male
    Admission Date: 2023-10-26
    Discharge Date: 2023-10-31
    Admitting Diagnosis: Fall at home, right hip pain.
    Discharge Diagnosis: Right intertrochanteric femur fracture, status post Open Reduction Internal Fixation (ORIF).

    History of Present Illness:
    Mr. Doe is a 78 y/o male with a history of hypertension, type 2 diabetes, and osteoarthritis who presented to the emergency department after a mechanical fall at home. He tripped on a rug. Patient reported immediate, severe pain in his right hip and inability to bear weight. X-rays confirmed a comminuted intertrochanteric fracture of the right femur.

    Hospital Course:
    Patient was admitted to the orthopedic service. On 2023-10-27, he underwent a successful ORIF of the right hip performed by Dr. Smith. Post-operatively, his pain has been managed with a combination of oxycodone and acetaminophen. He has been working with Physical Therapy and Occupational Therapy. He is currently toe-touch weight-bearing (TTWB) on the right lower extremity. His hospital course was otherwise uncomplicated. He is now stable for discharge to a skilled nursing facility for continued rehabilitation.

    Past Medical History:
    1. Hypertension
    2. Type 2 Diabetes Mellitus
    3. Osteoarthritis
    4. Hyperlipidemia

    Surgical History:
    1. Left Total Knee Arthroplasty (2018)
    2. Cholecystectomy (2005)

    Discharge Orders:
    - Precautions: Toe-touch weight-bearing on right lower extremity for 6 weeks. No hip flexion beyond 90 degrees, no adduction past midline, no internal rotation of the right hip.

    Social History:
    Patient is a retired carpenter. He lives with his wife in a single-story home with one step to enter. He was independent with all mobility and ADLs prior to the fall, using a single-point cane for community ambulation.
    </document>

    <document filename="PT_Notes_Hospital.txt">
    Physical Therapy Notes - Acute Care
    Patient: John Doe
    Date of Initial Evaluation: 2023-10-28 (Post-op Day 1)
    Subjective: Patient reports pain in R hip at 7/10. Anxious to get moving.
    Objective:
    - ROM: R hip flexion limited to 70 deg due to pain/precautions.
    - Strength: R hip abduction 1/5, knee extension 2/5. LLE and UEs 4/5 throughout.
    - Bed Mobility: Max A to roll, supine to sit.
    - Transfers: Max A from bed to chair with rolling walker (RW).
    - Gait: Hopped with RW for 10 feet with Max A. Poor balance.

    Date of Final Note: 2023-10-31 (Discharge)
    Subjective: Pain 4/10 with activity. Reports feeling stronger.
    Objective:
    - Bed Mobility: Mod A for supine to sit.
    - Transfers: Min A for sit to stand from bed and toilet with RW.
    - Gait: Ambulates 50 feet with RW and TTWB on RLE, requires Min A for sequencing and balance.
    - Equipment: Rolling walker issued.
    - Recommendation: Continue PT at SNF to improve strength, safety, and functional mobility to return home.
    </document>

    <document filename="Imaging_Report_XRAY_Hip.txt">
    Facility: General Hospital
    Patient: John Doe
    Exam: X-RAY RIGHT HIP 2 VIEWS
    Date: 2023-10-26
    Clinical History: 78-year-old male, fall, right hip pain.
    Findings:
    There is a comminuted intertrochanteric fracture of the right femur.
    Impression:
    Acute comminuted intertrochanteric right femur fracture.
    </document>
""")

# The prompt instructs the model to extract key information relevant to a
# Physical Therapist. It defines the categories (classes) of information
# to find in the text.
prompt_description = textwrap.dedent("""\
    Extract physical therapy-relevant information from the clinical notes.
    Identify the following classes, extracting the exact text from the document:
    - patient_info: Key patient demographic and social factors.
    - diagnosis: The primary reason for admission.
    - surgery: The surgical procedure performed.
    - medical_history: Relevant past medical conditions.
    - imaging_finding: Key results from imaging reports.
    - precaution: Specific movement or weight-bearing restrictions.
    - functional_status: Patient's current ability with mobility tasks.
    - functional_limitation: Specific impairments like weakness or limited ROM.
    - equipment: Assistive devices required by the patient.
    - prior_level_of_function: The patient's mobility level before the incident.
    """)

# The few-shot example provides a template for the model to follow.
# It includes a sample text and the corresponding structured extractions.
# This example uses attributes to link concepts, such as connecting a precaution
# (e.g., "non-weight bearing") to the specific body part it applies to.
examples = [
    lx.data.ExampleData(
        text="""65 y/o female s/p R TKA with precautions of WBAT and no flexion past 90 degrees. Pt ambulated 50 ft with a rolling walker.""",
        extractions=[
            lx.data.Extraction(
                extraction_class='patient_info',
                extraction_text='65 y/o female',
            ),
            lx.data.Extraction(
                extraction_class='surgery',
                extraction_text='R TKA',
                attributes={'body_part': 'right knee'},
            ),
            lx.data.Extraction(
                extraction_class='precaution',
                extraction_text='WBAT',
                attributes={'body_part': 'right lower extremity'},
            ),
            lx.data.Extraction(
                extraction_class='precaution',
                extraction_text='no flexion past 90 degrees',
                attributes={'body_part': 'right knee'},
            ),
            lx.data.Extraction(
                extraction_class='functional_status',
                extraction_text='ambulated 50 ft',
                attributes={'assistive_device': 'rolling walker'},
            ),
            lx.data.Extraction(
                extraction_class='equipment',
                extraction_text='rolling walker',
            ),
        ],
    )
]


def main():
  """Runs the Physical Therapy extraction example."""
  print('Running Physical Therapy extraction example...')

  # Run the extraction.
  # We use a powerful model like Gemini 1.5 Pro for this complex task,
  # but a smaller model like Flash could also be used.
  result = lx.extract(
      text_or_documents=input_text,
      prompt_description=prompt_description,
      examples=examples,
      model_id='gemini-1.5-pro-latest',
  )

  # Save the results to a JSONL file.
  output_filename = 'pt_extraction.jsonl'
  print(f'Saving results to {output_filename}...')
  lx.io.save_annotated_documents([result], output_name=output_filename)

  # Generate the interactive HTML visualization.
  html_filename = 'pt_visualization.html'
  print(f'Generating visualization to {html_filename}...')
  html_content = lx.visualize(output_filename)
  with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

  print(f'Successfully created {html_filename}. Open this file in a browser to'
        ' see the interactive results.')


if __name__ == '__main__':
  main()
