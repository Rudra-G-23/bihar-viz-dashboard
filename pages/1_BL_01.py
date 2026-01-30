import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="Level 01",
    layout="wide"
)

st.title("Level 01")
st.subheader("HCES DATA STORY")

PDF_PATH = Path("reports/HCES-DATA-STORY.pdf")
if not PDF_PATH.exists():
    st.error("PDF file not found.")
else:
    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="📄 Open PDF",
        data=pdf_bytes,
        file_name="HCES-DATA-STORY.pdf",
        mime="application/pdf"
    )

with st.expander("📜 Finding Preview"):
    ic1, ic2 = st.columns(2)
    with ic1:
        st.image("assets/pic/hh-data-story/hces-data-story.png", caption="HCES DATA STORY")
        st.image("assets/pic/hh-data-story/survey-hierarchy.png", caption="Survey Hierarchy")

    with ic2:
        st.image("assets/pic/hh-data-story/experiment.png", caption="Experiment Bihar Data")
        st.image("assets/pic/hh-data-story/item-code-level.png", caption="What is the issues")


with st.expander("🆔 Survey key columns", expanded=True):
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