# Physical Therapy Clinical Note Extraction

This example demonstrates how LangExtract can be used to extract structured information from clinical notes relevant to Physical Therapy (PT). This is a common task in healthcare settings, where therapists need to quickly synthesize information from various documents to create a treatment plan.

> **Disclaimer:** This demonstration is for illustrative purposes of LangExtract's baseline capability only. It does not represent a finished or approved product, is not intended to diagnose or suggest treatment of any disease or condition, and should not be used for medical advice.

## Use Case: PT Initial Evaluation

For a Physical Therapist, the initial evaluation of a new patient requires reviewing their medical history, surgical reports, hospital course, and physician orders. This example simulates this process by extracting key data points from a collection of mock clinical documents for a patient who has undergone hip surgery.

The example extracts the following types of information:
- **Patient Demographics and Social History**
- **Diagnosis and Surgical Procedures**
- **Medical History and Imaging Findings**
- **Precautions and Restrictions** (e.g., weight-bearing status)
- **Functional Status and Limitations**
- **Required Equipment**
- **Prior Level of Function**

## Relationship Extraction for Clinical Context

A key feature demonstrated here is the use of `attributes` to perform relationship extraction. This allows the model to connect related concepts. For instance, it links a specific precaution (like "no flexion past 90 degrees") to the body part it affects ("right knee"). This creates a much richer, more useful structured output than simple entity extraction alone.

## Example Code

The full code for this example can be found in [`examples/physical_therapy_example.py`](../../examples/physical_therapy_example.py).

```python
import langextract as lx
import textwrap

# The input text is a concatenation of a discharge summary, PT notes, and an
# imaging report for a patient who underwent hip surgery.
input_text = textwrap.dedent("""\
    <document filename="Discharge_Summary.txt">
    Patient: John Doe, 78-year-old male
    ...
    </document>

    <document filename="PT_Notes_Hospital.txt">
    Physical Therapy Notes - Acute Care
    ...
    </document>

    <document filename="Imaging_Report_XRAY_Hip.txt">
    Facility: General Hospital
    ...
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

  result = lx.extract(
      text_or_documents=input_text,
      prompt_description=prompt_description,
      examples=examples,
      model_id='gemini-1.5-pro-latest',
  )

  # Save and visualize the results
  output_filename = 'pt_extraction.jsonl'
  lx.io.save_annotated_documents([result], output_name=output_filename)
  html_filename = 'pt_visualization.html'
  html_content = lx.visualize(output_filename)
  with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

if __name__ == '__main__':
  main()
```

## Visualization of Results

Running this script will produce an interactive HTML file, `pt_visualization.html`. This file allows the therapist to hover over the original text and see the extracted entities highlighted. The color-coding and on-hover details make it easy to quickly review the patient's status. This visual feedback is crucial for verifying the accuracy of the extraction and building trust in the system.

## Key Features Demonstrated

- **Complex Medical NER**: Extracts a wide range of entities relevant to a specific clinical discipline (Physical Therapy).
- **Relationship Extraction**: Uses attributes to link entities, providing critical context (e.g., which precaution applies to which body part).
- **Multi-Document Synthesis**: Processes information from multiple source documents (discharge summary, PT notes, imaging reports) in a single run.
- **Interactive Visualization**: Generates a user-friendly, interactive HTML report for easy review and verification of the extracted data.
