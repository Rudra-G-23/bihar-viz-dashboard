import streamlit as st
from pathlib import Path
import base64

st.set_page_config(page_title="Level 01")

st.title("Level 01")
st.subheader("HCES DATA STORY")

PDF_PATH = Path("reports/HCES-DATA-STORY.pdf")

if not PDF_PATH.exists():
    st.error("PDF file not found.")
else:
    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{b64_pdf}"
            width="100%"
            height="500"
            style="border: none;"
        ></iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)

st.write('---')
st.subheader("Survey Identification")

st.markdown(
    """
| **Column Name**              | **Description**                                          |
| ---------------------------- | --------------------------------------------------------------------------------- |
| Survey_Name                  | Name of the survey conducted.                                                     |
| Year                         | Year when the survey was conducted.                                               |
| FSU_Serial_No                | Serial number of the First Stage Unit (FSU), like a cluster or area.              |
| Sector                       | Type of area: Rural or Urban.                                                     |
| State                        | Name of the state where the household is located.                                 |
| NSS_Region                   | NSS region code for grouping areas.                                               |
| District                     | Name of the district.                                                             |
| Stratum                      | Classification layer for sampling (helps in selecting representative households). |
| Sub_stratum                  | Sub-layer under Stratum for detailed grouping.                                    |
| Panel                        | Panel number if the survey is part of a repeated study.                           |
| Sub_sample                   | Sub-sample number within the main survey.                                         |
| FOD_Sub_Region               | Sub-region of the Field Operations Division (FOD).                                |
| Sample_SU_No                 | Sample Survey Unit Number (specific area selected).                               |
| Sample_Sub_Division_No       | Sub-division number of the sample area.                                           |
| Second_Stage_Stratum_No      | Stratum number for the second stage of sampling.                                  |
| Sample_Household_No          | Household number in the sample.                                                   |
| Questionnaire_No             | Questionnaire identification number used for the household.                       |
| Level                        | Level/section of data collection.                                                 |
| Survey_Code                  | Unique code assigned to the survey.                                               |
| Reason_for_Substitution_Code | Code indicating reason if a household was replaced/substituted.                   |
| Multiplier                   | Weight assigned to each household to represent population estimates.              |

Link: https://microdata.gov.in/NADA/index.php/catalog/237/data-dictionary/

"""
)